import argparse
import logging
import os
import shutil

import soundfile as sf
from modelscope.pipelines import pipeline
from tqdm import tqdm

# 将 modelscope 的日志级别设置为 ERROR
logging.getLogger('modelscope').setLevel(logging.ERROR)


def get_audio_length_soundfile(file_path):
    with sf.SoundFile(file_path) as f:
        length_in_seconds = len(f) / f.samplerate
    return length_in_seconds


def get_args():
    parser = argparse.ArgumentParser(description='Process audio file and threshold.')

    parser.add_argument('-i', '--input_path', type=str, required=True, help='Path to input the audio file')
    parser.add_argument('-o', '--output_path', type=str, default='result',
                        help='Path to save the audio file, default is result in the program root path')
    parser.add_argument('--thr', type=float, default=None, help='Comparison threshold value')

    args = parser.parse_args()

    return args.input_path, args.output_path, args.thr


def update_speakers(new_wav, new_wav_length, speakers, sv_pipeline):
    for speaker in speakers:
        speaker_wav = speaker['compare_wav']

        if thr is None:
            result = sv_pipeline([new_wav, speaker_wav])
        else:
            result = sv_pipeline([new_wav, speaker_wav], thr=thr)

        if result['text'] == 'yes':
            speaker['list'].append(new_wav)

            # 寻找长音频作为参考音频, 但音频时长不超过 1min
            if speaker['compare_wav_length'] < new_wav_length < 60:
                speaker['compare_wav'] = new_wav
                speaker['compare_wav_length'] = new_wav_length

            return True  # 找到匹配的 speaker 并更新了，返回 True

    return False  # 未找到匹配的 speaker，返回 False


def main():
    sv_pipeline = pipeline(
        task='speaker-verification',
        model='damo/speech_campplus_sv_zh-cn_16k-common',
        # model_revision='v2.0.2'  # 不填则为最新模型版本
    )

    speakers = []
    counter = 0
    files = os.listdir(input_path)

    for file in tqdm(files, desc="Audio compare"):
        new_wav = os.path.join(input_path, file)
        new_wav_length = get_audio_length_soundfile(new_wav)

        compare_flag = update_speakers(new_wav, new_wav_length, speakers, sv_pipeline)

        if not compare_flag:
            speakers.append({
                'list': [new_wav],
                'compare_wav': new_wav,
                'compare_wav_length': new_wav_length
            })

        counter += 1

        # 每处理 100 个文件后对 speakers 列表进行排序
        if counter % 100 == 0:
            speakers.sort(key=lambda x: len(x['list']), reverse=True)

    print(f'speaker num: {len(speakers)}')

    # 创建输出路径
    os.makedirs(output_path, exist_ok=True)

    # 复制文件到新的文件夹
    for num, speaker in enumerate(speakers, start=1):
        speaker_folder = os.path.join(output_path, f"speaker{num}")
        os.makedirs(speaker_folder, exist_ok=True)

        for wav_file in speaker['list']:
            shutil.copy(wav_file, speaker_folder)

    print("Files have been successfully copied to the output directory.")


if __name__ == '__main__':
    input_path, output_path, thr = get_args()
    main()
