#!/usr/bin/env python3
"""
🧪 Test Multi-Language TTS System
ทดสอบระบบ TTS หลายภาษา โดยเฉพาะภาษาลาวที่มีคำภาษาอังกฤษ
"""
import asyncio
import os
import sys
from pathlib import Path

# เพิ่ม path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tts_rvc_core import TTSRVCCore, create_core_instance

async def test_multi_language_tts():
    """ทดสอบระบบ TTS หลายภาษา"""
    print("🧪 Testing Multi-Language TTS System...")
    
    # สร้าง instance
    core = create_core_instance()
    
    # ตรวจสอบสถานะระบบ
    status = core.get_system_status()
    print(f"✅ System Status: {status}")
    
    if not status["tts_available"]:
        print("❌ TTS system not available")
        return
    
    # ข้อความทดสอบ
    test_cases = [
        {
            "name": "Lao with English words",
            "text": "ສະບາຍດີ Hello ທ່ານສະບາຍດີບໍ່ How are you? ຂ້ອຍສະບາຍດີ Thank you",
            "voice": "lo-LA-KeomanyNeural",
            "description": "ข้อความภาษาลาวที่มีคำภาษาอังกฤษปน"
        },
        {
            "name": "Lao with numbers",
            "text": "ວັນທີ 15 ມັງກອນ 2024 ສະບາຍດີ ທ່ານມີ 5 ຄົນ",
            "voice": "lo-LA-KeomanyNeural",
            "description": "ข้อความภาษาลาวที่มีตัวเลข"
        },
        {
            "name": "Mixed Lao and English",
            "text": "ສະບາຍດີ Hello world ທ່ານສະບາຍດີບໍ່ How are you today? ຂ້ອຍສະບາຍດີ Thank you very much",
            "voice": "lo-LA-KeomanyNeural",
            "description": "ข้อความผสมภาษาลาวและภาษาอังกฤษ"
        },
        {
            "name": "Thai with English",
            "text": "สวัสดีครับ Hello world สบายดีไหมครับ How are you? ขอบคุณครับ Thank you",
            "voice": "th-TH-PremwadeeNeural",
            "description": "ข้อความภาษาไทยที่มีคำภาษาอังกฤษปน"
        },
        {
            "name": "Pure Lao",
            "text": "ສະບາຍດີ ທ່ານສະບາຍດີບໍ່ ຂ້ອຍສະບາຍດີ ຂອບໃຈຫຼາຍໆ",
            "voice": "lo-LA-KeomanyNeural",
            "description": "ข้อความภาษาลาวล้วน"
        },
        {
            "name": "Pure English",
            "text": "Hello world How are you today? Thank you very much",
            "voice": "en-US-AriaNeural",
            "description": "ข้อความภาษาอังกฤษล้วน"
        }
    ]
    
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์ทดสอบ
    test_output_dir = Path("test_output")
    test_output_dir.mkdir(exist_ok=True)
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🔍 Test {i+1}: {test_case['name']}")
        print(f"📝 Description: {test_case['description']}")
        print(f"📄 Text: {test_case['text']}")
        print(f"🎤 Voice: {test_case['voice']}")
        
        try:
            # ทดสอบการตรวจจับภาษา
            print("🔤 Language Detection Test:")
            segments = core.detect_language_segments(test_case['text'])
            print(f"   Detected {len(segments)} segments:")
            for j, (segment, lang) in enumerate(segments):
                print(f"   {j+1}. '{segment}' -> {lang}")
            
            # ทดสอบ TTS หลายภาษา
            print("🎵 Multi-Language TTS Test:")
            audio_data = await core.generate_tts(
                test_case['text'], 
                test_case['voice'], 
                speed=1.0, 
                pitch="+0Hz",
                enable_multi_language=True
            )
            
            # บันทึกไฟล์เสียง
            output_file = test_output_dir / f"test_{i+1}_{test_case['name'].replace(' ', '_')}.wav"
            with open(output_file, "wb") as f:
                f.write(audio_data)
            
            print(f"   ✅ Generated: {len(audio_data)} bytes")
            print(f"   💾 Saved to: {output_file}")
            
            # ทดสอบ TTS ภาษาเดียว (เปรียบเทียบ)
            print("🎵 Single-Language TTS Test (for comparison):")
            single_audio_data = await core.generate_tts(
                test_case['text'], 
                test_case['voice'], 
                speed=1.0, 
                pitch="+0Hz",
                enable_multi_language=False
            )
            
            single_output_file = test_output_dir / f"test_{i+1}_{test_case['name'].replace(' ', '_')}_single.wav"
            with open(single_output_file, "wb") as f:
                f.write(single_audio_data)
            
            print(f"   ✅ Generated: {len(single_audio_data)} bytes")
            print(f"   💾 Saved to: {single_output_file}")
            
            # เปรียบเทียบขนาดไฟล์
            if len(audio_data) != len(single_audio_data):
                print(f"   📊 Size difference: Multi-language ({len(audio_data)}) vs Single ({len(single_audio_data)}) bytes")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Multi-language TTS testing completed!")
    print(f"📁 Test files saved in: {test_output_dir.absolute()}")

async def test_language_detection():
    """ทดสอบการตรวจจับภาษา"""
    print("\n🔤 Testing Language Detection...")
    
    core = create_core_instance()
    
    # ข้อความทดสอบการตรวจจับภาษา
    detection_tests = [
        "ສະບາຍດີ Hello world",
        "Hello ທ່ານສະບາຍດີບໍ່ world",
        "ວັນທີ 15 ມັງກອນ 2024",
        "สวัสดีครับ Hello world",
        "Hello สบายดีไหมครับ world",
        "123 ຫຼາຍໆ 456",
        "ສະບາຍດີ! Hello world? ຂອບໃຈຫຼາຍໆ.",
        "Hello world ສະບາຍດີ ທ່ານສະບາຍດີບໍ່ How are you? ຂ້ອຍສະບາຍດີ Thank you very much"
    ]
    
    for i, text in enumerate(detection_tests):
        print(f"\n🔍 Detection Test {i+1}: '{text}'")
        segments = core.detect_language_segments(text)
        print(f"   Result: {len(segments)} segments")
        for j, (segment, lang) in enumerate(segments):
            print(f"   {j+1}. '{segment}' -> {lang}")

async def test_voice_selection():
    """ทดสอบการเลือกเสียงตามภาษา"""
    print("\n🎤 Testing Voice Selection...")
    
    core = create_core_instance()
    
    # ทดสอบการเลือกเสียง
    languages = ['english', 'lao', 'thai', 'chinese', 'japanese', 'numbers', 'punctuation', 'unknown']
    base_voice = "lo-LA-KeomanyNeural"
    
    for lang in languages:
        selected_voice = core.get_voice_for_language(lang, base_voice)
        print(f"   {lang} -> {selected_voice}")

async def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Starting Multi-Language TTS Tests...")
    
    # ทดสอบการตรวจจับภาษา
    await test_language_detection()
    
    # ทดสอบการเลือกเสียง
    await test_voice_selection()
    
    # ทดสอบ TTS หลายภาษา
    await test_multi_language_tts()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 