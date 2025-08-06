#!/usr/bin/env python3
"""
🎯 Enhanced VICTOR-TTS API Server
รวมฟีเจอร์ใหม่และการจัดการข้อผิดพลาดที่ดีขึ้น
"""

import os
import sys
import asyncio
import logging
import base64
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import torch

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import enhanced modules
try:
    from rvc_api_enhanced import get_enhanced_rvc_converter, cleanup_enhanced_rvc
    from tts_rvc_core import TTSRVCCore, create_core_instance
    ENHANCED_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Enhanced modules not available: {e}")
    ENHANCED_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("VICTOR_TTS_ENHANCED")

# Initialize FastAPI app
app = FastAPI(
    title="VICTOR-TTS Enhanced API",
    description="Enhanced Text-to-Speech and Voice Conversion API",
    version="2.0.0"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Global instances
core_instance = None
rvc_converter = None

# Performance configuration
PERFORMANCE_CONFIG = {
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

# Request models
class TTSRequest(BaseModel):
    text: str
    voice: str = "th-TH-PremwadeeNeural"
    speed: float = 1.0
    pitch: str = "+0Hz"
    enable_multi_language: bool = False

class RVCRequest(BaseModel):
    audio_data: str  # base64 encoded
    model_name: str
    transpose: int = 0
    index_ratio: float = 0.75
    f0_method: str = "rmvpe"
    preset: str = "natural"

class UnifiedRequest(BaseModel):
    text: str
    tts_voice: str = "th-TH-PremwadeeNeural"
    enable_rvc: bool = False
    rvc_model: Optional[str] = None
    tts_speed: float = 1.0
    tts_pitch: str = "+0Hz"
    rvc_transpose: int = 0
    rvc_index_ratio: float = 0.75
    rvc_f0_method: str = "rmvpe"
    rvc_preset: str = "natural"
    enable_multi_language: bool = False

@app.on_event("startup")
async def startup_event():
    """Initialize systems on startup"""
    global core_instance, rvc_converter
    
    logger.info("🚀 Starting Enhanced VICTOR-TTS API Server...")
    
    try:
        # Initialize core system
        if ENHANCED_AVAILABLE:
            core_instance = create_core_instance(
                models_dir="logs",
                temp_dir="storage/temp",
                device=None,
                use_gpu=torch.cuda.is_available(),
                gpu_id=0,
                performance_config=PERFORMANCE_CONFIG
            )
            logger.info("✅ Core system initialized")
        
        # Initialize enhanced RVC converter
        if ENHANCED_AVAILABLE:
            rvc_converter = get_enhanced_rvc_converter(
                models_dir="logs",
                device="cuda:0" if torch.cuda.is_available() else "cpu",
                performance_config=PERFORMANCE_CONFIG
            )
            logger.info("✅ Enhanced RVC converter initialized")
        
        logger.info("🎉 Enhanced VICTOR-TTS API Server started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize systems: {e}")
        logger.error(f"Stack trace: {sys.exc_info()}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global core_instance, rvc_converter
    
    logger.info("🛑 Shutting down Enhanced VICTOR-TTS API Server...")
    
    try:
        if rvc_converter:
            cleanup_enhanced_rvc()
            logger.info("✅ RVC converter cleaned up")
        
        if core_instance:
            core_instance.cleanup_temp_files()
            logger.info("✅ Core system cleaned up")
        
        logger.info("🎉 Enhanced VICTOR-TTS API Server shutdown complete!")
        
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve enhanced web interface"""
    try:
        # Load enhanced web interface
        if os.path.exists("web_interface_complete.py"):
            import web_interface_complete
            return HTMLResponse(content=web_interface_complete.generate_html(), status_code=200)
        else:
            # Fallback to basic interface
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>VICTOR-TTS Enhanced</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #333; text-align: center; }
                    .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
                    .status.success { background: #d4edda; color: #155724; }
                    .status.error { background: #f8d7da; color: #721c24; }
                    .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
                    .endpoint h3 { margin: 0 0 10px 0; color: #007bff; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎯 VICTOR-TTS Enhanced API</h1>
                    <div class="status success">
                        ✅ Enhanced API Server is running!
                    </div>
                    
                    <div class="endpoint">
                        <h3>🔍 Health Check</h3>
                        <p><strong>GET</strong> <code>/health</code> - Check system status</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>🎤 TTS Endpoints</h3>
                        <p><strong>GET</strong> <code>/voices</code> - Get available voices</p>
                        <p><strong>POST</strong> <code>/tts</code> - Generate TTS audio</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>🎭 RVC Endpoints</h3>
                        <p><strong>GET</strong> <code>/models</code> - Get available RVC models</p>
                        <p><strong>POST</strong> <code>/voice_conversion</code> - Convert voice</p>
                        <p><strong>GET</strong> <code>/rvc/status</code> - Get RVC status</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>🔄 Unified Endpoints</h3>
                        <p><strong>POST</strong> <code>/unified</code> - TTS + RVC in one request</p>
                        <p><strong>POST</strong> <code>/full_tts</code> - Full TTS with effects</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>⚙️ System Endpoints</h3>
                        <p><strong>GET</strong> <code>/system/status</code> - Detailed system status</p>
                        <p><strong>GET</strong> <code>/system/performance</code> - Performance metrics</p>
                    </div>
                </div>
            </body>
            </html>
            """, status_code=200)
    except Exception as e:
        logger.error(f"Error serving web interface: {e}")
        return HTMLResponse(content=f"<h1>Error: {e}</h1>", status_code=500)

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    try:
        status = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "2.0.0",
            "enhanced": ENHANCED_AVAILABLE,
            "gpu_available": torch.cuda.is_available(),
            "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "core_available": core_instance is not None,
            "rvc_available": rvc_converter is not None if rvc_converter else False
        }
        
        # Add detailed status if available
        if core_instance:
            core_status = core_instance.get_system_status()
            status.update({
                "tts_available": core_status.get("tts_available", False),
                "rvc_available": core_status.get("rvc_available", False),
                "device": core_status.get("device", "unknown")
            })
        
        if rvc_converter:
            rvc_status = rvc_converter.get_status()
            status.update({
                "rvc_models_count": rvc_status.get("models_count", 0),
                "rvc_current_model": rvc_status.get("current_model", None),
                "rvc_memory_usage_mb": rvc_status.get("memory_usage_mb", 0)
            })
        
        return JSONResponse(content=status)
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500
        )

