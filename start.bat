@echo off
REM 🚀 VICTOR-TTS - Unified Start Script
REM ระบบเริ่มต้นแบบรวม เน้นการใช้งาน GPU

title VICTOR-TTS - Unified System

echo.
echo ========================================
echo 🎙️  VICTOR-TTS UNIFIED SYSTEM  🎙️
echo ========================================
echo 🔥 Complete TTS + Voice Conversion
echo ✅ Simplified and Organized
echo ✅ Easy to Use and Maintain
echo ✅ All-in-One Solution
echo ========================================
echo.

REM ตรวจสอบว่ามี Python Environment หรือไม่
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD="venv\Scripts\python.exe"
    echo ✅ Using Virtual Environment: venv\
) else if exist "env\Scripts\python.exe" (
    set PYTHON_CMD="env\Scripts\python.exe"
    echo ✅ Using Virtual Environment: env\
) else (
    set PYTHON_CMD=python
    echo ⚠️  Using System Python
)

:main_menu
echo.
echo 🎯 เลือกโหมดการใช้งาน:
echo ========================================
echo [1] 🌐 Web Interface (แนะนำ)
echo [2] 🖥️  Web Interface + GPU
echo [3] 📡 API Server (FastAPI)
echo [4] 🧪 ทดสอบระบบ
echo [5] 📋 ดูโมเดล RVC ที่มี
echo [0] ❌ ออกจากโปรแกรม
echo ========================================
echo.

set /p choice="👉 กรุณาเลือก (0-5): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto web_gpu
if "%choice%"=="3" goto api
if "%choice%"=="4" goto test
if "%choice%"=="5" goto models
if "%choice%"=="0" goto exit
goto invalid

:web
echo.
echo 🌐 เริ่มต้น Web Interface...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🎯 ใช้สำหรับ: สร้างเสียง + แปลงเสียง
echo 💻 Device: Auto-detect (GPU/CPU)
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
%PYTHON_CMD% web_interface.py
goto end

:web_gpu
echo.
echo 🖥️  เลือก GPU ที่ต้องการใช้:
echo ========================================
echo [0] GPU 0 (Default)
echo [1] GPU 1
echo [2] GPU 2
echo [3] GPU 3
echo ========================================
set /p gpu_choice="👉 เลือก GPU (0-3): "
echo.
echo 🌐 เริ่มต้น Web Interface ด้วย GPU %gpu_choice%...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🖥️  GPU: %gpu_choice%
echo 🎯 ใช้สำหรับ: สร้างเสียง + แปลงเสียง (GPU Accelerated)
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
set CUDA_VISIBLE_DEVICES=%gpu_choice%
%PYTHON_CMD% web_interface.py
goto end

:api
echo.
echo 📡 เริ่มต้น API Server...
echo ========================================
echo 🔗 API URL: http://localhost:6969
echo 📋 Docs: http://localhost:6969/docs
echo 🎯 ใช้สำหรับ: FastAPI Integration
echo 💻 Device: Auto-detect (GPU/CPU)
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
%PYTHON_CMD% main_api_server.py
goto end

:test
echo.
echo 🧪 ทดสอบระบบ...
echo ========================================
echo 🔍 ตรวจสอบ TTS + RVC + GPU...
echo ========================================
%PYTHON_CMD% test_web_interface_final.py
echo ========================================
echo.
pause
goto menu

:models
echo.
echo 📋 รายชื่อโมเดล RVC ที่มีอยู่...
echo ========================================
%PYTHON_CMD% -c "from rvc_api import RVCConverter; rvc = RVCConverter(); models = rvc.get_available_models(); print(f'พบโมเดล {len(models)} ตัว:'); [print(f'{i+1:2d}. {model}') for i, model in enumerate(models)]"
echo ========================================
echo.
pause
goto menu

:invalid
echo.
echo ❌ ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่
echo.
pause

:menu
cls
goto main_menu

:exit
echo.
echo 👋 ขอบคุณที่ใช้งาน VICTOR-TTS!
echo 🌟 หวังว่าจะมีประโยชน์กับคุณ
echo.
timeout /t 2 >nul
exit

:end
echo.
echo 🔄 โปรแกรมสิ้นสุดการทำงาน
echo 💡 เรียกใช้ start.bat อีกครั้งเพื่อใช้งานต่อ
echo.
pause
