@echo off
REM 🚀 VICTOR-TTS - GPU Optimized Start Script
REM ระบบเริ่มต้นแบบเน้นการใช้งาน GPU

title VICTOR-TTS - GPU Optimized

echo.
echo ========================================
echo 🎙️  VICTOR-TTS GPU OPTIMIZED  🎙️
echo ========================================
echo 🔥 GPU Accelerated TTS + Voice Conversion
echo ⚡ Maximum Performance
echo 🖥️  CUDA Optimized
echo 🚀 Fast Processing
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

echo.
echo 🖥️  เลือก GPU ที่ต้องการใช้:
echo ========================================
echo [0] GPU 0 (Default - แนะนำ)
echo [1] GPU 1
echo [2] GPU 2
echo [3] GPU 3
echo [A] Auto-detect (ระบบเลือกเอง)
echo ========================================
echo.

set /p gpu_choice="👉 เลือก GPU (0-3/A): "

if "%gpu_choice%"=="A" goto auto_gpu
if "%gpu_choice%"=="0" goto gpu_0
if "%gpu_choice%"=="1" goto gpu_1
if "%gpu_choice%"=="2" goto gpu_2
if "%gpu_choice%"=="3" goto gpu_3
goto invalid

:auto_gpu
echo.
echo 🔍 ระบบจะเลือก GPU ที่เหมาะสมที่สุด...
echo ========================================
echo 🌐 เริ่มต้น Web Interface...
echo 🔗 URL: http://localhost:7000
echo 🖥️  GPU: Auto-detect
echo ⚡ Performance: Optimized
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
%PYTHON_CMD% web_interface.py
goto end

:gpu_0
echo.
echo 🌐 เริ่มต้น Web Interface ด้วย GPU 0...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🖥️  GPU: 0 (Primary)
echo ⚡ Performance: Maximum
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
set CUDA_VISIBLE_DEVICES=0
%PYTHON_CMD% web_interface.py
goto end

:gpu_1
echo.
echo 🌐 เริ่มต้น Web Interface ด้วย GPU 1...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🖥️  GPU: 1 (Secondary)
echo ⚡ Performance: High
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
set CUDA_VISIBLE_DEVICES=1
%PYTHON_CMD% web_interface.py
goto end

:gpu_2
echo.
echo 🌐 เริ่มต้น Web Interface ด้วย GPU 2...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🖥️  GPU: 2 (Tertiary)
echo ⚡ Performance: High
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
set CUDA_VISIBLE_DEVICES=2
%PYTHON_CMD% web_interface.py
goto end

:gpu_3
echo.
echo 🌐 เริ่มต้น Web Interface ด้วย GPU 3...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🖥️  GPU: 3 (Quaternary)
echo ⚡ Performance: High
echo ========================================
echo.
echo ⏳ กำลังเริ่มต้น... (กด Ctrl+C เพื่อหยุด)
echo.
set CUDA_VISIBLE_DEVICES=3
%PYTHON_CMD% web_interface.py
goto end

:invalid
echo.
echo ❌ ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่
echo.
pause
goto menu

:menu
cls
goto start

:end
echo.
echo 🔄 โปรแกรมสิ้นสุดการทำงาน
echo 💡 เรียกใช้ start_gpu.bat อีกครั้งเพื่อใช้งานต่อ
echo.
pause 