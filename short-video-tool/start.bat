@echo off
chcp 65001 >nul
title ショート動画ジェネレーター

echo ===============================
echo  ショート動画ジェネレーター
echo ===============================
echo.

cd /d "%~dp0"

echo [1/4] Python依存パッケージを確認中...
pip install -q fastapi uvicorn python-multipart aiofiles httpx 2>nul

echo [2/4] Node依存パッケージを確認中...
cd src\client
if not exist "node_modules" (
  npm install --silent
)
cd ..\..

echo [3/4] バックエンドを起動中...
start /b python -m uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload

echo [4/4] フロントエンドを起動中...
cd src\client
start /b npm run dev -- --host 0.0.0.0
cd ..\..

echo.
echo ===============================
echo  起動完了！
echo  ブラウザで開いてください:
echo  http://localhost:5173
echo ===============================
echo.

timeout /t 3 >nul
start http://localhost:5173

echo 終了するにはこのウィンドウを閉じてください
pause >nul
