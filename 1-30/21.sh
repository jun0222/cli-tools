#!/bin/bash

# Gitリポジトリか確認
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "エラー: このディレクトリはGitリポジトリではありません。"
    exit 1
fi

# 変更のあるファイルを取得 (ステージングされていない変更を含む)
changed_files=$(git ls-files --modified --others --exclude-standard)

# 変更がない場合
if [ -z "$changed_files" ]; then
    echo "変更されたファイルがありません。"
    exit 0
fi

# 1ファイルずつコミット
for file in $changed_files; do
    git add "$file"
    git commit -m "$file"
    echo "Committed: $file"
done

# 最後に push
git push
echo "変更をリモートリポジトリにプッシュしました。"
