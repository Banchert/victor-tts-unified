#!/usr/bin/env python3
"""
🧪 ทดสอบการสร้างเสียง TTS หลายภาษา
ทดสอบระบบ TTS กับข้อความภาษาไทย ภาษาอังกฤษ และภาษาญี่ปุ่น
"""

import asyncio
import sys
from pathlib import Path
import base64

# เพิ่ม path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from tts_rvc_core import TTSRVCCore, create_core_instance
    print("✅ โหลด TTS-RVC Core สำเร็จ")
except ImportError as e:
    print(f"❌ ไม่สามารถโหลด TTS-RVC Core: {e}")
    sys.exit(1)

async def test_tts_languages():
    """ทดสอบการสร้างเสียง TTS หลายภาษา"""
    
    print("🚀 เริ่มทดสอบการสร้างเสียง TTS หลายภาษา...")
    
    try:
        # สร้าง core instance
        core = create_core_instance()
        print("✅ สร้าง Core Instance สำเร็จ")
        
        # ทดสอบข้อความหลายภาษา
        test_cases = [
            {
                "name": "ภาษาไทย",
                "text": "สวัสดีครับ ยินดีต้อนรับสู่ระบบ VICTOR-TTS สำหรับการแปลงข้อความเป็นเสียง",
                "voice": "th-TH-PremwadeeNeural"
            },
            {
                "name": "ภาษาอังกฤษ",
                "text": "Hello, welcome to our VICTOR-TTS system for text-to-speech conversion",
                "voice": "en-US-JennyNeural"
            },
            {
                "name": "ภาษาญี่ปุ่น",
                "text": "こんにちは、VICTOR-TTSシステムへようこそ。テキストから音声への変換システムです。",
                "voice": "ja-JP-NanamiNeural"
            },
            {
                "name": "ข้อความผสมภาษา",
                "text": "สวัสดีครับ Hello こんにちは นี่คือการทดสอบระบบ TTS ที่รองรับหลายภาษา",
                "voice": "th-TH-PremwadeeNeural"
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 ทดสอบที่ {i}: {test_case['name']}")
            print(f"ข้อความ: {test_case['text']}")
            print(f"เสียง: {test_case['voice']}")
            
            try:
                # สร้างเสียง TTS
                audio_data = await core.generate_tts(
                    text=test_case['text'],
                    voice=test_case['voice'],
                    speed=1.0,
                    pitch="+0Hz",
                    enable_multi_language=True
                )
                
                # บันทึกไฟล์เสียง
                output_dir = Path("test_output")
                output_dir.mkdir(exist_ok=True)
                
                output_file = output_dir / f"test_{i}_{test_case['name'].replace(' ', '_')}.wav"
                with open(output_file, 'wb') as f:
                    f.write(audio_data)
                
                # แสดงข้อมูล
                audio_size = len(audio_data)
                print(f"✅ สร้างเสียงสำเร็จ")
                print(f"📁 บันทึกที่: {output_file}")
                print(f"📊 ขนาดไฟล์: {audio_size / 1024:.1f} KB")
                
                # ทดสอบการตรวจจับภาษา (ถ้าเปิดใช้งาน multi-language)
                if test_case['name'] == "ข้อความผสมภาษา":
                    try:
                        language_segments = core.detect_language_segments(test_case['text'])
                        print(f"🌐 ตรวจจับภาษา: {len(language_segments)} ส่วน")
                        for j, (segment, lang) in enumerate(language_segments):
                            print(f"  ส่วน {j+1}: {segment[:30]}... ({lang})")
                    except Exception as e:
                        print(f"⚠️ ไม่สามารถตรวจจับภาษาได้: {e}")
                
                results.append({
                    "test": test_case['name'],
                    "success": True,
                    "file": str(output_file),
                    "size": audio_size
                })
                
            except Exception as e:
                print(f"❌ ล้มเหลว: {e}")
                results.append({
                    "test": test_case['name'],
                    "success": False,
                    "error": str(e)
                })
        
        # สรุปผลการทดสอบ
        print(f"\n📊 สรุปผลการทดสอบ:")
        print(f"ทั้งหมด: {len(test_cases)} รายการ")
        print(f"สำเร็จ: {sum(1 for r in results if r['success'])} รายการ")
        print(f"ล้มเหลว: {sum(1 for r in results if not r['success'])} รายการ")
        
        for result in results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}")
            if result['success']:
                print(f"   📁 {result['file']}")
                print(f"   📊 {result['size'] / 1024:.1f} KB")
            else:
                print(f"   ❌ {result['error']}")
        
        # ทดสอบการสร้างเสียงแบบ batch
        print(f"\n🔄 ทดสอบการสร้างเสียงแบบ batch...")
        try:
            batch_texts = [
                "สวัสดีครับ",
                "Hello there",
                "こんにちは",
                "ขอบคุณครับ Thank you ありがとうございます"
            ]
            
            batch_results = []
            for text in batch_texts:
                audio_data = await core.generate_tts(
                    text=text,
                    voice="th-TH-PremwadeeNeural",
                    speed=1.0,
                    enable_multi_language=True
                )
                
                output_file = output_dir / f"batch_{len(batch_results)+1}.wav"
                with open(output_file, 'wb') as f:
                    f.write(audio_data)
                
                batch_results.append({
                    "text": text,
                    "file": str(output_file),
                    "size": len(audio_data)
                })
            
            print(f"✅ สร้างเสียงแบบ batch สำเร็จ {len(batch_results)} ไฟล์")
            for result in batch_results:
                print(f"   📝 {result['text'][:30]}...")
                print(f"   📁 {result['file']}")
                print(f"   📊 {result['size'] / 1024:.1f} KB")
                
        except Exception as e:
            print(f"❌ การสร้างเสียงแบบ batch ล้มเหลว: {e}")
        
        print(f"\n🎉 การทดสอบเสร็จสิ้น!")
        print(f"📁 ไฟล์เสียงทั้งหมดอยู่ในโฟลเดอร์: {output_dir}")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทดสอบ: {e}")
        import traceback
        traceback.print_exc()

def test_web_interface():
    """ทดสอบ Web Interface"""
    print("\n🌐 ทดสอบ Web Interface...")
    
    try:
        from web_interface import WebInterface
        
        # สร้าง web interface
        web_interface = WebInterface(port=7000)
        print("✅ สร้าง Web Interface สำเร็จ")
        
        # ทดสอบการสร้างหน้า HTML
        html_content = web_interface.generate_html_page()
        if html_content and len(html_content) > 1000:
            print("✅ สร้างหน้า HTML สำเร็จ")
            print(f"📊 ขนาด HTML: {len(html_content)} ตัวอักษร")
        else:
            print("❌ การสร้างหน้า HTML ล้มเหลว")
        
        # ทดสอบการสร้าง server
        server = web_interface.create_simple_server()
        print("✅ สร้าง HTTP Server สำเร็จ")
        
        print("🌐 Web Interface พร้อมใช้งานที่ http://localhost:7000")
        
    except Exception as e:
        print(f"❌ การทดสอบ Web Interface ล้มเหลว: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 VICTOR-TTS Language Test")
    print("=" * 50)
    
    # ทดสอบ TTS
    asyncio.run(test_tts_languages())
    
    # ทดสอบ Web Interface
    test_web_interface()
    
    print("\n" + "=" * 50)
    print("✅ การทดสอบเสร็จสิ้น!") 