@echo off
REM 🚀 VICTOR-TTS - Universal Start Script
REM ระบบเริ่มต้นแบบครบวงจร รองรับทุกฟังก์ชัน

title VICTOR-TTS - Universal Launcher

echo.
echo ========================================
echo 🎙️  VICTOR-TTS UNIVERSAL SYSTEM  🎙️
echo ========================================
echo 🔥 Complete TTS + RVC Voice Conversion
echo ✅ All-in-One Solution
echo ✅ GPU/CPU Auto-Detection + Real-time Switching
echo ✅ Web Interface + API Server
echo ✅ Full GPU Support with Device Management
echo ========================================
echo.

REM ตรวจสอบ Python ที่ถูกต้อง - ใช้ Python 3.13 เป็นหลัก
if exist "C:\Python313\python.exe" (
    set PYTHON_CMD=C:\Python313\python.exe
    echo ✅ Using Python 3.13 from C:\Python313
) else if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
    echo ✅ Using Virtual Environment: venv\
) else if exist "env\Scripts\python.exe" (
    set PYTHON_CMD=env\Scripts\python.exe
    echo ✅ Using Virtual Environment: env\
) else (
    set PYTHON_CMD=python
    echo ⚠️  Using System Python
)

REM แสดงข้อมูล Python
echo 📌 Python Info:
%PYTHON_CMD% --version

REM ตรวจสอบว่ามี ffmpeg หรือไม่
if exist "ffmpeg.exe" (
    echo ✅ FFmpeg: Found
) else (
    echo ⚠️  FFmpeg: Not found (some features may not work)
)

:main_menu
echo.
echo 🎯 เลือกโหมดการใช้งาน:
echo ========================================
echo [1] 🌐 Web Interface (Port 7000) - แนะนำ!
echo [2] 🖥️  Web Interface + เลือก GPU
echo [3] 📡 API Server (Port 6969)
echo [4] 🔄 Web + API (ทั้งสองโหมด)
echo ========================================
echo 🧪 ทดสอบระบบ:
echo [5] 🔍 ทดสอบระบบทั้งหมด
echo [6] 🎤 ทดสอบ RVC MP3 Fix
echo [7] 📋 ดูโมเดล RVC ที่มี
echo [8] 🌍 ทดสอบหลายภาษา
echo ========================================
echo 🛠️  ตัวเลือกขั้นสูง:
echo [9] 📦 ติดตั้ง Dependencies
echo [10] 🏗️  สร้างไฟล์ EXE
echo [11] 🔧 ตรวจสอบสถานะ RVC
echo [12] 🚀 ปรับปรุงประสิทธิภาพ
echo [13] 🔍 ตรวจสอบ GPU Support
echo ========================================
echo [0] ❌ ออกจากโปรแกรม
echo ========================================
echo.

set /p choice="👉 กรุณาเลือก (0-13): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto web_gpu
if "%choice%"=="3" goto api
if "%choice%"=="4" goto web_api
if "%choice%"=="5" goto test_all
if "%choice%"=="6" goto test_rvc
if "%choice%"=="7" goto models
if "%choice%"=="8" goto test_lang
if "%choice%"=="9" goto install
if "%choice%"=="10" goto build_exe
if "%choice%"=="11" goto test_status
if "%choice%"=="12" goto optimize
if "%choice%"=="13" goto test_gpu
if "%choice%"=="0" goto exit
goto invalid

:web
echo.
echo 🌐 เริ่มต้น Web Interface...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🎯 ใช้สำหรับ: สร้างเสียง TTS + แปลงเสียง RVC
echo 💻 Device: Auto-detect (GPU/CPU) + Real-time Switching
echo 🔧 GPU Support: ✅ รองรับเต็มรูปแบบ
echo 📝 กด Ctrl+C เพื่อหยุดการทำงาน
echo ========================================
echo.
%PYTHON_CMD% web_interface.py
goto end

