@echo off
echo ========================================
echo VICTOR-TTS Docker Build Test (CPU Version)
echo ========================================

echo.
echo Testing Docker build with CPU version...
echo.

cd /d "%~dp0"

echo Building Docker image with CPU version...
docker build -f Dockerfile.cpu -t victor-tts-cpu:test ..

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS: Docker build completed!
    echo ========================================
    echo.
    echo To run the container:
    echo docker run -p 6969:6969 -p 7000:7000 victor-tts-cpu:test
    echo.
    echo To test with docker-compose:
    echo docker-compose -f docker-compose.simple.yml up
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Docker build failed!
    echo ========================================
    echo.
    echo Check the error messages above for details.
    echo.
)

pause 