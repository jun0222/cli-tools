#!/bin/sh

# 設定
MEMO_DIR="./memos"
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%H:%M")

# メモディレクトリが存在しない場合は作成
if [ ! -d "$MEMO_DIR" ]; then
  mkdir -p "$MEMO_DIR"
  echo "メモディレクトリを作成しました: $MEMO_DIR"
fi

# 出力ファイル名の選択
echo "メモの種類を選択してください:"
echo "1) 会議メモ（meeting-notes.md）"
echo "2) 作業メモ（work-notes.md）"
read -p "選択 (1-2): " file_choice

if [ "$file_choice" = "1" ]; then
  output_file="$MEMO_DIR/meeting-notes.md"
elif [ "$file_choice" = "2" ]; then
  output_file="$MEMO_DIR/work-notes.md"
else
  echo "無効な選択です。デフォルトの meeting-notes.md を使用します。"
  output_file="$MEMO_DIR/meeting-notes.md"
fi

temp_file=$(mktemp)

# タイトル入力
read -p "タイトルを入力してください: " title

# メモの本文入力
echo "メモ内容を入力してください（終了するには新しい行で「END」と入力）:"
memo_content=""
while read line; do
  if [ "$line" = "END" ]; then
    break
  fi
  if [ -z "$memo_content" ]; then
    memo_content="$line"
  else
    memo_content="$memo_content
$line"
  fi
done

# タイムスタンプ付きのタイトル
timestamp_title="## $title ($DATE $TIME)"

# 一時ファイルにメモ内容を記述
echo "$timestamp_title" > "$temp_file"
echo "" >> "$temp_file"
echo "$memo_content" >> "$temp_file"
echo "" >> "$temp_file"
echo "---" >> "$temp_file"
echo "" >> "$temp_file"

# 既存のファイルに追記
if [ -f "$output_file" ]; then
  cat "$output_file" >> "$temp_file"
fi

# 保存（先頭に追記された形になる）
mv "$temp_file" "$output_file"

echo ""
echo "メモが \"$output_file\" に保存されました。"