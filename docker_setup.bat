@echo off
REM 🐳 Quick Docker Setup for VICTOR-TTS + N8N

title VICTOR-TTS Docker Setup

echo.
echo ========================================
echo 🐳  VICTOR-TTS + N8N DOCKER SETUP  🐳
echo ========================================
echo ✅ Easy Setup and Management
echo ✅ Simple and Full Configurations  
echo ✅ Automated Health Checking
echo ========================================
echo.

REM ตรวจสอบ Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found! Please install Docker Desktop.
    echo 📥 Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose not found! Please install Docker Compose.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are ready!
echo.

echo 🚀 Choose installation type:
echo 1) Simple Setup (VICTOR-TTS + N8N only)
echo 2) Full Setup (with PostgreSQL, Redis, Nginx)
echo 3) Test Setup (for development)
echo 4) Management Menu
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🔨 Building and starting Simple setup...
    docker-compose -f docker-compose.simple.yml build
    docker-compose -f docker-compose.simple.yml up -d
    goto :health_check
)

if "%choice%"=="2" (
    echo.
    echo 🔨 Building and starting Full setup...
    docker-compose -f docker-compose.yml build
    docker-compose -f docker-compose.yml up -d
    goto :health_check
)

if "%choice%"=="3" (
    echo.
    echo 🔨 Building and starting Test setup...
    docker-compose -f docker-compose.test.yml build
    docker-compose -f docker-compose.test.yml up -d
    goto :health_check
)

if "%choice%"=="4" (
    echo.
    echo 🔧 Starting Management Menu...
    python docker_management.py
    goto :end
)

echo ❌ Invalid choice
pause
exit /b 1

:health_check
echo.
echo ⏳ Waiting for services to start...
timeout /t 15 /nobreak > nul

echo.
echo 🏥 Checking service health...

REM ตรวจสอบ VICTOR-TTS API
curl -s http://localhost:6969/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  VICTOR-TTS API: Not ready yet
) else (
    echo ✅ VICTOR-TTS API: Healthy
)

REM ตรวจสอบ N8N
curl -s http://localhost:5678 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  N8N: Not ready yet
) else (
    echo ✅ N8N: Healthy
)

REM ตรวจสอบ Web Interface
curl -s http://localhost:7000 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Web Interface: Not ready yet
) else (
    echo ✅ Web Interface: Healthy
)

echo.
echo 🌐 Available URLs:
echo ========================================
echo 🤖 N8N Workflow:        http://localhost:5678
echo 🎙️  VICTOR-TTS API:      http://localhost:6969
echo 🌐 VICTOR-TTS Web:      http://localhost:7000
echo 📊 API Documentation:   http://localhost:6969/docs
echo 🏥 Health Check:        http://localhost:6969/health
echo ========================================

echo.
echo 🎉 Setup completed!
echo.

:management_menu
echo 📋 Quick Management:
echo 1) View logs
echo 2) Check status
echo 3) Stop services
echo 4) Restart services
echo 5) Open N8N
echo 6) Open VICTOR-TTS Web
echo 7) Management Menu
echo 0) Exit
echo.

set /p mgmt_choice="Select option (0-7): "

if "%mgmt_choice%"=="1" (
    echo.
    echo 📋 Showing logs (Press Ctrl+C to stop)...
    docker-compose logs -f
    goto :management_menu
)

if "%mgmt_choice%"=="2" (
    echo.
    echo 📊 Services status:
    docker-compose ps
    echo.
    goto :management_menu
)

if "%mgmt_choice%"=="3" (
    echo.
    echo 🛑 Stopping services...
    docker-compose down
    echo ✅ Services stopped
    echo.
    goto :management_menu
)

if "%mgmt_choice%"=="4" (
    echo.
    echo 🔄 Restarting services...
    docker-compose restart
    echo ✅ Services restarted
    echo.
    goto :management_menu
)

if "%mgmt_choice%"=="5" (
    echo.
    echo 🌐 Opening N8N...
    start http://localhost:5678
    goto :management_menu
)

if "%mgmt_choice%"=="6" (
    echo.
    echo 🌐 Opening VICTOR-TTS Web...
    start http://localhost:7000
    goto :management_menu
)

if "%mgmt_choice%"=="7" (
    echo.
    echo 🔧 Starting Management Menu...
    python docker_management.py
    goto :management_menu
)

if "%mgmt_choice%"=="0" (
    goto :end
)

echo ❌ Invalid choice
goto :management_menu

:end
echo.
echo 👋 Goodbye!
pause
