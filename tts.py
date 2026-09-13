#!/usr/bin/env python3
"""Generate a TTS MP3 with the edge_tts Python package."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path


DEFAULT_VOICE = "ja-JP-NanamiNeural"
DEFAULT_RATE = "-20%"
COMMON_VOICES = (
    ("ja-JP-NanamiNeural", "日语女声，Microsoft Nanami，默认推荐"),
    ("ja-JP-KeitaNeural", "日语男声，Microsoft Keita"),
    ("en-US-JennyNeural", "美式英语女声，Microsoft Jenny"),
    ("en-US-GuyNeural", "美式英语男声，Microsoft Guy"),
    ("zh-HK-HiuMaanNeural", "粤语女声，Microsoft HiuMaan"),
)


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    pass


async def generate_speech(voice: str, rate: str, text: str, output: Path) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise SystemExit(
            "Python package edge-tts is not installed. Install it with:\n"
            "python3 -m pip install edge-tts"
        ) from exc

    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(output))


def parse_args() -> argparse.Namespace:
    voice_options = "\n".join(
        f"  {voice:<24} {description}" for voice, description in COMMON_VOICES
    )
    default_rate_help = DEFAULT_RATE.replace("%", "%%")
    parser = argparse.ArgumentParser(
        description="把文本转换成 MP3 语音文件。默认使用 Edge TTS 的日语女声。",
        formatter_class=HelpFormatter,
        epilog=f"""常用声音:
{voice_options}

rate 语速格式:
  +0%    正常语速
  -15%   慢 15%
  +10%   快 10%

执行示例:
  python3 tts.py --voice ja-JP-NanamiNeural --text "パクチーが大好きです。" --write-media "jp_female.mp3"
  python3 tts.py --voice ja-JP-KeitaNeural --text "おはようございます。" --write-media "jp_male.mp3"
  python3 tts.py --voice en-US-JennyNeural --text "I like cilantro very much." --write-media "en_female.mp3"
  python3 tts.py --voice en-US-GuyNeural --text "Good morning. Have a nice day." --write-media "en_male.mp3"
  python3 tts.py --voice zh-HK-HiuMaanNeural --text "我好鍾意食芫荽。" --write-media "cantonese.mp3"
  python3 tts.py --list-voices
""",
    )
    parser.add_argument(
        "--voice",
        default=DEFAULT_VOICE,
        choices=[voice for voice, _ in COMMON_VOICES],
        help=f"选择声音，默认 {DEFAULT_VOICE}。可选值见下方“常用声音”。",
    )
    parser.add_argument(
        "--rate",
        default=DEFAULT_RATE,
        help=f"设置语速，默认 {default_rate_help}。格式示例: +10%% 表示加快 10%%，-15%% 表示放慢 15%%。",
    )
    parser.add_argument(
        "--text",
        help="要转换成语音的文本。生成 MP3 时必填；使用 --list-voices 时不用填。",
    )
    parser.add_argument(
        "--write-media",
        "-o",
        dest="write_media",
        help=(
            "输出 MP3 文件路径。写相对路径时会保存到脚本所在目录，"
            "例如 hello.mp3 会保存为 /tmp/tts/hello.mp3。"
        ),
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="列出当前脚本支持的常用声音选项，然后退出，不生成 MP3。",
    )

    args = parser.parse_args()
    if not args.list_voices:
        missing = [
            option
            for option, value in (
                ("--text", args.text),
                ("--write-media", args.write_media),
            )
            if not value
        ]
        if missing:
            parser.error(f"生成 MP3 时必须提供这些参数: {', '.join(missing)}")
    return args


def main() -> int:
    args = parse_args()
    if args.list_voices:
        for voice, description in COMMON_VOICES:
            print(f"{voice}\t{description}")
        return 0

    output = Path(args.write_media)
    if not output.is_absolute():
        output = Path(__file__).resolve().parent / output

    asyncio.run(generate_speech(args.voice, args.rate, args.text, output))
    print(f"Generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
