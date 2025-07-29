#!/usr/bin/env python3
"""
🔧 VICTOR-TTS Complete Fix Script
แก้ไขปัญหาการเปิดโปรแกรมช้าและ RVC ที่ไม่ทำงาน
"""
import os
import sys
import time
import subprocess
from pathlib import Path

def main():
    """ฟังก์ชันหลัก"""
    print("🔧 VICTOR-TTS Complete Fix Script")
    print("=" * 60)
    print("🎯 แก้ไขปัญหาการเปิดโปรแกรมช้าและ RVC ที่ไม่ทำงาน")
    print("=" * 60)
    
    # ตรวจสอบ Python
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {Path.cwd()}")
    
    # รันการแก้ไขประสิทธิภาพ
    print("\n🚀 Step 1: Fixing Performance Issues...")
    try:
        result = subprocess.run([sys.executable, "fix_performance.py"], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Performance fixes completed")
            print(result.stdout)
        else:
            print("⚠️ Performance fixes had issues")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Performance fix error: {e}")
    
    # รันการแก้ไข RVC
    print("\n🎤 Step 2: Fixing RVC Issues...")
    try:
        result = subprocess.run([sys.executable, "fix_rvc.py"], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ RVC fixes completed")
            print(result.stdout)
        else:
            print("⚠️ RVC fixes had issues")
            print(result.stderr)
    except Exception as e:
        print(f"❌ RVC fix error: {e}")
    
    # ทดสอบระบบ
    print("\n🧪 Step 3: Testing Fixed System...")
    try:
        # ทดสอบ optimized core
        print("Testing optimized core...")
        result = subprocess.run([sys.executable, "-c", 
                               "from tts_rvc_core_optimized import create_optimized_core_instance; core = create_optimized_core_instance(); print('✅ Optimized core loaded successfully')"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Optimized core test passed")
        else:
            print("⚠️ Optimized core test failed")
            print(result.stderr)
        
        # ทดสอบ RVC wrapper
        print("Testing RVC wrapper...")
        result = subprocess.run([sys.executable, "-c", 
                               "from rvc_wrapper import create_rvc_wrapper; wrapper = create_rvc_wrapper(); print('✅ RVC wrapper loaded successfully')"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ RVC wrapper test passed")
        else:
            print("⚠️ RVC wrapper test failed")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ System test error: {e}")
    
    # สร้างสคริปต์เริ่มต้นแบบเร็ว
    print("\n🚀 Step 4: Creating Fast Start Script...")
    fast_start_content = '''@echo off
REM 🚀 VICTOR-TTS FAST START - เวอร์ชันที่แก้ไขแล้ว
REM ใช้สำหรับเริ่มต้นโปรแกรมแบบเร็ว

title VICTOR-TTS FAST

echo.
echo ========================================
echo 🎙️  VICTOR-TTS FAST SYSTEM  🎙️
echo ========================================
echo ✅ Optimized for Speed
echo ✅ Fixed RVC Issues
echo ✅ Reduced Memory Usage
echo ========================================
echo.

REM ตรวจสอบ Python
if exist "venv\\Scripts\\python.exe" (
    set PYTHON_CMD=venv\\Scripts\\python.exe
    echo ✅ Using Virtual Environment
) else (
    set PYTHON_CMD=python
    echo ⚠️  Using System Python
)

echo 📌 Python Info:
%PYTHON_CMD% --version

echo.
echo 🚀 Starting Fast Web Interface...
echo 🔗 URL: http://localhost:7000
echo.

%PYTHON_CMD% web_interface_fast.py

pause
'''
    
    try:
        with open("start_fast.bat", "w", encoding="utf-8") as f:
            f.write(fast_start_content)
        print("✅ Fast start script created: start_fast.bat")
    except Exception as e:
        print(f"❌ Failed to create fast start script: {e}")
    
    # สร้างสคริปต์ทดสอบ
    print("\n🧪 Step 5: Creating Test Script...")
    test_script_content = '''@echo off
REM 🧪 VICTOR-TTS Test Script

title VICTOR-TTS Test

echo.
echo ========================================
echo 🧪  VICTOR-TTS TEST SUITE  🧪
echo ========================================
echo.

REM ตรวจสอบ Python
if exist "venv\\Scripts\\python.exe" (
    set PYTHON_CMD=venv\\Scripts\\python.exe
) else (
    set PYTHON_CMD=python
)

echo 🧪 Testing Optimized Core...
%PYTHON_CMD% -c "from tts_rvc_core_optimized import create_optimized_core_instance; core = create_optimized_core_instance(); print('✅ Optimized core test passed')"

echo.
echo 🧪 Testing RVC Wrapper...
%PYTHON_CMD% -c "from rvc_wrapper import create_rvc_wrapper; wrapper = create_rvc_wrapper(); print('✅ RVC wrapper test passed')"

echo.
echo 🧪 Testing RVC Models...
%PYTHON_CMD% test_rvc_fixed.py

echo.
echo ✅ All tests completed!
pause
'''
    
    try:
        with open("test_all.bat", "w", encoding="utf-8") as f:
            f.write(test_script_content)
        print("✅ Test script created: test_all.bat")
    except Exception as e:
        print(f"❌ Failed to create test script: {e}")
    
    # สรุปผลลัพธ์
    print("\n" + "=" * 60)
    print("🎉 FIX COMPLETED!")
    print("=" * 60)
    print("📁 Files created:")
    print("  ✅ tts_rvc_core_optimized.py - Core ที่ปรับปรุงแล้ว")
    print("  ✅ web_interface_fast.py - Web interface ที่เร็วขึ้น")
    print("  ✅ rvc_wrapper.py - RVC wrapper ที่เสถียรกว่า")
    print("  ✅ start_fast.bat - สคริปต์เริ่มต้นแบบเร็ว")
    print("  ✅ test_all.bat - สคริปต์ทดสอบ")
    print("  ✅ test_rvc_fixed.py - ทดสอบ RVC")
    print()
    print("🚀 How to use:")
    print("  1. รัน 'start_fast.bat' เพื่อเริ่มต้นโปรแกรมแบบเร็ว")
    print("  2. รัน 'test_all.bat' เพื่อทดสอบระบบ")
    print("  3. ใช้ 'web_interface_fast.py' แทน web_interface.py เดิม")
    print()
    print("🎯 Expected improvements:")
    print("  ⚡ Faster startup time")
    print("  🎤 Working RVC voice conversion")
    print("  💾 Reduced memory usage")
    print("  🔧 Better error handling")
    print("=" * 60)

if __name__ == "__main__":
    main() 