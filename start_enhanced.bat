@echo off
title VICTOR-TTS Enhanced API Server
color 0A

echo.
echo ========================================
echo    VICTOR-TTS Enhanced API Server
echo ========================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found: 
python --version

:: Check if we're in the right directory
if not exist "main_api_server_enhanced.py" (
    echo ERROR: main_api_server_enhanced.py not found
    echo Please run this script from the victor-tts-unified directory
    pause
    exit /b 1
)

:: Check for required files
echo.
echo Checking required files...
if not exist "rvc_api_enhanced.py" (
    echo ERROR: rvc_api_enhanced.py not found
    echo Please ensure all enhanced files are present
    pause
    exit /b 1
)

if not exist "tts_rvc_core.py" (
    echo ERROR: tts_rvc_core.py not found
    echo Please ensure all core files are present
    pause
    exit /b 1
)

echo All required files found!

:: Check for port conflicts
echo.
echo Checking port 6969...
netstat -ano | findstr :6969 >nul
if not errorlevel 1 (
    echo Port 6969 is in use. Attempting to free it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :6969') do (
        echo Killing process %%a
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 3 /nobreak >nul
)

:: Create necessary directories
echo.
echo Creating directories...
if not exist "storage\temp\rvc" mkdir "storage\temp\rvc"
if not exist "logs" mkdir "logs"

:: Install dependencies if needed
echo.
echo Checking dependencies...
python -c "import fastapi, uvicorn, torch" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Start the enhanced server
echo.
echo Starting Enhanced VICTOR-TTS API Server...
echo Server will be available at: http://localhost:6969
echo Press Ctrl+C to stop the server
echo.

python main_api_server_enhanced.py --host 0.0.0.0 --port 6969

echo.
echo Server stopped.
pause 