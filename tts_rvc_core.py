#!/usr/bin/env python3
"""
🎯 TTS-RVC Core System - ระบบหลักรวม TTS และ RVC
รวมฟังก์ชันหลักทั้งหมดในไฟล์เดียว
"""
import os
import sys
import asyncio
from pathlib import Path
import logging
from typing import Optional, Dict, Any, List, Union

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTS_RVC_CORE")

class TTSRVCCore:
    """ระบบหลักสำหรับ TTS และ RVC"""
    
    def __init__(self, models_dir: str = "logs", temp_dir: str = "storage/temp", 
                 device: str = None, use_gpu: bool = True, gpu_id: int = 0):
        """
        เริ่มต้นระบบ TTS-RVC
        
        Args:
            models_dir: โฟลเดอร์ที่เก็บโมเดล RVC
            temp_dir: โฟลเดอร์สำหรับไฟล์ชั่วคราว
            device: อุปกรณ์ที่ใช้ประมวลผล (cpu, cuda:0, cuda:1, ...) - ถ้าเป็น None จะใช้ค่าตามการกำหนด use_gpu และ gpu_id
            use_gpu: เปิดใช้งาน GPU หรือไม่
            gpu_id: ID ของ GPU ที่ใช้ (0, 1, 2, ...)
        """
        self.models_dir = Path(models_dir)
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # ตั้งค่า GPU
        self.setup_device(device, use_gpu, gpu_id)
        
        # สถานะของระบบ
        self.tts_available = False
        self.rvc_available = False
        self.rvc_instance = None
        
        # โหลดระบบ
        self._initialize_systems()
        
        logger.info(f"TTS-RVC Core initialized - TTS: {self.tts_available}, RVC: {self.rvc_available}, Device: {self.device}")
    
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
            self.rvc_instance = RVCConverter(device=self.device, models_dir=self.models_dir)
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
                          pitch: str = "+0Hz") -> bytes:
        """
        สร้างเสียงจากข้อความด้วย Edge TTS
        
        Args:
            text: ข้อความที่ต้องการแปลง
            voice: เสียงที่ใช้ (เช่น th-TH-PremwadeeNeural)
            speed: ความเร็วในการพูด (0.5-2.0)
            pitch: ระดับเสียง (เช่น +0Hz, +10Hz)
            
        Returns:
            bytes: ข้อมูลเสียงในรูปแบบ bytes
        """
        if not self.tts_available:
            raise Exception("TTS system not available")
        
        try:
            import edge_tts
            
            # Log ข้อมูลพารามิเตอร์
            logger.info(f"Generating TTS with text='{text[:30]}...', voice='{voice}', speed={speed}, pitch={pitch}")
            
            # ตรวจสอบและทำความสะอาดข้อความ
            if not text or not text.strip():
                raise Exception("Text is empty or contains only whitespace")
            
            # ทำความสะอาดข้อความ - ลบอักขระพิเศษที่อาจทำให้เกิดปัญหา
            cleaned_text = text.strip()
            # ลบอักขระควบคุมที่ไม่จำเป็น
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
            
            # ปรับ rate สำหรับ speed
            if speed != 1.0:
                rate = f"{speed:+.0%}"
            else:
                rate = "+0%"
            
            logger.info(f"Using cleaned text: '{cleaned_text[:50]}...'")
            
            # สร้าง Communicate object
            communicate = edge_tts.Communicate(
                text=cleaned_text,
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
            
            logger.info(f"TTS generated: {len(audio_data)} bytes")
            return audio_data
            
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise Exception(f"TTS generation failed: {str(e)}")
    
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
            # บันทึกไฟล์ input
            temp_input = self.temp_dir / f"rvc_input_{os.getpid()}.wav"
            temp_output = self.temp_dir / f"rvc_output_{os.getpid()}.wav"
            
            with open(temp_input, "wb") as f:
                f.write(audio_data)
            
            # แปลงเสียง
            result_path = self.rvc_instance.convert_voice(
                input_path=str(temp_input),
                output_path=str(temp_output),
                model_name=model_name,
                transpose=transpose,
                index_ratio=index_ratio,
                f0_method=f0_method
            )
            
            # อ่านผลลัพธ์
            with open(result_path, "rb") as f:
                converted_audio = f.read()
            
            # ลบไฟล์ชั่วคราว
            temp_input.unlink(missing_ok=True)
            temp_output.unlink(missing_ok=True)
            if Path(result_path) != temp_output:
                Path(result_path).unlink(missing_ok=True)
            
            logger.info(f"Voice conversion completed: {len(converted_audio)} bytes")
            return converted_audio
            
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
            raise Exception(f"Voice conversion failed: {str(e)}")
    
    async def process_unified(self, text: str, tts_voice: str, 
                            enable_rvc: bool = False, rvc_model: str = None,
                            tts_speed: float = 1.0, tts_pitch: str = "+0Hz",
                            rvc_transpose: int = 0, rvc_index_ratio: float = 0.75,
                            rvc_f0_method: str = "rmvpe") -> Dict[str, Any]:
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
            
        Returns:
            Dict: ผลลัพธ์รวมทั้งข้อมูลเสียงและสถิติ
        """
        result = {
            "success": False,
            "audio_data": None,
            "processing_steps": [],
            "error": None,
            "stats": {}
        }
        
        try:
            # ขั้นตอนที่ 1: สร้าง TTS
            logger.info("Step 1: Generating TTS...")
            tts_audio = await self.generate_tts(text, tts_voice, tts_speed, tts_pitch)
            result["processing_steps"].append("tts_generation")
            result["stats"]["tts_audio_size"] = len(tts_audio)
            
            final_audio = tts_audio
            
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
                    if rvc_model not in available_models:
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
                            final_audio = converted_audio
                            result["processing_steps"].append("voice_conversion")
                            result["stats"]["rvc_audio_size"] = len(converted_audio)
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
                "audio_data": final_audio,
                "stats": {
                    **result["stats"],
                    "text_length": len(text),
                    "final_audio_size": len(final_audio),
                    "voice_conversion_applied": "voice_conversion" in result["processing_steps"],
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
