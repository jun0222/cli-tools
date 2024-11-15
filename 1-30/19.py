# markdown to html converter
# 実行例: python3 1-30/19.py markdown example.md example2.md

# ライブラリをインポート
import sys
import markdown

# 第一引数、第二引数、第三引数を変数に格納
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]

# 第一引数が"markdown"の場合
if arg1 == "markdown":
    
    # 第二引数のmdファイルをhtmlに変換し、第三引数のpathにファイルとして保存
    with open(arg3, "w") as f:
        f.write(markdown.markdown(open(arg2).read()))