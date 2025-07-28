@echo off
echo ========================================
echo    VICTOR-TTS UNIFIED - Quick Push
echo ========================================
echo.

echo กรุณาใส่ GitHub username ของคุณ:
set /p username="Username: "

echo.
echo กรุณาใส่ชื่อ repository (default: victor-tts-unified):
set /p repo_name="Repository name: "

if "%repo_name%"=="" set repo_name=victor-tts-unified

echo.
echo กำลังตั้งค่า remote origin...
git remote add origin https://github.com/%username%/%repo_name%.git

echo.
echo กำลัง push ไปยัง GitHub...
git push -u origin main

echo.
echo ========================================
echo    เสร็จสิ้น! โปรเจกต์ถูก push ไป GitHub แล้ว
echo ========================================
echo.
echo Repository URL: https://github.com/%username%/%repo_name%
echo.
pause 