from PIL import Image
import sys

def resize_image(input_path, output_path, target_size):
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            # 元の画像のアスペクト比を計算
            aspect_ratio = img.width / img.height
            
            # 新しいサイズを計算（アスペクト比を維持）
            if aspect_ratio > 1:
                new_width = target_size
                new_height = int(target_size / aspect_ratio)
            else:
                new_height = target_size
                new_width = int(target_size * aspect_ratio)
            
            # 画像をリサイズ
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # リサイズした画像を保存
            resized_img.save(output_path)
            print(f"画像を {new_width}x{new_height} にリサイズしました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("使用方法: python3 ./1-30/11.py <入力画像パス> <出力画像パス> <目標サイズ>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        target_size = int(sys.argv[3])
        resize_image(input_path, output_path, target_size)

# 使用例:
# python3 ./1-30/11.py input.jpg output.jpg 800