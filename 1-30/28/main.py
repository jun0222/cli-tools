#!/usr/bin/env python3
"""問題と答えのリストから、問題→n秒後に答えを読み上げる音声ファイルを生成するCLIツール"""

import argparse
import os
import struct
import subprocess
import tempfile
import wave

import pyttsx3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_input(filepath):
    """タブ区切りのQ&Aファイルを読み込む"""
    pairs = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                print(f"警告: {line_num}行目はタブ区切りではありません。スキップします。")
                continue
            question = parts[0].strip()
            answer = parts[1].strip()
            pairs.append((question, answer))
    return pairs


def text_to_wav(engine, text, output_path):
    """pyttsx3でテキストをWAVファイルに変換"""
    engine.save_to_file(text, output_path)
    engine.runAndWait()


def create_silence_wav(output_path, duration_sec, sample_rate=22050, channels=1, sample_width=2):
    """指定秒数の無音WAVファイルを生成"""
    num_frames = int(sample_rate * duration_sec)
    silence_data = struct.pack(f"<{num_frames * channels}h", *([0] * (num_frames * channels)))
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(silence_data)


def concatenate_wavs(wav_files, output_path):
    """複数のWAVファイルを結合する"""
    if not wav_files:
        return

    with wave.open(wav_files[0], "rb") as wf:
        params = wf.getparams()

    with wave.open(output_path, "wb") as out_wf:
        out_wf.setparams(params)
        for wav_file in wav_files:
            with wave.open(wav_file, "rb") as wf:
                out_wf.writeframes(wf.readframes(wf.getnframes()))


def normalize_wav(input_path, output_path, sample_rate=22050, channels=1):
    """ffmpegでWAVを統一フォーマットに変換"""
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-ar", str(sample_rate),
         "-ac", str(channels), "-sample_fmt", "s16", output_path],
        capture_output=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="問題と答えのリストから音声ファイルを生成します"
    )
    parser.add_argument("-o", "--output", default=os.path.join(SCRIPT_DIR, "output.mp3"), help="出力ファイルパス（デフォルト: 同ディレクトリのoutput.mp3）")
    parser.add_argument("-d", "--delay", type=int, default=5, help="問題と答えの間の秒数（デフォルト: 5）")
    parser.add_argument("--rate", type=int, default=150, help="読み上げ速度（デフォルト: 150）")
    args = parser.parse_args()

    input_path = os.path.join(SCRIPT_DIR, "input.txt")
    if not os.path.exists(input_path):
        print(f"エラー: {input_path} が見つかりません。")
        return 1

    # ffmpegの確認
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("エラー: ffmpegがインストールされていません。'brew install ffmpeg' を実行してください。")
        return 1

    pairs = parse_input(input_path)
    if not pairs:
        print("エラー: 有効なQ&Aペアが見つかりません。")
        return 1

    print(f"{len(pairs)}個のQ&Aペアを読み込みました。")
    print(f"問題と答えの間隔: {args.delay}秒")

    engine = pyttsx3.init()
    engine.setProperty("rate", args.rate)

    # 日本語の音声を探して設定
    voices = engine.getProperty("voices")
    for voice in voices:
        if "ja-JP" in voice.id or "ja_JP" in voice.id:
            engine.setProperty("voice", voice.id)
            print(f"音声: {voice.id}")
            break

    sample_rate = 22050
    channels = 1

    with tempfile.TemporaryDirectory() as tmpdir:
        all_segments = []

        for i, (question, answer) in enumerate(pairs):
            print(f"  [{i+1}/{len(pairs)}] 処理中: {question[:30]}...")

            q_raw = os.path.join(tmpdir, f"q_{i}_raw.aiff")
            q_norm = os.path.join(tmpdir, f"q_{i}.wav")
            text_to_wav(engine, question, q_raw)
            normalize_wav(q_raw, q_norm, sample_rate, channels)

            silence_path = os.path.join(tmpdir, f"silence_{i}.wav")
            create_silence_wav(silence_path, args.delay, sample_rate, channels)

            a_raw = os.path.join(tmpdir, f"a_{i}_raw.aiff")
            a_norm = os.path.join(tmpdir, f"a_{i}.wav")
            text_to_wav(engine, answer, a_raw)
            normalize_wav(a_raw, a_norm, sample_rate, channels)

            if i > 0:
                gap_path = os.path.join(tmpdir, f"gap_{i}.wav")
                create_silence_wav(gap_path, 2, sample_rate, channels)
                all_segments.append(gap_path)

            all_segments.append(q_norm)
            all_segments.append(silence_path)
            all_segments.append(a_norm)

        combined_wav = os.path.join(tmpdir, "combined.wav")
        concatenate_wavs(all_segments, combined_wav)

        print(f"音声ファイルを出力中: {args.output}")
        subprocess.run(
            ["ffmpeg", "-y", "-i", combined_wav, "-codec:a", "libmp3lame", "-q:a", "2", args.output],
            capture_output=True,
        )

    print("完了しました。")
    return 0


if __name__ == "__main__":
    exit(main())
