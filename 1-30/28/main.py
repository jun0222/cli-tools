#!/usr/bin/env python3
"""問題と答えのリストから、問題→n秒後に答えを読み上げる音声ファイルを生成するCLIツール"""
# python 1-30/28/main.py
import argparse
import os
import struct
import subprocess
import tempfile
import wave

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


def text_to_aiff(text, output_path, voice="Kyoko", rate=200):
    """macOS sayコマンドでテキストをAIFFファイルに変換"""
    result = subprocess.run(
        ["say", "-v", voice, "-r", str(rate), "-o", output_path, text],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"警告: say コマンドエラー: {result.stderr}")


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


def aiff_to_wav(input_path, output_path, sample_rate=22050, channels=1):
    """ffmpegでAIFFをWAVに変換（フォーマット統一）"""
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
    parser.add_argument("-m", "--mode", choices=["normal", "q", "reverse"], default="normal",
                        help="モード: normal=問題→答え, q=問題のみ, reverse=答え→問題（デフォルト: normal）")
    parser.add_argument("--rate", type=int, default=200, help="読み上げ速度（デフォルト: 200）")
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
    mode_label = {"normal": "問題→答え", "q": "問題のみ", "reverse": "答え→問題"}
    print(f"モード: {mode_label[args.mode]}、間隔: {args.delay}秒")

    sample_rate = 22050
    channels = 1

    with tempfile.TemporaryDirectory() as tmpdir:
        all_segments = []

        for i, (question, answer) in enumerate(pairs):
            print(f"  [{i+1}/{len(pairs)}] 処理中: {question[:30]}...")

            # 問題の音声生成
            q_aiff = os.path.join(tmpdir, f"q_{i}.aiff")
            q_wav = os.path.join(tmpdir, f"q_{i}.wav")
            text_to_aiff(question, q_aiff, rate=args.rate)
            aiff_to_wav(q_aiff, q_wav, sample_rate, channels)

            # 答えの音声生成
            a_aiff = os.path.join(tmpdir, f"a_{i}.aiff")
            a_wav = os.path.join(tmpdir, f"a_{i}.wav")
            if args.mode != "q":
                text_to_aiff(answer, a_aiff, rate=args.rate)
                aiff_to_wav(a_aiff, a_wav, sample_rate, channels)

            # ペア間の無音（最初以外）
            if i > 0:
                gap_path = os.path.join(tmpdir, f"gap_{i}.wav")
                create_silence_wav(gap_path, 2, sample_rate, channels)
                all_segments.append(gap_path)

            # 考える対象の文章長に応じて待ち時間を調整
            # 10文字を基準に、長いほど待ち時間を伸ばす
            if args.mode == "reverse":
                target_len = len(question)
            else:
                target_len = len(answer)
            delay_sec = args.delay * max(1.0, target_len / 10)

            silence_path = os.path.join(tmpdir, f"silence_{i}.wav")
            create_silence_wav(silence_path, delay_sec, sample_rate, channels)

            if args.mode == "q":
                all_segments.append(q_wav)
            elif args.mode == "reverse":
                all_segments.append(a_wav)
                all_segments.append(silence_path)
                all_segments.append(q_wav)
            else:
                all_segments.append(q_wav)
                all_segments.append(silence_path)
                all_segments.append(a_wav)

            # 末尾の間（1秒）
            after_path = os.path.join(tmpdir, f"after_{i}.wav")
            create_silence_wav(after_path, 1, sample_rate, channels)
            all_segments.append(after_path)

        # 全セグメントを結合
        combined_wav = os.path.join(tmpdir, "combined.wav")
        concatenate_wavs(all_segments, combined_wav)

        # MP3に変換（音量正規化付き）
        print(f"音声ファイルを出力中: {args.output}")
        subprocess.run(
            ["ffmpeg", "-y", "-i", combined_wav,
             "-filter:a", "loudnorm=I=-14:TP=-1:LRA=11",
             "-codec:a", "libmp3lame", "-q:a", "2", args.output],
            capture_output=True,
        )

    print("完了しました。")
    return 0


if __name__ == "__main__":
    exit(main())
