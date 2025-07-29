@echo off
REM 🧪 VICTOR-TTS Test Script

title VICTOR-TTS Test

echo.
echo ========================================
echo 🧪  VICTOR-TTS TEST SUITE  🧪
echo ========================================
echo.

REM ตรวจสอบ Python
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    set PYTHON_CMD=python
)

echo 🧪 Testing Optimized Core...
%PYTHON_CMD% -c "from tts_rvc_core_optimized import create_optimized_core_instance; core = create_optimized_core_instance(); print('✅ Optimized core test passed')"

echo.
echo 🧪 Testing RVC Wrapper...
%PYTHON_CMD% -c "from rvc_wrapper import create_rvc_wrapper; wrapper = create_rvc_wrapper(); print('✅ RVC wrapper test passed')"

echo.
echo 🧪 Testing RVC Models...
%PYTHON_CMD% test_rvc_fixed.py

echo.
echo ✅ All tests completed!
pause
