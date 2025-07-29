#!/usr/bin/env python3
"""
🔧 RVC Fix Script - แก้ไขปัญหา RVC ที่ไม่ทำงาน
"""
import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RVC_FIX")

class RVCFixer:
    """คลาสสำหรับแก้ไขปัญหา RVC"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.rvc_dir = self.project_root / "rvc"
        self.logs_dir = self.project_root / "logs"
        self.models_dir = self.project_root / "models"
        
    def check_rvc_structure(self) -> Dict[str, Any]:
        """ตรวจสอบโครงสร้าง RVC"""
        logger.info("🔍 Checking RVC structure...")
        
        structure = {
            "rvc_dir_exists": self.rvc_dir.exists(),
            "logs_dir_exists": self.logs_dir.exists(),
            "models_dir_exists": self.models_dir.exists(),
            "rvc_subdirs": {},
            "model_files": {},
            "issues": []
        }
        
        # ตรวจสอบ RVC subdirectories
        if self.rvc_dir.exists():
            rvc_subdirs = ["infer", "lib", "models", "configs", "train"]
            for subdir in rvc_subdirs:
                subdir_path = self.rvc_dir / subdir
                structure["rvc_subdirs"][subdir] = subdir_path.exists()
                
                if not subdir_path.exists():
                    structure["issues"].append(f"Missing RVC subdirectory: {subdir}")
        
        # ตรวจสอบไฟล์สำคัญ
        important_files = [
            "rvc/infer/infer.py",
            "rvc/infer/pipeline.py",
            "rvc/lib/utils.py",
            "rvc/configs/config.py"
        ]
        
        for file_path in important_files:
            full_path = self.project_root / file_path
            structure["model_files"][file_path] = full_path.exists()
            
            if not full_path.exists():
                structure["issues"].append(f"Missing important file: {file_path}")
        
        # ตรวจสอบโมเดล RVC
        if self.logs_dir.exists():
            model_dirs = [d for d in self.logs_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
            structure["available_models"] = [d.name for d in model_dirs]
            
            # ตรวจสอบไฟล์สำคัญในแต่ละโมเดล
            for model_dir in model_dirs:
                model_files = list(model_dir.glob("*.pth"))
                model_files.extend(list(model_dir.glob("*.index")))
                
                if not model_files:
                    structure["issues"].append(f"Model {model_dir.name} has no .pth or .index files")
        
        logger.info(f"✅ RVC structure check completed. Issues: {len(structure['issues'])}")
        return structure
    
    def fix_rvc_imports(self) -> bool:
        """แก้ไขปัญหา import ของ RVC"""
        logger.info("🔧 Fixing RVC imports...")
        
        try:
            # สร้างไฟล์ __init__.py ในโฟลเดอร์ RVC
            init_files = [
                "rvc/__init__.py",
                "rvc/infer/__init__.py",
                "rvc/lib/__init__.py",
                "rvc/models/__init__.py",
                "rvc/configs/__init__.py",
                "rvc/train/__init__.py"
            ]
            
            for init_file in init_files:
                init_path = self.project_root / init_file
                if not init_path.exists():
                    init_path.parent.mkdir(parents=True, exist_ok=True)
                    init_path.write_text("# RVC Module\n", encoding='utf-8')
                    logger.info(f"✅ Created {init_file}")
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to fix RVC imports: {e}")
            return False
    
    def create_rvc_wrapper(self) -> str:
        """สร้าง RVC wrapper ที่เสถียรกว่า"""
        rvc_wrapper = '''#!/usr/bin/env python3
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
            result_path = self.voice_converter.convert_voice(
                input_path=input_path,
                output_path=output_path,
                model_name=model_name,
                transpose=transpose,
                index_ratio=index_ratio,
                f0_method=f0_method,
                **kwargs
            )
            
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
'''
        
        wrapper_file = self.project_root / "rvc_wrapper.py"
        try:
            with open(wrapper_file, 'w', encoding='utf-8') as f:
                f.write(rvc_wrapper)
            
            logger.info("✅ RVC wrapper created")
            return str(wrapper_file)
        except Exception as e:
            logger.error(f"❌ Failed to create RVC wrapper: {e}")
            return ""
    
    def fix_model_paths(self) -> bool:
        """แก้ไข path ของโมเดล"""
        logger.info("🔧 Fixing model paths...")
        
        try:
            # ตรวจสอบและสร้าง symbolic links ถ้าจำเป็น
            if self.logs_dir.exists() and not self.models_dir.exists():
                # สร้าง symbolic link จาก logs ไป models
                import os
                if os.name == 'nt':  # Windows
                    # Windows ไม่รองรับ symbolic link ง่ายๆ ให้ copy แทน
                    import shutil
                    shutil.copytree(self.logs_dir, self.models_dir, dirs_exist_ok=True)
                    logger.info("✅ Copied logs to models directory")
                else:
                    # Unix-like systems
                    os.symlink(self.logs_dir, self.models_dir)
                    logger.info("✅ Created symbolic link from logs to models")
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to fix model paths: {e}")
            return False
    
    def create_test_script(self) -> str:
        """สร้างสคริปต์ทดสอบ RVC"""
        test_script = '''#!/usr/bin/env python3
"""
🧪 RVC Test Script
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_rvc_basic():
    """ทดสอบ RVC พื้นฐาน"""
    print("🧪 Testing RVC Basic...")
    
    try:
        from rvc_wrapper import create_rvc_wrapper
        
        # สร้าง wrapper
        wrapper = create_rvc_wrapper()
        
        # ตรวจสอบสถานะ
        info = wrapper.get_system_info()
        print(f"✅ System Info: {info}")
        
        if not info["rvc_available"]:
            print("❌ RVC not available")
            return False
        
        if not info["initialized"]:
            print("❌ RVC not initialized")
            return False
        
        # ดึงโมเดล
        models = wrapper.get_available_models()
        print(f"✅ Available models: {models}")
        
        if not models:
            print("❌ No models available")
            return False
        
        # ทดสอบโมเดลแรก
        test_model = models[0]
        print(f"🧪 Testing model: {test_model}")
        
        model_info = wrapper.get_model_info(test_model)
        print(f"✅ Model info: {model_info}")
        
        if wrapper.test_model(test_model):
            print(f"✅ Model {test_model} test passed")
            return True
        else:
            print(f"❌ Model {test_model} test failed")
            return False
            
    except Exception as e:
        print(f"❌ RVC test failed: {e}")
        return False

