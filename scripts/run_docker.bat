@echo off
echo ========================================
echo    VICTOR-TTS UNIFIED - Docker Setup
echo ========================================
echo.

echo ตรวจสอบ Docker...
docker --version
if %errorlevel% neq 0 (
    echo ❌ Docker ไม่ได้ติดตั้ง กรุณาติดตั้ง Docker Desktop
    pause
    exit /b 1
)

echo.
echo เลือกการรัน:
echo 1. Simple Version (VICTOR-TTS + N8N)
echo 2. Full Version (VICTOR-TTS + N8N + PostgreSQL + Redis)
echo 3. VICTOR-TTS Only
echo 4. Stop All Services
echo.

set /p choice="เลือกตัวเลือก (1-4): "

if "%choice%"=="1" (
    echo.
    echo กำลังรัน Simple Version...
    docker-compose -f docker/docker-compose.simple.yml up --build
) else if "%choice%"=="2" (
    echo.
    echo กำลังรัน Full Version...
    docker-compose -f docker/docker-compose.yml up --build
) else if "%choice%"=="3" (
    echo.
    echo กำลังรัน VICTOR-TTS Only...
    docker-compose -f docker/docker-compose.simple.yml up victor-tts-api --build
) else if "%choice%"=="4" (
    echo.
    echo กำลังหยุด services...
    docker-compose -f docker/docker-compose.yml down
    docker-compose -f docker/docker-compose.simple.yml down
) else (
    echo.
    echo ตัวเลือกไม่ถูกต้อง
)

echo.
echo ========================================
echo    เสร็จสิ้น!
echo ========================================
echo.
echo URLs:
echo - VICTOR-TTS API: http://localhost:6969
echo - N8N: http://localhost:5678
echo - Web Interface: http://localhost:7000
echo.
pause 