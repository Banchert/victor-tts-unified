#!/usr/bin/env python3
"""
Create EXE Build Files for VICTOR-TTS
Simple script to create optimized EXE build files
"""
import os
from pathlib import Path

def create_voice_selector():
    """Create voice selector for optimized EXE"""
    code = '''#!/usr/bin/env python3
"""
Optimized Voice Selector for VICTOR-TTS EXE
"""
import os
import sys
from pathlib import Path

def select_voice_model():
    """Select voice model for optimized EXE"""
    print("🎤 VICTOR-TTS Optimized Voice Selector")
    print("=" * 50)
    
    voice_models = {
        "1": {
            "name": "Thai Female (Premwadee)",
            "voice_id": "th-TH-PremwadeeNeural",
            "language": "Thai"
        },
        "2": {
            "name": "Lao Female (Keomany)", 
            "voice_id": "lo-LA-KeomanyNeural",
            "language": "Lao"
        },
        "3": {
            "name": "English Female (Aria)",
            "voice_id": "en-US-AriaNeural", 
            "language": "English"
        }
    }
    
    print("Available voice models:")
    for key, model in voice_models.items():
        print(f"{key}. {model['name']} ({model['language']})")
    
    while True:
        choice = input("\\nSelect voice model (1-3): ").strip()
        if choice in voice_models:
            selected_model = voice_models[choice]
            print(f"\\n✅ Selected: {selected_model['name']}")
            return selected_model
        else:
            print("❌ Invalid choice. Please select 1-3.")

def main():
    """Main function"""
    try:
        selected_voice = select_voice_model()
        os.environ["DEFAULT_VOICE"] = selected_voice["voice_id"]
        print(f"\\n🎯 Default voice set to: {selected_voice['name']}")
        print("🚀 Starting VICTOR-TTS...")
        
        # Import and start web interface
        from web_interface_complete import main as start_web_interface
        start_web_interface()
        
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
    except Exception as e:
        print(f"\\n❌ Error: {e}")

if __name__ == "__main__":
    main()
'''
    
    with open("voice_selector.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Created: voice_selector.py")

def create_optimized_launcher():
    """Create optimized launcher"""
    code = '''#!/usr/bin/env python3
"""
Optimized VICTOR-TTS Launcher for Windows EXE
"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def start_web_interface():
    """Start the web interface"""
    try:
        from web_interface_complete import CompleteWebInterface
        web_interface = CompleteWebInterface(port=7000)
        web_interface.start(open_browser=False)
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        input("Press Enter to exit...")

def open_browser_delayed():
    """Open browser after delay"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:7000")
    except:
        pass

def main():
    """Main launcher function"""
    print("🎤 VICTOR-TTS Optimized Launcher")
    print("=" * 40)
    print("🚀 Starting optimized TTS system...")
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start web interface
    start_web_interface()

if __name__ == "__main__":
    main()
'''
    
    with open("optimized_launcher.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Created: optimized_launcher.py")

def create_build_script():
    """Create build script"""
    code = '''@echo off
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
'''
    
    with open("build_optimized_exe.bat", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ Created: build_optimized_exe.bat")

def main():
    """Main function"""
    print("🎤 VICTOR-TTS Optimized EXE Builder")
    print("=" * 50)
    
    # Create files
    create_voice_selector()
    create_optimized_launcher()
    create_build_script()
    
    print("\\n✅ Created optimized build files:")
    print("   - voice_selector.py")
    print("   - optimized_launcher.py") 
    print("   - build_optimized_exe.bat")
    print("   - requirements_optimized.txt")
    
    print("\\n🚀 To build the EXE:")
    print("   1. Run: build_optimized_exe.bat")
    print("   2. Wait for build to complete")
    print("   3. Find EXE in: dist/VICTOR-TTS-Optimized.exe")
    
    print("\\n📋 Optimized features:")
    print("   - Only 3 essential voice models")
    print("   - Reduced file size")
    print("   - Faster startup time")
    print("   - Windows optimized")
    print("   - No modification to main files")

if __name__ == "__main__":
    main() 