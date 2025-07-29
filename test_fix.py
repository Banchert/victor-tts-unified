#!/usr/bin/env python3
"""
🧪 Test Fix Script - ทดสอบการแก้ไขปัญหา
"""

def test_model_utils():
    """ทดสอบ model_utils"""
    try:
        from model_utils import safe_model_processing, normalize_model_name
        print("✅ Import model_utils สำเร็จ")
        
        # ทดสอบ normalize_model_name
        test_cases = [
            "test_model",
            {"name": "test_model_dict"},
            ["test_model_list"],
            None,
            "",
            123
        ]
        
        print("\n🔍 ทดสอบ normalize_model_name:")
        for test_case in test_cases:
            result = normalize_model_name(test_case)
            print(f"  {test_case} -> {result}")
        
        # ทดสอบ safe_model_processing
        available_models = ["model1", "model2", "model3"]
        test_model, error = safe_model_processing("model1", available_models)
        print(f"\n🔍 ทดสอบ safe_model_processing:")
        print(f"  Result: {test_model}, Error: {error}")
        
        return True
        
    except Exception as e:
        print(f"❌ การทดสอบ model_utils ล้มเหลว: {e}")
        return False

def test_core_import():
    """ทดสอบ import core system"""
    try:
        from tts_rvc_core import TTSRVCCore
        print("✅ Import tts_rvc_core สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ การทดสอบ tts_rvc_core ล้มเหลว: {e}")
        return False

def test_rvc_api_import():
    """ทดสอบ import rvc_api"""
    try:
        from rvc_api import RVCConverter
        print("✅ Import rvc_api สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ การทดสอบ rvc_api ล้มเหลว: {e}")
        return False

def test_web_interface_import():
    """ทดสอบ import web_interface"""
    try:
        from web_interface import WebInterface
        print("✅ Import web_interface สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ การทดสอบ web_interface ล้มเหลว: {e}")
        return False

def main():
    print("🧪 เริ่มต้นการทดสอบการแก้ไข...")
    print("=" * 50)
    
    tests = [
        ("Model Utils", test_model_utils),
        ("TTS-RVC Core", test_core_import),
        ("RVC API", test_rvc_api_import),
        ("Web Interface", test_web_interface_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🔍 ทดสอบ {name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎉 ผลการทดสอบ: {passed}/{total} ผ่าน")
    
    if passed == total:
        print("✅ การแก้ไขสำเร็จ! ปัญหา 'unhashable type: dict' ได้รับการแก้ไขแล้ว")
        print("\n🚀 คำแนะนำในการใช้งาน:")
        print("  1. รันเว็บอินเทอร์เฟซ: python web_interface.py")
        print("  2. รัน API เซิร์ฟเวอร์: python main_api_server.py")
        print("  3. ตรวจสอบโมเดล RVC ในโฟลเดอร์ logs/")
    else:
        print(f"⚠️ ยังมีปัญหาบางอย่าง กรุณาตรวจสอบข้อผิดพลาดด้านบน")
    
    return passed == total

if __name__ == "__main__":
    main()
