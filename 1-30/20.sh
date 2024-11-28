#!/bin/bash

# ファイル名を受け取る
INPUT_FILE="$1"
TEMP_FILE="${INPUT_FILE}.tmp"

# ファイルが存在するかチェック
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File $INPUT_FILE does not exist."
  exit 1
fi

# 改行の末尾に半角スペース2つがない行だけ処理
awk '/  $/ {print $0} !/  $/ {print $0 "  "}' "$INPUT_FILE" > "$TEMP_FILE"

# 一時ファイルを元のファイルに上書き
mv "$TEMP_FILE" "$INPUT_FILE"

echo "Processed file saved as $INPUT_FILE"

# 使用例: sh ./1-30/20.sh file.md