@echo off

cd /d "%~dp0"

echo ================================
echo  Short Video Generator (Docker)
echo ================================
echo.
echo Starting...
echo.

docker compose up --build -d

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker is not running.
    echo Please start Docker Desktop first, then double-click this file again.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================
echo  Ready!
echo  Opening http://localhost:8000
echo ================================
echo.

timeout /t 3 >nul
start http://localhost:8000

echo Press any key to stop the server...
pause >nul

docker compose down
echo Stopped.
pause >nul
