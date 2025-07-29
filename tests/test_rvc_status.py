#!/usr/bin/env python3
"""
Quick test to check RVC status
"""
import sys
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

print("🧪 Testing RVC System Status...")
print("=" * 50)

# Test imports
try:
    print("✅ Python version:", sys.version)
    print("✅ Python path:", sys.executable)
    print()
    
    print("Testing audio libraries...")
    import librosa
    print("✅ librosa imported successfully")
    
    import soundfile
    print("✅ soundfile imported successfully")
    
    import numpy
    print("✅ numpy imported successfully")
    
    import scipy
    print("✅ scipy imported successfully")
    
    import resampy
    print("✅ resampy imported successfully")
    
    import numba
    print("✅ numba imported successfully")
    
    import noisereduce
    print("✅ noisereduce imported successfully")
    
    import pedalboard
    print("✅ pedalboard imported successfully")
    
    import pydub
    print("✅ pydub imported successfully")
    
    print()
    print("Testing RVC modules...")
    
    # Test RVC API
    from rvc_api import RVCConverter
    print("✅ RVC API imported successfully")
    
    # Initialize RVC
    rvc = RVCConverter()
    print("✅ RVC Converter initialized")
    
    # Get available models
    models = rvc.get_available_models()
    print(f"✅ Found {len(models)} RVC models:")
    for i, model in enumerate(models[:5]):  # Show first 5
        print(f"   {i+1}. {model}")
    if len(models) > 5:
        print(f"   ... and {len(models) - 5} more")
    
    print()
    print("Testing TTS-RVC Core...")
    
    # Test TTS-RVC Core
    from tts_rvc_core import TTSRVCCore
    core = TTSRVCCore()
    
    status = core.get_system_status()
    print(f"✅ TTS Available: {status['tts_available']}")
    print(f"✅ RVC Available: {status['rvc_available']}")
    print(f"✅ Device: {status['device']}")
    print(f"✅ GPU Name: {status['gpu_name']}")
    print(f"✅ RVC Models Count: {status['rvc_models_count']}")
    
    print()
    print("=" * 50)
    print("✅ All tests passed! RVC system is ready to use.")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"   Missing module: {e.name}")
    print()
    print("💡 Try running: pip install", e.name)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50) 