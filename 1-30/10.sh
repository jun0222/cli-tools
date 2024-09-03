#!/bin/bash
# 様々な種類の乱数を生成するツール

# 整数の乱数を生成する関数
generate_integer() {
    local min=$1
    local max=$2
    echo $((RANDOM % (max - min + 1) + min))
}

# 浮動小数点数の乱数を生成する関数
generate_float() {
    local min=$1
    local max=$2
    local scale=$3
    echo "scale=$scale; $min + ($max - $min) * $RANDOM / 32768" | bc
}

# 文字列の乱数を生成する関数
generate_string() {
    local length=$1
    tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w "$length" | head -n 1
}

# UUIDを生成する関数
generate_uuid() {
    uuidgen
}

# メイン処理
echo "乱数生成ツールへようこそ！"
echo "1: 整数の乱数"
echo "2: 浮動小数点数の乱数"
echo "3: ランダムな文字列"
echo "4: UUID"
read -p "生成したい乱数の種類を選択してください (1-4): " choice

case $choice in
    1)
        read -p "最小値を入力してください: " min
        read -p "最大値を入力してください: " max
        result=$(generate_integer "$min" "$max")
        echo "生成された整数: $result"
        ;;
    2)
        read -p "最小値を入力してください: " min
        read -p "最大値を入力してください: " max
        read -p "小数点以下の桁数を入力してください: " scale
        result=$(generate_float "$min" "$max" "$scale")
        echo "生成された浮動小数点数: $result"
        ;;
    3)
        read -p "文字列の長さを入力してください: " length
        result=$(generate_string "$length")
        echo "生成された文字列: $result"
        ;;
    4)
        result=$(generate_uuid)
        echo "生成されたUUID: $result"
        ;;
    *)
        echo "無効な選択です。プログラムを終了します。"
        exit 1
        ;;
esac
