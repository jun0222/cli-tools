#!/bin/bash

# 引数の数が正しいか確認
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <対象文字列> <検索する文字列> <置き換える文字列>"
  exit 1
fi

# 引数を変数に格納
input=$1    # 対象文字列
search=$2   # 検索する文字列
replace=$3  # 置き換える文字列

# 特殊文字に対するエスケープ処理
escaped_search=$(echo "$search" | sed 's/[]\/$*.^|[]/\\&/g')
escaped_replace=$(echo "$replace" | sed 's/[&/\]/\\&/g')

# 置き換え操作
output=$(echo "$input" | sed "s/$escaped_search/$escaped_replace/g")

# 結果を表示
echo "$output"
