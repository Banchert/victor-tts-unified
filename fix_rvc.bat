@echo off
REM 🔧 RVC System Fixer

title RVC System Fixer

echo.
echo ========================================
echo 🔧  RVC SYSTEM DIAGNOSTIC & FIXER  🔧
echo ========================================
echo ✅ Full System Check
echo ✅ Diagnose Common Issues  
echo ✅ Suggest Solutions
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

echo.
echo 🚀 Running RVC System Diagnostic...
echo.

%PYTHON_CMD% fix_rvc.py

pause
