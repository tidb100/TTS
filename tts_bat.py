#!/usr/bin/env python3
"""Generate TTS MP3 files from a text file with the edge_tts Python package."""

from __future__ import annotations

import argparse
import asyncio
import unicodedata
from pathlib import Path


DEFAULT_VOICE = "ja-JP-NanamiNeural"
DEFAULT_RATE = "-20%"
MAX_PREFIX_LENGTH = 50
COMMON_VOICES = (
    ("ja-JP-NanamiNeural", "日语女声，Microsoft Nanami，默认推荐"),
    ("ja-JP-KeitaNeural", "日语男声，Microsoft Keita"),
    ("en-US-JennyNeural", "美式英语女声，Microsoft Jenny"),
    ("en-US-GuyNeural", "美式英语男声，Microsoft Guy"),
    ("zh-HK-HiuMaanNeural", "粤语女声，Microsoft HiuMaan"),
)


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    pass


def remove_punctuation(text: str) -> str:
    return "".join(
        char for char in text if not unicodedata.category(char).startswith("P")
    ).strip()


def output_name(text: str) -> str:
    prefix = remove_punctuation(text)[:MAX_PREFIX_LENGTH].strip()
    if not prefix:
        prefix = "untitled"
    return f"{prefix}.mp3"


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


async def generate_batch(
    voice: str,
    rate: str,
    input_path: Path,
    output_dir: Path,
) -> int:
    converted_count = 0
    with input_path.open("r", encoding="utf-8") as input_file:
        for line_number, raw_line in enumerate(input_file, start=1):
            text = raw_line.strip()
            if not text:
                print(f"Skipped blank line: {line_number}")
                continue

            output_path = output_dir / output_name(text)
            print(f"Converting line {line_number}: {output_path}")
            await generate_speech(voice, rate, text, output_path)
            converted_count += 1

    return converted_count


def parse_args() -> argparse.Namespace:
    voice_options = "\n".join(
        f"  {voice:<24} {description}" for voice, description in COMMON_VOICES
    )
    default_rate_help = DEFAULT_RATE.replace("%", "%%")
    parser = argparse.ArgumentParser(
        description="批量把文本文件中的每一行转换成一个 MP3 文件。默认使用 Edge TTS 的日语女声。",
        formatter_class=HelpFormatter,
        epilog=f"""常用声音:
{voice_options}

rate 语速格式:
  +0%    正常语速
  -15%   慢 15%
  +10%   快 10%

执行示例:
  python3 tts_bat.py --input vocabulary/2.txt --output .
  python3 tts_bat.py --input sentences.txt --output mp3
  python3 tts_bat.py --voice ja-JP-KeitaNeural --input jp.txt --output jp_mp3
  python3 tts_bat.py --voice en-US-JennyNeural --rate=-10% --input english.txt --output en_mp3
  python3 tts_bat.py --voice zh-HK-HiuMaanNeural --input cantonese.txt --output hk_mp3
  python3 tts_bat.py --list-voices

输入文件例子 sentences.txt:
  パクチーが大好きです。
  おはようございます。
  ありがとうございます。

输出文件名规则:
  1. 每一行生成一个 MP3 文件。
  2. 空行会跳过。
  3. 文件名前缀取该行文本去掉标点符号后的前 50 个字符。
  4. 文件名不追加行号，例如:
     パクチーが大好きです.mp3
  5. 如果多行生成同名 MP3，后生成的文件会覆盖前一个。
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
        "--input",
        "-i",
        help="输入文本文件路径。脚本会按行读取，非空行逐行转换。使用 --list-voices 时不用填。",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="输出 MP3 目录。目录不存在时会自动创建。使用 --list-voices 时不用填。",
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
                ("--input", args.input),
                ("--output", args.output),
            )
            if not value
        ]
        if missing:
            parser.error(f"批量生成 MP3 时必须提供这些参数: {', '.join(missing)}")
    return args


def main() -> int:
    args = parse_args()
    if args.list_voices:
        for voice, description in COMMON_VOICES:
            print(f"{voice}\t{description}")
        return 0

    input_path = Path(args.input).expanduser()
    output_dir = Path(args.output).expanduser()
    if not input_path.is_absolute():
        input_path = Path.cwd() / input_path
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir

    if not input_path.exists():
        raise SystemExit(f"找不到输入文件: {input_path}")
    if not input_path.is_file():
        raise SystemExit(f"输入路径不是文件: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    converted_count = asyncio.run(
        generate_batch(args.voice, args.rate, input_path, output_dir)
    )
    print(f"Done. Converted {converted_count} line(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
