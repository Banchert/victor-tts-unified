#!/usr/bin/env python3
"""
🧪 ทดสอบระบบ TTS-RVC ที่จัดระเบียบใหม่
"""
import os
import sys
import asyncio
from pathlib import Path

# เพิ่ม path ของโปรเจค
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_core_system():
    """ทดสอบระบบ Core"""
    print("🔧 ทดสอบระบบ TTS-RVC Core...")
    
    try:
        from tts_rvc_core import TTSRVCCore, get_supported_voices
        
        # สร้าง Core instance
        core = TTSRVCCore()
        
        # ตรวจสอบสถานะ
        status = core.get_system_status()
        print(f"📊 สถานะระบบ:")
        print(f"   TTS: {'✅' if status['tts_available'] else '❌'}")
        print(f"   RVC: {'✅' if status['rvc_available'] else '❌'}")
        print(f"   โมเดล RVC: {status['rvc_models_count']} ตัว")
        
        if status['rvc_models_count'] > 0:
            print(f"   โมเดลตัวอย่าง: {', '.join(status['rvc_models'][:3])}")
        
        # ทดสอบ TTS
        if status['tts_available']:
            print("\\n🎵 ทดสอบ TTS...")
            test_text = "สวัสดีครับ นี่คือการทดสอบระบบใหม่"
            
            try:
                audio_data = await core.generate_tts(test_text, "th-TH-PremwadeeNeural")
                print(f"✅ TTS สำเร็จ: {len(audio_data):,} bytes")
            except Exception as e:
                print(f"❌ TTS ล้มเหลว: {e}")
        
        # ทดสอบ Unified Processing
        print("\\n🚀 ทดสอบระบบรวม...")
        test_text = "ทดสอบระบบที่จัดระเบียบใหม่แล้ว"
        
        result = await core.process_unified(
            text=test_text,
            tts_voice="th-TH-PremwadeeNeural",
            enable_rvc=status['rvc_available'] and status['rvc_models_count'] > 0,
            rvc_model=status['rvc_models'][0] if status['rvc_models_count'] > 0 else None
        )
        
        if result['success']:
            print("✅ ระบบรวมทำงานสำเร็จ!")
            print(f"   ขั้นตอน: {', '.join(result['processing_steps'])}")
            print(f"   ขนาดเสียง: {len(result['audio_data']):,} bytes")
        else:
            print(f"❌ ระบบรวมล้มเหลว: {result.get('error')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ ไม่สามารถ import TTS-RVC Core: {e}")
        return False
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_file_structure():
    """ทดสอบโครงสร้างไฟล์ใหม่"""
    print("\\n📁 ทดสอบโครงสร้างไฟล์...")
    
    required_dirs = [
        "storage",
        "storage/temp", 
        "storage/output",
        "models",
        "tests",
        "config",
        "legacy"
    ]
    
    required_files = [
        "tts_rvc_core.py",
        "main_api_server.py", 
        "web_interface.py"
    ]
    
    all_good = True
    
    # ตรวจสอบโฟลเดอร์
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (ไม่พบ)")
            all_good = False
    
    # ตรวจสอบไฟล์
    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} (ไม่พบ)")
            all_good = False
    
    return all_good

def test_legacy_compatibility():
    """ทดสอบความเข้ากันได้กับระบบเดิม"""
    print("\\n🔄 ทดสอบความเข้ากันได้...")
    
    legacy_files = [
        "rvc_api.py",
        "rvc_fallback.py", 
        "logs"  # โฟลเดอร์โมเดล
    ]
    
    compatibility_score = 0
    total_checks = len(legacy_files)
    
    for item in legacy_files:
        if Path(item).exists():
            print(f"✅ {item} พร้อมใช้งาน")
            compatibility_score += 1
        else:
            print(f"⚠️ {item} ไม่พบ")
    
    compatibility_percent = (compatibility_score / total_checks) * 100
    print(f"\\n📊 ความเข้ากันได้: {compatibility_percent:.1f}% ({compatibility_score}/{total_checks})")
    
    return compatibility_percent >= 70

async def run_all_tests():
    """รันการทดสอบทั้งหมด"""
    print("🧪 เริ่มการทดสอบระบบที่จัดระเบียบใหม่")
    print("=" * 50)
    
    results = {}
    
    # ทดสอบโครงสร้างไฟล์
    results['file_structure'] = test_file_structure()
    
    # ทดสอบความเข้ากันได้
    results['legacy_compatibility'] = test_legacy_compatibility()
    
    # ทดสอบระบบ Core
    results['core_system'] = await test_core_system()
    
    # สรุปผล
    print("\\n" + "=" * 50)
    print("📋 สรุปผลการทดสอบ:")
    
    for test_name, result in results.items():
        status = "✅ ผ่าน" if result else "❌ ไม่ผ่าน"
        test_display = {
            'file_structure': 'โครงสร้างไฟล์',
            'legacy_compatibility': 'ความเข้ากันได้',
            'core_system': 'ระบบ Core'
        }
        print(f"   {test_display[test_name]}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\\n🎉 การทดสอบผ่านทั้งหมด! ระบบพร้อมใช้งาน")
    else:
        print("\\n⚠️ มีการทดสอบที่ไม่ผ่าน กรุณาตรวจสอบ")
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
