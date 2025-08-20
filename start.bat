@echo off
echo Instagram Reels Viewer - Full Stack Application
echo ===============================================
echo.
echo This will start both backend (Port 8080) and frontend (Port 5173)
echo.
echo Please ensure you have:
echo - Java 17 or higher
echo - Node.js 16 or higher
echo - Chrome browser installed
echo.
pause

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && mvn spring-boot:run"

timeout /t 10 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8080
echo Frontend: http://localhost:5173
echo.
echo Wait for both servers to fully start, then open http://localhost:5173 in your browser.
echo.
pause
