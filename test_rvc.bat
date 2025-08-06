@echo off
REM 🧪 RVC Test Script - ทดสอบการทำงานของ RVC

title RVC System Test

echo.
echo ========================================
echo 🧪  RVC SYSTEM DIAGNOSTIC TEST  🧪
echo ========================================
echo ✅ Testing RVC Components
echo ✅ Checking Model Files
echo ✅ Verifying Dependencies
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
echo 🚀 Running RVC Test...
echo.

%PYTHON_CMD% test_rvc_simple.py

echo.
echo 📊 Test completed. Check results above.
echo.

pause
