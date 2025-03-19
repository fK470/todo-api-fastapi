# Python のイメージを使用 (バージョンは適宜変更)
FROM python:3.9-slim-buster

# 作業ディレクトリの設定
WORKDIR /app

# パッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY . .

# ポートの公開 (FastAPI のデフォルトは 8000)
EXPOSE 8000

# アプリケーションの起動 (uvicorn を使用)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]