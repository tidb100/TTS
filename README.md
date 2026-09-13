# TTS

一个简单的 Edge TTS 命令行工具，用 Python 把文本转换成 MP3 语音文件。

## 功能 Features

- 支持日语、英语、粤语等 Edge TTS 声音
- 默认使用日语女声 `ja-JP-NanamiNeural`
- 默认语速为 `-20%`
- 使用 `--text` 指定文本
- 使用 `--write-media` 指定输出 MP3 文件
- 内置常用声音列表和执行示例

## 安装 Installation

需要 Python 3，并安装 `edge-tts`：

```bash
python3 -m pip install edge-tts
```

## 使用方法 Usage

查看帮助：

Show help:

```bash
python3 tts.py --help
```

查看常用声音：

List common voices:

```bash
python3 tts.py --list-voices
```

生成 MP3：

Generate an MP3:

```bash
python3 tts.py --text "パクチーが大好きです。" --write-media "jp_female.mp3"
```

## 常用声音 Common Voices

- 日语女声 / Japanese female: `ja-JP-NanamiNeural`
- 日语男声 / Japanese male: `ja-JP-KeitaNeural`
- 美式英语女声 / US English female: `en-US-JennyNeural`
- 美式英语男声 / US English male: `en-US-GuyNeural`
- 粤语女声 / Cantonese female: `zh-HK-HiuMaanNeural`

## 示例 Examples

日语女声：

Japanese female:

```bash
python3 tts.py --voice ja-JP-NanamiNeural --text "パクチーが大好きです。" --write-media "jp_female.mp3"
```

日语男声：

Japanese male:

```bash
python3 tts.py --voice ja-JP-KeitaNeural --text "おはようございます。" --write-media "jp_male.mp3"
```

美式英语女声：

US English female:

```bash
python3 tts.py --voice en-US-JennyNeural --text "I like cilantro very much." --write-media "en_female.mp3"
```

美式英语男声：

US English male:

```bash
python3 tts.py --voice en-US-GuyNeural --text "Good morning. Have a nice day." --write-media "en_male.mp3"
```

粤语女声：

Cantonese female:

```bash
python3 tts.py --voice zh-HK-HiuMaanNeural --text "我好鍾意食芫荽。" --write-media "cantonese.mp3"
```

## 参数 Arguments

- `--voice`: 声音名称。默认 `ja-JP-NanamiNeural`。
- `--rate`: 语速。默认 `-20%`。例如 `+10%` 表示加快 10%，`-15%` 表示放慢 15%。
- `--text`: 要转换成语音的文本。生成 MP3 时必填。
- `--write-media`, `-o`: 输出 MP3 文件路径。
- `--list-voices`: 列出脚本内置的常用声音，然后退出。
