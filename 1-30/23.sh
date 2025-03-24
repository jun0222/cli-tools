#!/bin/bash

# 出力ファイル名
output_file="id-pw.md"
temp_file=$(mktemp)

# タイトル入力
read -p "タイトルを入力してください: " title

# IDとPasswordの入力（表示あり）
read -p "Enter ID: " user_id
read -p "Enter Password: " user_password

# 一時ファイルに追記内容を記述
{
  echo "## $title"
  echo ""
  echo "- ID: $user_id"
  echo "- Password: $user_password"
} >> "$temp_file"

# 追加項目の入力確認ループ
while true; do
  read -p "他に入力したい項目はありますか？ (y/n): " yn
  case $yn in
    [Yy]* ) 
      read -p "項目名（例：email）: " field
      read -p "値（例：foo@example.com）: " value
      echo "- $field: $value" >> "$temp_file"
      ;;
    [Nn]* ) 
      break
      ;;
    * ) echo "y か n で答えてください。";;
  esac
done

# 改行追加してから元の内容を後ろに追加
echo "" >> "$temp_file"
if [ -f "$output_file" ]; then
  cat "$output_file" >> "$temp_file"
fi

# 上書き保存（先頭に追記された形になる）
mv "$temp_file" "$output_file"

echo ""
echo "Markdownファイル \"$output_file\" の先頭に追加されました。"
