import yt_dlp # python3 -m pip install yt-dlp --break-system-packages でインストール

# 動画のURL
url = ''

ydl_opts = {
    'cookiesfrombrowser': ('chrome',),  # ブラウザのログイン情報を使う
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'best'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
