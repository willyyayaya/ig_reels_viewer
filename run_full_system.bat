@echo off
echo 🎬 Instagram Reels Viewer - 完整系統啟動
echo ⚠️  警告：此工具僅供教育目的使用
echo.

echo 🔧 準備啟動前後端服務...
echo 將開啟兩個命令提示字元視窗
echo.

echo 🚀 啟動後端服務...
start "IG Reels Viewer - Backend" run_backend.bat

timeout /t 5 /nobreak

echo 🎨 啟動前端服務...
start "IG Reels Viewer - Frontend" run_frontend.bat

echo.
echo ✅ 系統啟動完成！
echo.
echo 📋 訪問地址：
echo    前端界面: http://localhost:3000
echo    後端 API: http://localhost:8000
echo    API 文檔: http://localhost:8000/docs
echo.
echo ⚠️  請注意：此工具僅供教育目的使用，請勿違反 Instagram 使用條款
echo.
pause
