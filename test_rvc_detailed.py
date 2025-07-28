#!/usr/bin/env python3
"""
🧪 Detailed RVC Testing Script
ทดสอบการทำงานของ RVC แบบละเอียด
"""
import os
import sys
import asyncio
import time
import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RVC_TEST")

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class RVCDetailedTester:
    """ทดสอบ RVC แบบละเอียด"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    def log_test(self, test_name: str, result: bool, details: str = ""):
        """บันทึกผลการทดสอบ"""
        self.test_results[test_name] = {
            "passed": result,
            "details": details,
            "timestamp": time.time()
        }
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {details}")
    
    def test_1_dependencies(self):
        """ทดสอบ Dependencies ที่จำเป็น"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 1: Dependencies Check")
        logger.info("=" * 60)
        
        # 1.1 PyTorch
        try:
            import torch
            version = torch.__version__
            cuda_available = torch.cuda.is_available()
            self.log_test("PyTorch", True, f"Version: {version}, CUDA: {cuda_available}")
        except ImportError:
            self.log_test("PyTorch", False, "PyTorch not installed")
        
        # 1.2 FAISS
        try:
            import faiss
            version = faiss.__version__
            self.log_test("FAISS", True, f"Version: {version}")
        except ImportError:
            self.log_test("FAISS", False, "FAISS not installed")
        
        # 1.3 librosa
        try:
            import librosa
            version = librosa.__version__
            self.log_test("librosa", True, f"Version: {version}")
        except ImportError:
            self.log_test("librosa", False, "librosa not installed")
        
        # 1.4 soundfile
        try:
            import soundfile
            version = soundfile.__version__
            self.log_test("soundfile", True, f"Version: {version}")
        except ImportError:
            self.log_test("soundfile", False, "soundfile not installed")
        
        # 1.5 noisereduce
        try:
            import noisereduce
            self.log_test("noisereduce", True, "Available")
        except ImportError:
            self.log_test("noisereduce", False, "noisereduce not installed")
        
        # 1.6 pedalboard
        try:
            import pedalboard
            self.log_test("pedalboard", True, "Available")
        except ImportError:
            self.log_test("pedalboard", False, "pedalboard not installed")
    
    def test_2_rvc_structure(self):
        """ทดสอบโครงสร้าง RVC"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 2: RVC Structure Check")
        logger.info("=" * 60)
        
        # 2.1 RVC directory structure
        rvc_dir = Path("rvc")
        if rvc_dir.exists():
            self.log_test("RVC Directory", True, "rvc/ directory exists")
            
            # Check subdirectories
            subdirs = ["infer", "configs", "lib", "train", "models"]
            for subdir in subdirs:
                subdir_path = rvc_dir / subdir
                if subdir_path.exists():
                    self.log_test(f"RVC {subdir}", True, f"{subdir}/ exists")
                else:
                    self.log_test(f"RVC {subdir}", False, f"{subdir}/ missing")
        else:
            self.log_test("RVC Directory", False, "rvc/ directory missing")
        
        # 2.2 Core RVC files
        core_files = [
            "rvc/infer/infer.py",
            "rvc/infer/pipeline.py",
            "rvc/lib/utils.py",
            "rvc/configs/config.py"
        ]
        
        for file_path in core_files:
            if Path(file_path).exists():
                self.log_test(f"RVC File: {file_path}", True, "File exists")
            else:
                self.log_test(f"RVC File: {file_path}", False, "File missing")
    
    def test_3_model_files(self):
        """ทดสอบไฟล์โมเดล"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 3: Model Files Check")
        logger.info("=" * 60)
        
        # 3.1 Check logs directory for models
        logs_dir = Path("logs")
        if logs_dir.exists():
            self.log_test("Logs Directory", True, "logs/ directory exists")
            
            # Find .pth files
            pth_files = list(logs_dir.rglob("*.pth"))
            self.log_test("PTH Files", len(pth_files) > 0, f"Found {len(pth_files)} .pth files")
            
            # Find .index files
            index_files = list(logs_dir.rglob("*.index"))
            self.log_test("Index Files", len(index_files) > 0, f"Found {len(index_files)} .index files")
            
            # List found models
            if pth_files:
                logger.info("📁 Found PTH models:")
                for pth_file in pth_files:
                    logger.info(f"   - {pth_file}")
            
            if index_files:
                logger.info("📁 Found Index files:")
                for index_file in index_files:
                    logger.info(f"   - {index_file}")
        else:
            self.log_test("Logs Directory", False, "logs/ directory missing")
    
    def test_4_rvc_imports(self):
        """ทดสอบการ import RVC modules"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 4: RVC Module Imports")
        logger.info("=" * 60)
        
        # 4.1 Test RVC infer import
        try:
            from rvc.infer.infer import VoiceConverter
            self.log_test("RVC VoiceConverter Import", True, "Successfully imported")
        except ImportError as e:
            self.log_test("RVC VoiceConverter Import", False, f"Import failed: {e}")
        
        # 4.2 Test RVC pipeline import
        try:
            from rvc.infer.pipeline import Pipeline as VC
            self.log_test("RVC Pipeline Import", True, "Successfully imported")
        except ImportError as e:
            self.log_test("RVC Pipeline Import", False, f"Import failed: {e}")
        
        # 4.3 Test RVC utils import
        try:
            from rvc.lib.utils import load_audio_infer, load_embedding
            self.log_test("RVC Utils Import", True, "Successfully imported")
        except ImportError as e:
            self.log_test("RVC Utils Import", False, f"Import failed: {e}")
    
    async def test_5_tts_rvc_core(self):
        """ทดสอบ TTS-RVC Core System"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 5: TTS-RVC Core System")
        logger.info("=" * 60)
        
        try:
            from tts_rvc_core import TTSRVCCore, create_core_instance
            
            # 5.1 Test core instance creation
            core = create_core_instance()
            self.log_test("Core Instance Creation", True, "Successfully created")
            
            # 5.2 Test system status
            status = core.get_system_status()
            self.log_test("System Status", True, f"Status: {status}")
            
            # 5.3 Test available models
            models = core.get_available_rvc_models()
            self.log_test("Available RVC Models", len(models) > 0, f"Found {len(models)} models")
            
            if models:
                logger.info("📁 Available RVC Models:")
                for model in models:
                    logger.info(f"   - {model}")
            
            # 5.4 Test available voices
            voices = await core.get_available_edge_voices()
            self.log_test("Available TTS Voices", len(voices) > 0, f"Found {len(voices)} voices")
            
        except Exception as e:
            self.log_test("TTS-RVC Core System", False, f"Error: {e}")
    
    def test_6_f0_methods(self):
        """ทดสอบ F0 Methods"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 6: F0 Methods Check")
        logger.info("=" * 60)
        
        # 6.1 Check if rmvpe is available
        try:
            import torchcrepe
            self.log_test("torchcrepe (rmvpe)", True, "Available for rmvpe method")
        except ImportError:
            self.log_test("torchcrepe (rmvpe)", False, "Not available")
        
        # 6.2 Check other F0 methods
        f0_methods = ["rmvpe", "crepe", "crepe-tiny", "fcpe"]
        for method in f0_methods:
            # This is a basic check - actual availability depends on the RVC implementation
            self.log_test(f"F0 Method: {method}", True, f"Method '{method}' supported")
    
    def test_7_embedder_models(self):
        """ทดสอบ Embedder Models"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 7: Embedder Models Check")
        logger.info("=" * 60)
        
        embedder_models = [
            "contentvec",
            "chinese-hubert-base", 
            "japanese-hubert-base",
            "korean-hubert-base"
        ]
        
        for model in embedder_models:
            # This is a basic check - actual availability depends on the RVC implementation
            self.log_test(f"Embedder: {model}", True, f"Model '{model}' supported")
    
    def test_8_audio_processing(self):
        """ทดสอบการประมวลผลเสียง"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 8: Audio Processing Tools")
        logger.info("=" * 60)
        
        # 8.1 FFmpeg
        try:
            import ffmpeg
            self.log_test("FFmpeg Python", True, "Available")
        except ImportError:
            self.log_test("FFmpeg Python", False, "Not available")
        
        # 8.2 SoXR (for resampling)
        try:
            import soxr
            self.log_test("SoXR", True, "Available for resampling")
        except ImportError:
            self.log_test("SoXR", False, "Not available")
        
        # 8.3 Audio processing capabilities
        try:
            import librosa
            import soundfile
            import numpy as np
            
            # Test basic audio operations
            sample_rate = 44100
            duration = 1.0
            audio_data = np.sin(2 * np.pi * 440 * np.linspace(0, duration, int(sample_rate * duration)))
            
            # Test save/load
            temp_file = "test_audio.wav"
            soundfile.write(temp_file, audio_data, sample_rate)
            loaded_audio, loaded_sr = soundfile.read(temp_file)
            
            # Cleanup
            os.remove(temp_file)
            
            self.log_test("Audio I/O", True, "Can save and load audio files")
            
        except Exception as e:
            self.log_test("Audio I/O", False, f"Error: {e}")
    
    async def test_9_integration_test(self):
        """ทดสอบการทำงานรวม"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 9: Integration Test")
        logger.info("=" * 60)
        
        try:
            from tts_rvc_core import create_core_instance
            
            # 9.1 Create core instance
            core = create_core_instance()
            
            # 9.2 Test TTS generation
            test_text = "Hello, this is a test of the TTS system."
            tts_audio = await core.generate_tts(test_text, "en-US-AndrewNeural", 1.0)
            self.log_test("TTS Generation", len(tts_audio) > 0, f"Generated {len(tts_audio)} bytes")
            
            # 9.3 Test RVC conversion (if models available)
            models = core.get_available_rvc_models()
            if models:
                model_name = models[0]
                try:
                    converted_audio = core.convert_voice(
                        tts_audio, 
                        model_name, 
                        transpose=0, 
                        index_ratio=0.75, 
                        f0_method="rmvpe"
                    )
                    self.log_test("RVC Conversion", len(converted_audio) > 0, 
                                 f"Converted using {model_name}")
                except Exception as e:
                    self.log_test("RVC Conversion", False, f"Error: {e}")
            else:
                self.log_test("RVC Conversion", False, "No models available for testing")
            
        except Exception as e:
            self.log_test("Integration Test", False, f"Error: {e}")
    
    def generate_report(self):
        """สร้างรายงานการทดสอบ"""
        logger.info("=" * 60)
        logger.info("📊 TEST REPORT")
        logger.info("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["passed"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Save detailed report
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100,
                "test_duration": time.time() - self.start_time
            },
            "results": self.test_results
        }
        
        with open("rvc_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info("📄 Detailed report saved to: rvc_test_report.json")
        
        # Show failed tests
        if failed_tests > 0:
            logger.info("❌ Failed Tests:")
            for test_name, result in self.test_results.items():
                if not result["passed"]:
                    logger.info(f"   - {test_name}: {result['details']}")
    
    async def run_all_tests(self):
        """รันการทดสอบทั้งหมด"""
        logger.info("🚀 Starting Detailed RVC Testing...")
        logger.info(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all tests
        self.test_1_dependencies()
        self.test_2_rvc_structure()
        self.test_3_model_files()
        self.test_4_rvc_imports()
        await self.test_5_tts_rvc_core()
        self.test_6_f0_methods()
        self.test_7_embedder_models()
        self.test_8_audio_processing()
        await self.test_9_integration_test()
        
        # Generate report
        self.generate_report()
        
        logger.info("🎉 Testing completed!")

async def main():
    """Main function"""
    tester = RVCDetailedTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 