@echo off
echo ========================================
echo    VICTOR-TTS UNIFIED - Build Optimized EXE
echo ========================================
echo.

echo กำลังตรวจสอบ dependencies...
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)"

echo.
echo กำลังสร้าง VICTOR-TTS UNIFIED.exe (Optimized)...
echo รวม: TTS + RVC + 16 Models + Web Interface
echo ขนาดโดยประมาณ: 2-5 GB
echo เวลา: 10-30 นาที
echo.

REM ลบไฟล์เก่า
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo กำลังสร้าง .exe แบบ optimize...
pyinstaller --clean --onefile --optimize=2 victor_tts.spec

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo ไฟล์ .exe อยู่ที่: dist\VICTOR-TTS-UNIFIED.exe
echo.
echo วิธีการใช้งาน:
echo 1. เปิดไฟล์ dist\VICTOR-TTS-UNIFIED.exe
echo 2. รอสักครู่ให้ระบบโหลด (1-2 นาที)
echo 3. เปิดเว็บเบราว์เซอร์ไปที่ http://localhost:7000
echo.
echo Features ที่รวม:
echo - Text-to-Speech (Edge TTS)
echo - Voice Conversion (RVC) - 16 models
echo - Web Interface
echo - Audio Processing
echo.
pause 