@echo off
title Install TTS Dependencies

echo.
echo ========================================
echo    📦 INSTALL TTS DEPENDENCIES
echo ========================================
echo.

echo 🔍 ตรวจสอบ Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python ไม่ได้ติดตั้ง
    pause
    exit /b 1
)

echo.
echo 📦 กำลังติดตั้ง Dependencies...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ ติดตั้งสำเร็จ!
    echo.
    echo 🚀 ตอนนี้คุณสามารถรัน TTS ได้แล้ว:
    echo    run_tts_only.bat
    echo.
) else (
    echo.
    echo ❌ เกิดข้อผิดพลาด
    echo 💡 ลองใช้: pip install --upgrade pip
    echo.
)

pause 