import argparse
import yt_dlp # python3 -m pip install yt-dlp --break-system-packages でインストール
import os

def load_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
            return urls
    except FileNotFoundError:
        print(f"❌ URLファイルが見つかりません: {file_path}")
        return []

def main():
    parser = argparse.ArgumentParser(description="YouTubeダウンロードツール")
    parser.add_argument('--url-file', required=True, help='URL一覧のファイルパス')
    parser.add_argument('--audio-only', action='store_true', help='音声のみをMP3でダウンロード')
    parser.add_argument('--output-dir', default='downloads', help='保存先ディレクトリ')
    parser.add_argument('--format', help='動画フォーマット指定（yt-dlpのformatに準拠）')

    args = parser.parse_args()
    urls = load_urls_from_file(args.url_file)

    if not urls:
        print("❌ URLが読み込めませんでした。")
        return

    os.makedirs(args.output_dir, exist_ok=True)

    # yt-dlpのオプション構築
    ydl_opts = {
        'cookiesfrombrowser': ('chrome',),
        'outtmpl': os.path.join(args.output_dir, '%(title)s.%(ext)s'),
    }

    if args.audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    elif args.format:
        ydl_opts['format'] = args.format
    else:
        ydl_opts['format'] = 'best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"🔽 ダウンロード開始: {url}")
            try:
                ydl.download([url])
            except Exception as e:
                print(f"❌ エラー: {url} → {e}")

if __name__ == "__main__":
    main()
