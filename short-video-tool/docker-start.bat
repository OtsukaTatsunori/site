@echo off
chcp 65001 >nul
title ショート動画ジェネレーター (Docker)

echo ===============================
echo  ショート動画ジェネレーター
echo ===============================
echo.

cd /d "%~dp0"

echo 起動中（初回は数分かかります）...
echo.

docker compose up --build -d

if %errorlevel% neq 0 (
    echo.
    echo [エラー] Docker が起動していません。
    echo Docker Desktop を起動してから、もう一度このファイルをダブルクリックしてください。
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================
echo  起動完了！
echo  ブラウザが自動で開きます
echo ===============================
echo.

timeout /t 3 >nul
start http://localhost:8000

echo 終了するには何かキーを押してください...
echo （サーバーはバックグラウンドで動き続けます）
echo.
echo 完全に停止したい場合はもう一度このウィンドウで
echo 何かキーを押してください。
pause >nul

echo.
echo サーバーを停止しますか？ (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    docker compose down
    echo 停止しました。
)
pause >nul
