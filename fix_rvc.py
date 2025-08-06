#!/usr/bin/env python3
"""
🔧 RVC System Fixer - แก้ไขปัญหา RVC ที่พบบ่อย
"""

import os
import sys
from pathlib import Path
import importlib.util

def check_pytorch():
    """ตรวจสอบ PyTorch"""
    print("🔍 Checking PyTorch...")
    try:
        import torch
        print(f"   ✅ PyTorch {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"   ✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"   📊 CUDA version: {torch.version.cuda}")
        else:
            print("   ⚠️  CUDA not available, using CPU")
        return True
    except ImportError:
        print("   ❌ PyTorch not found")
        return False
    except Exception as e:
        print(f"   ❌ PyTorch error: {e}")
        return False

def check_audio_libs():
    """ตรวจสอบ audio libraries"""
    print("\n🎵 Checking Audio Libraries...")
    
    libs = [
        ("soundfile", "soundfile"),
        ("librosa", "librosa"),
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("faiss", "faiss"),
        ("torchcrepe", "torchcrepe")
    ]
    
    all_good = True
    for lib_name, import_name in libs:
        try:
            __import__(import_name)
            print(f"   ✅ {lib_name}")
        except ImportError:
            print(f"   ❌ {lib_name} - Missing")
            all_good = False
        except Exception as e:
            print(f"   ⚠️  {lib_name} - Error: {e}")
    
    return all_good

def check_rvc_files():
    """ตรวจสอบไฟล์ RVC"""
    print("\n📁 Checking RVC Files...")
    
    required_files = [
        "rvc/infer/infer.py",
        "rvc/infer/pipeline.py", 
        "rvc/lib/utils.py",
        "rvc_api.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def check_model_files():
    """ตรวจสอบโมเดลไฟล์"""
    print("\n🎭 Checking Model Files...")
    
    logs_dir = Path("logs")
    if not logs_dir.exists():
        print("   ❌ logs directory not found")
        return False
    
    model_dirs = [d for d in logs_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    print(f"   📁 Found {len(model_dirs)} model directories")
    
    valid_models = 0
    for model_dir in model_dirs:
        pth_files = list(model_dir.glob("*.pth"))
        index_files = list(model_dir.glob("*.index"))
        
        # Filter out training files
        model_pth_files = [f for f in pth_files if not (f.name.startswith('D_') or f.name.startswith('G_'))]
        
        if model_pth_files and index_files:
            print(f"   ✅ {model_dir.name} - {len(model_pth_files)} pth, {len(index_files)} index")
            valid_models += 1
        else:
            missing = []
            if not model_pth_files:
                missing.append("pth")
            if not index_files:
                missing.append("index")
            print(f"   ⚠️  {model_dir.name} - Missing: {', '.join(missing)}")
    
    print(f"   📊 Valid models: {valid_models}/{len(model_dirs)}")
    return valid_models > 0

def test_rvc_initialization():
    """ทดสอบการเริ่มต้น RVC"""
    print("\n🚀 Testing RVC Initialization...")
    
    try:
        # Test step by step
        print("   1. Importing RVC API...")
        from rvc_api import RVCConverter
        print("      ✅ Import successful")
        
        print("   2. Creating RVC instance...")
        rvc = RVCConverter()
        print("      ✅ Instance created")
        
        print("   3. Getting models...")
        models = rvc.get_available_models()
        print(f"      ✅ Found {len(models)} models")
        
        print("   4. Checking availability...")
        available = rvc.is_available()
        print(f"      ✅ RVC available: {available}")
        
        if models:
            print("   5. Testing model info...")
            info = rvc.get_model_info(models[0])
            print(f"      ✅ Model info retrieved for {models[0]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ RVC initialization failed: {e}")
        import traceback
        print("   📋 Error details:")
        for line in traceback.format_exc().split('\n')[-10:]:
            if line.strip():
                print(f"      {line}")
        return False

def diagnose_common_issues():
    """วินิจฉัยปัญหาที่พบบ่อย"""
    print("\n🩺 Diagnosing Common Issues...")
    
    issues = []
    
    # Check if models directory is accessible
    if not Path("logs").exists():
        issues.append("Models directory 'logs' not found")
    elif not any(Path("logs").iterdir()):
        issues.append("Models directory is empty")
    
    # Check Python path
    try:
        import rvc
        print("   ✅ RVC module accessible")
    except ImportError:
        issues.append("RVC module not in Python path")
    
    # Check device availability
    try:
        import torch
        if not torch.cuda.is_available():
            issues.append("CUDA not available - using CPU only")
    except:
        issues.append("PyTorch not properly configured")
    
    if issues:
        print("   ⚠️  Found issues:")
        for issue in issues:
            print(f"      - {issue}")
    else:
        print("   ✅ No common issues detected")
    
    return len(issues) == 0

def suggest_fixes():
    """แนะนำการแก้ไข"""
    print("\n💡 Suggested Fixes:")
    print("   1. Make sure all dependencies are installed:")
    print("      pip install torch torchvision torchaudio soundfile librosa")
    print("      pip install faiss-cpu torchcrepe")
    print("")
    print("   2. Check if RVC models are properly placed in 'logs' directory")
    print("      Each model should have .pth and .index files")
    print("")
    print("   3. If using GPU, ensure CUDA is properly installed")
    print("      Check: torch.cuda.is_available()")
    print("")
    print("   4. Try restarting the application after making changes")
    print("")
    print("   5. Check the original error in main application logs")

def main():
    """ฟังก์ชันหลัก"""
    print("🔧 RVC SYSTEM DIAGNOSTIC & FIXER")
    print("=" * 50)
    
    tests = [
        ("PyTorch", check_pytorch),
        ("Audio Libraries", check_audio_libs), 
        ("RVC Files", check_rvc_files),
        ("Model Files", check_model_files),
        ("RVC Initialization", test_rvc_initialization),
        ("Common Issues", diagnose_common_issues)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC RESULTS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
        if not result:
            all_passed = False
    
    print(f"\n🎯 Overall Status: {'✅ HEALTHY' if all_passed else '❌ ISSUES FOUND'}")
    
    if not all_passed:
        suggest_fixes()
    else:
        print("🎉 All checks passed! RVC should be working properly.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    print(f"\n{'✅ Diagnosis completed successfully!' if success else '❌ Issues detected - please check above.'}")
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