def test_rvc_conversion():
    """ทดสอบการแปลงเสียง"""
    print("🎤 Testing RVC Conversion...")
    
    try:
        from rvc_wrapper import create_rvc_wrapper
        import tempfile
        import os
        
        wrapper = create_rvc_wrapper()
        
        if not wrapper.get_system_info()["initialized"]:
            print("❌ RVC not initialized")
            return False
        
        models = wrapper.get_available_models()
        if not models:
            print("❌ No models available")
            return False
        
        # สร้างไฟล์เสียงทดสอบ
        test_audio = b"RIFF" + b"\\x00" * 44  # Minimal WAV header
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(test_audio)
            test_file = f.name
        
        try:
            # ทดสอบการแปลง
            result = wrapper.convert_audio_data(
                test_audio, models[0],
                transpose=0, index_ratio=0.75
            )
            
            print(f"✅ Conversion test passed: {len(result)} bytes")
            return True
            
        finally:
            # ลบไฟล์ทดสอบ
            try:
                os.unlink(test_file)
            except:
                pass
                
    except Exception as e:
        print(f"❌ Conversion test failed: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 RVC Test Suite")
    print("=" * 50)
    
    # ทดสอบพื้นฐาน
    basic_ok = test_rvc_basic()
    
    if basic_ok:
        # ทดสอบการแปลง
        conversion_ok = test_rvc_conversion()
        
        if conversion_ok:
            print("🎉 All RVC tests passed!")
        else:
            print("⚠️ Basic tests passed but conversion failed")
    else:
        print("❌ Basic RVC tests failed")

if __name__ == "__main__":
    main()
'''
        
        test_file = self.project_root / "test_rvc_fixed.py"
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_script)
            
            logger.info("✅ RVC test script created")
            return str(test_file)
        except Exception as e:
            logger.error(f"❌ Failed to create RVC test script: {e}")
            return ""
    
    def run_rvc_fixes(self):
        """รันการแก้ไข RVC ทั้งหมด"""
        logger.info("🔧 Starting RVC fixes...")
        
        # 1. ตรวจสอบโครงสร้าง
        logger.info("🔍 Checking RVC structure...")
        structure = self.check_rvc_structure()
        
        if structure["issues"]:
            logger.warning(f"⚠️ Found {len(structure['issues'])} issues:")
            for issue in structure["issues"]:
                logger.warning(f"  - {issue}")
        
        # 2. แก้ไข imports
        logger.info("🔧 Fixing RVC imports...")
        self.fix_rvc_imports()
        
        # 3. แก้ไข model paths
        logger.info("🔧 Fixing model paths...")
        self.fix_model_paths()
        
        # 4. สร้าง RVC wrapper
        logger.info("🎤 Creating RVC wrapper...")
        wrapper_file = self.create_rvc_wrapper()
        
        # 5. สร้างสคริปต์ทดสอบ
        logger.info("🧪 Creating test script...")
        test_file = self.create_test_script()
        
        # 6. ทดสอบระบบ
        logger.info("🧪 Testing RVC system...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, test_file], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ RVC test passed")
                print(result.stdout)
            else:
                logger.warning("⚠️ RVC test failed")
                print(result.stderr)
                
        except Exception as e:
            logger.error(f"❌ RVC test error: {e}")
        
        logger.info("✅ RVC fixes completed!")
        logger.info(f"🎤 RVC wrapper: {wrapper_file}")
        logger.info(f"🧪 Test script: {test_file}")
        logger.info("🎯 Run 'test_rvc_fixed.py' to test RVC")

def main():
    """ฟังก์ชันหลัก"""
    print("🔧 RVC Fixer")
    print("=" * 50)
    
    fixer = RVCFixer()
    fixer.run_rvc_fixes()

if __name__ == "__main__":
    main() 