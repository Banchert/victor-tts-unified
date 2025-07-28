#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VICTOR-TTS Launcher for EXE
Launcher script for creating standalone EXE with GPU support
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def check_gpu():
    """ตรวจสอบ GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_info = []
            for i in range(gpu_count):
                name = torch.cuda.get_device_name(i)
                memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                gpu_info.append(f"GPU {i}: {name} ({memory:.1f}GB)")
            return True, gpu_info
        else:
            return False, ["No GPU found - Using CPU"]
    except ImportError:
        return False, ["PyTorch not available - Using CPU"]

def start_web_interface():
    """เริ่มต้น Web Interface"""
    try:
        from web_interface import main
        main()
    except ImportError:
        print("❌ Web Interface not available")
        return False
    except Exception as e:
        print(f"❌ Error starting Web Interface: {e}")
        return False

def start_api_server():
    """เริ่มต้น API Server"""
    try:
        import uvicorn
        from main_api_server import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("❌ API Server not available")
        return False
    except Exception as e:
        print(f"❌ Error starting API Server: {e}")
        return False

def main():
    """Main launcher function"""
    print("🐉 VICTOR-TTS Launcher")
    print("=" * 50)
    
    # ตรวจสอบ GPU
    gpu_available, gpu_info = check_gpu()
    print(f"🔍 GPU Status: {'✅ Available' if gpu_available else '❌ Not Available'}")
    for info in gpu_info:
        print(f"   {info}")
    
    print("\n🎯 Available Options:")
    print("1. 🖥️  Web Interface (Recommended)")
    print("2. 🔌 API Server")
    print("3. 🌐 Web Interface + API Server")
    print("4. 🚀 Web Interface + GPU Selection")
    print("5. 🔍 GPU Test")
    print("0. ❌ Exit")
    
    while True:
        try:
            choice = input("\n👉 Select option (0-5): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                print("\n🚀 Starting Web Interface...")
                start_web_interface()
            elif choice == "2":
                print("\n🔌 Starting API Server...")
                start_api_server()
            elif choice == "3":
                print("\n🌐 Starting Web Interface + API Server...")
                # Start API server in background
                api_thread = threading.Thread(target=start_api_server, daemon=True)
                api_thread.start()
                time.sleep(2)
                # Start Web Interface
                start_web_interface()
            elif choice == "4":
                print("\n🚀 Starting Web Interface with GPU Selection...")
                # Set environment variable for GPU selection
                os.environ["VICTOR_TTS_GPU_SELECTION"] = "1"
                start_web_interface()
            elif choice == "5":
                print("\n🔍 Testing GPU Support...")
                test_gpu()
            else:
                print("❌ Invalid choice. Please select 0-5.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def test_gpu():
    """ทดสอบ GPU support"""
    print("🔍 GPU Test Results:")
    print("-" * 30)
    
    # Test PyTorch
    try:
        import torch
        print(f"✅ PyTorch Version: {torch.__version__}")
        print(f"✅ CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"✅ CUDA Version: {torch.version.cuda}")
            print(f"✅ GPU Count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(i)
                memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print(f"✅ GPU {i}: {name} ({memory:.1f}GB)")
        else:
            print("❌ No GPU detected")
    except ImportError:
        print("❌ PyTorch not available")
    
    # Test TTS-RVC Core
    try:
        from tts_rvc_core import TTSRVCCore
        core = TTSRVCCore()
        info = core.get_device_info()
        print(f"\n✅ TTS-RVC Core Device: {info['current_device']}")
        print(f"✅ GPU Available: {info['gpu_available']}")
        print(f"✅ GPU Count: {info['gpu_count']}")
        if info['gpu_info']:
            for gpu in info['gpu_info']:
                print(f"✅ GPU {gpu['id']}: {gpu['name']} ({gpu['memory']:.1f}GB)")
    except ImportError:
        print("❌ TTS-RVC Core not available")
    except Exception as e:
        print(f"❌ TTS-RVC Core Error: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 