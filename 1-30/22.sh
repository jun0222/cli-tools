#!/bin/sh

set -e  # エラー時にスクリプトを終了

# 整理対象のディレクトリ
sources="$HOME/Desktop $HOME/Downloads"

# 各カテゴリごとに、移動対象のファイルパターンをリスト化
groups="
Presentations|*.pptx *.ppt *.key *.odp
Installers|*.zip *.dmg *.pkg *.tar *.gz *.7z
SourceCode|*.html *.js *.ts *.jsx *.tsx *.sql *.css *.yml *.py *.rb *.java
Images|スクリーンショット* *.png *.jpg *.jpeg *.gif *.bmp *.svg
Videos|画面収録* *.mov *.mp4 *.avi *.mkv *.wmv
Documents|*.csv *.txt *.json *.md *.xm *.drawio *.pdf *.doc *.docx *.odt *.xls *.xlsx
3dData|*.stl *.obj *.fbx *.blend *.3ds
Music|*.mp3 *.wav *.flac *.m4a *.ogg
"

# 各整理元ディレクトリを個別に処理
for src in $sources; do
  if [ ! -d "$src" ]; then
    echo "Directory $src does not exist. Skipping..."
    continue
  fi

  echo "Processing $src"

  # `groups` のリストを1行ずつ処理
  echo "$groups" | while IFS='|' read -r group patterns; do
    dest_dir="$src/$group"

    # フォルダがなければ作成
    [ -d "$dest_dir" ] || mkdir -p "$dest_dir"

    # 各パターンごとにファイルを移動
    for pattern in $patterns; do
      for file in "$src"/$pattern; do
        [ -f "$file" ] && mv "$file" "$dest_dir/" && echo "Moved '$file' -> '$dest_dir/'"
      done
    done
  done
done

echo "ディレクトリ整理が完了しました。"
