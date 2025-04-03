# R2Uploader
MIT License

# 使い方
1. `pip install -r requirements.txt`
2. `config.json`にcloudflare r2のエンドポイント・アクセストークン・シークレットアクセスキーを入力。 (`public_url`は任意)
3. `upload`フォルダにフォルダ / ファイルを入れる。 (フォルダを入れた場合、フォルダを維持したままアップロードされます。)
4. `python main.py`で実行

# Futures
- 画像の場合、位置情報などの情報を削除。(exifの削除)
  - 画像の向き等も保持されます。

これだけ
自由に使っていいよ