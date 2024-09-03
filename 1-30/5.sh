#!/bin/bash

# 更新されたファイルのパスを取得
updated_file="ファイル名.md"

# ファイルの1行目を取得
first_line=$(head -n 1 "$updated_file" | sed "s/#//g")

# Gitに追加
git add "$updated_file"

# 1行目をコミットメッセージとして使用してコミット
git commit -m "autocommit: $first_line"