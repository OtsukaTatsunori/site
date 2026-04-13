#!/bin/bash
# ショート動画ジェネレーター 起動スクリプト
# 使い方: ダブルクリック or ターミナルで ./start.sh

cd "$(dirname "$0")"

echo "==============================="
echo " ショート動画ジェネレーター"
echo "==============================="
echo ""

# 依存パッケージの確認・インストール
echo "[1/4] Python依存パッケージを確認中..."
pip3 install -q fastapi uvicorn python-multipart aiofiles httpx 2>/dev/null

echo "[2/4] Node依存パッケージを確認中..."
cd src/client
if [ ! -d "node_modules" ]; then
  npm install --silent
fi
cd ../..

# バックエンド起動
echo "[3/4] バックエンドを起動中..."
python3 -m uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# フロントエンド起動
echo "[4/4] フロントエンドを起動中..."
cd src/client
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
cd ../..

echo ""
echo "==============================="
echo " 起動完了！"
echo " ブラウザで開いてください:"
echo " http://localhost:5173"
echo "==============================="
echo ""
echo "終了するには Ctrl+C を押してください"
echo ""

# Ctrl+C で両方のプロセスを終了
cleanup() {
  echo ""
  echo "サーバーを停止中..."
  kill $BACKEND_PID 2>/dev/null
  kill $FRONTEND_PID 2>/dev/null
  exit 0
}
trap cleanup INT TERM

# プロセスが終了するまで待機
wait
