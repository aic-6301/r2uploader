import os
import json
import boto3
import shutil
from botocore.config import Config
from PIL import Image, ImageOps
import io

# Load configuration
with open("config.json") as f:
    config = json.load(f)

s3 = boto3.client(
    "s3",
    endpoint_url=config['endpoint'],
    aws_access_key_id=config['access_key_id'],
    aws_secret_access_key=config['secret_access_key'],
    config=Config(signature_version="s3v4"),
)

bucket = config['bucket']
public_url = config['public_url']

def upload_folder_to_s3(folder_path, bucket_name):
    count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == ".gitkeep":
                continue
                
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, folder_path).replace("\\", "/")
                
            # 画像ファイルの場合
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    print(f"処理中: {file_path}")
                    # PILを使って画像を開く
                    img = Image.open(file_path)
                    
                    # 画像の向きを保持
                    img = ImageOps.exif_transpose(img)
                    
                    format_name = os.path.splitext(file)[1].strip('.').upper()
                    if format_name == 'JPG':
                        format_name = 'JPEG'

                    img_buffer = io.BytesIO()
                    
                    # JPEGの場合は品質を指定して保存
                    if format_name == 'JPEG':
                        img.save(img_buffer, format=format_name, quality=95, optimize=True)
                    else:
                        img.save(img_buffer, format=format_name)
                    
                    img_buffer.seek(0)
                    
                    # メモリ上のデータをS3にアップロード
                    s3.upload_fileobj(img_buffer, bucket_name, s3_key)
                except Exception as e:
                    print(f"画像処理に失敗しました {file_path}: {e}")
                    # 失敗した場合は元のファイルをそのままアップロード
                    s3.upload_file(file_path, bucket_name, s3_key)
            else:
                # 画像以外のファイルは直接アップロード
                s3.upload_file(file_path, bucket_name, s3_key)
                
            print(f"アップロード完了: {file_path} → {public_url}/{s3_key}")
            count += 1
        
    if count == 0:
        print("アップロードするファイルがありませんでした。")
    else:
        print(f"{count}ファイルをアップロードしました。")

# Upload the contents of the "upload/" folder
upload_folder_to_s3("upload", bucket)