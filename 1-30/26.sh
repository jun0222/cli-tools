#!/bin/bash

# 使い方を表示する関数
show_usage() {
  echo "使い方: $0 [テキスト]"
  echo "引数なしで実行すると対話モードになります"
  echo ""
  echo "例:"
  echo "  $0 \"重要なメッセージ\"  # 対話式で色を選択"
  echo "  $0                    # 全て対話式で入力"
}

# 色を対話的に選択させる関数
select_color() {
  echo "色を選択してください:"
  echo "1) \033[31m赤\033[0m"
  echo "2) \033[32m緑\033[0m"
  echo "3) \033[33m黄\033[0m"
  echo "4) \033[34m青\033[0m"
  echo "5) \033[35mマゼンタ\033[0m"
  echo "6) \033[36mシアン\033[0m"
  echo "0) キャンセル"
  echo ""
  read -p "番号を入力してください (1-6): " COLOR_NUM
  
  case $COLOR_NUM in
    1)
      COLOR_CODE="31"
      COLOR_NAME="赤"
      ;;
    2)
      COLOR_CODE="32"
      COLOR_NAME="緑"
      ;;
    3)
      COLOR_CODE="33"
      COLOR_NAME="黄"
      ;;
    4)
      COLOR_CODE="34"
      COLOR_NAME="青"
      ;;
    5)
      COLOR_CODE="35"
      COLOR_NAME="マゼンタ"
      ;;
    6)
      COLOR_CODE="36"
      COLOR_NAME="シアン"
      ;;
    0)
      echo "キャンセルされました"
      exit 0
      ;;
    *)
      echo "無効な選択です。もう一度試してください。"
      select_color
      ;;
  esac
  
  echo "選択された色: \033[${COLOR_CODE}m${COLOR_NAME}\033[0m"
}

# テキストを対話的に入力させる関数
input_text() {
  read -p "テキストを入力してください: " TEXT
  
  if [ -z "$TEXT" ]; then
    echo "テキストが空です。もう一度試してください。"
    input_text
  fi
}

# 引数からテキストを取得
TEXT="$*"

# テキストが指定されていない場合は対話的に入力を求める
if [ -z "$TEXT" ]; then
  input_text
fi

# 色を対話的に選択
select_color

# 色付きテキストを出力
echo ""
echo "結果:"
echo -e "\033[${COLOR_CODE}m${TEXT}\033[0m"

# コピー用コマンドを表示
echo ""
echo "コピー用コマンド:"
printf 'echo "\\033[%sm%s\\033[0m"\n' "${COLOR_CODE}" "${TEXT}"