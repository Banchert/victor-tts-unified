#!/usr/bin/env python3
"""
🎯 TTS-RVC Core System - ระบบหลักรวม TTS และ RVC
รวมฟังก์ชันหลักทั้งหมดในไฟล์เดียว
"""
import os
import sys
import asyncio
import re
from pathlib import Path
import logging
from typing import Optional, Dict, Any, List, Union, Tuple
from model_utils import safe_model_processing, normalize_model_name

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTS_RVC_CORE")

class TTSRVCCore:
    """ระบบหลักสำหรับ TTS และ RVC"""
    
    def __init__(self, models_dir: str = "logs", temp_dir: str = "storage/temp", 
                 device: str = None, use_gpu: bool = True, gpu_id: int = 0,
                 performance_config: Dict[str, Any] = None):
        """
        เริ่มต้นระบบ TTS-RVC
        
        Args:
            models_dir: โฟลเดอร์ที่เก็บโมเดล RVC
            temp_dir: โฟลเดอร์สำหรับไฟล์ชั่วคราว
            device: อุปกรณ์ที่ใช้ประมวลผล (cpu, cuda:0, cuda:1, ...) - ถ้าเป็น None จะใช้ค่าตามการกำหนด use_gpu และ gpu_id
            use_gpu: เปิดใช้งาน GPU หรือไม่
            gpu_id: ID ของ GPU ที่ใช้ (0, 1, 2, ...)
            performance_config: การตั้งค่าประสิทธิภาพ
        """
        self.models_dir = Path(models_dir)
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # โหลดการตั้งค่าประสิทธิภาพ
        self.performance_config = self._load_performance_config(performance_config)
        
        # ตั้งค่า GPU
        self.setup_device(device, use_gpu, gpu_id)
        
        # สถานะของระบบ
        self.tts_available = False
        self.rvc_available = False
        self.rvc_instance = None
        
        # โหลดระบบ
        self._initialize_systems()
        
        logger.info(f"TTS-RVC Core initialized - TTS: {self.tts_available}, RVC: {self.rvc_available}, Device: {self.device}")
        logger.info(f"Performance config: TTS concurrent={self.performance_config.get('tts_max_concurrent', 1)}, RVC batch={self.performance_config.get('rvc_batch_size', 1)}")
    
    def _load_performance_config(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """โหลดการตั้งค่าประสิทธิภาพ"""
        if config:
            return config
        
        # ลองโหลดจากไฟล์
        config_file = Path("config/performance_config.json")
        if config_file.exists():
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load performance config: {e}")
        
        # ใช้ค่าเริ่มต้น
        return {
            "tts_batch_size": 1,
            "tts_chunk_size": 5000,
            "tts_max_concurrent": 1,
            "rvc_batch_size": 1,
            "rvc_use_half_precision": True,
            "rvc_cache_models": True,
            "audio_sample_rate": 44100,
            "audio_chunk_duration": 10,
            "audio_use_soxr": True,
            "use_multiprocessing": True,
            "max_workers": 1,
            "memory_limit_gb": 2,
            "gpu_memory_fraction": 0.8,
            "gpu_allow_growth": True,
            "gpu_mixed_precision": True
        }
    
    def setup_device(self, device: str = None, use_gpu: bool = True, gpu_id: int = 0):
        """
        ตั้งค่าอุปกรณ์ที่ใช้ประมวลผล
        
        Args:
            device: อุปกรณ์ที่ใช้ประมวลผล (cpu, cuda:0, cuda:1, ...) - ถ้าเป็น None จะใช้ค่าตามการกำหนด use_gpu และ gpu_id
            use_gpu: เปิดใช้งาน GPU หรือไม่
            gpu_id: ID ของ GPU ที่ใช้ (0, 1, 2, ...)
        """
        # ตรวจสอบ GPU
        self.gpu_available = False
        self.gpu_info = None
        
        try:
            import torch
            self.gpu_available = torch.cuda.is_available()
            
            if self.gpu_available:
                gpu_count = torch.cuda.device_count()
                
                # เก็บข้อมูล GPU
                self.gpu_info = []
                for i in range(gpu_count):
                    name = torch.cuda.get_device_name(i)
                    memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                    self.gpu_info.append({
                        "id": i,
                        "name": name,
                        "memory": memory
                    })
                logger.info(f"Found {gpu_count} GPUs: {', '.join(g['name'] for g in self.gpu_info)}")
        except ImportError:
            logger.warning("PyTorch not available, using CPU only")
        except Exception as e:
            logger.warning(f"Error detecting GPU: {e}")
        
        # กำหนด device
        if device is not None:
            # ใช้ device ที่ระบุโดยตรง
            self.device = device
        elif not use_gpu or not self.gpu_available:
            # ใช้ CPU
            self.device = "cpu"
        else:
            # ใช้ GPU ตาม ID
            try:
                if gpu_id < len(self.gpu_info):
                    self.device = f"cuda:{gpu_id}"
                else:
                    logger.warning(f"GPU ID {gpu_id} not found, using GPU 0 instead")
                    self.device = "cuda:0"
            except:
                self.device = "cuda:0"
        
        # ตั้งค่าสิ่งแวดล้อม
        if "cuda" in self.device and self.gpu_available:
            gpu_id_num = int(self.device.split(":")[-1])
            os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id_num)
            logger.info(f"Using GPU {gpu_id_num}: {self.get_gpu_name(gpu_id_num)}")
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            self.device = "cpu"
            logger.info("Using CPU")
    
    def get_gpu_name(self, gpu_id: int = 0) -> str:
        """ดึงชื่อของ GPU ตาม ID"""
        if self.gpu_info and gpu_id < len(self.gpu_info):
            return self.gpu_info[gpu_id]["name"]
        return "Unknown"
    
    def _initialize_systems(self):
        """เริ่มต้นระบบ TTS และ RVC"""
        # เริ่มต้น TTS
        try:
            import edge_tts
            self.tts_available = True
            logger.info("✅ Edge TTS system loaded")
        except ImportError:
            logger.warning("⚠️ Edge TTS not available")
        
        # เริ่มต้น RVC
        try:
            from rvc_api import RVCConverter
            self.rvc_instance = RVCConverter(
                device=self.device, 
                models_dir=str(self.models_dir),
                performance_config=self.performance_config
            )
            self.rvc_available = True
            logger.info(f"✅ RVC system loaded on {self.device}")
        except ImportError as e:
            logger.warning(f"⚠️ RVC system not available: {e}")
        except Exception as e:
            logger.warning(f"⚠️ RVC system initialization failed: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """ดึงสถานะระบบ"""
        return {
            "tts_available": self.tts_available,
            "rvc_available": self.rvc_available,
            "device": self.device,
            "gpu_name": self.get_gpu_name(int(self.device.split(':')[-1])) if "cuda" in self.device and self.gpu_available else "CPU",
            "rvc_models_count": len(self.get_available_rvc_models()) if self.rvc_available else 0
        }
    
    async def test_edge_tts_connection(self, voice: str = "th-TH-PremwadeeNeural") -> bool:
        """ทดสอบการเชื่อมต่อ Edge TTS"""
        try:
            import edge_tts
            
            # ทดสอบด้วยข้อความสั้นๆ
            test_text = "สวัสดี"
            communicate = edge_tts.Communicate(text=test_text, voice=voice)
            
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            if audio_data:
                logger.info(f"Edge TTS connection test successful with voice: {voice}")
                return True
            else:
                logger.error(f"Edge TTS connection test failed - no audio received for voice: {voice}")
                return False
                
        except Exception as e:
            logger.error(f"Edge TTS connection test failed: {e}")
            return False
    
    async def get_available_edge_voices(self) -> List[str]:
        """ดึงรายชื่อ voice ที่มีใน Edge TTS"""
        try:
            import edge_tts
            voices = await edge_tts.list_voices()
            return [voice["ShortName"] for voice in voices]
        except Exception as e:
            logger.error(f"Error getting Edge TTS voices: {e}")
            return []
    
    def get_available_rvc_models(self) -> List[str]:
        """ดึงรายชื่อโมเดล RVC ที่มีอยู่"""
        if not self.rvc_available:
            return []
        
        try:
            return self.rvc_instance.get_available_models()
        except Exception as e:
            logger.error(f"Error getting RVC models: {e}")
            return []
    
    async def generate_tts(self, text: str, voice: str, speed: float = 1.0, 
                          pitch: str = "+0Hz", enable_multi_language: bool = False) -> bytes:
        """
        สร้างเสียงจากข้อความด้วย Edge TTS
        
        Args:
            text: ข้อความที่ต้องการแปลง
            voice: เสียงที่ใช้ (เช่น th-TH-PremwadeeNeural)
            speed: ความเร็วในการพูด (0.5-2.0)
            pitch: ระดับเสียง (เช่น +0Hz, +10Hz)
            enable_multi_language: เปิดใช้งานการประมวลผลหลายภาษา
            
        Returns:
            bytes: ข้อมูลเสียงในรูปแบบ bytes
        """
        if not self.tts_available:
            raise Exception("TTS system not available")
        
        try:
            import edge_tts
            
            # Log ข้อมูลพารามิเตอร์
            logger.info(f"Generating TTS with text='{text[:30]}...', voice='{voice}', speed={speed}, pitch={pitch}, multi_lang={enable_multi_language}")
            
            # ตรวจสอบและทำความสะอาดข้อความ
            if not text or not text.strip():
                raise Exception("Text is empty or contains only whitespace")
            
            # ทำความสะอาดข้อความ - ลบอักขระควบคุมที่ไม่จำเป็น
            cleaned_text = text.strip()
            cleaned_text = ''.join(char for char in cleaned_text if ord(char) >= 32 or char in '\n\r\t')
            
            if not cleaned_text:
                raise Exception("Text is empty after cleaning")
            
            # ตรวจสอบ voice
            if not voice or not voice.strip():
                raise Exception("Voice is not specified")
            
            # ตรวจสอบว่า voice มีอยู่จริงหรือไม่
            try:
                available_voices = await self.get_available_edge_voices()
                if voice not in available_voices:
                    logger.warning(f"Voice '{voice}' not found in available voices. Available voices: {available_voices[:5]}...")
                    # ลองใช้ voice เริ่มต้น
                    fallback_voice = "th-TH-PremwadeeNeural"
                    if fallback_voice in available_voices:
                        logger.info(f"Using fallback voice: {fallback_voice}")
                        voice = fallback_voice
                    else:
                        raise Exception(f"Voice '{voice}' not available and no fallback voice found")
            except Exception as voice_error:
                logger.warning(f"Could not verify voice availability: {voice_error}")
                # ดำเนินการต่อโดยไม่ตรวจสอบ voice
            
            # ถ้าเปิดใช้งานหลายภาษา ให้แยกข้อความตามภาษา
            if enable_multi_language:
                language_segments = self.detect_language_segments(cleaned_text)
                logger.info(f"Detected {len(language_segments)} language segments: {[(seg[:20] + '...' if len(seg) > 20 else seg, lang) for seg, lang in language_segments]}")
                
                if len(language_segments) > 1:
                    # มีหลายภาษา ให้ประมวลผลแยกกัน
                    all_audio_data = []
                    
                    # ใช้การตั้งค่าประสิทธิภาพ
                    max_concurrent = self.performance_config.get("tts_max_concurrent", 1)
                    
                    # กรอง segments ที่ไม่ต้องการ
                    valid_segments = []
                    for segment_text, language in language_segments:
                        if not segment_text.strip():
                            continue
                        
                        # ข้ามเครื่องหมายวรรคตอนเดี่ยวๆ
                        if language == 'punctuation' and len(segment_text.strip()) <= 2:
                            logger.debug(f"Skipping punctuation segment: '{segment_text}'")
                            continue
                        
                        valid_segments.append((segment_text, language))
                    
                    if max_concurrent > 1 and len(valid_segments) > 1:
                        # ใช้ concurrent processing
                        logger.info(f"Processing {len(valid_segments)} segments with max_concurrent={max_concurrent}")
                        
                        semaphore = asyncio.Semaphore(max_concurrent)
                        
                        async def process_segment(segment_text, language):
                            async with semaphore:
                                segment_voice = self.get_voice_for_language(language, voice)
                                logger.info(f"Processing segment '{segment_text[:30]}...' with language '{language}' using voice '{segment_voice}'")
                                
                                try:
                                    segment_audio = await self._generate_single_tts(segment_text, segment_voice, speed, pitch)
                                    if segment_audio and len(segment_audio) > 0:
                                        return segment_audio
                                except Exception as e:
                                    logger.warning(f"Failed to generate audio for segment '{segment_text}': {e}")
                                    return None
                        
                        # รัน segments แบบ concurrent
                        tasks = [process_segment(text, lang) for text, lang in valid_segments]
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        # รวบรวมผลลัพธ์
                        for result in results:
                            if isinstance(result, bytes) and len(result) > 0:
                                all_audio_data.append(result)
                    else:
                        # ใช้ sequential processing
                        for segment_text, language in valid_segments:
                            segment_voice = self.get_voice_for_language(language, voice)
                            logger.info(f"Processing segment '{segment_text[:30]}...' with language '{language}' using voice '{segment_voice}'")
                            
                            try:
                                segment_audio = await self._generate_single_tts(segment_text, segment_voice, speed, pitch)
                                if segment_audio and len(segment_audio) > 0:
                                    all_audio_data.append(segment_audio)
                            except Exception as e:
                                logger.warning(f"Failed to generate audio for segment '{segment_text}': {e}")
                                continue
                    
                    # รวมเสียงทั้งหมด
                    if all_audio_data:
                        combined_audio = self._combine_audio_segments(all_audio_data)
                        logger.info(f"Multi-language TTS generated: {len(combined_audio)} bytes from {len(all_audio_data)} segments")
                        return combined_audio
                    else:
                        raise Exception("No audio was generated from any segments")
                else:
                    # มีภาษาเดียว ใช้วิธีเดิม
                    logger.info("Single language detected, using standard TTS")
                    return await self._generate_single_tts(cleaned_text, voice, speed, pitch)
            else:
                # ไม่เปิดใช้งานหลายภาษา ใช้วิธีเดิม
                return await self._generate_single_tts(cleaned_text, voice, speed, pitch)
            
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise Exception(f"TTS generation failed: {str(e)}")
    
    async def _generate_single_tts(self, text: str, voice: str, speed: float = 1.0, 
                                  pitch: str = "+0Hz") -> bytes:
        """
        สร้างเสียงจากข้อความภาษาเดียว
        
        Args:
            text: ข้อความที่ต้องการแปลง
            voice: เสียงที่ใช้
            speed: ความเร็วในการพูด
            pitch: ระดับเสียง
            
        Returns:
            bytes: ข้อมูลเสียงในรูปแบบ bytes
        """
        import edge_tts
        
        # ปรับ rate สำหรับ speed
        if speed != 1.0:
            rate = f"{speed:+.0%}"
        else:
            rate = "+0%"
        
        logger.info(f"Generating single TTS: '{text[:50]}...' with voice '{voice}'")
        
        # สร้าง Communicate object
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch
        )
        
        # สร้างเสียง
        audio_data = b""
        chunk_count = 0
        
        try:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
                    chunk_count += 1
                elif chunk["type"] == "WordBoundary":
                    logger.debug(f"Word boundary: {chunk}")
                elif chunk["type"] == "SentenceBoundary":
                    logger.debug(f"Sentence boundary: {chunk}")
        except Exception as stream_error:
            logger.error(f"Error during streaming: {stream_error}")
            raise Exception(f"Streaming error: {str(stream_error)}")
        
        logger.info(f"Received {chunk_count} audio chunks")
        
        # ตรวจสอบว่าได้เสียงจริงหรือไม่
        if not audio_data:
            logger.error("No audio was received. Please verify that your parameters are correct.")
            raise Exception("No audio was received. Please verify that your parameters are correct.")
        
        logger.info(f"Single TTS generated: {len(audio_data)} bytes")
        return audio_data
    
    def _combine_audio_segments(self, audio_segments: List[bytes]) -> bytes:
        """
        รวมเสียงจากหลายส่วนเข้าด้วยกัน
        
        Args:
            audio_segments: รายการข้อมูลเสียง
            
        Returns:
            bytes: ข้อมูลเสียงที่รวมแล้ว
        """
        try:
            # กรองส่วนที่ว่างเปล่าออก
            valid_segments = [seg for seg in audio_segments if seg and len(seg) > 0]
            
            if not valid_segments:
                raise Exception("No valid audio segments to combine")
            
            if len(valid_segments) == 1:
                # มีส่วนเดียว ไม่ต้องรวม
                return valid_segments[0]
            
            # Edge TTS ส่งมาเป็น MP3 ต้องแปลงและรวมด้วย pydub
            from pydub import AudioSegment
            import io
            
            combined_audio = None
            
            for i, segment_data in enumerate(valid_segments):
                try:
                    # แปลง bytes เป็น AudioSegment
                    audio_io = io.BytesIO(segment_data)
                    segment = AudioSegment.from_mp3(audio_io)
                    
                    if combined_audio is None:
                        combined_audio = segment
                    else:
                        # เพิ่มความเงียบ 100ms ระหว่างส่วน
                        silence = AudioSegment.silent(duration=100)
                        combined_audio = combined_audio + silence + segment
                        
                except Exception as e:
                    logger.warning(f"Failed to process segment {i}: {e}")
                    # ถ้าแปลงไม่ได้ ให้ข้ามส่วนนี้ไป
                    continue
            
            if combined_audio is None:
                # ถ้าไม่สามารถแปลงได้เลย ให้ใช้วิธีรวม bytes แบบเดิม
                logger.warning("Failed to combine with pydub, using byte concatenation")
                combined_bytes = b""
                for segment in valid_segments:
                    combined_bytes += segment
                return combined_bytes
            
            # แปลงกลับเป็น MP3 bytes
            output_io = io.BytesIO()
            combined_audio.export(output_io, format="mp3")
            combined_bytes = output_io.getvalue()
            
            logger.info(f"Combined {len(valid_segments)} audio segments into {len(combined_bytes)} bytes")
            return combined_bytes
            
        except Exception as e:
            logger.error(f"Error combining audio segments: {e}")
            # ถ้าไม่สามารถรวมได้ ให้ส่งคืนส่วนแรก
            return audio_segments[0] if audio_segments else b""
    
    def convert_voice(self, audio_data: bytes, model_name: str, 
                     transpose: int = 0, index_ratio: float = 0.75,
                     f0_method: str = "rmvpe") -> bytes:
        """
        แปลงเสียงด้วย RVC
        
        Args:
            audio_data: ข้อมูลเสียงที่ต้องการแปลง
            model_name: ชื่อโมเดล RVC
            transpose: การขยับ pitch (-12 ถึง 12)
            index_ratio: อัตราส่วน index (0.0-1.0)
            f0_method: วิธีการคำนวณ f0
            
        Returns:
            bytes: ข้อมูลเสียงที่แปลงแล้ว
        """
        if not self.rvc_available:
            raise Exception("RVC system not available")
        
        try:
            # สร้างชื่อไฟล์ที่ไม่ซ้ำกัน
            import time
            timestamp = int(time.time() * 1000)
            temp_input = self.temp_dir / f"rvc_input_{timestamp}.wav"
            temp_output = self.temp_dir / f"rvc_output_{timestamp}.wav"
            
            # แปลงไฟล์เสียงให้เป็นรูปแบบ WAV ที่ถูกต้อง
            try:
                import io
                import soundfile as sf
                import numpy as np
                from pydub import AudioSegment
                
                # ลองอ่านเป็น MP3 ก่อน (Edge TTS ส่งมาเป็น MP3)
                try:
                    # แปลง MP3 เป็น WAV โดยใช้ pydub
                    audio_io = io.BytesIO(audio_data)
                    audio_segment = AudioSegment.from_mp3(audio_io)
                    
                    # แปลงเป็น numpy array
                    samples = np.array(audio_segment.get_array_of_samples())
                    
                    # ถ้าเป็น stereo ให้แปลงเป็น mono
                    if audio_segment.channels == 2:
                        samples = samples.reshape((-1, 2))
                        samples = np.mean(samples, axis=1)
                    
                    # Normalize audio
                    samples = samples.astype(np.float32) / 32768.0
                    
                    # บันทึกเป็น WAV
                    sf.write(str(temp_input), samples, audio_segment.frame_rate, format='WAV', subtype='PCM_16')
                    
                    logger.info(f"Converted MP3 to WAV: {temp_input} (sample_rate={audio_segment.frame_rate})")
                    
                except Exception as mp3_error:
                    logger.debug(f"Not MP3 format or pydub conversion failed: {mp3_error}")
                    
                    # ถ้าไม่ใช่ MP3 ให้ลองอ่านเป็น WAV โดยตรง
                    audio_io = io.BytesIO(audio_data)
                    audio_array, sample_rate = sf.read(audio_io)
                    
                    # แปลงเป็น mono ถ้าเป็น stereo
                    if len(audio_array.shape) > 1:
                        audio_array = np.mean(audio_array, axis=1)
                    
                    # ตรวจสอบและแก้ไขข้อมูลเสียง
                    if np.isnan(audio_array).any():
                        audio_array = np.nan_to_num(audio_array, nan=0.0)
                    
                    # บันทึกเป็นไฟล์ WAV ที่ถูกต้อง
                    sf.write(str(temp_input), audio_array, sample_rate, format='WAV', subtype='PCM_16')
                    
                    logger.info(f"Saved audio as WAV: {temp_input} (sample_rate={sample_rate})")
                
            except Exception as conversion_error:
                logger.error(f"Failed to convert audio format: {conversion_error}")
                
                # ถ้าแปลงไม่ได้เลย ให้ลองบันทึกเป็นไฟล์ชั่วคราวและใช้ ffmpeg
                temp_mp3 = self.temp_dir / f"temp_{timestamp}.mp3"
                with open(temp_mp3, "wb") as f:
                    f.write(audio_data)
                
                # ใช้ ffmpeg แปลงเป็น WAV
                import subprocess
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-i", str(temp_mp3),
                    "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1",
                    str(temp_input)
                ]
                
                result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    logger.error(f"FFmpeg conversion failed: {result.stderr}")
                    raise Exception(f"Audio format conversion failed: {result.stderr}")
                
                # ลบไฟล์ MP3 ชั่วคราว
                temp_mp3.unlink(missing_ok=True)
                logger.info(f"Converted audio using FFmpeg: {temp_input}")
            
            # ตรวจสอบว่าไฟล์ถูกสร้างขึ้นหรือไม่
            if not temp_input.exists():
                raise Exception("Failed to create input audio file")
            
            # ตรวจสอบขนาดไฟล์
            file_size = temp_input.stat().st_size
            if file_size == 0:
                raise Exception("Input audio file is empty")
            
            logger.info(f"Created input file: {temp_input} ({file_size} bytes)")
            
            # แปลงเสียง
            result_path = self.rvc_instance.convert_voice(
                input_path=str(temp_input),
                output_path=str(temp_output),
                model_name=model_name,
                transpose=transpose,
                index_ratio=index_ratio,
                f0_method=f0_method
            )
            
            # ตรวจสอบว่าการแปลงสำเร็จหรือไม่
            if result_path is None:
                raise Exception("RVC conversion failed - no output path returned")
            
            # ตรวจสอบว่าไฟล์ผลลัพธ์ถูกสร้างขึ้นหรือไม่
            if not Path(result_path).exists():
                raise Exception(f"RVC output file not found: {result_path}")
            
            # อ่านผลลัพธ์
            with open(result_path, "rb") as f:
                converted_audio = f.read()
            
            if len(converted_audio) == 0:
                raise Exception("RVC output file is empty")
            
            # ลบไฟล์ชั่วคราว
            try:
                temp_input.unlink(missing_ok=True)
                if Path(result_path) != temp_output:
                    Path(result_path).unlink(missing_ok=True)
                temp_output.unlink(missing_ok=True)
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp files: {cleanup_error}")
            
            logger.info(f"Voice conversion completed: {len(converted_audio)} bytes")
            return converted_audio
            
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
            # ลบไฟล์ชั่วคราวในกรณี error
            try:
                temp_input.unlink(missing_ok=True)
                temp_output.unlink(missing_ok=True)
            except:
                pass
            raise Exception(f"Voice conversion failed: {str(e)}")
    
    async def process_unified(self, text: str, tts_voice: str, 
                            enable_rvc: bool = False, rvc_model: str = None,
                            tts_speed: float = 1.0, tts_pitch: str = "+0Hz",
                            rvc_transpose: int = 0, rvc_index_ratio: float = 0.75,
                            rvc_f0_method: str = "rmvpe", enable_multi_language: bool = False) -> Dict[str, Any]:
        """
        ประมวลผลรวม TTS + RVC ในคำสั่งเดียว
        
        Args:
            text: ข้อความที่ต้องการแปลง
            tts_voice: เสียง TTS
            enable_rvc: เปิดใช้ RVC หรือไม่
            rvc_model: โมเดล RVC (ถ้าเปิดใช้)
            tts_speed: ความเร็ว TTS
            tts_pitch: ระดับเสียง TTS
            rvc_transpose: การขยับ pitch RVC
            rvc_index_ratio: อัตราส่วน index RVC
            rvc_f0_method: วิธีการ f0 RVC
            enable_multi_language: เปิดใช้งานการประมวลผลหลายภาษา
            
        Returns:
            Dict: ผลลัพธ์รวมทั้งข้อมูลเสียงและสถิติ
        """
        result = {
            "success": False,
            "tts_audio_data": None,
            "rvc_audio_data": None,
            "final_audio_data": None,
            "processing_steps": [],
            "error": None,
            "stats": {}
        }
        
        try:
            # ขั้นตอนที่ 1: สร้าง TTS
            logger.info("Step 1: Generating TTS...")
            tts_audio = await self.generate_tts(text, tts_voice, tts_speed, tts_pitch, enable_multi_language)
            result["processing_steps"].append("tts_generation")
            result["stats"]["tts_audio_size"] = len(tts_audio)
            result["tts_audio_data"] = tts_audio
            
            # เพิ่มข้อมูลการตรวจจับภาษา
            if enable_multi_language:
                language_segments = self.detect_language_segments(text)
                result["stats"]["language_segments"] = len(language_segments)
                result["stats"]["detected_languages"] = list(set(lang for _, lang in language_segments))
                
                # เพิ่มรายละเอียดการตรวจจับภาษา
                language_segments_detail = []
                for segment_text, language in language_segments:
                    voice = self.get_voice_for_language(language, tts_voice)
                    language_segments_detail.append({
                        "text": segment_text,
                        "language": language,
                        "voice": voice
                    })
                result["stats"]["language_segments_detail"] = language_segments_detail
                
                logger.info(f"Detected languages: {result['stats']['detected_languages']}")
                logger.info(f"Language segments: {len(language_segments)} segments")
            
            final_audio = tts_audio
            rvc_audio = None
            
            # ขั้นตอนที่ 2: แปลงเสียงด้วย RVC (ถ้าเปิดใช้)
            if enable_rvc and rvc_model:
                logger.info(f"Step 2: Checking RVC model '{rvc_model}'...")
                
                # ตรวจสอบว่า RVC system พร้อมใช้งานหรือไม่
                if not self.rvc_available:
                    logger.warning("RVC system not available")
                    result["processing_steps"].append("rvc_unavailable")
                    result["error"] = "RVC system not available"
                else:
                    # ตรวจสอบว่าโมเดลมีอยู่จริงหรือไม่
                    available_models = self.get_available_rvc_models()
                    
                    # แปลง rvc_model ให้เป็น string อย่างปลอดภัย (แก้ไข unhashable error)
                    rvc_model, model_error = safe_model_processing(
                        rvc_model, 
                        available_models,
                        available_models[0] if available_models else None
                    )
                    
                    if model_error:
                        logger.warning(f"Model processing warning: {model_error}")
                    
                    if rvc_model and rvc_model not in available_models:
                        logger.warning(f"RVC model '{rvc_model}' not found. Available models: {available_models}")
                        result["processing_steps"].append("rvc_model_not_found")
                        result["error"] = f"RVC model '{rvc_model}' not found"
                    else:
                        logger.info(f"Step 2: Applying voice conversion with model '{rvc_model}'...")
                        try:
                            converted_audio = self.convert_voice(
                                tts_audio, rvc_model, rvc_transpose, 
                                rvc_index_ratio, rvc_f0_method
                            )
                            rvc_audio = converted_audio
                            final_audio = converted_audio
                            result["processing_steps"].append("voice_conversion")
                            result["stats"]["rvc_audio_size"] = len(converted_audio)
                            result["rvc_audio_data"] = converted_audio
                            logger.info(f"Voice conversion successful: {len(converted_audio)} bytes")
                        except Exception as rvc_error:
                            logger.error(f"Voice conversion failed: {rvc_error}")
                            result["processing_steps"].append("rvc_failed")
                            result["error"] = f"Voice conversion failed: {str(rvc_error)}"
                            # ใช้เสียง TTS เดิม
            elif enable_rvc and not rvc_model:
                logger.warning("RVC enabled but no model specified")
                result["processing_steps"].append("rvc_no_model")
                result["error"] = "RVC enabled but no model specified"
            
            # ขั้นตอนที่ 3: เตรียมผลลัพธ์
            result.update({
                "success": True,
                "final_audio_data": final_audio,
                "stats": {
                    **result["stats"],
                    "text_length": len(text),
                    "final_audio_size": len(final_audio),
                    "voice_conversion_applied": "voice_conversion" in result["processing_steps"],
                    "multi_language_enabled": enable_multi_language,
                    "device": self.device
                }
            })
            
            logger.info(f"Unified processing completed: {result['processing_steps']}")
            return result
            
        except Exception as e:
            logger.error(f"Unified processing failed: {e}")
            result.update({
                "success": False,
                "error": str(e)
            })
            return result
    
    def smart_chunk_text(self, text: str, max_chunk_size: int = 8000) -> List[str]:
        """
        แบ่งข้อความอย่างชาญฉลาด เพื่อไม่ให้เกินขีดจำกัดของ TTS
        
        Args:
            text: ข้อความที่ต้องการแบ่ง
            max_chunk_size: ขนาดสูงสุดของแต่ละส่วน
            
        Returns:
            List[str]: รายการข้อความที่แบ่งแล้ว
        """
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # แบ่งตามประโยค
        sentences = text.replace(".", ".\\n").replace("!", "!\\n").replace("?", "?\\n").split("\\n")
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # ถ้าเพิ่มประโยคนี้แล้วยังไม่เกินขีดจำกัด
            if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
            else:
                # เก็บ chunk ปัจจุบัน
                if current_chunk:
                    chunks.append(current_chunk)
                
                # เริ่ม chunk ใหม่
                if len(sentence) <= max_chunk_size:
                    current_chunk = sentence
                else:
                    # ประโยคยาวเกินไป ต้องแบ่งเป็นคำ
                    words = sentence.split()
                    temp_chunk = ""
                    for word in words:
                        if len(temp_chunk) + len(word) + 1 <= max_chunk_size:
                            if temp_chunk:
                                temp_chunk += " " + word
                            else:
                                temp_chunk = word
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk)
                            temp_chunk = word
                    current_chunk = temp_chunk
        
        # เพิ่ม chunk สุดท้าย
        if current_chunk:
            chunks.append(current_chunk)
        
        logger.info(f"Text chunked into {len(chunks)} parts")
        return chunks
    
    async def process_long_text(self, text: str, tts_voice: str,
                               max_chunk_size: int = 8000, **kwargs) -> Dict[str, Any]:
        """
        ประมวลผลข้อความยาวด้วยการแบ่ง chunk
        
        Args:
            text: ข้อความยาว
            tts_voice: เสียง TTS
            max_chunk_size: ขนาดสูงสุดของแต่ละ chunk
            **kwargs: พารามิเตอร์อื่นๆ สำหรับ process_unified
            
        Returns:
            Dict: ผลลัพธ์รวมจากทุก chunk
        """
        # แบ่งข้อความ
        chunks = self.smart_chunk_text(text, max_chunk_size)
        
        if len(chunks) == 1:
            # ข้อความสั้น ใช้ process_unified ธรรมดา
            return await self.process_unified(text, tts_voice, **kwargs)
        
        # ประมวลผล chunk ทีละตัว
        all_audio_data = []
        all_processing_steps = []
        total_stats = {
            "chunks_count": len(chunks),
            "total_text_length": len(text),
            "chunk_sizes": [len(chunk) for chunk in chunks]
        }
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}: {len(chunk)} chars")
            
            chunk_result = await self.process_unified(chunk, tts_voice, **kwargs)
            
            if chunk_result["success"]:
                all_audio_data.append(chunk_result["audio_data"])
                all_processing_steps.extend([f"chunk_{i+1}_{step}" for step in chunk_result["processing_steps"]])
            else:
                logger.error(f"Chunk {i+1} failed: {chunk_result.get('error')}")
                return {
                    "success": False,
                    "error": f"Chunk {i+1} processing failed: {chunk_result.get('error')}",
                    "chunks_processed": i
                }
            
            # หน่วงเวลาเล็กน้อยระหว่าง chunk
            await asyncio.sleep(0.1)
        
        # รวมเสียงทั้งหมด
        try:
            combined_audio = b"".join(all_audio_data)
            
            return {
                "success": True,
                "audio_data": combined_audio,
                "processing_steps": all_processing_steps,
                "stats": {
                    **total_stats,
                    "final_audio_size": len(combined_audio),
                    "chunks_processed": len(chunks),
                    "processing_method": "multi_chunk",
                    "device": self.device
                }
            }
        except Exception as e:
            logger.error(f"Audio combination failed: {e}")
            return {
                "success": False,
                "error": f"Audio combination failed: {str(e)}",
                "chunks_processed": len(chunks)
            }
    
    def cleanup_temp_files(self):
        """ลบไฟล์ชั่วคราวที่เก่า"""
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - 3600  # 1 ชั่วโมง
            
            for file_path in self.temp_dir.glob("*"):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink(missing_ok=True)
            
            logger.info("Temp files cleaned")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            
    def change_device(self, new_device: str = None, use_gpu: bool = None, gpu_id: int = None):
        """
        เปลี่ยนอุปกรณ์ที่ใช้ประมวลผล
        
        Args:
            new_device: อุปกรณ์ที่ใช้ประมวลผลใหม่ (cpu, cuda:0, cuda:1, ...)
            use_gpu: เปิดใช้งาน GPU หรือไม่
            gpu_id: ID ของ GPU ที่ใช้ (0, 1, 2, ...)
        
        Returns:
            bool: True ถ้าเปลี่ยนสำเร็จ, False ถ้าไม่สำเร็จ
        """
        try:
            # ถ้าไม่ได้ระบุค่าใหม่ ให้ใช้ค่าเดิม
            if use_gpu is None:
                use_gpu = "cuda" in self.device
            if gpu_id is None and "cuda:" in self.device:
                gpu_id = int(self.device.split(":")[-1])
            elif gpu_id is None:
                gpu_id = 0
                
            # บันทึก device เดิม
            old_device = self.device
            
            # ตั้งค่า device ใหม่
            self.setup_device(new_device, use_gpu, gpu_id)
            
            # ถ้า device เปลี่ยน ให้เริ่มระบบใหม่
            if old_device != self.device:
                logger.info(f"Device changed from {old_device} to {self.device}, reinitializing systems")
                self._initialize_systems()
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error changing device: {e}")
            return False
    
    def get_device_info(self) -> Dict[str, Any]:
        """ดึงข้อมูลอุปกรณ์ที่ใช้"""
        return {
            "current_device": self.device,
            "gpu_available": self.gpu_available,
            "gpu_count": len(self.gpu_info) if self.gpu_info else 0,
            "gpu_info": self.gpu_info or [],
            "device_options": self._get_device_options()
        }
    
    def _get_device_options(self) -> List[Dict[str, Any]]:
        """ดึงตัวเลือกอุปกรณ์ที่ใช้ได้"""
        options = [
            {
                "value": "cpu",
                "label": "CPU Only",
                "description": "ใช้ CPU เท่านั้น (เสถียรที่สุด)",
                "icon": "🖥️"
            }
        ]
        
        if self.gpu_available and self.gpu_info:
            for gpu in self.gpu_info:
                options.append({
                    "value": f"cuda:{gpu['id']}",
                    "label": f"GPU {gpu['id']}: {gpu['name']}",
                    "description": f"ใช้ GPU {gpu['id']} ({gpu['memory']:.1f}GB)",
                    "icon": "🚀"
                })
            
            # เพิ่มตัวเลือก AUTO
            if len(self.gpu_info) > 0:
                options.append({
                    "value": "auto",
                    "label": "AUTO (Best GPU)",
                    "description": "เลือก GPU ที่ดีที่สุดอัตโนมัติ",
                    "icon": "⚡"
                })
        
        return options
    
    def change_device_auto(self, device_choice: str) -> Dict[str, Any]:
        """
        เปลี่ยนอุปกรณ์ตามตัวเลือกที่เลือก
        
        Args:
            device_choice: ตัวเลือก (cpu, cuda:0, cuda:1, auto)
        """
        try:
            if device_choice == "auto":
                # เลือก GPU ที่ดีที่สุด (memory มากที่สุด)
                if self.gpu_available and self.gpu_info:
                    best_gpu = max(self.gpu_info, key=lambda x: x['memory'])
                    device_choice = f"cuda:{best_gpu['id']}"
                    logger.info(f"Auto-selected GPU {best_gpu['id']}: {best_gpu['name']} ({best_gpu['memory']:.1f}GB)")
                else:
                    device_choice = "cpu"
                    logger.info("No GPU available, using CPU")
            
            # เปลี่ยนอุปกรณ์
            success = self.change_device(device_choice)
            
            return {
                "success": success,
                "device": self.device,
                "device_info": self.get_device_info(),
                "message": f"Changed to {self.device}"
            }
            
        except Exception as e:
            logger.error(f"Error in change_device_auto: {e}")
            return {
                "success": False,
                "error": str(e),
                "device": self.device
            }

    def detect_language_segments(self, text: str) -> List[Tuple[str, str]]:
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
            'lao': r'[\u0E80-\u0EFF]+(?:\\s+[\u0E80-\u0EFF]+)*',
            'thai': r'[\u0E00-\u0E7F]+(?:\\s+[\u0E00-\u0E7F]+)*',
            'chinese': r'[\u4E00-\u9FFF]+(?:\\s+[\u4E00-\u9FFF]+)*',
            'japanese': r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+(?:\\s+[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)*',
            'numbers': r'\\d+(?:\\.\\d+)?',
            'punctuation': r'[^\\w\\s\u0E00-\u0E7F\u0E80-\u0EFF\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF]'
        }
        
        # ตรวจสอบว่ามีตัวอักษรลาวในข้อความหรือไม่
        has_lao = bool(re.search(r'[\u0E80-\u0EFF]', text))
        has_english = bool(re.search(r'[a-zA-Z]', text))
        
        # ถ้ามีทั้งลาวและอังกฤษ ให้ใช้ multi-language detection
        if has_lao and has_english:
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
        else:
            # ถ้ามีภาษาเดียว ให้ใช้ภาษาเดียว
            if has_lao:
                return [(text, 'lao')]
            elif has_english:
                return [(text, 'english')]
            else:
                return [(text, 'unknown')]
        

    
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
        
        return merged
    
    def get_voice_for_language(self, language: str, base_voice: str) -> str:
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
        
        return language_voice_mapping.get(language, base_voice)

    def apply_audio_effects(self, audio_data: bytes, effects: Dict[str, Any]) -> bytes:
        """
        ใช้เอฟเฟกต์พิเศษกับเสียง
        
        Args:
            audio_data: ข้อมูลเสียงที่ต้องการใส่เอฟเฟกต์
            effects: dictionary ของเอฟเฟกต์ที่ต้องการ
            
        Returns:
            bytes: ข้อมูลเสียงที่ใส่เอฟเฟกต์แล้ว
        """
        try:
            # ถ้าไม่มีเอฟเฟกต์ใดเปิดอยู่ ให้ส่งคืนเดิม
            if not any(effects.get(key, False) for key in ['demon_mode', 'robot_mode', 'echo_mode', 'reverb_mode']):
                return audio_data
            
            # แปลงจาก bytes เป็น numpy array
            import io
            import soundfile as sf
            from pedalboard import (
                Pedalboard, Chorus, Distortion, Reverb, PitchShift, 
                Limiter, Gain, Bitcrush, Clipping, Compressor, Delay
            )
            
            # อ่านเสียงจาก bytes
            audio_io = io.BytesIO(audio_data)
            audio_array, sample_rate = sf.read(audio_io)
            
            # สร้าง pedalboard
            board = Pedalboard()
            
            # Demon Mode: Pitch down + Distortion + Dark reverb
            if effects.get('demon_mode', False):
                logger.info("Applying demon mode effect")
                # ลดเสียงลง 8 semitones
                pitch_shift = PitchShift(semitones=-8)
                board.append(pitch_shift)
                
                # เพิ่ม distortion
                distortion = Distortion(drive_db=35)
                board.append(distortion)
                
                # เพิ่ม dark reverb
                reverb = Reverb(
                    room_size=0.9,
                    damping=0.8,
                    wet_level=0.4,
                    dry_level=0.7,
                    width=0.5
                )
                board.append(reverb)
            
            # Robot Mode: Bitcrush + Chorus + High pitch
            if effects.get('robot_mode', False):
                logger.info("Applying robot mode effect")
                # เพิ่มเสียงขึ้น 2 semitones
                pitch_shift = PitchShift(semitones=2)
                board.append(pitch_shift)
                
                # เพิ่ม bitcrush สำหรับเสียงดิจิตอล
                bitcrush = Bitcrush(bit_depth=6)
                board.append(bitcrush)
                
                # เพิ่ม chorus สำหรับเสียงแปลกๆ
                chorus = Chorus(
                    rate_hz=2.0,
                    depth=0.5,
                    centre_delay_ms=10,
                    feedback=0.3,
                    mix=0.6
                )
                board.append(chorus)
            
            # Echo Mode: Delay effect
            if effects.get('echo_mode', False):
                logger.info("Applying echo mode effect")
                delay = Delay(
                    delay_seconds=0.3,
                    feedback=0.5,
                    mix=0.4
                )
                board.append(delay)
            
            # Reverb Mode: Natural reverb
            if effects.get('reverb_mode', False):
                logger.info("Applying reverb mode effect")
                reverb = Reverb(
                    room_size=0.7,
                    damping=0.3,
                    wet_level=0.5,
                    dry_level=0.8,
                    width=1.0
                )
                board.append(reverb)
            
            # ใช้เอฟเฟกต์กับเสียง
            if len(board) > 0:
                processed_audio = board(audio_array, sample_rate)
                
                # แปลงกลับเป็น bytes
                output_io = io.BytesIO()
                sf.write(output_io, processed_audio, sample_rate, format='WAV')
                processed_data = output_io.getvalue()
                
                logger.info(f"Applied {len(board)} audio effects, size: {len(audio_data)} -> {len(processed_data)} bytes")
                return processed_data
            else:
                return audio_data
                
        except Exception as e:
            logger.error(f"Error applying audio effects: {e}")
            # ถ้าเกิดข้อผิดพลาด ให้ส่งคืนเสียงเดิม
            return audio_data

# เสียงที่รองรับ
SUPPORTED_VOICES = {
    "th-TH-PremwadeeNeural": {"name": "Premwadee (Thai Female)", "gender": "Female", "language": "Thai"},
    "th-TH-NiranNeural": {"name": "Niran (Thai Male)", "gender": "Male", "language": "Thai"},
    "th-TH-NiwatNeural": {"name": "Niwat (Thai Male)", "gender": "Male", "language": "Thai"},
    "lo-LA-ChanthavongNeural": {"name": "Chanthavong (Lao Male)", "gender": "Male", "language": "Lao"},
    "lo-LA-KeomanyNeural": {"name": "Keomany (Lao Female)", "gender": "Female", "language": "Lao"},
    "en-US-AriaNeural": {"name": "Aria (US Female)", "gender": "Female", "language": "English"},
    "en-US-GuyNeural": {"name": "Guy (US Male)", "gender": "Male", "language": "English"},
    "en-US-JennyNeural": {"name": "Jenny (US Female)", "gender": "Female", "language": "English"},
    "ja-JP-NanamiNeural": {"name": "Nanami (Japanese Female)", "gender": "Female", "language": "Japanese"},
    "zh-CN-XiaoxiaoNeural": {"name": "Xiaoxiao (Chinese Female)", "gender": "Female", "language": "Chinese"}
}

# Helper functions
def create_core_instance(**kwargs) -> TTSRVCCore:
    """สร้าง instance ของ TTS-RVC Core"""
    return TTSRVCCore(**kwargs)

def get_supported_voices() -> Dict[str, Dict[str, str]]:
    """ดึงรายการเสียงที่รองรับ"""
    return SUPPORTED_VOICES

# Test function
async def test_core_system():
    """ทดสอบระบบ Core"""
    print("🔧 Testing TTS-RVC Core System...")
    
    # ตรวจสอบ GPU
    try:
        import torch
        if torch.cuda.is_available():
            device = f"cuda:{torch.cuda.current_device()}"
            print(f"Found GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = "cpu"
            print("No GPU available, using CPU")
    except ImportError:
        device = "cpu"
        print("PyTorch not available, using CPU")
    
    # สร้าง instance
    core = create_core_instance(device=device)
    
    # ตรวจสอบสถานะ
    status = core.get_system_status()
    print(f"✅ System Status: {status}")
    
    # ทดสอบ TTS
    if status["tts_available"]:
        print("🎵 Testing TTS...")
        try:
            test_text = "สวัสดีครับ นี่คือการทดสอบระบบ TTS"
            audio_data = await core.generate_tts(test_text, "th-TH-PremwadeeNeural")
            print(f"✅ TTS Test: {len(audio_data)} bytes generated")
        except Exception as e:
            print(f"❌ TTS Test failed: {e}")
    
    # ทดสอบ RVC (ถ้ามีโมเดล)
    if status["rvc_available"] and status["rvc_models_count"] > 0:
        print("🎭 Testing RVC...")
        try:
            # ใช้เสียงจาก TTS ทดสอบ
            if 'audio_data' in locals():
                model_name = core.get_available_rvc_models()[0]
                converted = core.convert_voice(audio_data, model_name)
                print(f"✅ RVC Test: {len(converted)} bytes converted using {model_name}")
        except Exception as e:
            print(f"❌ RVC Test failed: {e}")
    
    # ทดสอบระบบรวม
    print("🚀 Testing Unified Processing...")
    try:
        result = await core.process_unified(
            text="ทดสอบระบบรวม TTS และ RVC",
            tts_voice="th-TH-PremwadeeNeural",
            enable_rvc=status["rvc_available"] and status["rvc_models_count"] > 0,
            rvc_model=core.get_available_rvc_models()[0] if status["rvc_models_count"] > 0 else None
        )
        print(f"✅ Unified Test: {result['success']}, Steps: {result['processing_steps']}")
    except Exception as e:
        print(f"❌ Unified Test failed: {e}")
    
    print("🎉 Core system testing completed!")

if __name__ == "__main__":
    # รัน test
    asyncio.run(test_core_system())
