#!/bin/bash

# 指定ファイルに関しては、内容を見てコミットメッセージに反映する
updated_file="output.md"
first_line=$(head -n 1 "$updated_file" | sed "s/#//g")
git add "$updated_file"
git commit -m "autocommit: $first_line"

# それ以外のファイルは、全ての変更を同じメッセージでコミットする
git add .
git commit -m "autocommit"
git push origin HEAD