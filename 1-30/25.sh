#!/bin/bash

# 24色のカラーコードをセット（ループを使わずに直接記述）
COLOR_TEXT="カラーテキスト表示"

# ANSIエスケープシーケンスを使用して前景色を設定
# 8色基本 + 明るい色の8色
# echo "\033[30m$COLOR_TEXT\033[0m - 黒 (30)"
echo "\033[31m$COLOR_TEXT\033[0m - 赤 (31)"
echo "\033[32m$COLOR_TEXT\033[0m - 緑 (32)"
echo "\033[33m$COLOR_TEXT\033[0m - 黄 (33)"
echo "\033[34m$COLOR_TEXT\033[0m - 青 (34)"
echo "\033[35m$COLOR_TEXT\033[0m - マゼンタ (35)"
echo "\033[36m$COLOR_TEXT\033[0m - シアン (36)"
# echo "\033[37m$COLOR_TEXT\033[0m - 白 (37)"

# echo "\033[90m$COLOR_TEXT\033[0m - 明るい黒/グレー (90)"
# echo "\033[91m$COLOR_TEXT\033[0m - 明るい赤 (91)"
# echo "\033[92m$COLOR_TEXT\033[0m - 明るい緑 (92)"
# echo "\033[93m$COLOR_TEXT\033[0m - 明るい黄 (93)"
# echo "\033[94m$COLOR_TEXT\033[0m - 明るい青 (94)"
# echo "\033[95m$COLOR_TEXT\033[0m - 明るいマゼンタ (95)"
# echo "\033[96m$COLOR_TEXT\033[0m - 明るいシアン (96)"
# echo "\033[97m$COLOR_TEXT\033[0m - 明るい白 (97)"

# 256色モードを使って追加の8色を表示
# echo "\033[38;5;208m$COLOR_TEXT\033[0m - オレンジ (38;5;208)"
# echo "\033[38;5;165m$COLOR_TEXT\033[0m - ピンク (38;5;165)"
# echo "\033[38;5;75m$COLOR_TEXT\033[0m - ライトブルー (38;5;75)"
# echo "\033[38;5;40m$COLOR_TEXT\033[0m - ライム (38;5;40)"
# echo "\033[38;5;129m$COLOR_TEXT\033[0m - 紫 (38;5;129)"
# echo "\033[38;5;166m$COLOR_TEXT\033[0m - 茶色 (38;5;166)"
# echo "\033[38;5;51m$COLOR_TEXT\033[0m - ターコイズ (38;5;51)"
# echo "\033[38;5;201m$COLOR_TEXT\033[0m - ホットピンク (38;5;201)"

# もう一つの方法: printfを使用した例
# printf "\n代替方法（printf使用）:\n"
# printf "\033[31m%s\033[0m - 赤（printfバージョン）\n" "$COLOR_TEXT"