@echo off
echo Starting Instagram Reels Viewer Backend...
echo ========================================

cd backend

echo Checking Java version...
java -version
if %errorlevel% neq 0 (
    echo Error: Java not found. Please install Java 17 or higher.
    pause
    exit /b 1
)

echo.
echo Building and starting Spring Boot application...
mvn spring-boot:run

pause
