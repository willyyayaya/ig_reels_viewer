@echo off
echo 🎬 啟動 Instagram Reels Viewer 前端...
echo.
cd frontend
echo 📦 安裝依賴...
call npm install
echo.
echo 🚀 啟動開發服務器...
call npm run dev
pause
