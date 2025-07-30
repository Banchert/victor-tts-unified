@echo off
REM 🚀 VICTOR-TTS COMPLETE START
REM เวอร์ชันครบถ้วน - รวมทุกฟีเจอร์และเครื่องมือ

title VICTOR-TTS COMPLETE

echo.
echo ========================================
echo 🎙️  VICTOR-TTS COMPLETE SYSTEM  🎙️
echo ========================================
echo ✅ Complete TTS + RVC System
echo ✅ All Features and Tools Included
echo ✅ Enhanced UI Design
echo ✅ Better Result Positioning
echo ✅ Speed Control and Effects
echo ✅ Multi-language Support
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
echo 🚀 Starting Complete Web Interface...
echo 🔗 URL: http://localhost:7000
echo.

%PYTHON_CMD% web_interface_complete.py

pause 