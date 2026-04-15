#!/bin/bash
# ショート動画ジェネレーター 起動スクリプト (Node不要版)
# 使い方: ./start.sh

cd "$(dirname "$0")"

echo "==============================="
echo " ショート動画ジェネレーター"
echo "==============================="
echo ""

echo "[1/3] Python依存パッケージを確認中..."
pip3 install -q fastapi uvicorn python-multipart aiofiles httpx 2>/dev/null

echo "[2/3] フロントエンド資材を確認中..."
if [ ! -f "static/index.html" ]; then
  echo ""
  echo "【警告】static/index.html が見つかりません。"
  echo "git pull で最新を取得するか、Node.js 環境で:"
  echo "  cd src/client && npm install && npm run build && cp -r dist/* ../../static/"
  echo "を実行してから再度このスクリプトを実行してください。"
  exit 1
fi

echo "[3/3] サーバーを起動中..."
echo ""
echo "==============================="
echo " ブラウザで開いてください:"
echo " http://localhost:8000"
echo "==============================="
echo ""
echo " 終了するには Ctrl+C を押してください"
echo ""

python3 -m uvicorn src.server.main:app --host 0.0.0.0 --port 8000
