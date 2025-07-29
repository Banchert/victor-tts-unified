@echo off
REM 🚀 VICTOR-TTS IMPROVED START
REM เวอร์ชันที่ปรับปรุงแล้ว - ผลลัพธ์อยู่ใกล้ปุ่ม

title VICTOR-TTS IMPROVED

echo.
echo ========================================
echo 🎙️  VICTOR-TTS IMPROVED SYSTEM  🎙️
echo ========================================
echo ✅ Enhanced UI Design
echo ✅ Better Result Positioning
echo ✅ Smooth Animations
echo ✅ Modern Gradient Design
echo ========================================
echo.

REM ตรวจสอบ Python
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
    echo ✅ Using Virtual Environment
) else (
    set PYTHON_CMD=python
    echo ⚠️  Using System Python
)

echo 📌 Python Info:
%PYTHON_CMD% --version

echo.
echo 🚀 Starting Improved Web Interface...
echo 🔗 URL: http://localhost:7000
echo.

%PYTHON_CMD% web_interface_improved.py

pause 