@app.get("/voices")
async def get_voices():
    """Get available TTS voices"""
    try:
        if not core_instance:
            raise HTTPException(status_code=503, detail="Core system not available")
        
        voices = await core_instance.get_available_edge_voices()
        return JSONResponse(content={"voices": voices})
        
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def get_models():
    """Get available RVC models"""
    try:
        if not rvc_converter:
            raise HTTPException(status_code=503, detail="RVC converter not available")
        
        models = rvc_converter.get_available_models()
        return JSONResponse(content={"models": models})
        
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/styles")
async def get_styles():
    """Get available speaking styles"""
    styles = {
        "neutral": "Neutral speaking style",
        "excited": "Excited and energetic",
        "calm": "Calm and relaxed",
        "professional": "Professional and formal",
        "casual": "Casual and friendly"
    }
    return JSONResponse(content={"styles": styles})

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    """Generate TTS audio"""
    try:
        if not core_instance:
            raise HTTPException(status_code=503, detail="Core system not available")
        
        logger.info(f"Generating TTS: voice={request.voice}, text_length={len(request.text)}")
        
        audio_data = await core_instance.generate_tts(
            text=request.text,
            voice=request.voice,
            speed=request.speed,
            pitch=request.pitch,
            enable_multi_language=request.enable_multi_language
        )
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate TTS audio")
        
        # Encode to base64
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        return JSONResponse(content={
            "audio": audio_b64,
            "format": "wav",
            "sample_rate": 44100,
            "duration": len(audio_data) / (44100 * 2)  # Approximate duration
        })
        
    except Exception as e:
        logger.error(f"TTS generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice_conversion")
