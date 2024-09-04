#!/bin/bash

# 引数の数をチェック
if [ $# -lt 3 ]; then
    echo "使用法: $0 <コマンド> <開始番号> <終了番号>"
    exit 1
fi

# 引数を変数に格納
command=$1
start=$2
end=$3

# 指定された範囲で繰り返し実行
for i in $(seq $start $end); do
    echo "================================================"
    echo "実行: $command $i"
    $command $i
done

# 実行例
# echo "実行例:"
# echo "./$(basename $0) echo 1 5"
# echo "結果:"
# echo "実行: echo 1"
# echo "1"
# echo "実行: echo 2"
# echo "2"
# echo "実行: echo 3"
# echo "3"
# echo "実行: echo 4"
# echo "4"
# echo "実行: echo 5"
# echo "5"

