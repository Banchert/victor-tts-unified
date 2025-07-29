#!/usr/bin/env python3
"""
🎤 RVC Wrapper - เวอร์ชันที่เสถียรกว่า
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
if rvc_path.exists():
    sys.path.insert(0, str(rvc_path))

logger = logging.getLogger("RVC_WRAPPER")

class RVCWrapper:
    """RVC Wrapper ที่เสถียรกว่า"""
    
    def __init__(self, device: str = "cpu", models_dir: str = "logs"):
        """
        เริ่มต้น RVC Wrapper
        
        Args:
            device: อุปกรณ์ที่ใช้ (cpu, cuda:0, etc.)
            models_dir: โฟลเดอร์ที่เก็บโมเดล
        """
        self.device = device
        self.models_dir = Path(models_dir)
        self.models_cache = {}
        self.initialized = False
        
        # ตรวจสอบ RVC availability
        self.rvc_available = self._check_rvc_availability()
        
        if self.rvc_available:
            self._initialize_rvc()
        else:
            logger.warning("⚠️ RVC not available")
    
    def _check_rvc_availability(self) -> bool:
        """ตรวจสอบว่า RVC พร้อมใช้งานหรือไม่"""
        try:
            # ตรวจสอบไฟล์สำคัญ
            required_files = [
                "rvc/infer/infer.py",
                "rvc/lib/utils.py",
                "rvc/configs/config.py"
            ]
            
            for file_path in required_files:
                if not (Path(__file__).parent / file_path).exists():
                    logger.warning(f"Missing required file: {file_path}")
                    return False
            
            # ตรวจสอบ dependencies
            try:
                import torch
                import numpy
                logger.info("✅ RVC dependencies available")
                return True
            except ImportError as e:
                logger.warning(f"Missing RVC dependencies: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking RVC availability: {e}")
            return False
    
    def _initialize_rvc(self):
        """เริ่มต้น RVC system"""
        try:
            # Import RVC modules
            from rvc.infer.infer import VoiceConverter
            from rvc.configs.config import Config
            
            self.voice_converter = VoiceConverter()
            self.config = Config()
            self.config.device = self.device
            self.config.weight_root = str(self.models_dir)
            
            # โหลด embedder
            self._load_embedder()
            
            self.initialized = True
            logger.info(f"✅ RVC initialized on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ RVC initialization failed: {e}")
            self.initialized = False
    
    def _load_embedder(self):
        """โหลด embedder model"""
        try:
            # ใช้ contentvec เป็น embedder หลัก
            embedder_model = "contentvec"
            self.voice_converter.load_hubert(embedder_model)
            logger.info(f"✅ Loaded embedder: {embedder_model}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load embedder: {e}")
            # ลองใช้ embedder อื่น
            try:
                self.voice_converter.load_hubert("contentvec")
                logger.info("✅ Loaded fallback embedder")
            except Exception as e2:
                logger.error(f"❌ All embedders failed: {e2}")
                raise
    
    def get_available_models(self) -> List[str]:
        """ดึงรายชื่อโมเดล RVC ที่มีอยู่"""
        if not self.rvc_available or not self.initialized:
            return []
        
        try:
            models = []
            if self.models_dir.exists():
                for model_dir in self.models_dir.iterdir():
                    if model_dir.is_dir() and not model_dir.name.startswith('.'):
                        # ตรวจสอบว่าเป็นโมเดลที่ถูกต้อง
                        pth_files = list(model_dir.glob("*.pth"))
                        index_files = list(model_dir.glob("*.index"))
                        
                        if pth_files and index_files:
                            models.append(model_dir.name)
            
            logger.info(f"✅ Found {len(models)} RVC models")
            return models
            
        except Exception as e:
            logger.error(f"❌ Error getting models: {e}")
            return []
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """ดึงข้อมูลโมเดล"""
        if not self.rvc_available or not self.initialized:
            return {"error": "RVC not available"}
        
        try:
            model_dir = self.models_dir / model_name
            if not model_dir.exists():
                return {"error": f"Model {model_name} not found"}
            
            # หาไฟล์ .pth และ .index
            pth_files = list(model_dir.glob("*.pth"))
            index_files = list(model_dir.glob("*.index"))
            
            return {
                "name": model_name,
                "directory": str(model_dir),
                "pth_files": [f.name for f in pth_files],
                "index_files": [f.name for f in index_files],
                "valid": len(pth_files) > 0 and len(index_files) > 0
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting model info: {e}")
            return {"error": str(e)}
    
    def convert_voice(self, input_path: str, output_path: str, model_name: str,
                     transpose: int = 0, index_ratio: float = 0.75,
                     f0_method: str = "rmvpe", **kwargs) -> str:
        """
        แปลงเสียงด้วย RVC
        
        Args:
            input_path: ไฟล์เสียงเข้า
            output_path: ไฟล์เสียงออก
            model_name: ชื่อโมเดล
            transpose: การขยับ pitch
            index_ratio: อัตราส่วน index
            f0_method: วิธีการ f0
            
        Returns:
            str: path ของไฟล์ผลลัพธ์
        """
        if not self.rvc_available or not self.initialized:
            raise Exception("RVC not available or not initialized")
        
        try:
            # ตรวจสอบไฟล์เข้า
            if not Path(input_path).exists():
                raise Exception(f"Input file not found: {input_path}")
            
            # ตรวจสอบโมเดล
            model_info = self.get_model_info(model_name)
            if "error" in model_info:
                raise Exception(f"Model error: {model_info['error']}")
            
            if not model_info.get("valid", False):
                raise Exception(f"Model {model_name} is not valid")
            
            logger.info(f"🎤 Converting voice with model: {model_name}")
            logger.info(f"📁 Input: {input_path}")
            logger.info(f"📁 Output: {output_path}")
            
            # แปลงเสียง
            # หาไฟล์ .pth และ .index
            model_dir = self.models_dir / model_name
            pth_files = list(model_dir.glob("*.pth"))
            index_files = list(model_dir.glob("*.index"))
            
            if not pth_files or not index_files:
                raise Exception(f"Model {model_name} missing .pth or .index files")
            
            model_path = str(pth_files[0])
            index_path = str(index_files[0])
            
            result_path = self.voice_converter.convert_audio(
                audio_input_path=input_path,
                audio_output_path=output_path,
                model_path=model_path,
                index_path=index_path,
                pitch=transpose,
                f0_method=f0_method,
                index_rate=index_ratio,
                **kwargs
            )
            
            # ตรวจสอบว่า result_path เป็น None หรือไม่
            if result_path is None:
                result_path = output_path
            
            # ตรวจสอบผลลัพธ์
            if not Path(result_path).exists():
                raise Exception("Conversion failed - output file not created")
            
            logger.info(f"✅ Voice conversion completed: {result_path}")
            return result_path
            
        except Exception as e:
            logger.error(f"❌ Voice conversion failed: {e}")
            raise
    
    def convert_audio_data(self, audio_data: bytes, model_name: str,
                          transpose: int = 0, index_ratio: float = 0.75,
                          f0_method: str = "rmvpe", **kwargs) -> bytes:
        """
        แปลงข้อมูลเสียง bytes
        
        Args:
            audio_data: ข้อมูลเสียง
            model_name: ชื่อโมเดล
            transpose: การขยับ pitch
            index_ratio: อัตราส่วน index
            f0_method: วิธีการ f0
            
        Returns:
            bytes: ข้อมูลเสียงที่แปลงแล้ว
        """
        try:
            # สร้างไฟล์ชั่วคราว
            import tempfile
            import time
            
            timestamp = int(time.time() * 1000)
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_input:
                temp_input.write(audio_data)
                temp_input_path = temp_input.name
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
                temp_output_path = temp_output.name
            
            try:
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
                with open(result_path, 'rb') as f:
                    converted_audio = f.read()
                
                return converted_audio
                
            finally:
                # ลบไฟล์ชั่วคราว
                try:
                    os.unlink(temp_input_path)
                    os.unlink(temp_output_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"❌ Audio data conversion failed: {e}")
            raise
    
    def test_model(self, model_name: str) -> bool:
        """ทดสอบโมเดล"""
        try:
            model_info = self.get_model_info(model_name)
            if "error" in model_info:
                logger.error(f"❌ Model test failed: {model_info['error']}")
                return False
            
            if not model_info.get("valid", False):
                logger.error(f"❌ Model {model_name} is not valid")
                return False
            
            logger.info(f"✅ Model {model_name} test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Model test failed: {e}")
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """ดึงข้อมูลระบบ"""
        return {
            "rvc_available": self.rvc_available,
            "initialized": self.initialized,
            "device": self.device,
            "models_dir": str(self.models_dir),
            "models_count": len(self.get_available_models()),
            "torch_available": "torch" in sys.modules,
            "cuda_available": torch.cuda.is_available() if "torch" in sys.modules else False
        }

# Helper functions
def create_rvc_wrapper(**kwargs):
    """สร้าง RVC wrapper instance"""
    return RVCWrapper(**kwargs)

def test_rvc_system():
    """ทดสอบระบบ RVC"""
    print("🧪 Testing RVC system...")
    
    wrapper = create_rvc_wrapper()
    info = wrapper.get_system_info()
    
    print(f"✅ RVC System Info: {info}")
    
    if info["rvc_available"] and info["initialized"]:
        models = wrapper.get_available_models()
        print(f"✅ Available models: {models}")
        
        if models:
            # ทดสอบโมเดลแรก
            test_model = models[0]
            if wrapper.test_model(test_model):
                print(f"✅ Model {test_model} test passed")
            else:
                print(f"❌ Model {test_model} test failed")
    else:
        print("❌ RVC system not available")

if __name__ == "__main__":
    test_rvc_system()
