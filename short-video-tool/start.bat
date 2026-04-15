@echo off
chcp 65001 >nul
title ショート動画ジェネレーター

echo ===============================
echo  ショート動画ジェネレーター
echo ===============================
echo.

cd /d "%~dp0"

echo [1/3] Python依存パッケージを確認中...
pip install -q fastapi uvicorn python-multipart aiofiles httpx 2>nul

echo [2/3] フロントエンド資材を確認中...
if not exist "static\index.html" (
  echo.
  echo 【警告】static\index.html が見つかりません。
  echo git pull で最新を取得するか、Node.js 環境で
  echo  cd src\client ^& npm install ^& npm run build
  echo を実行してから再度このスクリプトを実行してください。
  echo.
  pause
  exit /b 1
)

echo [3/3] サーバーを起動中...
echo.
echo ===============================
echo  ブラウザで開いてください:
echo  http://localhost:8000
echo ===============================
echo.
echo  終了するには Ctrl+C を押してください
echo.

timeout /t 2 >nul
start http://localhost:8000

python -m uvicorn src.server.main:app --host 0.0.0.0 --port 8000
