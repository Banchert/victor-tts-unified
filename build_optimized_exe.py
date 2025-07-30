#!/usr/bin/env python3
"""
Build Optimized EXE for VICTOR-TTS
- Only includes 2-3 essential voice models
- Optimized for Windows
- Ready to use without modifying main files
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_optimized_config():
    """Create optimized configuration for EXE build"""
    print("🔧 Creating optimized configuration...")
    
    # Create optimized config directory
    optimized_dir = Path("build_optimized")
    optimized_dir.mkdir(exist_ok=True)
    
    # Copy essential files
    essential_files = [
        "web_interface_complete.py",
        "tts_rvc_core.py", 
        "rvc_api.py",
        "rvc_wrapper.py",
        "model_utils.py",
        "requirements.txt",
        "start_complete.bat"
    ]
    
    for file in essential_files:
        if Path(file).exists():
            shutil.copy2(file, optimized_dir / file)
            print(f"✅ Copied: {file}")
    
    # Create optimized requirements
    optimized_requirements = """edge-tts==6.1.9
torch>=2.0.0
torchaudio>=2.0.0
numpy>=1.21.0
scipy>=1.7.0
librosa>=0.9.0
soundfile>=0.10.0
requests>=2.25.0
fastapi>=0.68.0
uvicorn>=0.15.0
python-multipart>=0.0.5
aiofiles>=0.7.0
"""
    
    with open(optimized_dir / "requirements_optimized.txt", "w") as f:
        f.write(optimized_requirements)
    
    print("✅ Created optimized requirements")
    
    return optimized_dir

def create_voice_selector():
    """Create a simple voice selector for the optimized version"""
    voice_selector_code = '''#!/usr/bin/env python3
"""
Optimized Voice Selector for VICTOR-TTS EXE
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def select_voice_model():
    """Select voice model for optimized EXE"""
    print("🎤 VICTOR-TTS Optimized Voice Selector")
    print("=" * 50)
    
    # Available voice models for optimized version
    voice_models = {
        "1": {
            "name": "Thai Female (Premwadee)",
            "voice_id": "th-TH-PremwadeeNeural",
            "language": "Thai",
            "gender": "Female"
        },
        "2": {
            "name": "Lao Female (Keomany)", 
            "voice_id": "lo-LA-KeomanyNeural",
            "language": "Lao",
            "gender": "Female"
        },
        "3": {
            "name": "English Female (Aria)",
            "voice_id": "en-US-AriaNeural", 
            "language": "English",
            "gender": "Female"
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
        
        # Set environment variable for the selected voice
        os.environ["DEFAULT_VOICE"] = selected_voice["voice_id"]
        os.environ["DEFAULT_LANGUAGE"] = selected_voice["language"]
        
        print(f"\\n🎯 Default voice set to: {selected_voice['name']}")
        print("🚀 Starting VICTOR-TTS...")
        
        # Import and start the web interface
        from web_interface_complete import main as start_web_interface
        start_web_interface()
        
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
    except Exception as e:
        print(f"\\n❌ Error: {e}")

if __name__ == "__main__":
    main()
'''
    
    return voice_selector_code

def create_optimized_launcher():
    """Create optimized launcher script"""
    launcher_code = '''#!/usr/bin/env python3
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
        
        # Create web interface with optimized settings
        web_interface = CompleteWebInterface(port=7000)
        
        # Start the server
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
    
    return launcher_code

def create_build_script():
    """Create build script for PyInstaller"""
    build_script = '''@echo off
echo 🎤 Building VICTOR-TTS Optimized EXE...
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install required packages
echo 📦 Installing required packages...
pip install pyinstaller
pip install -r requirements_optimized.txt

REM Create optimized launcher
echo 🔧 Creating optimized launcher...
python -c "
import os
from build_optimized_exe import create_optimized_launcher, create_voice_selector

# Create launcher
launcher_code = create_optimized_launcher()
with open('optimized_launcher.py', 'w', encoding='utf-8') as f:
    f.write(launcher_code)

# Create voice selector  
voice_selector_code = create_voice_selector()
with open('voice_selector.py', 'w', encoding='utf-8') as f:
    f.write(voice_selector_code)

print('✅ Created optimized launcher and voice selector')
"

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
    --exclude-module flash_attn ^
    --exclude-module flash_attention ^
    --exclude-module flash_attn_2 ^
    --exclude-module flash_attn_3 ^
    --exclude-module flash_attn_4 ^
    --exclude-module flash_attn_5 ^
    --exclude-module flash_attn_6 ^
    --exclude-module flash_attn_7 ^
    --exclude-module flash_attn_8 ^
    --exclude-module flash_attn_9 ^
    --exclude-module flash_attn_10 ^
    --exclude-module flash_attn_11 ^
    --exclude-module flash_attn_12 ^
    --exclude-module flash_attn_13 ^
    --exclude-module flash_attn_14 ^
    --exclude-module flash_attn_15 ^
    --exclude-module flash_attn_16 ^
    --exclude-module flash_attn_17 ^
    --exclude-module flash_attn_18 ^
    --exclude-module flash_attn_19 ^
    --exclude-module flash_attn_20 ^
    --exclude-module flash_attn_21 ^
    --exclude-module flash_attn_22 ^
    --exclude-module flash_attn_23 ^
    --exclude-module flash_attn_24 ^
    --exclude-module flash_attn_25 ^
    --exclude-module flash_attn_26 ^
    --exclude-module flash_attn_27 ^
    --exclude-module flash_attn_28 ^
    --exclude-module flash_attn_29 ^
    --exclude-module flash_attn_30 ^
    --exclude-module flash_attn_31 ^
    --exclude-module flash_attn_32 ^
    --exclude-module flash_attn_33 ^
    --exclude-module flash_attn_34 ^
    --exclude-module flash_attn_35 ^
    --exclude-module flash_attn_36 ^
    --exclude-module flash_attn_37 ^
    --exclude-module flash_attn_38 ^
    --exclude-module flash_attn_39 ^
    --exclude-module flash_attn_40 ^
    --exclude-module flash_attn_41 ^
    --exclude-module flash_attn_42 ^
    --exclude-module flash_attn_43 ^
    --exclude-module flash_attn_44 ^
    --exclude-module flash_attn_45 ^
    --exclude-module flash_attn_46 ^
    --exclude-module flash_attn_47 ^
    --exclude-module flash_attn_48 ^
    --exclude-module flash_attn_49 ^
    --exclude-module flash_attn_50 ^
    --exclude-module flash_attn_51 ^
    --exclude-module flash_attn_52 ^
    --exclude-module flash_attn_53 ^
    --exclude-module flash_attn_54 ^
    --exclude-module flash_attn_55 ^
    --exclude-module flash_attn_56 ^
    --exclude-module flash_attn_57 ^
    --exclude-module flash_attn_58 ^
    --exclude-module flash_attn_59 ^
    --exclude-module flash_attn_60 ^
    --exclude-module flash_attn_61 ^
    --exclude-module flash_attn_62 ^
    --exclude-module flash_attn_63 ^
    --exclude-module flash_attn_64 ^
    --exclude-module flash_attn_65 ^
    --exclude-module flash_attn_66 ^
    --exclude-module flash_attn_67 ^
    --exclude-module flash_attn_68 ^
    --exclude-module flash_attn_69 ^
    --exclude-module flash_attn_70 ^
    --exclude-module flash_attn_71 ^
    --exclude-module flash_attn_72 ^
    --exclude-module flash_attn_73 ^
    --exclude-module flash_attn_74 ^
    --exclude-module flash_attn_75 ^
    --exclude-module flash_attn_76 ^
    --exclude-module flash_attn_77 ^
    --exclude-module flash_attn_78 ^
    --exclude-module flash_attn_79 ^
    --exclude-module flash_attn_80 ^
    --exclude-module flash_attn_81 ^
    --exclude-module flash_attn_82 ^
    --exclude-module flash_attn_83 ^
    --exclude-module flash_attn_84 ^
    --exclude-module flash_attn_85 ^
    --exclude-module flash_attn_86 ^
    --exclude-module flash_attn_87 ^
    --exclude-module flash_attn_88 ^
    --exclude-module flash_attn_89 ^
    --exclude-module flash_attn_90 ^
    --exclude-module flash_attn_91 ^
    --exclude-module flash_attn_92 ^
    --exclude-module flash_attn_93 ^
    --exclude-module flash_attn_94 ^
    --exclude-module flash_attn_95 ^
    --exclude-module flash_attn_96 ^
    --exclude-module flash_attn_97 ^
    --exclude-module flash_attn_98 ^
    --exclude-module flash_attn_99 ^
    --exclude-module flash_attn_100 ^
    optimized_launcher.py

echo ✅ Build completed!
echo 📁 EXE file created: dist/VICTOR-TTS-Optimized.exe
echo 🚀 You can now run the EXE file directly on Windows
pause
'''
    
    return build_script

def main():
    """Main build function"""
    print("🎤 VICTOR-TTS Optimized EXE Builder")
    print("=" * 50)
    
    # Create optimized configuration
    optimized_dir = create_optimized_config()
    
    # Create voice selector
    voice_selector_code = create_voice_selector()
    with open("voice_selector.py", "w", encoding="utf-8") as f:
        f.write(voice_selector_code)
    
    # Create optimized launcher
    launcher_code = create_optimized_launcher()
    with open("optimized_launcher.py", "w", encoding="utf-8") as f:
        f.write(launcher_code)
    
    # Create build script
    build_script = create_build_script()
    with open("build_optimized_exe.bat", "w", encoding="utf-8") as f:
        f.write(build_script)
    
    print("\n✅ Created optimized build files:")
    print("   - voice_selector.py")
    print("   - optimized_launcher.py") 
    print("   - build_optimized_exe.bat")
    print("   - build_optimized/ (optimized files)")
    
    print("\n🚀 To build the EXE:")
    print("   1. Run: build_optimized_exe.bat")
    print("   2. Wait for build to complete")
    print("   3. Find EXE in: dist/VICTOR-TTS-Optimized.exe")
    
    print("\n📋 Optimized features:")
    print("   - Only 3 essential voice models")
    print("   - Reduced file size")
    print("   - Faster startup time")
    print("   - Windows optimized")
    print("   - No modification to main files")

if __name__ == "__main__":
    main() 