#!/usr/bin/env python3
"""
🚀 ทดสอบ Voice Conversion แบบด่วน
ทดสอบการทำงานของ RVC กับไฟล์เสียงที่ถูกต้อง
"""

import asyncio
import sys
import os
from pathlib import Path

# เพิ่ม path ของโปรเจค
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from tts_rvc_core import TTSRVCCore

async def test_rvc_quick():
    """ทดสอบ RVC แบบด่วน"""
    print("🚀 ทดสอบ Voice Conversion แบบด่วน")
    print("=" * 50)
    
    try:
        # สร้าง core instance
        print("📦 กำลังโหลด TTS-RVC Core...")
        core = TTSRVCCore(
            models_dir="logs",
            temp_dir="storage/temp",
            device="cpu",
            use_gpu=False
        )
        
        # ตรวจสอบสถานะ
        status = core.get_system_status()
        print(f"✅ TTS: {status['tts_available']}")
        print(f"✅ RVC: {status['rvc_available']}")
        print(f"📁 Models: {len(status.get('rvc_models', []))}")
        
        if not status['tts_available']:
            print("❌ TTS ไม่พร้อมใช้งาน")
            return
        
        if not status['rvc_available']:
            print("❌ RVC ไม่พร้อมใช้งาน")
            return
        
        # ทดสอบ TTS
        print("\n🎤 ทดสอบ TTS...")
        test_text = "สวัสดีครับ นี่คือการทดสอบระบบ TTS และ RVC"
        tts_audio = await core.generate_tts(
            text=test_text,
            voice="th-TH-PremwadeeNeural",
            speed=1.0,
            enable_multi_language=False
        )
        
        print(f"✅ TTS สำเร็จ: {len(tts_audio)} bytes")
        
        # ทดสอบ RVC
        print("\n🎭 ทดสอบ RVC...")
        rvc_models = core.get_available_rvc_models()
        
        if not rvc_models:
            print("❌ ไม่พบโมเดล RVC")
            return
        
        # เลือกโมเดลแรก
        test_model = rvc_models[0]
        print(f"🎯 ใช้โมเดล: {test_model}")
        
        # แปลงเสียง
        import time
        start_time = time.time()
        
        rvc_audio = core.convert_voice(
            audio_data=tts_audio,
            model_name=test_model,
            transpose=0,
            index_ratio=0.75,
            f0_method="rmvpe"
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ RVC สำเร็จ: {len(rvc_audio)} bytes")
        print(f"⏱️ เวลาประมวลผล: {processing_time:.2f} วินาที")
        
        # บันทึกไฟล์ทดสอบ
        test_output_dir = Path("test_output")
        test_output_dir.mkdir(exist_ok=True)
        
        # บันทึก TTS
        tts_file = test_output_dir / "test_tts_quick.wav"
        with open(tts_file, "wb") as f:
            f.write(tts_audio)
        
        # บันทึก RVC
        rvc_file = test_output_dir / "test_rvc_quick.wav"
        with open(rvc_file, "wb") as f:
            f.write(rvc_audio)
        
        print(f"\n💾 บันทึกไฟล์:")
        print(f"   TTS: {tts_file}")
        print(f"   RVC: {rvc_file}")
        
        print("\n🎉 การทดสอบสำเร็จ!")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_rvc_quick()) 