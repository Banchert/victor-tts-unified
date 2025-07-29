#!/usr/bin/env python3
"""
🧪 RVC Test Script
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_rvc_basic():
    """ทดสอบ RVC พื้นฐาน"""
    print("🧪 Testing RVC Basic...")
    
    try:
        from rvc_wrapper import create_rvc_wrapper
        
        # สร้าง wrapper
        wrapper = create_rvc_wrapper()
        
        # ตรวจสอบสถานะ
        info = wrapper.get_system_info()
        print(f"✅ System Info: {info}")
        
        if not info["rvc_available"]:
            print("❌ RVC not available")
            return False
        
        if not info["initialized"]:
            print("❌ RVC not initialized")
            return False
        
        # ดึงโมเดล
        models = wrapper.get_available_models()
        print(f"✅ Available models: {models}")
        
        if not models:
            print("❌ No models available")
            return False
        
        # ทดสอบโมเดลแรก
        test_model = models[0]
        print(f"🧪 Testing model: {test_model}")
        
        model_info = wrapper.get_model_info(test_model)
        print(f"✅ Model info: {model_info}")
        
        if wrapper.test_model(test_model):
            print(f"✅ Model {test_model} test passed")
            return True
        else:
            print(f"❌ Model {test_model} test failed")
            return False
            
    except Exception as e:
        print(f"❌ RVC test failed: {e}")
        return False

def test_rvc_conversion():
    """ทดสอบการแปลงเสียง"""
    print("🎤 Testing RVC Conversion...")
    
    try:
        from rvc_wrapper import create_rvc_wrapper
        import tempfile
        import os
        
        wrapper = create_rvc_wrapper()
        
        if not wrapper.get_system_info()["initialized"]:
            print("❌ RVC not initialized")
            return False
        
        models = wrapper.get_available_models()
        if not models:
            print("❌ No models available")
            return False
        
        # สร้างไฟล์เสียงทดสอบที่ถูกต้อง
        import wave
        import numpy as np
        
        # สร้างไฟล์ WAV ที่ถูกต้อง
        sample_rate = 44100
        duration = 1  # 1 วินาที
        frequency = 440  # 440 Hz
        
        # สร้าง sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # แปลงเป็น 16-bit PCM
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # สร้างไฟล์ชั่วคราว
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            test_file = f.name
        
        # บันทึกเป็น WAV
        with wave.open(test_file, 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        # อ่านไฟล์ที่สร้างขึ้น
        with open(test_file, 'rb') as f:
            test_audio = f.read()
        
        try:
            # ทดสอบการแปลง
            result = wrapper.convert_audio_data(
                test_audio, models[0],
                transpose=0, index_ratio=0.75
            )
            
            print(f"✅ Conversion test passed: {len(result)} bytes")
            return True
            
        finally:
            # ลบไฟล์ทดสอบ
            try:
                os.unlink(test_file)
            except:
                pass
                
    except Exception as e:
        print(f"❌ Conversion test failed: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 RVC Test Suite")
    print("=" * 50)
    
    # ทดสอบพื้นฐาน
    basic_ok = test_rvc_basic()
    
    if basic_ok:
        # ทดสอบการแปลง
        conversion_ok = test_rvc_conversion()
        
        if conversion_ok:
            print("🎉 All RVC tests passed!")
        else:
            print("⚠️ Basic tests passed but conversion failed")
    else:
        print("❌ Basic RVC tests failed")

if __name__ == "__main__":
    main()
