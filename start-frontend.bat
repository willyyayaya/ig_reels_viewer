@echo off
echo Starting Instagram Reels Viewer Frontend...
echo =========================================

cd frontend

echo Checking Node.js version...
node --version
if %errorlevel% neq 0 (
    echo Error: Node.js not found. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
npm install

echo.
echo Starting development server...
npm run dev

pause
