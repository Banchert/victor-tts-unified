#!/usr/bin/env python3
"""
🎯 Optimized TTS-RVC Core - ระบบหลักที่ปรับปรุงประสิทธิภาพ
"""
import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OPTIMIZED_CORE")

class OptimizedTTSRVCCore:
    """ระบบหลักที่ปรับปรุงประสิทธิภาพ"""
    
    def __init__(self, models_dir: str = "logs", temp_dir: str = "storage/temp", 
                 device: str = None, use_gpu: bool = True, gpu_id: int = 0):
        """เริ่มต้นระบบแบบเร็ว"""
        self.models_dir = Path(models_dir)
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # ตั้งค่า GPU แบบเร็ว
        self.setup_device_fast(device, use_gpu, gpu_id)
        
        # สถานะของระบบ
        self.tts_available = False
        self.rvc_available = False
        self.rvc_instance = None
        
        # โหลดระบบแบบ lazy
        self._lazy_initialize()
        
        logger.info(f"Optimized Core initialized - TTS: {self.tts_available}, RVC: {self.rvc_available}")
    
    def setup_device_fast(self, device: str = None, use_gpu: bool = True, gpu_id: int = 0):
        """ตั้งค่า GPU แบบเร็ว"""
        try:
            import torch
            if torch.cuda.is_available() and use_gpu:
                if device:
                    self.device = device
                else:
                    self.device = f"cuda:{gpu_id}" if gpu_id < torch.cuda.device_count() else "cuda:0"
                logger.info(f"Using GPU: {self.device}")
            else:
                self.device = "cpu"
                logger.info("Using CPU")
        except ImportError:
            self.device = "cpu"
            logger.info("PyTorch not available, using CPU")
    
    def _lazy_initialize(self):
        """โหลดระบบแบบ lazy loading"""
        # โหลด TTS ทันที
        try:
            import edge_tts
            self.tts_available = True
            logger.info("✅ Edge TTS loaded")
        except ImportError:
            logger.warning("⚠️ Edge TTS not available")
        
        # RVC จะโหลดเมื่อต้องการใช้
        self.rvc_loaded = False
    
    def _load_rvc_lazy(self):
        """โหลด RVC เมื่อต้องการใช้"""
        if self.rvc_loaded:
            return
        
        try:
            from rvc_api import RVCConverter
            self.rvc_instance = RVCConverter(device=self.device, models_dir=str(self.models_dir))
            self.rvc_available = True
            self.rvc_loaded = True
            logger.info(f"✅ RVC loaded on {self.device}")
        except Exception as e:
            logger.warning(f"⚠️ RVC loading failed: {e}")
            self.rvc_available = False
    
    async def generate_tts(self, text: str, voice: str, speed: float = 1.0) -> bytes:
        """สร้าง TTS แบบเร็ว"""
        if not self.tts_available:
            raise Exception("TTS not available")
        
        try:
            import edge_tts
            
            # ปรับ rate
            rate = f"{speed:+.0%}" if speed != 1.0 else "+0%"
            
            communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
            
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            return audio_data
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise
    
    def convert_voice(self, audio_data: bytes, model_name: str, 
                     transpose: int = 0, index_ratio: float = 0.75,
                     preset: str = "fast", **kwargs) -> bytes:
        """แปลงเสียง RVC แบบเร็ว"""
        # โหลด RVC ถ้ายังไม่ได้โหลด
        self._load_rvc_lazy()
        
        if not self.rvc_available:
            raise Exception("RVC not available")
        
        try:
            # สร้างไฟล์ชั่วคราว
            import time
            timestamp = int(time.time() * 1000)
            temp_input = self.temp_dir / f"input_{timestamp}.wav"
            temp_output = self.temp_dir / f"output_{timestamp}.wav"
            
            # บันทึกไฟล์เสียง
            with open(temp_input, "wb") as f:
                f.write(audio_data)
            
            # ใช้ preset หรือ custom parameters
            if preset and preset in self.rvc_instance.get_conversion_presets():
                preset_params = self.rvc_instance.get_conversion_presets()[preset]
                logger.info(f"Using preset: {preset} - {preset_params.get('description', '')}")
                
                # Merge preset with custom kwargs
                conversion_params = {**preset_params, **kwargs}
                conversion_params['pitch'] = transpose  # Override with transpose
                conversion_params['index_rate'] = index_ratio  # Override with index_ratio
            else:
                # Use custom parameters
                conversion_params = {
                    'pitch': transpose,
                    'index_rate': index_ratio,
                    **kwargs
                }
            
            # แปลงเสียง
            result_path = self.rvc_instance.convert_voice(
                input_path=str(temp_input),
                output_path=str(temp_output),
                model_name=model_name,
                **conversion_params
            )
            
            if not result_path:
                raise Exception("Voice conversion failed - no output generated")
            
            # อ่านผลลัพธ์
            with open(result_path, "rb") as f:
                converted_audio = f.read()
            
            # ลบไฟล์ชั่วคราว
            temp_input.unlink(missing_ok=True)
            temp_output.unlink(missing_ok=True)
            
            logger.info(f"Voice conversion completed: {len(converted_audio)} bytes")
            return converted_audio
            
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
            # ลบไฟล์ชั่วคราวในกรณีเกิดข้อผิดพลาด
            temp_input.unlink(missing_ok=True)
            temp_output.unlink(missing_ok=True)
            raise
    
    def get_available_rvc_models(self) -> List[str]:
        """ดึงโมเดล RVC แบบเร็ว"""
        if not self.rvc_loaded:
            self._load_rvc_lazy()
        
        if not self.rvc_available:
            return []
        
        try:
            return self.rvc_instance.get_available_models()
        except Exception as e:
            logger.error(f"Error getting RVC models: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """ดึงสถานะระบบ"""
        status = {
            "tts_available": self.tts_available,
            "rvc_available": self.rvc_available,
            "device": self.device,
            "rvc_loaded": self.rvc_loaded
        }
        
        # เพิ่มข้อมูล RVC models ถ้าโหลดแล้ว
        if self.rvc_loaded and self.rvc_instance:
            try:
                models = self.rvc_instance.get_available_models()
                status["rvc_models"] = {
                    "count": len(models),
                    "models": models[:10],  # Show first 10 models
                    "total": len(models)
                }
                
                # เพิ่มข้อมูล presets
                presets = self.rvc_instance.get_conversion_presets()
                status["rvc_presets"] = list(presets.keys())
                
            except Exception as e:
                logger.warning(f"Error getting RVC status: {e}")
                status["rvc_error"] = str(e)
        
        # เพิ่มข้อมูลระบบ
        try:
            import torch
            if torch.cuda.is_available():
                status["gpu_info"] = {
                    "cuda_available": True,
                    "gpu_count": torch.cuda.device_count(),
                    "current_device": self.device,
                    "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else None
                }
                
                # GPU Memory info
                if "cuda" in self.device:
                    gpu_id = int(self.device.split(":")[-1]) if ":" in self.device else 0
                    if gpu_id < torch.cuda.device_count():
                        memory_allocated = torch.cuda.memory_allocated(gpu_id) / 1024**3  # GB
                        memory_reserved = torch.cuda.memory_reserved(gpu_id) / 1024**3   # GB
                        status["gpu_info"]["memory_allocated_gb"] = round(memory_allocated, 2)
                        status["gpu_info"]["memory_reserved_gb"] = round(memory_reserved, 2)
            else:
                status["gpu_info"] = {"cuda_available": False}
        except Exception as e:
            status["gpu_info"] = {"error": str(e)}
        
        return status
    
    def get_conversion_presets(self) -> Dict[str, Any]:
        """ดึงรายการ presets สำหรับ voice conversion"""
        self._load_rvc_lazy()
        if self.rvc_available and self.rvc_instance:
            return self.rvc_instance.get_conversion_presets()
        return {}
    
    def convert_voice_batch(self, audio_files: List[str], output_dir: str, 
                          model_name: str, **kwargs) -> List[str]:
        """แปลงเสียงหลายไฟล์พร้อมกัน"""
        self._load_rvc_lazy()
        if not self.rvc_available:
            raise Exception("RVC not available")
        
        return self.rvc_instance.convert_voice_batch(
            input_files=audio_files,
            output_dir=output_dir,
            model_name=model_name,
            **kwargs
        )
    
    def cleanup(self):
        """ทำความสะอาดระบบ"""
        try:
            if self.rvc_instance:
                self.rvc_instance.cleanup()
            logger.info("Optimized Core cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

# Helper functions
def create_optimized_core_instance(**kwargs):
    """สร้าง instance แบบเร็ว"""
    return OptimizedTTSRVCCore(**kwargs)

def get_supported_voices():
    """ดึงรายการเสียงที่รองรับ"""
    return {
        "th-TH-PremwadeeNeural": {"name": "Premwadee (Thai Female)", "gender": "Female", "language": "Thai"},
        "th-TH-NiranNeural": {"name": "Niran (Thai Male)", "gender": "Male", "language": "Thai"},
        "en-US-AriaNeural": {"name": "Aria (US Female)", "gender": "Female", "language": "English"},
        "en-US-GuyNeural": {"name": "Guy (US Male)", "gender": "Male", "language": "English"}
    }
