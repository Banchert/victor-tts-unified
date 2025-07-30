@echo off
title VICTOR-TTS GITHUB SIMPLE VERSION

echo.
echo ========================================
echo VICTOR-TTS GITHUB SIMPLE VERSION
echo ========================================
echo Simple and stable version
echo ========================================
echo.

:: ตรวจสอบ Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python found

:: สร้างไดเรกทอรี
echo.
echo Creating directories...
if not exist "storage\temp" mkdir "storage\temp"
if not exist "storage\output" mkdir "storage\output"
if not exist "models" mkdir "models"
if not exist "logs" mkdir "logs"
if not exist "config" mkdir "config"
if not exist "test_output" mkdir "test_output"
echo OK: Directories ready

:: ตรวจสอบและติดตั้ง dependencies
echo.
echo Checking dependencies...
python -c "import torch, fastapi, uvicorn, edge_tts" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    echo This may take a few minutes...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
    echo OK: Dependencies installed
) else (
    echo OK: Dependencies found
)

:: ทำความสะอาดไฟล์เก่า
echo.
echo Cleaning up...
if exist "storage\temp\*" del /q "storage\temp\*" >nul 2>&1
echo OK: Cleanup done

:: ตรวจสอบ GPU
echo.
echo Checking GPU...
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')" 2>nul
echo OK: System check completed

:: เริ่มต้นเซิร์ฟเวอร์
echo.
echo ========================================
echo STARTING VICTOR-TTS SIMPLE SERVER
echo ========================================
echo Server: http://localhost:6969
echo Web Interface: http://localhost:6969
echo API Docs: http://localhost:6969/docs
echo.
echo Opening browser in 5 seconds...
echo Press Ctrl+C to stop
echo ========================================
echo.

:: รอ 5 วินาทีแล้วเปิดเบราว์เซอร์
timeout /t 5 /nobreak >nul
start http://localhost:6969

:: เริ่มต้นเซิร์ฟเวอร์
python main_api_server.py --host 0.0.0.0 --port 6969

:: หากเซิร์ฟเวอร์หยุดทำงาน
echo.
echo Server stopped
pause 