#!/usr/bin/env python3
"""
🎤 RVC API Wrapper
Wrapper สำหรับ RVC (Retrieval-Based Voice Conversion) system
"""
import os
import sys
import logging
import torch
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Any

# Add RVC to path
rvc_path = Path(__file__).parent / "rvc"
sys.path.insert(0, str(rvc_path))

from rvc.infer.infer import VoiceConverter
from rvc.infer.pipeline import Pipeline as VCPipeline
from rvc.lib.utils import load_audio_infer, load_embedding
from rvc.configs.config import Config

logger = logging.getLogger("RVC_API")

class RVCConverter:
    """RVC Voice Converter Wrapper"""
    
    def __init__(self, device: str = "cpu", models_dir: str = "logs"):
        """
        เริ่มต้น RVC Converter
        
        Args:
            device: อุปกรณ์ที่ใช้ (cpu, cuda:0, etc.)
            models_dir: โฟลเดอร์ที่เก็บโมเดล
        """
        self.device = device
        self.models_dir = Path(models_dir)
        self.voice_converter = VoiceConverter()
        self.config = Config()
        self.config.device = device
        
        # ตั้งค่า models directory
        self.config.weight_root = str(self.models_dir)
        
        # โหลด embedder model
        self._load_embedder()
        
        logger.info(f"RVC Converter initialized on {device}")
    
    def _load_embedder(self):
        """โหลด embedder model"""
        try:
            # ใช้ contentvec เป็น embedder หลัก
            embedder_model = "contentvec"
            self.voice_converter.load_hubert(embedder_model)
            logger.info(f"Loaded embedder: {embedder_model}")
        except Exception as e:
            logger.error(f"Failed to load embedder: {e}")
            raise
    
    def get_available_models(self) -> List[str]:
        """
        ดึงรายชื่อโมเดล RVC ที่มีอยู่
        
        Returns:
            List[str]: รายชื่อโมเดล
        """
        models = []
        
        if not self.models_dir.exists():
            logger.warning(f"Models directory not found: {self.models_dir}")
            return models
        
        # ค้นหาไฟล์ .pth ในโฟลเดอร์ย่อย
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                pth_files = list(model_dir.glob("*.pth"))
                if pth_files:
                    # ใช้ชื่อโฟลเดอร์เป็นชื่อโมเดล
                    models.append(model_dir.name)
        
        logger.info(f"Found {len(models)} RVC models: {models}")
        return models
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        ดึงข้อมูลโมเดล
        
        Args:
            model_name: ชื่อโมเดล
            
        Returns:
            Dict: ข้อมูลโมเดล
        """
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            return {"error": f"Model {model_name} not found"}
        
        info = {
            "name": model_name,
            "path": str(model_dir),
            "files": {}
        }
        
        # ตรวจสอบไฟล์ต่างๆ
        pth_files = list(model_dir.glob("*.pth"))
        index_files = list(model_dir.glob("*.index"))
        
        info["files"]["pth"] = [f.name for f in pth_files]
        info["files"]["index"] = [f.name for f in index_files]
        
        return info
    
    def convert_voice(self, input_path: str, output_path: str, model_name: str,
                     transpose: int = 0, index_ratio: float = 0.75,
                     f0_method: str = "rmvpe", **kwargs) -> str:
        """
        แปลงเสียงด้วย RVC
        
        Args:
            input_path: ไฟล์เสียง input
            output_path: ไฟล์เสียง output
            model_name: ชื่อโมเดล RVC
            transpose: การขยับ pitch (-12 ถึง 12)
            index_ratio: อัตราส่วน index (0.0-1.0)
            f0_method: วิธีการคำนวณ f0 (rmvpe, crepe, etc.)
            
        Returns:
            str: path ของไฟล์ output
        """
        try:
            # ตรวจสอบโมเดล
            available_models = self.get_available_models()
            if model_name not in available_models:
                raise ValueError(f"Model {model_name} not found. Available: {available_models}")
            
            # โหลดโมเดลก่อนใช้งาน
            model_path = str(self.models_dir / model_name)
            # หาไฟล์ .pth ในโฟลเดอร์โมเดล
            pth_files = list(Path(model_path).glob("*.pth"))
            if pth_files:
                pth_file = str(pth_files[0])
                self.voice_converter.get_vc(pth_file, sid=0)
            else:
                raise ValueError(f"No .pth file found in {model_path}")
            
            # ใช้ voice converter
            self.voice_converter.convert_audio(
                audio_input_path=input_path,
                audio_output_path=output_path,
                model_path=model_path,
                index_path="",  # จะหา index file อัตโนมัติ
                pitch=transpose,
                f0_method=f0_method,
                index_rate=index_ratio,
                **kwargs
            )
            
            logger.info(f"Voice conversion completed: {input_path} -> {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
            raise
    
    def convert_audio_data(self, audio_data: bytes, model_name: str,
                          transpose: int = 0, index_ratio: float = 0.75,
                          f0_method: str = "rmvpe", **kwargs) -> bytes:
        """
        แปลงข้อมูลเสียง (bytes) ด้วย RVC
        
        Args:
            audio_data: ข้อมูลเสียงในรูปแบบ bytes
            model_name: ชื่อโมเดล RVC
            transpose: การขยับ pitch
            index_ratio: อัตราส่วน index
            f0_method: วิธีการ f0
            
        Returns:
            bytes: ข้อมูลเสียงที่แปลงแล้ว
        """
        import tempfile
        import soundfile as sf
        
        try:
            # สร้างไฟล์ชั่วคราว
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_input:
                temp_input.write(audio_data)
                temp_input_path = temp_input.name
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_output:
                temp_output_path = temp_output.name
            
            # แปลงเสียง
            result_path = self.convert_voice(
                input_path=temp_input_path,
                output_path=temp_output_path,
                model_name=model_name,
                transpose=transpose,
                index_ratio=index_ratio,
                f0_method=f0_method,
                **kwargs
            )
            
            # อ่านผลลัพธ์
            with open(result_path, "rb") as f:
                converted_audio = f.read()
            
            # ลบไฟล์ชั่วคราว
            os.unlink(temp_input_path)
            os.unlink(temp_output_path)
            
            return converted_audio
            
        except Exception as e:
            logger.error(f"Audio data conversion failed: {e}")
            raise
    
    def test_model(self, model_name: str) -> bool:
        """
        ทดสอบโมเดล
        
        Args:
            model_name: ชื่อโมเดล
            
        Returns:
            bool: True ถ้าโมเดลใช้งานได้
        """
        try:
            # ตรวจสอบว่าโมเดลมีอยู่
            model_info = self.get_model_info(model_name)
            if "error" in model_info:
                return False
            
            # ตรวจสอบไฟล์ที่จำเป็น
            if not model_info["files"]["pth"]:
                logger.error(f"No .pth file found for model {model_name}")
                return False
            
            logger.info(f"Model {model_name} test passed")
            return True
            
        except Exception as e:
            logger.error(f"Model {model_name} test failed: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        ดึงข้อมูลระบบ
        
        Returns:
            Dict: ข้อมูลระบบ
        """
        return {
            "device": self.device,
            "models_dir": str(self.models_dir),
            "available_models": self.get_available_models(),
            "config": {
                "weight_root": self.config.weight_root,
                "device": self.config.device
            }
        } 