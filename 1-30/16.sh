#!/bin/bash

# 引数が指定されているか確認
if [ -z "$1" ]; then
  echo "URLを指定してください。"
  exit 1
fi

if [ -z "$2" ]; then
  echo "HTTPメソッドを指定してください。"
  exit 1
fi

# 引数からURLとHTTPメソッドを取得
url=$1
method=$2

# curlコマンドを生成
curl_command="curl -X $method $url"

# 生成されたcurlコマンドを表示
echo "生成されたcurlコマンド: $curl_command"

# curlコマンドを実行
# eval $curl_command

# 利用例:
# sh ./1-30/16.sh http://example.com GET
# sh ./1-30/16.sh http://example.com POST


