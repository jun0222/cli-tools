import argparse
from moviepy.editor import VideoFileClip
import os

def compress_video(input_path, output_path, target_resolution=(1280, 720), bitrate="500k"):
    """
    動画の容量を小さくするための圧縮関数
    
    :param input_path: 元の動画ファイルのパス
    :param output_path: 圧縮後の動画を保存するパス
    :param target_resolution: 圧縮後の解像度 (幅, 高さ)
    :param bitrate: ビットレートを指定 ("500k" のように指定する)
    """
    try:
        # 動画を読み込み
        clip = VideoFileClip(input_path)

        # 動画をリサイズ（解像度を変更）
        resized_clip = clip.resize(newsize=target_resolution)

        # 一時ファイルとして圧縮する
        temp_output = "temp_" + os.path.basename(output_path)

        # 圧縮した動画を一時ファイルに保存
        resized_clip.write_videofile(
            temp_output,
            bitrate=bitrate,
            codec="libx264",  # H.264形式で保存
            audio_codec="aac",  # AAC音声形式
            temp_audiofile="temp-audio.m4a",  # 一時的な音声ファイル
            remove_temp=True  # 一時ファイルを削除
        )

        # 圧縮後の動画を移動
        os.rename(temp_output, output_path)
        print(f"動画を圧縮して {output_path} に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    # 引数解析のためのセットアップ
    parser = argparse.ArgumentParser(description="動画ファイルを圧縮します")
    parser.add_argument("input", help="入力動画ファイルのパスを指定してください")
    parser.add_argument("output", help="出力動画ファイルのパスを指定してください")
    parser.add_argument("--resolution", type=str, default="1280x720", help="圧縮後の解像度 (デフォルトは1280x720)")
    parser.add_argument("--bitrate", type=str, default="500k", help="圧縮後のビットレート (デフォルトは500k)")

    args = parser.parse_args()

    # 解像度をパース
    resolution = tuple(map(int, args.resolution.split("x")))

    # 動画を圧縮
    compress_video(args.input, args.output, target_resolution=resolution, bitrate=args.bitrate)

# 実行例
#  python ./1-30/18.py /path/to/input.mov /path/to/output.mov