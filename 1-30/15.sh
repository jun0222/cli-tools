#!/bin/bash

# 引数が指定されているか確認
if [ -z "$1" ]; then
  echo "拡張子を指定してください。"
  exit 1
fi

# 新規ファイル名を生成
filename="$(date +%Y%m%d%s).$1"

# 新規ファイルを作成
touch $filename

# 作成したファイル名を表示
echo "新規ファイルを作成しました: $filename"
