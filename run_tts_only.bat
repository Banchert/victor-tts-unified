@echo off
chcp 65001 >nul
title VICTOR-TTS Only

echo.
echo ========================================
echo    🎙️ VICTOR-TTS ONLY
echo ========================================
echo.

:: ตรวจสอบ Python
echo 🔍 ตรวจสอบ Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python ไม่ได้ติดตั้ง กรุณาติดตั้ง Python 3.10+
    echo 📥 ดาวน์โหลด: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: ตรวจสอบไฟล์หลัก
if not exist "main_api_server.py" (
    echo ❌ ไม่พบไฟล์ main_api_server.py
    pause
    exit /b 1
)

if not exist "web_interface_complete.py" (
    echo ❌ ไม่พบไฟล์ web_interface_complete.py
    pause
    exit /b 1
)

echo ✅ ระบบพร้อมใช้งาน
echo.

:: ตรวจสอบ ports
echo 🔍 ตรวจสอบ ports...
netstat -an | findstr ":6969" >nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 6969 กำลังใช้งานอยู่ จะใช้ port 6970 แทน
    set API_PORT=6970
    set API_URL=http://localhost:6970
) else (
    set API_PORT=6969
    set API_URL=http://localhost:6969
)

netstat -an | findstr ":7000" >nul
if %errorlevel% equ 0 (
    echo ⚠️  Port 7000 กำลังใช้งานอยู่ จะใช้ port 7001 แทน
    set WEB_PORT=7001
    set WEB_URL=http://localhost:7001
) else (
    set WEB_PORT=7000
    set WEB_URL=http://localhost:7000
)

echo.
echo 📋 เลือกการใช้งาน:
echo.
echo 1. 🚀 เริ่มต้น TTS API + Web UI (ครบถ้วน)
echo 2. 🌐 เริ่มต้น Web Interface เท่านั้น
echo 3. 🔧 เริ่มต้น API Server เท่านั้น
echo 4. 📦 ติดตั้ง Dependencies
echo 5. ❌ ออกจากโปรแกรม
echo.

set /p choice="เลือกตัวเลือก (1-5): "

if "%choice%"=="1" goto start_full
if "%choice%"=="2" goto start_web_only
if "%choice%"=="3" goto start_api_only
if "%choice%"=="4" goto install_deps
if "%choice%"=="5" goto exit_program

echo.
echo ❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1-5
echo.
goto start_full

:start_full
echo.
echo 🚀 กำลังเริ่มต้น VICTOR-TTS แบบครบถ้วน...
echo.
echo 📍 URLs ที่จะเปิด:
echo    🌐 Web Interface: %WEB_URL%
echo    🔧 API Server: %API_URL%
echo    📊 Health Check: %API_URL%/health
echo.
echo ⏳ กำลังโหลดระบบ... (อาจใช้เวลาสักครู่)
echo.

:: เริ่มต้น API Server ในพื้นหลัง
start "VICTOR-TTS API Server" cmd /k "python main_api_server.py --port %API_PORT%"

:: รอสักครู่ให้ API Server เริ่มต้น
timeout /t 5 /nobreak >nul

:: เริ่มต้น Web Interface
start "VICTOR-TTS Web Interface" cmd /k "python web_interface_complete.py --port %WEB_PORT%"

:: เปิดเบราว์เซอร์
timeout /t 3 /nobreak >nul
start %WEB_URL%

echo.
echo ✅ VICTOR-TTS เริ่มต้นสำเร็จ!
echo.
echo 💡 Tips:
echo    - กด Ctrl+C ในหน้าต่าง Command Prompt เพื่อหยุด
echo    - เข้าถึง Web UI ที่: %WEB_URL%
echo    - เข้าถึง API ที่: %API_URL%
echo.
pause
goto start_full

:start_web_only
echo.
echo 🌐 กำลังเริ่มต้น Web Interface เท่านั้น...
echo.
echo 📍 URL: %WEB_URL%
echo.

python web_interface_complete.py --port %WEB_PORT%

echo.
echo ✅ Web Interface หยุดทำงาน
echo.
pause
goto start_full

:start_api_only
echo.
echo 🔧 กำลังเริ่มต้น API Server เท่านั้น...
echo.
echo 📍 URLs:
echo    🔧 API Server: %API_URL%
echo    📊 Health Check: %API_URL%/health
echo.

python main_api_server.py --port %API_PORT%

echo.
echo ✅ API Server หยุดทำงาน
echo.
pause
goto start_full

:install_deps
echo.
echo 📦 กำลังติดตั้ง Dependencies...
echo.

:: ตรวจสอบ pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip ไม่ได้ติดตั้ง
    pause
    goto start_full
)

echo ⏳ กำลังติดตั้ง packages...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ ติดตั้ง Dependencies สำเร็จ!
) else (
    echo.
    echo ❌ เกิดข้อผิดพลาดในการติดตั้ง
    echo 💡 ลองใช้: pip install --upgrade pip
)

echo.
pause
goto start_full

:exit_program
echo.
echo 👋 ขอบคุณที่ใช้งาน VICTOR-TTS!
echo.
echo 🌐 เข้าถึงได้ที่:
echo    - Web Interface: %WEB_URL%
echo    - API Server: %API_URL%
echo    - Health Check: %API_URL%/health
echo.
echo 🔄 N8N ของคุณ: http://localhost:5678
echo.
exit /b 0 