:web_gpu
echo.
echo 🖥️  เลือก GPU ที่ต้องการใช้:
echo ========================================
echo [0] GPU 0 (Default)
echo [1] GPU 1
echo [2] GPU 2
echo [3] GPU 3
echo [C] CPU Only
echo [A] AUTO (เลือก GPU ที่ดีที่สุด)
echo ========================================
set /p gpu_choice="👉 เลือก GPU (0-3), C สำหรับ CPU, หรือ A สำหรับ AUTO: "

if /i "%gpu_choice%"=="C" (
    set CUDA_VISIBLE_DEVICES=-1
    echo 💻 ใช้งานแบบ CPU Only
) else if /i "%gpu_choice%"=="A" (
    echo ⚡ ใช้งานแบบ AUTO (เลือก GPU ที่ดีที่สุด)
    echo 🔧 ระบบจะเลือก GPU ที่มี memory มากที่สุด
    set CUDA_VISIBLE_DEVICES=
) else (
    set CUDA_VISIBLE_DEVICES=%gpu_choice%
    echo 🖥️  ใช้งาน GPU %gpu_choice%
)

echo.
echo 🌐 เริ่มต้น Web Interface...
echo ========================================
echo 🔗 URL: http://localhost:7000
echo 🎯 ใช้สำหรับ: สร้างเสียง TTS + แปลงเสียง RVC
echo 💻 Device: %gpu_choice% (สามารถเปลี่ยนได้ใน Web Interface)
echo 📝 กด Ctrl+C เพื่อหยุดการทำงาน
echo ========================================
echo.
%PYTHON_CMD% web_interface.py
goto end

:api
echo.
echo 📡 เริ่มต้น API Server...
echo ========================================
echo 🔗 API URL: http://localhost:6969
echo 📋 API Docs: http://localhost:6969/docs
echo 🎯 ใช้สำหรับ: N8N/API Integration
echo 💻 Device: Auto-detect (GPU/CPU) + Real-time Switching
echo 🔧 GPU Support: ✅ รองรับเต็มรูปแบบ
echo 📝 กด Ctrl+C เพื่อหยุดการทำงาน
echo ========================================
echo.
%PYTHON_CMD% main_api_server.py
goto end

:web_api
echo.
echo 🔄 เริ่มต้นทั้ง Web Interface และ API Server...
echo ========================================
echo 🌐 Web URL: http://localhost:7000
echo 📡 API URL: http://localhost:6969
echo 📋 API Docs: http://localhost:6969/docs
echo 💻 Device: Auto-detect (GPU/CPU) + Real-time Switching
echo 🔧 GPU Support: ✅ รองรับเต็มรูปแบบ
echo ========================================
echo.
start "VICTOR-TTS API" %PYTHON_CMD% main_api_server.py
timeout /t 3 >nul
start "VICTOR-TTS Web" %PYTHON_CMD% web_interface.py
echo.
echo ✅ ทั้งสองระบบกำลังทำงาน
echo 📝 ปิดหน้าต่างนี้จะไม่หยุดการทำงานของระบบ
echo.
pause
goto menu

:test_all
echo.
echo 🧪 ทดสอบระบบทั้งหมด...
echo ========================================
if exist "test_rvc_detailed.py" (
    %PYTHON_CMD% test_rvc_detailed.py
) else (
    echo ⚠️  ไม่พบไฟล์ทดสอบ
)
echo ========================================
echo.
pause
goto menu

:test_rvc
echo.
echo 🎤 ทดสอบ RVC MP3 Conversion Fix...
echo ========================================
%PYTHON_CMD% test_rvc_mp3_fix.py
echo ========================================
echo.
pause
goto menu

:test_lang
echo.
echo 🌍 ทดสอบระบบหลายภาษา...
echo ========================================
if exist "test_multi_language.py" (
    %PYTHON_CMD% test_multi_language.py
) else (
    echo ⚠️  ไม่พบไฟล์ทดสอบ
)
echo ========================================
echo.
pause
goto menu

:test_status
echo.
echo 🔧 ตรวจสอบสถานะ RVC...
echo ========================================
%PYTHON_CMD% test_rvc_status.py
echo ========================================
echo.
pause
goto menu

