#!/usr/bin/env python3
"""MP3ファイルを指定回数繰り返した音声ファイルを生成するCLIツール"""

import argparse
import os
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(
        description="MP3ファイルを指定回数繰り返します"
    )
    parser.add_argument("input", help="入力MP3ファイルパス")
    parser.add_argument("repeat", type=int, help="繰り返し回数")
    parser.add_argument("-o", "--output", help="出力ファイルパス（デフォルト: 入力ファイル名_xN.mp3）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"エラー: '{args.input}' が見つかりません。")
        return 1

    if args.repeat < 1:
        print("エラー: 繰り返し回数は1以上を指定してください。")
        return 1

    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_x{args.repeat}{ext}"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for _ in range(args.repeat):
            f.write(f"file '{os.path.abspath(args.input)}'\n")
        list_path = f.name

    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
             "-codec", "copy", args.output],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"エラー: ffmpeg失敗\n{result.stderr}")
            return 1
    finally:
        os.unlink(list_path)

    print(f"完了: {args.output} ({args.repeat}回繰り返し)")
    return 0


if __name__ == "__main__":
    exit(main())
