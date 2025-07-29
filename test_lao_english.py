#!/usr/bin/env python3
"""
Test Multi-Language TTS for Lao + English
ทดสอบระบบ multi-language TTS สำหรับภาษาลาว + อังกฤษ
"""

import asyncio
import sys
import os

# เพิ่ม path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tts_rvc_core import TTSRVCCore

async def test_multi_language():
    """ทดสอบระบบ multi-language"""
    print("Testing Multi-Language TTS (Lao + English)...")
    
    # สร้าง core instance
    core = TTSRVCCore()
    
    # ทดสอบข้อความที่มีหลายภาษา
    test_cases = [
        {
            "text": "ສະບາຍດີ Hello ທຸກຄົນ! How are you? ຂ້ອຍດີ",
            "description": "Lao + English + Lao"
        },
        {
            "text": "Hello ສະບາຍດີ ທຸກຄົນ! How are you today?",
            "description": "English + Lao + English"
        },
        {
            "text": "ສະບາຍດີ ທຸກຄົນ! ຂ້ອຍຊື່ວ່າ John ແລະ ຂ້ອຍມາຈາກ America",
            "description": "Lao + English + Lao"
        },
        {
            "text": "Welcome to ລາວ! ປະເທດທີ່ສວຍງາມ",
            "description": "English + Lao"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Text: {test_case['text']}")
        
        try:
            # ทดสอบการตรวจจับภาษา
            segments = core.detect_language_segments(test_case['text'])
            print(f"Language detection: {len(segments)} segments")
            for j, (text, lang) in enumerate(segments):
                voice = core.get_voice_for_language(lang, 'lo-LA-KeomanyNeural')
                print(f"  Segment {j+1}: '{text}' -> {lang} ({voice})")
            
            # ทดสอบการสร้างเสียง
            print("Generating audio...")
            audio_data = await core.generate_tts(
                test_case['text'], 
                'lo-LA-KeomanyNeural', 
                enable_multi_language=True
            )
            print(f"Audio generated: {len(audio_data)} bytes")
            
            # บันทึกไฟล์เสียง
            output_file = f"test_lao_english_{i}.wav"
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            print(f"Saved: {output_file}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_multi_language()) 