:optimize
echo.
echo 🚀 ปรับปรุงประสิทธิภาพระบบ...
echo ========================================
echo 🔧 กำลังวิเคราะห์ระบบและปรับการตั้งค่า...
echo.
%PYTHON_CMD% performance_optimization.py
echo ========================================
echo.
echo 💡 การปรับปรุงเสร็จสิ้น! ระบบจะทำงานเร็วขึ้น
echo 📝 ไฟล์ config ถูกบันทึกที่: config/performance_config.json
echo.
pause
goto menu

:test_gpu
echo.
echo 🔍 ตรวจสอบ GPU Support...
echo ========================================
echo 🔧 กำลังตรวจสอบการรองรับ GPU...
echo.
%PYTHON_CMD% -c "import torch; print('PyTorch Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda if torch.cuda.is_available() else 'N/A'); print('GPU Count:', torch.cuda.device_count() if torch.cuda.is_available() else 0); [print('GPU', i, ':', torch.cuda.get_device_name(i), '(', round(torch.cuda.get_device_properties(i).total_memory / (1024**3), 1), 'GB)') for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else print('No GPU found')"
echo.
echo 🔧 ทดสอบ GPU Support ในระบบ...
%PYTHON_CMD% -c "from tts_rvc_core import TTSRVCCore; core = TTSRVCCore(); info = core.get_device_info(); print('Current Device:', info['current_device']); print('GPU Available:', info['gpu_available']); print('GPU Count:', info['gpu_count']); print('Device Options:'); [print('  -', opt['value'], ':', opt['label']) for opt in info['device_options']]"
echo ========================================
echo.
echo 💡 หมายเหตุ:
echo   • หากพบ GPU: สามารถใช้ GPU ได้ (เร็วขึ้น 3-5 เท่า)
echo   • หากไม่พบ GPU: ใช้ CPU เท่านั้น (เสถียรที่สุด)
echo   • สามารถเปลี่ยนอุปกรณ์ได้ใน Web Interface
echo.
pause
goto menu

:models
echo.
echo 📋 รายชื่อโมเดล RVC ที่มีอยู่...
echo ========================================
%PYTHON_CMD% -c "from rvc_api import RVCConverter; rvc = RVCConverter(); models = rvc.get_available_models(); print(f'\nพบโมเดล {len(models)} ตัว:\n' + '='*40); [print(f'{i+1:2d}. {model}') for i, model in enumerate(sorted(models))]"
echo ========================================
echo.
pause
goto menu

:install
echo.
echo 📦 ติดตั้ง Dependencies...
echo ========================================
echo 🔧 กำลังติดตั้ง packages จาก requirements.txt
echo.
%PYTHON_CMD% -m pip install -r requirements.txt
echo.
echo 🔧 ติดตั้ง packages เพิ่มเติมสำหรับ RVC
%PYTHON_CMD% -m pip install librosa soundfile numpy scipy resampy numba noisereduce pedalboard torchcrepe pydub
echo.
echo ✅ ติดตั้งเสร็จสิ้น
echo ========================================
echo.
pause
goto menu

:build_exe
echo.
echo 🏗️  สร้างไฟล์ EXE...
echo ========================================
if exist "build_exe.bat" (
    call build_exe.bat
) else (
    echo ⚠️  ไม่พบ build_exe.bat
    echo 🔧 ใช้ PyInstaller โดยตรง...
    %PYTHON_CMD% -m PyInstaller victor_tts.spec --noconfirm
)
echo ========================================
echo.
pause
goto menu

:invalid
echo.
echo ❌ ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่
echo.
pause

:menu
cls
goto main_menu

:exit
echo.
echo 👋 ขอบคุณที่ใช้งาน VICTOR-TTS!
echo 🌟 Voice Conversion System by VICTOR
echo 💬 หากมีปัญหาการใช้งาน ติดต่อผู้พัฒนา
echo.
timeout /t 2 >nul
exit

:end
echo.
echo 🔄 โปรแกรมสิ้นสุดการทำงาน
echo 💡 เรียกใช้ start.bat อีกครั้งเพื่อใช้งานต่อ
echo.
pause
goto menu
