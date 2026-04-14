FROM node:22-slim AS frontend-build
WORKDIR /app/client
COPY src/client/package.json src/client/package-lock.json ./
RUN npm ci --silent
COPY src/client/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# FFmpegと日本語フォントをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*

# Notoフォントをassets/fontsにコピー
RUN mkdir -p /app/assets/fonts && \
    cp /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc /app/assets/fonts/

# Python依存パッケージ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# バックエンドのコード
COPY src/server/ /app/src/server/

# フロントエンドのビルド済みファイル
COPY --from=frontend-build /app/client/dist /app/static

# フォルダ作成
RUN mkdir -p /app/assets/backgrounds /app/assets/bgm /app/assets/fonts /app/assets/overlays \
    /app/templates /app/projects /app/temp/tts /app/output

# 設定ファイル
COPY config.json /app/

# サンプル素材があればコピー
COPY assets/ /app/assets/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
