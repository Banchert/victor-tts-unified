#!/usr/bin/env python3
"""
Test script to verify RVC MP3 conversion fix
"""
import asyncio
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_rvc_mp3_conversion():
    """Test RVC with MP3 input from Edge TTS"""
    try:
        from tts_rvc_core import TTSRVCCore
        
        # Initialize core
        logger.info("Initializing TTS-RVC Core...")
        core = TTSRVCCore()
        
        # Test parameters
        test_text = "สวัสดีครับ ทดสอบระบบ RVC กับไฟล์ MP3 จาก Edge TTS"
        tts_voice = "th-TH-PremwadeeNeural"
        rvc_model = "STS73"  # Use one of your available models
        
        # Step 1: Generate TTS (returns MP3)
        logger.info("Step 1: Generating TTS audio...")
        tts_audio = await core.generate_tts(
            text=test_text,
            voice=tts_voice,
            speed=1.0,
            pitch="+0Hz"
        )
        logger.info(f"TTS generated: {len(tts_audio)} bytes")
        
        # Save TTS output for inspection
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        tts_file = output_dir / "test_tts_output.mp3"
        with open(tts_file, "wb") as f:
            f.write(tts_audio)
        logger.info(f"Saved TTS output to: {tts_file}")
        
        # Step 2: Convert voice with RVC
        logger.info(f"Step 2: Converting voice with RVC model '{rvc_model}'...")
        try:
            rvc_audio = core.convert_voice(
                audio_data=tts_audio,
                model_name=rvc_model,
                transpose=0,
                index_ratio=0.75,
                f0_method="rmvpe"
            )
            logger.info(f"RVC conversion successful: {len(rvc_audio)} bytes")
            
            # Save RVC output
            rvc_file = output_dir / "test_rvc_output.wav"
            with open(rvc_file, "wb") as f:
                f.write(rvc_audio)
            logger.info(f"Saved RVC output to: {rvc_file}")
            
            return True
            
        except Exception as rvc_error:
            logger.error(f"RVC conversion failed: {rvc_error}")
            return False
            
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_unified_process():
    """Test unified TTS + RVC process"""
    try:
        from tts_rvc_core import TTSRVCCore
        
        # Initialize core
        logger.info("\n" + "="*60)
        logger.info("Testing Unified TTS + RVC Process")
        logger.info("="*60)
        
        core = TTSRVCCore()
        
        # Test parameters
        test_text = "Hello, this is a test. สวัสดีครับ นี่คือการทดสอบ"
        tts_voice = "th-TH-PremwadeeNeural"
        rvc_model = "STS73"
        
        # Process unified
        logger.info("Processing unified TTS + RVC...")
        result = await core.process_unified(
            text=test_text,
            tts_voice=tts_voice,
            enable_rvc=True,
            rvc_model=rvc_model,
            enable_multi_language=True
        )
        
        # Check results
        if result["success"]:
            logger.info("✅ Unified process successful!")
            logger.info(f"   - TTS audio: {len(result.get('tts_audio', b''))} bytes")
            logger.info(f"   - RVC audio: {len(result.get('rvc_audio', b''))} bytes")
            logger.info(f"   - Process steps: {result.get('process_steps', [])}")
            
            # Save outputs
            output_dir = Path("test_output")
            output_dir.mkdir(exist_ok=True)
            
            if result.get('tts_audio'):
                with open(output_dir / "unified_tts.mp3", "wb") as f:
                    f.write(result['tts_audio'])
                    
            if result.get('rvc_audio'):
                with open(output_dir / "unified_rvc.wav", "wb") as f:
                    f.write(result['rvc_audio'])
                    
            return True
        else:
            logger.error(f"❌ Unified process failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"Unified test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    logger.info("🧪 Starting RVC MP3 Conversion Tests")
    logger.info("="*60)
    
    # Test 1: Direct conversion
    test1_result = await test_rvc_mp3_conversion()
    logger.info(f"\nTest 1 (Direct Conversion): {'✅ PASSED' if test1_result else '❌ FAILED'}")
    
    # Test 2: Unified process
    test2_result = await test_unified_process()
    logger.info(f"\nTest 2 (Unified Process): {'✅ PASSED' if test2_result else '❌ FAILED'}")
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 Test Summary:")
    logger.info(f"   - Direct Conversion: {'✅ PASSED' if test1_result else '❌ FAILED'}")
    logger.info(f"   - Unified Process: {'✅ PASSED' if test2_result else '❌ FAILED'}")
    logger.info(f"   - Overall: {'✅ ALL TESTS PASSED' if test1_result and test2_result else '❌ SOME TESTS FAILED'}")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(main()) 