async def convert_voice(request: RVCRequest):
    """Convert voice using RVC"""
    try:
        if not rvc_converter:
            raise HTTPException(status_code=503, detail="RVC converter not available")
        
        # Decode audio data
        try:
            audio_data = base64.b64decode(request.audio_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid audio data format")
        
        # Save input audio to temp file
        input_path = f"storage/temp/rvc_input_{int(time.time())}.wav"
        output_path = f"storage/temp/rvc_output_{int(time.time())}.wav"
        
        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        
        with open(input_path, 'wb') as f:
            f.write(audio_data)
        
        # Get preset if specified
        presets = rvc_converter.get_conversion_presets()
        preset_params = presets.get(request.preset, {})
        
        # Convert voice
        logger.info(f"Converting voice: model={request.model_name}, preset={request.preset}")
        
        result_path = rvc_converter.convert_voice(
            input_path=input_path,
            output_path=output_path,
            model_name=request.model_name,
            pitch=request.transpose,
            index_rate=request.index_ratio,
            f0_method=request.f0_method,
            **preset_params
        )
        
        if not result_path or not os.path.exists(result_path):
            raise HTTPException(status_code=500, detail="Voice conversion failed")
        
        # Read output audio
        with open(result_path, 'rb') as f:
            output_audio = f.read()
        
        # Cleanup temp files
        try:
            os.remove(input_path)
            os.remove(result_path)
        except:
            pass
        
        # Encode to base64
        audio_b64 = base64.b64encode(output_audio).decode('utf-8')
        
        return JSONResponse(content={
            "audio": audio_b64,
            "format": "wav",
            "model_used": request.model_name,
            "preset_used": request.preset
        })
        
    except Exception as e:
        logger.error(f"Voice conversion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/unified")
async def process_unified(request: UnifiedRequest):
    """Process unified TTS + RVC request"""
    try:
        if not core_instance:
            raise HTTPException(status_code=503, detail="Core system not available")
        
        logger.info(f"Processing unified request: tts_voice={request.tts_voice}, enable_rvc={request.enable_rvc}")
        
        result = await core_instance.process_unified(
            text=request.text,
            tts_voice=request.tts_voice,
            enable_rvc=request.enable_rvc,
            rvc_model=request.rvc_model,
            tts_speed=request.tts_speed,
            tts_pitch=request.tts_pitch,
            rvc_transpose=request.rvc_transpose,
            rvc_index_ratio=request.rvc_index_ratio,
            rvc_f0_method=request.rvc_f0_method,
            enable_multi_language=request.enable_multi_language
        )
        
        if not result or 'audio' not in result:
            raise HTTPException(status_code=500, detail="Unified processing failed")
        
        # Encode audio to base64
        audio_b64 = base64.b64encode(result['audio']).decode('utf-8')
        
        return JSONResponse(content={
            "audio": audio_b64,
            "format": "wav",
            "tts_voice": request.tts_voice,
            "rvc_model": request.rvc_model if request.enable_rvc else None,
            "processing_time": result.get('processing_time', 0)
        })
        
    except Exception as e:
        logger.error(f"Unified processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/full_tts")
async def full_tts(request: UnifiedRequest):
    """Full TTS with enhanced features"""
    try:
        if not core_instance:
            raise HTTPException(status_code=503, detail="Core system not available")
        
        logger.info(f"Full TTS request: voice={request.tts_voice}, enable_rvc={request.enable_rvc}")
        
        # Process with effects
        effects = {
            "reverb": 0.1,
            "compression": 0.2,
            "normalization": True
        }
        
        result = await core_instance.process_unified(
            text=request.text,
            tts_voice=request.tts_voice,
            enable_rvc=request.enable_rvc,
            rvc_model=request.rvc_model,
            tts_speed=request.tts_speed,
            tts_pitch=request.tts_pitch,
            rvc_transpose=request.rvc_transpose,
            rvc_index_ratio=request.rvc_index_ratio,
            rvc_f0_method=request.rvc_f0_method,
            enable_multi_language=request.enable_multi_language
        )
        
        if not result or 'audio' not in result:
            raise HTTPException(status_code=500, detail="Full TTS processing failed")
        
        # Apply audio effects
        if request.enable_rvc:
            audio_with_effects = core_instance.apply_audio_effects(result['audio'], effects)
        else:
            audio_with_effects = result['audio']
        
        # Encode to base64
        audio_b64 = base64.b64encode(audio_with_effects).decode('utf-8')
        
        return JSONResponse(content={
            "audio": audio_b64,
            "format": "wav",
            "tts_voice": request.tts_voice,
            "rvc_model": request.rvc_model if request.enable_rvc else None,
            "effects_applied": list(effects.keys()),
            "processing_time": result.get('processing_time', 0)
        })
        
    except Exception as e:
        logger.error(f"Full TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rvc/status")
async def get_rvc_status():
    """Get detailed RVC status"""
    try:
        if not rvc_converter:
            raise HTTPException(status_code=503, detail="RVC converter not available")
        
        status = rvc_converter.get_status()
        return JSONResponse(content=status)
        
    except Exception as e:
        logger.error(f"RVC status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/status")
async def get_system_status():
    """Get detailed system status"""
    try:
        status = {
            "timestamp": time.time(),
            "version": "2.0.0",
            "enhanced": ENHANCED_AVAILABLE,
            "gpu": {
                "available": torch.cuda.is_available(),
                "name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                "memory_total": torch.cuda.get_device_properties(0).total_memory / (1024**3) if torch.cuda.is_available() else 0,
                "memory_allocated": torch.cuda.memory_allocated() / (1024**3) if torch.cuda.is_available() else 0
            },
            "core": {
                "available": core_instance is not None,
                "status": core_instance.get_system_status() if core_instance else None
            },
            "rvc": {
                "available": rvc_converter is not None,
                "status": rvc_converter.get_status() if rvc_converter else None
            }
        }
        
        return JSONResponse(content=status)
        
    except Exception as e:
        logger.error(f"System status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/performance")
async def get_performance_metrics():
    """Get performance metrics"""
    try:
        metrics = {
            "timestamp": time.time(),
            "memory": {
                "system_total": 0,  # Would need psutil
                "system_available": 0,
                "gpu_allocated": torch.cuda.memory_allocated() / (1024**3) if torch.cuda.is_available() else 0,
                "gpu_cached": torch.cuda.memory_reserved() / (1024**3) if torch.cuda.is_available() else 0
            },
            "rvc": {
                "conversion_stats": rvc_converter.conversion_stats if rvc_converter else None
            }
        }
        
        return JSONResponse(content=metrics)
        
    except Exception as e:
        logger.error(f"Performance metrics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced VICTOR-TTS API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=6969, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Starting Enhanced VICTOR-TTS API Server on {args.host}:{args.port}")
    
    uvicorn.run(
        "main_api_server_enhanced:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    ) 