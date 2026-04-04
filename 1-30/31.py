#!/usr/bin/env python3
"""インターバル音声ファイル生成ツール - 指定したインターバルと繰り返し回数で数字を読み上げる音声ファイルを生成"""

import argparse
import os
import sys
import tempfile
from gtts import gTTS
from pydub import AudioSegment


def generate_number_speech(number, lang='ja'):
    """数字を音声で読み上げたMP3を生成"""
    try:
        tts = gTTS(text=str(number), lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()
        tts.save(temp_file.name)
        audio = AudioSegment.from_mp3(temp_file.name)
        os.unlink(temp_file.name)
        return audio
    except Exception as e:
        print(f"エラー: 音声生成失敗（数字: {number}）: {e}", file=sys.stderr)
        return None


def generate_interval_audio(interval_seconds, repeat_count, output_file, lang='ja', verbose=False):
    """
    インターバル音声ファイルを生成

    Args:
        interval_seconds: インターバル秒数
        repeat_count: 繰り返し回数
        output_file: 出力ファイル名
        lang: 音声言語
        verbose: 詳細出力
    """
    if verbose:
        print(f"音声ファイル生成開始...")
        print(f"  インターバル: {interval_seconds}秒")
        print(f"  繰り返し回数: {repeat_count}回")
        total_seconds = interval_seconds * repeat_count
        print(f"  総時間: {total_seconds}秒 ({total_seconds // 60}分{total_seconds % 60}秒)")

    # 無音を生成
    silence = AudioSegment.silent(duration=interval_seconds * 1000)

    # 全体のオーディオを初期化
    final_audio = AudioSegment.empty()

    for i in range(repeat_count):
        if verbose:
            print(f"  [{i+1}/{repeat_count}] 生成中...", end='\r')

        # インターバル（無音）を追加
        final_audio += silence

        # 数字の読み上げ音声を生成
        number_audio = generate_number_speech(i + 1, lang)
        if number_audio is None:
            return False
        final_audio += number_audio

    if verbose:
        print()  # 改行

    # MP3として出力
    if verbose:
        print(f"ファイル保存中: {output_file}")
    final_audio.export(output_file, format='mp3', bitrate='192k')

    if verbose:
        file_size = os.path.getsize(output_file)
        file_size_mb = file_size / (1024 * 1024)
        print(f"完了: {output_file}")
        print(f"  ファイルサイズ: {file_size_mb:.2f} MB")
        print(f"  総時間: {len(final_audio) / 1000:.1f}秒")
    else:
        print(f"完了: {output_file}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="インターバル音声ファイル生成 - 指定秒数ごとに数字を読み上げる音声ファイルを作成"
    )
    parser.add_argument("interval", type=int, help="インターバル秒数（1-3600）")
    parser.add_argument("repeat", type=int, help="繰り返し回数（1-1000）")
    parser.add_argument("-o", "--output", help="出力ファイルパス（デフォルト: interval_Ns_xM.mp3）")
    parser.add_argument("-l", "--lang", default="ja", help="音声言語（デフォルト: ja）")
    parser.add_argument("-v", "--verbose", action="store_true", help="詳細出力")
    args = parser.parse_args()

    # バリデーション
    if args.interval < 1 or args.interval > 3600:
        print("エラー: インターバルは1〜3600秒の範囲で指定してください", file=sys.stderr)
        return 1

    if args.repeat < 1 or args.repeat > 1000:
        print("エラー: 繰り返し回数は1〜1000回の範囲で指定してください", file=sys.stderr)
        return 1

    # 出力ファイル名を決定
    if not args.output:
        args.output = f"interval_{args.interval}s_x{args.repeat}.mp3"
    elif not args.output.endswith('.mp3'):
        args.output += '.mp3'

    # 音声ファイル生成
    success = generate_interval_audio(
        args.interval,
        args.repeat,
        args.output,
        args.lang,
        args.verbose
    )

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())