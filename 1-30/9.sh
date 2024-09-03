#!/bin/bash
# 実行例:  sh ./1-30/9.sh 456aBaedEE
# TODO: 小文字対応


# アスキーアートの定義
ascii_art_0="
 ###
#   #
#   #
#   #
 ###
"
ascii_art_1="
  #
 ##
  #
  #
 ###
"
ascii_art_2="
 ###
#   #
  ##
 #
#####
"
ascii_art_3="
 ###
#   #
  ##
#   #
 ###
"
ascii_art_4="
#   #
#   #
#####
    #
    #
"
ascii_art_5="
#####
#
####
    #
####
"
ascii_art_6="
 ###
#
####
#   #
 ###
"
ascii_art_7="
#####
   #
  #
 #
#
"
ascii_art_8="
 ###
#   #
 ###
#   #
 ###
"
ascii_art_9="
 ###
#   #
 ####
    #
 ###
"
ascii_art_A="
 ###
#   #
#####
#   #
#   #
"
ascii_art_B="
####
#   #
####
#   #
####
"
ascii_art_C="
 ###
#   #
#
#   #
 ###
"
ascii_art_D="
####
#   #
#   #
#   #
####
"
ascii_art_E="
#####
#
###
#
#####
"
ascii_art_F="
#####
#
###
#
#
"
ascii_art_G="
 ###
#
#  ##
#   #
 ###
"
ascii_art_H="
#   #
#   #
#####
#   #
#   #
"
ascii_art_I="
###
 #
 #
 #
###
"
ascii_art_J="
  ###
   #
   #
#  #
 ##
"
ascii_art_K="
#   #
#  #
###
#  #
#   #
"
ascii_art_L="
#
#
#
#
#####
"
ascii_art_M="
#   #
## ##
# # #
#   #
#   #
"
ascii_art_N="
#   #
##  #
# # #
#  ##
#   #
"
ascii_art_O="
 ###
#   #
#   #
#   #
 ###
"
ascii_art_P="
####
#   #
####
#
#
"
ascii_art_Q="
 ###
#   #
# # #
#  #
 ## #
"
ascii_art_R="
####
#   #
####
#  #
#   #
"
ascii_art_S="
 ####
#
 ###
    #
####
"
ascii_art_T="
#####
  #
  #
  #
  #
"
ascii_art_U="
#   #
#   #
#   #
#   #
 ###
"
ascii_art_V="
#   #
#   #
#   #
 # #
  #
"
ascii_art_W="
#   #
#   #
# # #
## ##
#   #
"
ascii_art_X="
#   #
 # #
  #
 # #
#   #
"
ascii_art_Y="
#   #
 # #
  #
  #
  #
"
ascii_art_Z="
#####
   #
  #
 #
#####
"
ascii_art_a="
 ###
#   #
#####
#   #
#   #
"
ascii_art_b="
####
#   #
####
#   #
####
"
    ascii_art_c="
 ###
#   #
#
#   #
 ###
"
ascii_art_d="
####
#   #
#   #
#   #
####
"
ascii_art_e="
#####
#
###
#
#####
"
ascii_art_f="
#####
#
###
#
#
"
ascii_art_g="
 ###
#
#  ##
#   #
 ###
"
ascii_art_h="
#   #
#   #
#####
#   #
#   #
"
ascii_art_i="
###
 #
 #
 #
###
"
ascii_art_j="
  ###
   #
   #
#  #
 ##
"
ascii_art_k="
#   #
#  #
###
#  #
#   #
"
ascii_art_l="
#
#
#
#
#####
"
ascii_art_m="
#   #
## ##
# # #
#   #
#   #
"
ascii_art_n="
#   #
##  #
# # #
#  ##
#   #
"
ascii_art_o="
 ###
#   #
#   #
#   #
 ###
"
ascii_art_p="
####
#   #
####
#
#
"
ascii_art_q="
 ###
#   #
# # #
#  #
 ## #
"
ascii_art_r="
####
#   #
####
#  #
#   #
"
ascii_art_s="
 ####
#
 ###
    #
####
"
ascii_art_t="
#####
  #
  #
  #
  #
"
ascii_art_u="
#   #
#   #
#   #
#   #
 ###
"
ascii_art_v="
#   #
#   #
#   #
 # #
  #
"
ascii_art_w="
#   #
#   #
# # #
## ##
#   #
"
ascii_art_x="
#   #
 # #
  #
 # #
#   #
"
ascii_art_y="
#   #
 # #
  #
  #
  #
"
ascii_art_z="
#####
   #
  #
 #
#####
"

# 引数をアスキーアートに変換する関数
convert_to_ascii_art() {
    local input=$1
    local length=${#input}
    local output=""

    for ((i=0; i<length; i++)); do
        char=${input:$i:1}
        char_lower=$(echo "$char" | tr '[:upper:]' '[:lower:]')
        ascii_art_var="ascii_art_${char_lower}"
        if [ -n "${!ascii_art_var}" ]; then
            output+="${!ascii_art_var}\n"
        else
            echo "エラー: 文字 '$char' はサポートされていません。"
            exit 1
        fi
    done

    echo -e "$output"
}

# メイン処理
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <数字またはアルファベット>"
    exit 1
fi

convert_to_ascii_art "$1"

