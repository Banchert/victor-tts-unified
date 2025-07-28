#!/usr/bin/env python3
"""
🧪 Fixed RVC Testing Script
ทดสอบการทำงานของ RVC หลังจากแก้ไข
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
logger = logging.getLogger("RVC_FIXED_TEST")

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class RVCFixedTester:
    """ทดสอบ RVC หลังจากแก้ไข"""
    
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
    
    def test_1_rvc_api_import(self):
        """ทดสอบการ import RVC API"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 1: RVC API Import")
        logger.info("=" * 60)
        
        try:
            from rvc_api import RVCConverter
            self.log_test("RVC API Import", True, "Successfully imported RVCConverter")
        except ImportError as e:
            self.log_test("RVC API Import", False, f"Import failed: {e}")
        except Exception as e:
            self.log_test("RVC API Import", False, f"Error: {e}")
    
    def test_2_rvc_converter_creation(self):
        """ทดสอบการสร้าง RVC Converter"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 2: RVC Converter Creation")
        logger.info("=" * 60)
        
        try:
            from rvc_api import RVCConverter
            
            # สร้าง converter
            converter = RVCConverter(device="cpu", models_dir="logs")
            self.log_test("RVC Converter Creation", True, "Successfully created")
            
            # ทดสอบ system info
            system_info = converter.get_system_info()
            self.log_test("System Info", True, f"Device: {system_info['device']}")
            
            return converter
            
        except Exception as e:
            self.log_test("RVC Converter Creation", False, f"Error: {e}")
            return None
    
    def test_3_model_detection(self, converter=None):
        """ทดสอบการตรวจจับโมเดล"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 3: Model Detection")
        logger.info("=" * 60)
        
        if converter is None:
            try:
                from rvc_api import RVCConverter
                converter = RVCConverter(device="cpu", models_dir="logs")
            except Exception as e:
                self.log_test("Model Detection", False, f"Converter creation failed: {e}")
                return None
        
        try:
            # ดึงรายชื่อโมเดล
            models = converter.get_available_models()
            self.log_test("Available Models", len(models) > 0, f"Found {len(models)} models")
            
            if models:
                logger.info("📁 Available RVC Models:")
                for model in models:
                    logger.info(f"   - {model}")
                
                # ทดสอบข้อมูลโมเดลแรก
                first_model = models[0]
                model_info = converter.get_model_info(first_model)
                self.log_test("Model Info", "error" not in model_info, 
                             f"Model {first_model}: {len(model_info.get('files', {}).get('pth', []))} .pth files")
                
                return models
            else:
                self.log_test("Model Detection", False, "No models found")
                return []
                
        except Exception as e:
            self.log_test("Model Detection", False, f"Error: {e}")
            return []
    
    def test_4_model_testing(self, converter=None, models=None):
        """ทดสอบโมเดล"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 4: Model Testing")
        logger.info("=" * 60)
        
        if converter is None or not models:
            self.log_test("Model Testing", False, "No converter or models available")
            return
        
        try:
            # ทดสอบโมเดลแรก
            test_model = models[0]
            is_valid = converter.test_model(test_model)
            self.log_test("Model Validation", is_valid, f"Model {test_model} validation")
            
        except Exception as e:
            self.log_test("Model Testing", False, f"Error: {e}")
    
    async def test_5_tts_rvc_integration(self):
        """ทดสอบการทำงานรวม TTS-RVC"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 5: TTS-RVC Integration")
        logger.info("=" * 60)
        
        try:
            from tts_rvc_core import create_core_instance
            
            # สร้าง core instance
            core = create_core_instance()
            self.log_test("Core Instance", True, "Successfully created")
            
            # ตรวจสอบสถานะ
            status = core.get_system_status()
            self.log_test("System Status", True, f"TTS: {status['tts_available']}, RVC: {status['rvc_available']}")
            
            # ตรวจสอบโมเดล RVC
            models = core.get_available_rvc_models()
            self.log_test("RVC Models in Core", len(models) > 0, f"Found {len(models)} models")
            
            if models:
                logger.info("📁 RVC Models in Core:")
                for model in models:
                    logger.info(f"   - {model}")
            
            # ทดสอบ TTS
            test_text = "Hello, this is a test of the TTS system."
            tts_audio = await core.generate_tts(test_text, "en-US-AndrewNeural", 1.0)
            self.log_test("TTS Generation", len(tts_audio) > 0, f"Generated {len(tts_audio)} bytes")
            
            # ทดสอบ RVC conversion (ถ้ามีโมเดล)
            if models and status['rvc_available']:
                try:
                    converted_audio = core.convert_voice(
                        tts_audio, 
                        models[0], 
                        transpose=0, 
                        index_ratio=0.75, 
                        f0_method="rmvpe"
                    )
                    self.log_test("RVC Conversion", len(converted_audio) > 0, 
                                 f"Converted using {models[0]}")
                except Exception as e:
                    self.log_test("RVC Conversion", False, f"Error: {e}")
            else:
                self.log_test("RVC Conversion", False, "No models or RVC not available")
            
        except Exception as e:
            self.log_test("TTS-RVC Integration", False, f"Error: {e}")
    
    def test_6_audio_processing(self):
        """ทดสอบการประมวลผลเสียง"""
        logger.info("=" * 60)
        logger.info("🧪 TEST 6: Audio Processing")
        logger.info("=" * 60)
        
        try:
            import numpy as np
            import soundfile as sf
            
            # สร้างเสียงทดสอบ
            sample_rate = 44100
            duration = 1.0
            frequency = 440  # A4 note
            
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio_data = np.sin(2 * np.pi * frequency * t)
            
            # บันทึกไฟล์
            test_file = "test_audio.wav"
            sf.write(test_file, audio_data, sample_rate)
            
            # อ่านไฟล์
            loaded_audio, loaded_sr = sf.read(test_file)
            
            # ลบไฟล์
            os.remove(test_file)
            
            self.log_test("Audio Processing", len(loaded_audio) > 0, 
                         f"Created and loaded {len(loaded_audio)} samples")
            
        except Exception as e:
            self.log_test("Audio Processing", False, f"Error: {e}")
    
    def generate_report(self):
        """สร้างรายงานการทดสอบ"""
        logger.info("=" * 60)
        logger.info("📊 FIXED TEST REPORT")
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
        
        with open("rvc_fixed_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        logger.info("📄 Fixed test report saved to: rvc_fixed_test_report.json")
        
        # Show failed tests
        if failed_tests > 0:
            logger.info("❌ Failed Tests:")
            for test_name, result in self.test_results.items():
                if not result["passed"]:
                    logger.info(f"   - {test_name}: {result['details']}")
    
    async def run_all_tests(self):
        """รันการทดสอบทั้งหมด"""
        logger.info("🚀 Starting Fixed RVC Testing...")
        logger.info(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run tests
        self.test_1_rvc_api_import()
        converter = self.test_2_rvc_converter_creation()
        models = self.test_3_model_detection(converter)
        self.test_4_model_testing(converter, models)
        await self.test_5_tts_rvc_integration()
        self.test_6_audio_processing()
        
        # Generate report
        self.generate_report()
        
        logger.info("🎉 Fixed testing completed!")

async def main():
    """Main function"""
    tester = RVCFixedTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 