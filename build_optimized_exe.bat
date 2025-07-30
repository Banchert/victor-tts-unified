@echo off
echo 🎤 Building VICTOR-TTS Optimized EXE...
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install PyInstaller
echo 📦 Installing PyInstaller...
pip install pyinstaller

REM Install optimized requirements
echo 📦 Installing optimized requirements...
pip install -r requirements_optimized.txt

REM Build EXE with PyInstaller
echo 🏗️ Building EXE with PyInstaller...
pyinstaller --onefile ^
    --windowed ^
    --name "VICTOR-TTS-Optimized" ^
    --add-data "templates;templates" ^
    --add-data "assets;assets" ^
    --hidden-import edge_tts ^
    --hidden-import torch ^
    --hidden-import torchaudio ^
    --hidden-import numpy ^
    --hidden-import scipy ^
    --hidden-import librosa ^
    --hidden-import soundfile ^
    --hidden-import requests ^
    --hidden-import fastapi ^
    --hidden-import uvicorn ^
    --hidden-import aiofiles ^
    --exclude-module matplotlib ^
    --exclude-module PIL ^
    --exclude-module cv2 ^
    --exclude-module pandas ^
    --exclude-module seaborn ^
    --exclude-module jupyter ^
    --exclude-module IPython ^
    --exclude-module notebook ^
    --exclude-module tensorflow ^
    --exclude-module keras ^
    --exclude-module sklearn ^
    --exclude-module scikit-learn ^
    --exclude-module plotly ^
    --exclude-module bokeh ^
    --exclude-module dash ^
    --exclude-module streamlit ^
    --exclude-module gradio ^
    --exclude-module transformers ^
    --exclude-module diffusers ^
    --exclude-module accelerate ^
    --exclude-module datasets ^
    --exclude-module faiss ^
    --exclude-module sentencepiece ^
    --exclude-module tokenizers ^
    --exclude-module huggingface_hub ^
    --exclude-module safetensors ^
    --exclude-module xformers ^
    --exclude-module triton ^
    --exclude-module apex ^
    --exclude-module deepspeed ^
    --exclude-module fairscale ^
    --exclude-module megatron ^
    --exclude-module colossalai ^
    web_interface_complete.py

echo ✅ Build completed!
echo 📁 EXE file created: dist/VICTOR-TTS-Optimized.exe
echo 🚀 You can now run the EXE file directly on Windows
pause
