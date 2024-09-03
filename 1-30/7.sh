#!/bin/bash

directory="./1-30"

# 指定されたディレクトリ内の最大の数字を持つ .sh ファイルを見つける
max_number=$(ls "$directory"/*.sh 2>/dev/null | grep -oE '[0-9]+\.sh$' | sort -n | tail -n 1 | cut -d. -f1)

# 最大の数字が見つからない場合は 0 とする
if [ -z "$max_number" ]; then
    max_number=0
fi

# 次の番号を計算
next_number=$((max_number + 1))

# 新しいファイル名を作成
new_file="$directory/$next_number.sh"

# 新しいファイルを作成し、シェバンを書き込む
echo '#!/bin/bash' > "$new_file"

# ファイルに実行権限を付与
chmod +x "$new_file"

echo "新しいファイル '$new_file' が作成されました。"
