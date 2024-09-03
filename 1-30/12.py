from PIL import Image, ImageDraw, ImageFont
import sys

def create_dummy_image(width, height, text):
    # 画像を作成
    image = Image.new('RGB', (width, height), color='lightgray')
    draw = ImageDraw.Draw(image)

    # フォントを設定（システムにインストールされているフォントを使用）
    try:
        font = ImageFont.truetype('/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc', 40)
    except IOError:
        font = ImageFont.load_default()

    # テキストを描画
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((width - text_width) / 2, (height - text_height) / 2)
    draw.text(position, text, fill='black', font=font)

    # サイズ情報を描画
    size_text = f"{width}x{height}"
    size_bbox = draw.textbbox((0, 0), size_text, font=font)
    size_width = size_bbox[2] - size_bbox[0]
    size_height = size_bbox[3] - size_bbox[1]
    size_position = ((width - size_width) / 2, height - size_height - 10)
    draw.text(size_position, size_text, fill='black', font=font)

    return image

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("使用方法: python3 ./1-30/12.py <幅> <高さ> <テキスト>")
    else:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        text = sys.argv[3]
        
        image = create_dummy_image(width, height, text)
        output_path = f"dummy_{width}x{height}.png"
        image.save(output_path)
        print(f"ダミー画像を作成しました: {output_path}")

# 使用例:
# python3 ./1-30/12.py 800 600 "サンプルテキスト"
# 上記のコマンドは、幅800ピクセル、高さ600ピクセルのダミー画像を作成し、
# 中央に "サンプルテキスト" を表示します。
# 出力ファイル名は "dummy_800x600.png" となります。
