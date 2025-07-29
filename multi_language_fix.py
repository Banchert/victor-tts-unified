#!/usr/bin/env python3
"""
Multi-Language Fix for TTS System
แก้ไขระบบ multi-language detection ให้สามารถอ่านภาษาอังกฤษในข้อความภาษาลาวได้
"""

import re
import asyncio
import logging
from typing import List, Tuple, Dict, Any
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiLanguageDetector:
    """ระบบตรวจจับและแยกข้อความตามภาษา"""
    
    def __init__(self):
        # รูปแบบการตรวจจับภาษาแบบปรับปรุง
        self.language_patterns = {
            'lao': {
                'pattern': r'[\u0E80-\u0EFF]+(?:\s+[\u0E80-\u0EFF]+)*',
                'name': 'Lao',
                'voice': 'lo-LA-KeomanyNeural'
            },
            'thai': {
                'pattern': r'[\u0E00-\u0E7F]+(?:\s+[\u0E00-\u0E7F]+)*',
                'name': 'Thai', 
                'voice': 'th-TH-PremwadeeNeural'
            },
            'english': {
                'pattern': r'[a-zA-Z]+(?:\s+[a-zA-Z]+)*',
                'name': 'English',
                'voice': 'en-US-AriaNeural'
            },
            'chinese': {
                'pattern': r'[\u4E00-\u9FFF]+(?:\s+[\u4E00-\u9FFF]+)*',
                'name': 'Chinese',
                'voice': 'zh-CN-XiaoxiaoNeural'
            },
            'japanese': {
                'pattern': r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+(?:\s+[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)*',
                'name': 'Japanese',
                'voice': 'ja-JP-NanamiNeural'
            },
            'numbers': {
                'pattern': r'\d+(?:\.\d+)?',
                'name': 'Numbers',
                'voice': None  # ใช้เสียงของข้อความรอบข้าง
            },
            'punctuation': {
                'pattern': r'[^\w\s\u0E00-\u0E7F\u0E80-\u0EFF\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF]',
                'name': 'Punctuation',
                'voice': None  # ใช้เสียงของข้อความรอบข้าง
            }
        }
    
    def detect_language_segments(self, text: str) -> List[Tuple[str, str, str]]:
        """
        ตรวจจับและแยกข้อความตามภาษาแบบปรับปรุง
        
        Args:
            text: ข้อความที่ต้องการแยก
            
        Returns:
            List[Tuple[str, str, str]]: รายการ (ข้อความ, ภาษา, เสียง)
        """
        if not text.strip():
            return []
        
        segments = []
        
        # สร้าง regex pattern รวม
        all_patterns = []
        for lang_code, lang_info in self.language_patterns.items():
            pattern = f'(?P<{lang_code}>{lang_info["pattern"]})'
            all_patterns.append(pattern)
        
        combined_pattern = '|'.join(all_patterns)
        
        # หา matches ทั้งหมด
        matches = list(re.finditer(combined_pattern, text, re.UNICODE))
        
        if not matches:
            # ถ้าไม่เจอรูปแบบใดๆ ให้ถือว่าเป็นภาษาเริ่มต้น
            return [(text, 'unknown', 'lo-LA-KeomanyNeural')]
        
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
                    segments.append((gap_text, surrounding_lang, self._get_voice_for_language(surrounding_lang)))
            
            # เพิ่มข้อความที่ตรงกับรูปแบบ
            for lang_code, lang_info in self.language_patterns.items():
                if match.group(lang_code):
                    segments.append((match.group(lang_code), lang_info['name'], lang_info['voice']))
                    break
            
            current_pos = match.end()
        
        # เพิ่มข้อความที่เหลือ
        if current_pos < len(text):
            remaining_text = text[current_pos:]
            if remaining_text.strip():
                surrounding_lang = self._determine_surrounding_language(matches, current_pos)
                segments.append((remaining_text, surrounding_lang, self._get_voice_for_language(surrounding_lang)))
        
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
            for lang_code, lang_info in self.language_patterns.items():
                if closest_match.group(lang_code):
                    return lang_info['name']
        
        return 'Lao'  # ค่าเริ่มต้น
    
    def _get_voice_for_language(self, language: str) -> str:
        """เลือกเสียงที่เหมาะสมสำหรับแต่ละภาษา"""
        voice_mapping = {
            'Lao': 'lo-LA-KeomanyNeural',
            'Thai': 'th-TH-PremwadeeNeural',
            'English': 'en-US-AriaNeural',
            'Chinese': 'zh-CN-XiaoxiaoNeural',
            'Japanese': 'ja-JP-NanamiNeural',
            'Numbers': 'lo-LA-KeomanyNeural',  # ใช้เสียงลาวเป็นค่าเริ่มต้น
            'Punctuation': 'lo-LA-KeomanyNeural',  # ใช้เสียงลาวเป็นค่าเริ่มต้น
            'unknown': 'lo-LA-KeomanyNeural'
        }
        
        return voice_mapping.get(language, 'lo-LA-KeomanyNeural')
    
    def _merge_adjacent_segments(self, segments: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """รวมส่วนที่ติดกันและมีภาษาเดียวกัน"""
        if not segments:
            return []
        
        merged = []
        current_text = segments[0][0]
        current_lang = segments[0][1]
        current_voice = segments[0][2]
        
        for text, lang, voice in segments[1:]:
            # รวมถ้าภาษาเดียวกัน
            if lang == current_lang and voice == current_voice:
                current_text += text
            else:
                # บันทึกส่วนปัจจุบัน
                merged.append((current_text, current_lang, current_voice))
                # เริ่มส่วนใหม่
                current_text = text
                current_lang = lang
                current_voice = voice
        
        # บันทึกส่วนสุดท้าย
        merged.append((current_text, current_lang, current_voice))
        
        return merged

def create_enhanced_tts_core():
    """สร้าง TTS Core ที่ปรับปรุงแล้ว"""
    
    # อ่านไฟล์ tts_rvc_core.py
    core_file = Path("tts_rvc_core.py")
    if not core_file.exists():
        logger.error("ไม่พบไฟล์ tts_rvc_core.py")
        return False
    
    # อ่านเนื้อหา
    with open(core_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # แทนที่ฟังก์ชัน detect_language_segments
    old_detect_function = '''    def detect_language_segments(self, text: str) -> List[Tuple[str, str]]:
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
        
        # แยกข้อความเป็นส่วนๆ
        current_pos = 0
        
        for match in matches:
            # เพิ่มข้อความที่ไม่ตรงกับรูปแบบใดๆ (ช่องว่าง, ฯลฯ)
            if match.start() > current_pos:
                gap_text = text[current_pos:match.start()]
                if gap_text.strip():
                    segments.append((gap_text, 'unknown'))
            
            # เพิ่มข้อความที่ตรงกับรูปแบบ
            for i, (lang, pattern) in enumerate(patterns.items()):
                if match.group(i + 1):
                    segments.append((match.group(i + 1), lang))
                    break
            
            current_pos = match.end()
        
        # เพิ่มข้อความที่เหลือ
        if current_pos < len(text):
            remaining_text = text[current_pos:]
            if remaining_text.strip():
                segments.append((remaining_text, 'unknown'))
        
        return segments'''
    
    new_detect_function = '''    def detect_language_segments(self, text: str) -> List[Tuple[str, str, str]]:
        """
        ตรวจจับและแยกข้อความตามภาษาแบบปรับปรุง
        
        Args:
            text: ข้อความที่ต้องการแยก
            
        Returns:
            List[Tuple[str, str, str]]: รายการ (ข้อความ, ภาษา, เสียง)
        """
        if not text.strip():
            return []
        
        segments = []
        
        # รูปแบบการตรวจจับภาษาแบบปรับปรุง
        language_patterns = {
            'lao': {
                'pattern': r'[\u0E80-\u0EFF]+(?:\s+[\u0E80-\u0EFF]+)*',
                'name': 'Lao',
                'voice': 'lo-LA-KeomanyNeural'
            },
            'thai': {
                'pattern': r'[\u0E00-\u0E7F]+(?:\s+[\u0E00-\u0E7F]+)*',
                'name': 'Thai', 
                'voice': 'th-TH-PremwadeeNeural'
            },
            'english': {
                'pattern': r'[a-zA-Z]+(?:\s+[a-zA-Z]+)*',
                'name': 'English',
                'voice': 'en-US-AriaNeural'
            },
            'chinese': {
                'pattern': r'[\u4E00-\u9FFF]+(?:\s+[\u4E00-\u9FFF]+)*',
                'name': 'Chinese',
                'voice': 'zh-CN-XiaoxiaoNeural'
            },
            'japanese': {
                'pattern': r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+(?:\s+[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)*',
                'name': 'Japanese',
                'voice': 'ja-JP-NanamiNeural'
            },
            'numbers': {
                'pattern': r'\d+(?:\.\d+)?',
                'name': 'Numbers',
                'voice': 'lo-LA-KeomanyNeural'
            },
            'punctuation': {
                'pattern': r'[^\w\s\u0E00-\u0E7F\u0E80-\u0EFF\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF]',
                'name': 'Punctuation',
                'voice': 'lo-LA-KeomanyNeural'
            }
        }
        
        # สร้าง regex pattern รวม
        all_patterns = []
        for lang_code, lang_info in language_patterns.items():
            pattern = f'(?P<{lang_code}>{lang_info["pattern"]})'
            all_patterns.append(pattern)
        
        combined_pattern = '|'.join(all_patterns)
        
        # หา matches ทั้งหมด
        matches = list(re.finditer(combined_pattern, text, re.UNICODE))
        
        if not matches:
            # ถ้าไม่เจอรูปแบบใดๆ ให้ถือว่าเป็นภาษาเริ่มต้น
            return [(text, 'Lao', 'lo-LA-KeomanyNeural')]
        
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
                    segments.append((gap_text, surrounding_lang, self._get_voice_for_language(surrounding_lang)))
            
            # เพิ่มข้อความที่ตรงกับรูปแบบ
            for lang_code, lang_info in language_patterns.items():
                if match.group(lang_code):
                    segments.append((match.group(lang_code), lang_info['name'], lang_info['voice']))
                    break
            
            current_pos = match.end()
        
        # เพิ่มข้อความที่เหลือ
        if current_pos < len(text):
            remaining_text = text[current_pos:]
            if remaining_text.strip():
                surrounding_lang = self._determine_surrounding_language(matches, current_pos)
                segments.append((remaining_text, surrounding_lang, self._get_voice_for_language(surrounding_lang)))
        
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
            language_patterns = {
                'lao': 'Lao',
                'thai': 'Thai',
                'english': 'English',
                'chinese': 'Chinese',
                'japanese': 'Japanese',
                'numbers': 'Numbers',
                'punctuation': 'Punctuation'
            }
            
            for lang_code, lang_name in language_patterns.items():
                if closest_match.group(lang_code):
                    return lang_name
        
        return 'Lao'  # ค่าเริ่มต้น
    
    def _get_voice_for_language(self, language: str) -> str:
        """เลือกเสียงที่เหมาะสมสำหรับแต่ละภาษา"""
        voice_mapping = {
            'Lao': 'lo-LA-KeomanyNeural',
            'Thai': 'th-TH-PremwadeeNeural',
            'English': 'en-US-AriaNeural',
            'Chinese': 'zh-CN-XiaoxiaoNeural',
            'Japanese': 'ja-JP-NanamiNeural',
            'Numbers': 'lo-LA-KeomanyNeural',
            'Punctuation': 'lo-LA-KeomanyNeural',
            'unknown': 'lo-LA-KeomanyNeural'
        }
        
        return voice_mapping.get(language, 'lo-LA-KeomanyNeural')
    
    def _merge_adjacent_segments(self, segments: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """รวมส่วนที่ติดกันและมีภาษาเดียวกัน"""
        if not segments:
            return []
        
        merged = []
        current_text = segments[0][0]
        current_lang = segments[0][1]
        current_voice = segments[0][2]
        
        for text, lang, voice in segments[1:]:
            # รวมถ้าภาษาเดียวกัน
            if lang == current_lang and voice == current_voice:
                current_text += text
            else:
                # บันทึกส่วนปัจจุบัน
                merged.append((current_text, current_lang, current_voice))
                # เริ่มส่วนใหม่
                current_text = text
                current_lang = lang
                current_voice = voice
        
        # บันทึกส่วนสุดท้าย
        merged.append((current_text, current_lang, current_voice))
        
        return merged'''
    
    # แทนที่ฟังก์ชัน
    if old_detect_function in content:
        content = content.replace(old_detect_function, new_detect_function)
        
        # บันทึกไฟล์ใหม่
        backup_file = Path("tts_rvc_core_backup.py")
        if not backup_file.exists():
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content.replace(new_detect_function, old_detect_function))
            logger.info(f"✅ สร้างไฟล์ backup: {backup_file}")
        
        with open(core_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ แก้ไขไฟล์ tts_rvc_core.py สำเร็จ")
        return True
    else:
        logger.error("❌ ไม่พบฟังก์ชัน detect_language_segments ในไฟล์")
        return False

def update_generate_tts_function():
    """อัปเดตฟังก์ชัน generate_tts ให้รองรับ multi-language แบบใหม่"""
    
    core_file = Path("tts_rvc_core.py")
    if not core_file.exists():
        logger.error("ไม่พบไฟล์ tts_rvc_core.py")
        return False
    
    with open(core_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # แทนที่ส่วนของ multi-language processing ใน generate_tts
    old_multi_lang_section = '''        if enable_multi_language:
            # ตรวจจับและแยกข้อความตามภาษา
            segments = self.detect_language_segments(text)
            
            if len(segments) == 1:
                # ถ้ามีภาษาเดียว ให้ใช้เสียงเดียว
                return await self._generate_single_tts(text, voice, speed, pitch)
            
            # สร้างเสียงสำหรับแต่ละส่วน
            audio_segments = []
            for segment_text, segment_language in segments:
                if not segment_text.strip():
                    continue
                
                # เลือกเสียงที่เหมาะสม
                segment_voice = self.get_voice_for_language(segment_language, voice)
                
                # สร้างเสียง
                segment_audio = await self._generate_single_tts(
                    segment_text, segment_voice, speed, pitch
                )
                audio_segments.append(segment_audio)
            
            # รวมเสียงทั้งหมด
            if audio_segments:
                return self._combine_audio_segments(audio_segments)
            else:
                raise Exception("ไม่สามารถสร้างเสียงได้")'''
    
    new_multi_lang_section = '''        if enable_multi_language:
            # ตรวจจับและแยกข้อความตามภาษาแบบปรับปรุง
            segments = self.detect_language_segments(text)
            
            if len(segments) == 1:
                # ถ้ามีภาษาเดียว ให้ใช้เสียงเดียว
                return await self._generate_single_tts(text, voice, speed, pitch)
            
            # สร้างเสียงสำหรับแต่ละส่วน
            audio_segments = []
            for segment_text, segment_language, segment_voice in segments:
                if not segment_text.strip():
                    continue
                
                # สร้างเสียงด้วยเสียงที่เหมาะสม
                segment_audio = await self._generate_single_tts(
                    segment_text, segment_voice, speed, pitch
                )
                audio_segments.append(segment_audio)
            
            # รวมเสียงทั้งหมด
            if audio_segments:
                return self._combine_audio_segments(audio_segments)
            else:
                raise Exception("ไม่สามารถสร้างเสียงได้")'''
    
    # แทนที่ส่วน
    if old_multi_lang_section in content:
        content = content.replace(old_multi_lang_section, new_multi_lang_section)
        
        with open(core_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ อัปเดตฟังก์ชัน generate_tts สำเร็จ")
        return True
    else:
        logger.error("❌ ไม่พบส่วน multi-language processing ใน generate_tts")
        return False

def create_test_script():
    """สร้างสคริปต์ทดสอบ multi-language"""
    
    test_script = '''#!/usr/bin/env python3
"""
Test Multi-Language TTS
ทดสอบระบบ multi-language TTS
"""

import asyncio
import sys
import os

# เพิ่ม path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tts_rvc_core import TTSRVCCore

async def test_multi_language():
    """ทดสอบระบบ multi-language"""
    print("🧪 ทดสอบระบบ Multi-Language TTS...")
    
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
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n📝 ทดสอบที่ {i}: {test_case['description']}")
        print(f"ข้อความ: {test_case['text']}")
        
        try:
            # ทดสอบการตรวจจับภาษา
            segments = core.detect_language_segments(test_case['text'])
            print(f"🔍 ตรวจจับภาษา: {len(segments)} ส่วน")
            for j, (text, lang, voice) in enumerate(segments):
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
            output_file = f"test_multi_lang_{i}.wav"
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            print(f"💾 บันทึกไฟล์: {output_file}")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
    
    print("\\n🎉 ทดสอบเสร็จสิ้น!")

if __name__ == "__main__":
    asyncio.run(test_multi_language())
'''
    
    with open("test_multi_language.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    logger.info("✅ สร้างไฟล์ test_multi_language.py")

def main():
    """ฟังก์ชันหลัก"""
    print("🔧 แก้ไขระบบ Multi-Language Detection...")
    
    # สร้าง enhanced TTS core
    if create_enhanced_tts_core():
        print("✅ แก้ไขฟังก์ชัน detect_language_segments สำเร็จ")
    else:
        print("❌ แก้ไขฟังก์ชัน detect_language_segments ไม่สำเร็จ")
        return
    
    # อัปเดตฟังก์ชัน generate_tts
    if update_generate_tts_function():
        print("✅ อัปเดตฟังก์ชัน generate_tts สำเร็จ")
    else:
        print("❌ อัปเดตฟังก์ชัน generate_tts ไม่สำเร็จ")
        return
    
    # สร้างสคริปต์ทดสอบ
    create_test_script()
    
    print("\n🎉 แก้ไขระบบ Multi-Language สำเร็จ!")
    print("📝 ฟีเจอร์ใหม่:")
    print("  - ตรวจจับภาษาอังกฤษในข้อความลาว")
    print("  - ใช้เสียงที่เหมาะสมสำหรับแต่ละภาษา")
    print("  - รวมส่วนที่ติดกันและมีภาษาเดียวกัน")
    print("  - รองรับการผสมผสานภาษาหลายภาษา")
    
    print("\n🧪 ทดสอบระบบ:")
    print("  python test_multi_language.py")

if __name__ == "__main__":
    main() 