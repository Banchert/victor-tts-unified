#!/usr/bin/env python3
"""
Fix Multi-Language Detection for Lao + English
แก้ไขระบบ multi-language detection ให้สามารถอ่านภาษาอังกฤษในข้อความภาษาลาวได้
"""

import re
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_tts_rvc_core():
    """แก้ไขไฟล์ tts_rvc_core.py เพื่อปรับปรุง multi-language detection"""
    
    core_file = Path("tts_rvc_core.py")
    if not core_file.exists():
        logger.error("ไม่พบไฟล์ tts_rvc_core.py")
        return False
    
    # อ่านเนื้อหา
    with open(core_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # แทนที่ฟังก์ชัน detect_language_segments
    old_function = '''    def detect_language_segments(self, text: str) -> List[Tuple[str, str]]:
        """
        ตรวจจับและแยกข้อความตามภาษา
        
        Args:
            text: ข้อความที่ต้องการแยก
            
        Returns:
            List[Tuple[str, str]]: รายการ (ข้อความ, ภาษา)
        """
        segments = []
        
        # รูปแบบการตรวจจับภาษา
        patterns = {
            'english': r'[a-zA-Z]+(?:\s+[a-zA-Z]+)*',
            'lao': r'[\u0E80-\u0EFF]+(?:\s+[\u0E80-\u0EFF]+)*',
            'thai': r'[\u0E00-\u0E7F]+(?:\s+[\u0E00-\u0E7F]+)*',
            'chinese': r'[\u4E00-\u9FFF]+(?:\s+[\u4E00-\u9FFF]+)*',
            'japanese': r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+(?:\s+[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)*',
            'numbers': r'\d+(?:\.\d+)?',
            'punctuation': r'[^\w\s\u0E00-\u0E7F\u0E80-\u0EFF\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF]'
        }
        
        # รวมรูปแบบทั้งหมด
        all_patterns = '|'.join(f'({pattern})' for pattern in patterns.values())
        
        # หา matches ทั้งหมด
        matches = list(re.finditer(all_patterns, text, re.UNICODE))
        
        if not matches:
            # ถ้าไม่เจอรูปแบบใดๆ ให้ถือว่าเป็นภาษาเริ่มต้น
            return [(text, 'unknown')]
        
        # จัดเรียงตามตำแหน่ง
        matches.sort(key=lambda x: x.start())
        
        current_pos = 0
        for match in matches:
            # เพิ่มข้อความที่ไม่ตรงกับรูปแบบใดๆ
            if match.start() > current_pos:
                unknown_text = text[current_pos:match.start()].strip()
                if unknown_text:
                    segments.append((unknown_text, 'unknown'))
            
            # ระบุภาษา
            matched_text = match.group()
            language = 'unknown'
            
            for i, (lang, pattern) in enumerate(patterns.items()):
                if re.match(pattern, matched_text, re.UNICODE):
                    language = lang
                    break
            
            segments.append((matched_text, language))
            current_pos = match.end()
        
        # เพิ่มข้อความที่เหลือ
        if current_pos < len(text):
            remaining_text = text[current_pos:].strip()
            if remaining_text:
                segments.append((remaining_text, 'unknown'))
        
        # รวมส่วนที่ติดกันและเป็นภาษาเดียวกัน
        merged_segments = []
        current_text = ""
        current_lang = None
        
        for text_segment, lang in segments:
            if current_lang is None:
                current_lang = lang
                current_text = text_segment
            elif lang == current_lang:
                current_text += " " + text_segment
            else:
                if current_text:
                    merged_segments.append((current_text.strip(), current_lang))
                current_text = text_segment
                current_lang = lang
        
        if current_text:
            merged_segments.append((current_text.strip(), current_lang))
        
        return merged_segments'''
    
    new_function = '''    def detect_language_segments(self, text: str) -> List[Tuple[str, str]]:
        """
        ตรวจจับและแยกข้อความตามภาษาแบบปรับปรุง
        
        Args:
            text: ข้อความที่ต้องการแยก
            
        Returns:
            List[Tuple[str, str]]: รายการ (ข้อความ, ภาษา)
        """
        if not text.strip():
            return []
        
        segments = []
        
        # รูปแบบการตรวจจับภาษาแบบปรับปรุง
        patterns = {
            'english': r'[a-zA-Z]+(?:\\s+[a-zA-Z]+)*',
            'lao': r'[\\u0E80-\\u0EFF]+(?:\\s+[\\u0E80-\\u0EFF]+)*',
            'thai': r'[\\u0E00-\\u0E7F]+(?:\\s+[\\u0E00-\\u0E7F]+)*',
            'chinese': r'[\\u4E00-\\u9FFF]+(?:\\s+[\\u4E00-\\u9FFF]+)*',
            'japanese': r'[\\u3040-\\u309F\\u30A0-\\u30FF\\u4E00-\\u9FFF]+(?:\\s+[\\u3040-\\u309F\\u30A0-\\u30FF\\u4E00-\\u9FFF]+)*',
            'numbers': r'\\d+(?:\\.\\d+)?',
            'punctuation': r'[^\\w\\s\\u0E00-\\u0E7F\\u0E80-\\u0EFF\\u4E00-\\u9FFF\\u3040-\\u309F\\u30A0-\\u30FF]'
        }
        
        # สร้าง regex pattern รวมแบบปรับปรุง
        all_patterns = []
        for lang_code, pattern in patterns.items():
            all_patterns.append(f'(?P<{lang_code}>{pattern})')
        
        combined_pattern = '|'.join(all_patterns)
        
        # หา matches ทั้งหมด
        matches = list(re.finditer(combined_pattern, text, re.UNICODE))
        
        if not matches:
            # ถ้าไม่เจอรูปแบบใดๆ ให้ถือว่าเป็นภาษาลาว
            return [(text, 'lao')]
        
        # จัดเรียงตามตำแหน่ง
        matches.sort(key=lambda x: x.start())
        
        # แยกข้อความเป็นส่วนๆ
        current_pos = 0
        
        for match in matches:
            # เพิ่มข้อความที่ไม่ตรงกับรูปแบบใดๆ (ช่องว่าง, ฯลฯ)
            if match.start() > current_pos:
                gap_text = text[current_pos:match.start()]
                if gap_text.strip():
                    # กำหนดภาษาตามข้อความรอบข้าง
                    surrounding_lang = self._determine_surrounding_language(matches, current_pos)
                    segments.append((gap_text, surrounding_lang))
            
            # เพิ่มข้อความที่ตรงกับรูปแบบ
            for lang_code in patterns.keys():
                if match.group(lang_code):
                    segments.append((match.group(lang_code), lang_code))
                    break
            
            current_pos = match.end()
        
        # เพิ่มข้อความที่เหลือ
        if current_pos < len(text):
            remaining_text = text[current_pos:]
            if remaining_text.strip():
                surrounding_lang = self._determine_surrounding_language(matches, current_pos)
                segments.append((remaining_text, surrounding_lang))
        
        # รวมส่วนที่ติดกันและมีภาษาเดียวกัน
        merged_segments = self._merge_adjacent_segments(segments)
        
        return merged_segments
    
    def _determine_surrounding_language(self, matches: List, position: int) -> str:
        """กำหนดภาษาตามข้อความรอบข้าง"""
        # หา match ที่ใกล้ที่สุด
        closest_match = None
        min_distance = float('inf')
        
        for match in matches:
            distance = min(abs(match.start() - position), abs(match.end() - position))
            if distance < min_distance:
                min_distance = distance
                closest_match = match
        
        if closest_match:
            # กำหนดภาษาตาม match ที่ใกล้ที่สุด
            for lang_code in ['lao', 'thai', 'english', 'chinese', 'japanese', 'numbers', 'punctuation']:
                if closest_match.group(lang_code):
                    return lang_code
        
        return 'lao'  # ค่าเริ่มต้น
    
    def _merge_adjacent_segments(self, segments: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """รวมส่วนที่ติดกันและมีภาษาเดียวกัน"""
        if not segments:
            return []
        
        merged = []
        current_text = segments[0][0]
        current_lang = segments[0][1]
        
        for text, lang in segments[1:]:
            # รวมถ้าภาษาเดียวกัน
            if lang == current_lang:
                current_text += text
            else:
                # บันทึกส่วนปัจจุบัน
                merged.append((current_text, current_lang))
                # เริ่มส่วนใหม่
                current_text = text
                current_lang = lang
        
        # บันทึกส่วนสุดท้าย
        merged.append((current_text, current_lang))
        
        return merged'''
    
    # แทนที่ฟังก์ชัน
    if old_function in content:
        content = content.replace(old_function, new_function)
        
        # บันทึกไฟล์ใหม่
        with open(core_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ แก้ไขฟังก์ชัน detect_language_segments สำเร็จ")
        return True
    else:
        logger.error("❌ ไม่พบฟังก์ชัน detect_language_segments ในไฟล์")
        return False

def update_get_voice_for_language():
    """อัปเดตฟังก์ชัน get_voice_for_language"""
    
    core_file = Path("tts_rvc_core.py")
    if not core_file.exists():
        logger.error("ไม่พบไฟล์ tts_rvc_core.py")
        return False
    
    with open(core_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # แทนที่ฟังก์ชัน get_voice_for_language
    old_voice_function = '''    def get_voice_for_language(self, language: str, base_voice: str) -> str:
        """
        เลือกเสียงที่เหมาะสมสำหรับแต่ละภาษา
        
        Args:
            language: ภาษาที่ต้องการ
            base_voice: เสียงเริ่มต้น
            
        Returns:
            str: เสียงที่เหมาะสม
        """
        # แมปปิ้งภาษาไปยังเสียง
        language_voice_mapping = {
            'english': 'en-US-AriaNeural',
            'lao': 'lo-LA-KeomanyNeural',
            'thai': 'th-TH-PremwadeeNeural',
            'chinese': 'zh-CN-XiaoxiaoNeural',
            'japanese': 'ja-JP-NanamiNeural'
        }
        
        # ถ้าเป็นตัวเลขหรือเครื่องหมายวรรคตอน ให้ใช้เสียงเริ่มต้น
        if language in ['numbers', 'punctuation', 'unknown']:
            return base_voice
        
        return language_voice_mapping.get(language, base_voice)'''
    
    new_voice_function = '''    def get_voice_for_language(self, language: str, base_voice: str) -> str:
        """
        เลือกเสียงที่เหมาะสมสำหรับแต่ละภาษา
        
        Args:
            language: ภาษาที่ต้องการ
            base_voice: เสียงเริ่มต้น
            
        Returns:
            str: เสียงที่เหมาะสม
        """
        # แมปปิ้งภาษาไปยังเสียง
        language_voice_mapping = {
            'english': 'en-US-AriaNeural',
            'lao': 'lo-LA-KeomanyNeural',
            'thai': 'th-TH-PremwadeeNeural',
            'chinese': 'zh-CN-XiaoxiaoNeural',
            'japanese': 'ja-JP-NanamiNeural'
        }
        
        # ถ้าเป็นตัวเลขหรือเครื่องหมายวรรคตอน ให้ใช้เสียงของข้อความรอบข้าง
        if language in ['numbers', 'punctuation']:
            return base_voice
        
        # ถ้าเป็น unknown ให้ใช้เสียงลาวเป็นค่าเริ่มต้น
        if language == 'unknown':
            return 'lo-LA-KeomanyNeural'
        
        return language_voice_mapping.get(language, base_voice)'''
    
    # แทนที่ฟังก์ชัน
    if old_voice_function in content:
        content = content.replace(old_voice_function, new_voice_function)
        
        with open(core_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ อัปเดตฟังก์ชัน get_voice_for_language สำเร็จ")
        return True
    else:
        logger.error("❌ ไม่พบฟังก์ชัน get_voice_for_language ในไฟล์")
        return False

def create_test_script():
    """สร้างสคริปต์ทดสอบ multi-language"""
    
    test_script = '''#!/usr/bin/env python3
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
    print("🧪 ทดสอบระบบ Multi-Language TTS (ลาว + อังกฤษ)...")
    
    # สร้าง core instance
    core = TTSRVCCore()
    
    # ทดสอบข้อความที่มีหลายภาษา
    test_cases = [
        {
            "text": "ສະບາຍດີ Hello ທຸກຄົນ! How are you? ຂ້ອຍດີ",
            "description": "ลาว + อังกฤษ + ลาว"
        },
        {
            "text": "Hello ສະບາຍດີ ທຸກຄົນ! How are you today?",
            "description": "อังกฤษ + ลาว + อังกฤษ"
        },
        {
            "text": "ສະບາຍດີ ທຸກຄົນ! ຂ້ອຍຊື່ວ່າ John ແລະ ຂ້ອຍມາຈາກ America",
            "description": "ลาว + อังกฤษ + ลาว"
        },
        {
            "text": "Welcome to ລາວ! ປະເທດທີ່ສວຍງາມ",
            "description": "อังกฤษ + ลาว"
        },
        {
            "text": "ສະບາຍດີ! My name is ຂ້ອຍ ແລະ I love ລາວ language",
            "description": "ลาว + อังกฤษ + ลาว + อังกฤษ + ลาว"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n📝 ทดสอบที่ {i}: {test_case['description']}")
        print(f"ข้อความ: {test_case['text']}")
        
        try:
            # ทดสอบการตรวจจับภาษา
            segments = core.detect_language_segments(test_case['text'])
            print(f"🔍 ตรวจจับภาษา: {len(segments)} ส่วน")
            for j, (text, lang) in enumerate(segments):
                voice = core.get_voice_for_language(lang, 'lo-LA-KeomanyNeural')
                print(f"  ส่วน {j+1}: '{text}' -> {lang} ({voice})")
            
            # ทดสอบการสร้างเสียง
            print("🎵 สร้างเสียง...")
            audio_data = await core.generate_tts(
                test_case['text'], 
                'lo-LA-KeomanyNeural', 
                enable_multi_language=True
            )
            print(f"✅ สร้างเสียงสำเร็จ: {len(audio_data)} bytes")
            
            # บันทึกไฟล์เสียง
            output_file = f"test_lao_english_{i}.wav"
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            print(f"💾 บันทึกไฟล์: {output_file}")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
    
    print("\\n🎉 ทดสอบเสร็จสิ้น!")

if __name__ == "__main__":
    asyncio.run(test_multi_language())
'''
    
    with open("test_lao_english.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    logger.info("✅ สร้างไฟล์ test_lao_english.py")

def create_web_interface_update():
    """สร้างไฟล์อัปเดต web interface"""
    
    update_script = '''#!/usr/bin/env python3
"""
Update Web Interface for Multi-Language Support
อัปเดต web interface เพื่อรองรับ multi-language
"""

import re
from pathlib import Path

def update_web_interface():
    """อัปเดต web interface"""
    
    # อัปเดต web_interface_complete.py
    web_file = Path("web_interface_complete.py")
    if not web_file.exists():
        print("❌ ไม่พบไฟล์ web_interface_complete.py")
        return False
    
    with open(web_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # เพิ่ม checkbox สำหรับ multi-language
    old_checkbox_section = '''                <details>
                    <summary>🎭 เอฟเฟกต์ทำมะชาดพิเศษ</summary>
                    <div class="effects-grid">
                        <div class="checkbox-container">
                            <input type="checkbox" id="demon-mode-check" name="demon_mode">
                            <label for="demon-mode-check">👹 โหมดปีศาจ</label>
                        </div>
                        <div class="checkbox-container">
                            <input type="checkbox" id="robot-mode-check" name="robot_mode">
                            <label for="robot-mode-check">🤖 โหมดหุ่นยนต์</label>
                        </div>
                         <!-- Add more effects here if needed -->
                    </div>
                </details>'''
    
    new_checkbox_section = '''                <details>
                    <summary>🎭 เอฟเฟกต์ทำมะชาดพิเศษ</summary>
                    <div class="effects-grid">
                        <div class="checkbox-container">
                            <input type="checkbox" id="demon-mode-check" name="demon_mode">
                            <label for="demon-mode-check">👹 โหมดปีศาจ</label>
                        </div>
                        <div class="checkbox-container">
                            <input type="checkbox" id="robot-mode-check" name="robot_mode">
                            <label for="robot-mode-check">🤖 โหมดหุ่นยนต์</label>
                        </div>
                        <div class="checkbox-container">
                            <input type="checkbox" id="multi-language-check" name="multi_language" checked>
                            <label for="multi-language-check">🌍 Multi-Language (ลาว+อังกฤษ)</label>
                        </div>
                         <!-- Add more effects here if needed -->
                    </div>
                </details>'''
    
    # แทนที่ส่วน checkbox
    if old_checkbox_section in content:
        content = content.replace(old_checkbox_section, new_checkbox_section)
        
        # อัปเดต JavaScript เพื่อรองรับ multi-language
        old_js_section = '''                // Collect Machad effects
                const machadEffects = {
                    demon_mode: demonModeCheck.checked,
                    robot_mode: robotModeCheck.checked,
                };'''
        
        new_js_section = '''                // Collect Machad effects
                const machadEffects = {
                    demon_mode: demonModeCheck.checked,
                    robot_mode: robotModeCheck.checked,
                };
                
                // Get multi-language setting
                const multiLanguageCheck = document.getElementById('multi-language-check');
                const enableMultiLanguage = multiLanguageCheck ? multiLanguageCheck.checked : true;'''
        
        if old_js_section in content:
            content = content.replace(old_js_section, new_js_section)
            
            # อัปเดต payload
            old_payload = '''                const payload = {
                    text: text,
                    tts_voice: selectedVoice,
                    tts_speed: selectedSpeed,
                    enable_rvc: !!rvcModelName,
                    rvc_model: rvcModelName,
                    rvc_transpose: 0,
                    rvc_index_ratio: 0.7,
                    rvc_f0_method: "rmvpe"
                };'''
            
            new_payload = '''                const payload = {
                    text: text,
                    tts_voice: selectedVoice,
                    tts_speed: selectedSpeed,
                    enable_rvc: !!rvcModelName,
                    rvc_model: rvcModelName,
                    rvc_transpose: 0,
                    rvc_index_ratio: 0.7,
                    rvc_f0_method: "rmvpe",
                    enable_multi_language: enableMultiLanguage
                };'''
            
            if old_payload in content:
                content = content.replace(old_payload, new_payload)
        
        with open(web_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ อัปเดต web_interface_complete.py สำเร็จ")
        return True
    else:
        print("❌ ไม่พบส่วน checkbox ในไฟล์")
        return False

if __name__ == "__main__":
    update_web_interface()
'''
    
    with open("update_web_interface.py", 'w', encoding='utf-8') as f:
        f.write(update_script)
    
    logger.info("✅ สร้างไฟล์ update_web_interface.py")

def main():
    """ฟังก์ชันหลัก"""
    print("🔧 แก้ไขระบบ Multi-Language Detection สำหรับลาว + อังกฤษ...")
    
    # แก้ไขฟังก์ชัน detect_language_segments
    if fix_tts_rvc_core():
        print("✅ แก้ไขฟังก์ชัน detect_language_segments สำเร็จ")
    else:
        print("❌ แก้ไขฟังก์ชัน detect_language_segments ไม่สำเร็จ")
        return
    
    # อัปเดตฟังก์ชัน get_voice_for_language
    if update_get_voice_for_language():
        print("✅ อัปเดตฟังก์ชัน get_voice_for_language สำเร็จ")
    else:
        print("❌ อัปเดตฟังก์ชัน get_voice_for_language ไม่สำเร็จ")
        return
    
    # สร้างสคริปต์ทดสอบ
    create_test_script()
    
    # สร้างสคริปต์อัปเดต web interface
    create_web_interface_update()
    
    print("\n🎉 แก้ไขระบบ Multi-Language สำเร็จ!")
    print("📝 ฟีเจอร์ใหม่:")
    print("  - ตรวจจับภาษาอังกฤษในข้อความลาว")
    print("  - ใช้เสียงที่เหมาะสมสำหรับแต่ละภาษา")
    print("  - รวมส่วนที่ติดกันและมีภาษาเดียวกัน")
    print("  - รองรับการผสมผสานภาษาลาว + อังกฤษ")
    
    print("\n🧪 ทดสอบระบบ:")
    print("  python test_lao_english.py")
    
    print("\n🌐 อัปเดต Web Interface:")
    print("  python update_web_interface.py")

if __name__ == "__main__":
    main() 