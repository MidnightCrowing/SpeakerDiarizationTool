# SpeakerDiarizationTool

## 简介

该脚本使用 ModelScope 提供的说话人验证模型对输入的音频文件进行处理，并根据说话人的相似性将音频文件分类存储在不同的文件夹中。

## 环境配置

使用以下命令安装依赖:

```bash
pip install -r requirements.txt
```

## 使用方法

在根目录下运行以下命令:

```bash
python main.py -i <输入音频文件路径> -o <输出文件夹路径> --thr <阈值>
```

### 参数说明

- `-i` 或 `--input_path`: 必需。指定输入音频文件的路径。
- `-o` 或 `--output_path`: 可选。指定保存分类后音频文件的路径，默认为程序根目录下的 `result` 文件夹。
- `--thr`: 可选。比较阈值。如果未提供，则使用模型的默认阈值。

### 示例

```bash
python main.py -i ./input_audios -o ./output_audios --thr 0.8
```

该命令将处理 `./input_audios` 目录下的音频文件，并将分类后的文件保存到 `./output_audios` 目录中，使用的比较阈值为 `0.8`。

## 注意事项

- 输入的音频文件建议为单声道 16kHz 采样率的文件，以确保与模型的兼容性。
- 经测试，说话人区分效果不好，建议阈值设置为 0.75 以上，或根据测试结果进行调整。

## 许可证

该项目使用 MIT 许可证，详见 [LICENSE](./LICENSE) 文件。

## 致谢

感谢 ModelScope 提供的说话人验证模型及相关工具: https://www.modelscope.cn/models/iic/speech_campplus_sv_zh-cn_16k-common
