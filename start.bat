@echo off
chcp 65001 >nul
title VICTOR-TTS UNIFIED - Launcher

echo.
echo ========================================
echo    🎙️ VICTOR-TTS UNIFIED LAUNCHER
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

:: ตรวจสอบ requirements
if not exist "requirements.txt" (
    echo ❌ ไม่พบไฟล์ requirements.txt
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

:: แสดงเมนู
:menu
echo 📋 เลือกการใช้งาน:
echo.
echo 1. 🚀 เริ่มต้น VICTOR-TTS (API + Web UI)
echo 2. 🌐 เริ่มต้น Web Interface เท่านั้น
echo 3. 🔧 เริ่มต้น API Server เท่านั้น
echo 4. 🐳 เริ่มต้นด้วย Docker
echo 5. 📦 ติดตั้ง Dependencies
echo 6. 🔍 ตรวจสอบระบบ
echo 7. ❌ ออกจากโปรแกรม
echo.

set /p choice="เลือกตัวเลือก (1-7): "

if "%choice%"=="1" goto start_full
if "%choice%"=="2" goto start_web_only
if "%choice%"=="3" goto start_api_only
if "%choice%"=="4" goto start_docker
if "%choice%"=="5" goto install_deps
if "%choice%"=="6" goto check_system
if "%choice%"=="7" goto exit_program

echo.
echo ❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1-7
echo.
goto menu

:start_full
echo.
echo 🚀 กำลังเริ่มต้น VICTOR-TTS แบบครบถ้วน...
echo.
echo 📍 URLs ที่จะเปิด:
echo    🌐 Web Interface: http://localhost:7000
echo    🔧 API Server: http://localhost:6969
echo    📊 Health Check: http://localhost:6969/health
echo.
echo ⏳ กำลังโหลดระบบ... (อาจใช้เวลาสักครู่)
echo.

:: เริ่มต้น API Server ในพื้นหลัง
start "VICTOR-TTS API Server" cmd /k "python main_api_server.py"

:: รอสักครู่ให้ API Server เริ่มต้น
timeout /t 5 /nobreak >nul

:: เริ่มต้น Web Interface
start "VICTOR-TTS Web Interface" cmd /k "python web_interface_complete.py"

:: เปิดเบราว์เซอร์
timeout /t 3 /nobreak >nul
start http://localhost:7000

echo.
echo ✅ VICTOR-TTS เริ่มต้นสำเร็จ!
echo.
echo 💡 Tips:
echo    - กด Ctrl+C ในหน้าต่าง Command Prompt เพื่อหยุด
echo    - ตรวจสอบ logs หากมีปัญหา
echo    - เข้าถึง Web UI ที่: http://localhost:7000
echo.
pause
goto menu

:start_web_only
echo.
echo 🌐 กำลังเริ่มต้น Web Interface เท่านั้น...
echo.
echo 📍 URL: http://localhost:7000
echo.

python web_interface_complete.py

echo.
echo ✅ Web Interface หยุดทำงาน
echo.
pause
goto menu

:start_api_only
echo.
echo 🔧 กำลังเริ่มต้น API Server เท่านั้น...
echo.
echo 📍 URLs:
echo    🔧 API Server: http://localhost:6969
echo    📊 Health Check: http://localhost:6969/health
echo.

python main_api_server.py

echo.
echo ✅ API Server หยุดทำงาน
echo.
pause
goto menu

:start_docker
echo.
echo 🐳 กำลังเริ่มต้นด้วย Docker...
echo.

if not exist "scripts\run_docker.bat" (
    echo ❌ ไม่พบไฟล์ scripts\run_docker.bat
    echo 📥 กรุณาติดตั้ง Docker ก่อน
    pause
    goto menu
)

scripts\run_docker.bat
goto menu

:install_deps
echo.
echo 📦 กำลังติดตั้ง Dependencies...
echo.

:: ตรวจสอบ pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip ไม่ได้ติดตั้ง
    pause
    goto menu
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
goto menu

:check_system
echo.
echo 🔍 กำลังตรวจสอบระบบ...
echo.

echo 📋 ข้อมูลระบบ:
echo    🐍 Python: 
python --version 2>&1
echo    📦 pip: 
pip --version 2>&1
echo.

echo 📁 ไฟล์หลัก:
if exist "main_api_server.py" (
    echo    ✅ main_api_server.py
) else (
    echo    ❌ main_api_server.py
)

if exist "web_interface_complete.py" (
    echo    ✅ web_interface_complete.py
) else (
    echo    ❌ web_interface_complete.py
)

if exist "tts_rvc_core.py" (
    echo    ✅ tts_rvc_core.py
) else (
    echo    ❌ tts_rvc_core.py
)

if exist "requirements.txt" (
    echo    ✅ requirements.txt
) else (
    echo    ❌ requirements.txt
)

echo.
echo 📊 ตรวจสอบ ports:
netstat -an | findstr ":6969" >nul 2>&1
if %errorlevel% equ 0 (
    echo    ⚠️  Port 6969 กำลังใช้งานอยู่
) else (
    echo    ✅ Port 6969 ว่าง
)

netstat -an | findstr ":7000" >nul 2>&1
if %errorlevel% equ 0 (
    echo    ⚠️  Port 7000 กำลังใช้งานอยู่
) else (
    echo    ✅ Port 7000 ว่าง
)

echo.
echo ✅ ตรวจสอบระบบเสร็จสิ้น
echo.
pause
goto menu

:exit_program
echo.
echo 👋 ขอบคุณที่ใช้งาน VICTOR-TTS UNIFIED!
echo.
echo 🌐 เข้าถึงได้ที่:
echo    - Web Interface: http://localhost:7000
echo    - API Server: http://localhost:6969
echo    - Health Check: http://localhost:6969/health
echo.
echo 📞 หากมีปัญหา ตรวจสอบ logs ใน /logs directory
echo.
exit /b 0 