#!/usr/bin/env python3
"""
🎙️ VICTOR-TTS UNIFIED API SERVER
รวมระบบ TTS + RVC ในตัวเดียวแบบเรียบง่าย
"""
# Standard library imports
import os
import sys
import time
import asyncio
import logging
import json
import base64
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import importlib.util

# Third-party imports
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.staticfiles import StaticFiles

# Conditional imports for config parsing
try:
    import toml
    CONFIG_PARSER_AVAILABLE = True
except ImportError:
    CONFIG_PARSER_AVAILABLE = False
    print("⚠️ TOML parser not available, using default settings")
    
# Conditional imports for GPU
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
    if GPU_AVAILABLE:
        print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ No GPU detected, using CPU")
except ImportError:
    print("⚠️ PyTorch not available, using CPU")
    GPU_AVAILABLE = False

# FastAPI imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Audio libraries
try:
    import edge_tts
    import soundfile as sf
    import numpy as np
    AUDIO_LIBS_AVAILABLE = True
    print("✅ Audio libraries loaded successfully")
except ImportError as e:
    AUDIO_LIBS_AVAILABLE = False
    print(f"⚠️ Audio libraries not available: {e}")

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Try to import config parser
try:
    import tomli
    CONFIG_PARSER_AVAILABLE = True
except ImportError:
    CONFIG_PARSER_AVAILABLE = False
    print("⚠️ TOML parser not available, using default settings")

# Setup GPU if available
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
    if GPU_AVAILABLE:
        print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ No GPU detected, using CPU")
except ImportError:
    GPU_AVAILABLE = False
    print("⚠️ PyTorch not available, using CPU")

# Try to import RVC
try:
    from rvc_api import RVCConverter
    RVC_AVAILABLE = True
    print("✅ RVC system loaded")
except ImportError:
    try:
        from rvc_api import RVCAPI
        RVC_AVAILABLE = True
        print("✅ RVC system loaded (RVCAPI)")
    except ImportError:
        RVC_AVAILABLE = False
        print("⚠️ RVC system not available")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VICTOR-TTS-UNIFIED")

# FastAPI app
app = FastAPI(
    title="VICTOR-TTS UNIFIED API",
    description="🎙️ Unified TTS + Voice Conversion Platform",
    version="3.0.0-UNIFIED",
    docs_url="/docs",
    redoc_url="/redoc"
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

# Global configuration
config = {
    "models_dir": "models",
    "models_dir_fallback": "logs",
    "temp_dir": "storage/temp",
    "output_dir": "storage/output",
    "max_file_size": 52428800,  # 50MB
    "max_text_length": 10000000,
    "max_chunk_size": 8000,
    "cleanup_interval": 3600,  # 1 hour
    "gpu": {
        "enabled": True,
        "device_id": 0,
        "memory_limit": 0,
        "use_fp16": True
    }
}

# Load configuration from file
def load_config():
    """Load configuration from TOML file"""
    global config
    
    config_file = Path("config/unified_config.toml")
    if CONFIG_PARSER_AVAILABLE and config_file.exists():
        try:
            with open(config_file, "r") as f:
                toml_config = toml.load(f)
            
            # Update directories
            if "directories" in toml_config:
                for key in ["models_dir", "temp_dir", "output_dir"]:
                    if key in toml_config["directories"]:
                        config[key] = toml_config["directories"][key]
            
            # Update TTS settings
            if "tts" in toml_config:
                if "max_text_length" in toml_config["tts"]:
                    config["max_text_length"] = toml_config["tts"]["max_text_length"]
                if "max_chunk_size" in toml_config["tts"]:
                    config["max_chunk_size"] = toml_config["tts"]["max_chunk_size"]
            
            # Update API settings
            if "api_server" in toml_config:
                if "max_file_size" in toml_config["api_server"]:
                    config["max_file_size"] = toml_config["api_server"]["max_file_size"]
                if "cleanup_interval" in toml_config["api_server"]:
                    config["cleanup_interval"] = toml_config["api_server"]["cleanup_interval"]
            
            # Update GPU settings
            if "gpu" in toml_config:
                for key in ["enabled", "device_id", "memory_limit", "use_fp16"]:
                    if key in toml_config["gpu"]:
                        config["gpu"][key] = toml_config["gpu"][key]
            
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")

# Create directories
for dir_path in [config["temp_dir"], config["output_dir"], config["models_dir"]]:
    Path(dir_path).mkdir(parents=True, exist_ok=True)

# Global instances
rvc_instance = None

# Setup GPU based on configuration and command line arguments
def setup_gpu(args):
    """Setup GPU based on configuration and command line arguments"""
    global config
    
    # Check if GPU is actually available
    try:
        import torch
        GPU_AVAILABLE = torch.cuda.is_available()
        gpu_count = torch.cuda.device_count()
        if GPU_AVAILABLE and gpu_count > 0:
            logger.info(f"Found {gpu_count} GPU(s): {[torch.cuda.get_device_name(i) for i in range(gpu_count)]}")
        else:
            logger.info("No GPU detected by PyTorch")
            GPU_AVAILABLE = False
    except Exception as e:
        logger.warning(f"Error detecting GPU: {e}")
        GPU_AVAILABLE = False
    
    # Command line arguments override config file
    if args.cpu:
        config["gpu"]["enabled"] = False
        logger.info("Using CPU (forced by command line)")
    elif args.gpu is not None and GPU_AVAILABLE:
        config["gpu"]["enabled"] = True
        config["gpu"]["device_id"] = args.gpu
        logger.info(f"Using GPU {args.gpu} (from command line)")
    else:
        # No GPU available or not specified
        if not GPU_AVAILABLE:
            config["gpu"]["enabled"] = False
            logger.info("No GPU available, using CPU")
    
    # Apply GPU memory limit if specified
    if args.memory_limit > 0:
        config["gpu"]["memory_limit"] = args.memory_limit
    
    # Apply mixed precision if specified
    if args.fp16:
        config["gpu"]["use_fp16"] = True
    
    # Setup environment based on GPU configuration
    if config["gpu"]["enabled"] and GPU_AVAILABLE:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(config["gpu"]["device_id"])
        
        # Set memory limit if configured
        if config["gpu"]["memory_limit"] > 0:
            try:
                import torch
                torch.cuda.set_per_process_memory_fraction(
                    config["gpu"]["memory_limit"] / 
                    torch.cuda.get_device_properties(0).total_memory
                )
                logger.info(f"GPU memory limit set to {config['gpu']['memory_limit']} bytes")
            except Exception as e:
                logger.warning(f"Failed to set GPU memory limit: {e}")
        
        # Enable mixed precision if configured
        if config["gpu"]["use_fp16"]:
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"
            logger.info("Mixed precision (FP16) enabled")
            
        try:
            import torch
            if torch.cuda.is_available():
                logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                logger.warning("GPU was configured but torch.cuda.is_available() is False")
                os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
                config["gpu"]["enabled"] = False
        except Exception as e:
            logger.warning(f"Error initializing GPU: {e}")
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            config["gpu"]["enabled"] = False
    else:
        # Force CPU mode
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        config["gpu"]["enabled"] = False
        logger.info("Using CPU mode")
        
    # Set configuration for RVC
    if "CUDA_VISIBLE_DEVICES" in os.environ:
        logger.info(f"CUDA_VISIBLE_DEVICES set to: {os.environ['CUDA_VISIBLE_DEVICES']}")

# Edge TTS voices (basic set)
EDGE_VOICES = {
    "th-TH-PremwadeeNeural": {"name": "Premwadee (Thai Female)", "gender": "Female", "language": "Thai"},
    "th-TH-NiranNeural": {"name": "Niran (Thai Male)", "gender": "Male", "language": "Thai"},
    "th-TH-NiwatNeural": {"name": "Niwat (Thai Male)", "gender": "Male", "language": "Thai"},
    "lo-LA-ChanthavongNeural": {"name": "Chanthavong (Lao Male)", "gender": "Male", "language": "Lao"},
    "lo-LA-KeomanyNeural": {"name": "Keomany (Lao Female)", "gender": "Female", "language": "Lao"},
    "en-US-AriaNeural": {"name": "Aria (US Female)", "gender": "Female", "language": "English"},
    "en-US-GuyNeural": {"name": "Guy (US Male)", "gender": "Male", "language": "English"},
    "ja-JP-NanamiNeural": {"name": "Nanami (Japanese Female)", "gender": "Female", "language": "Japanese"},
    "zh-CN-XiaoxiaoNeural": {"name": "Xiaoxiao (Chinese Female)", "gender": "Female", "language": "Chinese"}
}

# Request/Response Models
class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    voice: str = Field(..., description="Voice to use")
    speed: float = Field(1.0, description="Speech speed (0.5-2.0)")
    
class VoiceConversionRequest(BaseModel):
    model_name: str = Field(..., description="RVC model name")
    transpose: int = Field(0, description="Transpose (-12 to 12)")
    index_ratio: float = Field(0.75, description="Index ratio (0.0-1.0)")
    f0_method: str = Field("rmvpe", description="F0 method")

class UnifiedRequest(BaseModel):
    text: str = Field(..., description="Text to convert")
    tts_voice: str = Field(..., description="TTS voice")
    speed: float = Field(1.0, description="Speech speed")
    enable_rvc: bool = Field(False, description="Enable voice conversion")
    rvc_params: Optional[VoiceConversionRequest] = Field(None, description="RVC parameters")

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None

# Utility functions
def cleanup_temp_files():
    """Clean up old temporary files"""
    try:
        temp_dir = Path(config["temp_dir"])
        cutoff_time = datetime.now().timestamp() - config["cleanup_interval"]
        
        for file_path in temp_dir.glob("*"):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                file_path.unlink(missing_ok=True)
                
        logger.info("Temp files cleaned")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

def initialize_rvc():
    """Initialize RVC system"""
    global RVC_AVAILABLE, rvc_instance
    try:
        # Try to import RVC modules
        try:
            from rvc_api import RVCAPI
            rvc_instance = RVCAPI()
            RVC_AVAILABLE = True
            logger.info("✅ RVC system initialized (RVCAPI)")
            return True
        except ImportError:
            try:
                from rvc_api import RVCConverter
                device = f"cuda:{config['gpu']['device_id']}" if config["gpu"]["enabled"] and GPU_AVAILABLE else "cpu"
                rvc_instance = RVCConverter(device=device)
                RVC_AVAILABLE = True
                logger.info(f"✅ RVC system initialized (RVCConverter) on {device}")
                return True
            except ImportError:
                RVC_AVAILABLE = False
                logger.warning("⚠️ RVC system not available")
                return False
    except Exception as e:
        logger.warning(f"⚠️ RVC system not available: {e}")
        RVC_AVAILABLE = False
        return False

def get_available_models():
    """Get available RVC models"""
    try:
        if not initialize_rvc():
            return []
        return rvc_instance.get_available_models()
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return []

async def generate_tts(text: str, voice: str, speed: float = 1.0) -> bytes:
    """Generate TTS audio"""
    if not AUDIO_LIBS_AVAILABLE:
        raise HTTPException(status_code=500, detail="Audio libraries not available")
    
    if voice not in EDGE_VOICES:
        raise HTTPException(status_code=400, detail=f"Voice '{voice}' not available")
    
    try:
        # Create communicate object
        rate = f"{speed:+.0%}" if speed != 1.0 else "+0%"
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        
        # Generate audio
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

def apply_voice_conversion(audio_data: bytes, rvc_params: VoiceConversionRequest) -> bytes:
    """Apply voice conversion to audio"""
    if not initialize_rvc():
        raise HTTPException(status_code=500, detail="RVC not available")
    
    try:
        # Save input audio to temp file
        temp_input = Path(config["temp_dir"]) / f"input_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.wav"
        temp_output = Path(config["temp_dir"]) / f"output_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.wav"
        
        with open(temp_input, "wb") as f:
            f.write(audio_data)
        
        # Convert voice
        result_path = rvc_instance.convert_voice(
            input_path=str(temp_input),
            output_path=str(temp_output),
            model_name=rvc_params.model_name,
            transpose=rvc_params.transpose,
            index_ratio=rvc_params.index_ratio,
            f0_method=rvc_params.f0_method
        )
        
        # Read converted audio
        with open(result_path, "rb") as f:
            converted_audio = f.read()
        
        # Cleanup
        temp_input.unlink(missing_ok=True)
        temp_output.unlink(missing_ok=True)
        
        return converted_audio
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice conversion failed: {str(e)}")

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    models = get_available_models()
    
    # Get GPU status by checking directly
    gpu_enabled = False
    gpu_info = "None"
    
    try:
        import torch
        print(f"DEBUG: torch imported successfully")
        print(f"DEBUG: torch.cuda.is_available() = {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            gpu_enabled = True
            device_id = 0  # Default to first GPU
            gpu_name = torch.cuda.get_device_name(device_id)
            memory_total = torch.cuda.get_device_properties(device_id).total_memory / (1024**3)
            memory_allocated = torch.cuda.memory_allocated(device_id) / (1024**3)
            gpu_info = f"{gpu_name} (Using {memory_allocated:.2f}GB / {memory_total:.2f}GB)"
            print(f"DEBUG: GPU enabled = {gpu_enabled}, info = {gpu_info}")
        else:
            gpu_enabled = False
            gpu_info = "No GPU available"
            print(f"DEBUG: torch.cuda.is_available() returned False")
    except ImportError as e:
        gpu_enabled = False
        gpu_info = f"PyTorch not available: {e}"
        print(f"DEBUG: ImportError - {e}")
    except Exception as e:
        gpu_enabled = False
        gpu_info = f"Error getting GPU info: {e}"
        print(f"DEBUG: Exception - {e}")
    
    return APIResponse(
        success=True,
        message="VICTOR-TTS UNIFIED API is running",
        data={
            "status": "healthy",
            "version": "3.0.0-UNIFIED",
            "features": {
                "tts_available": AUDIO_LIBS_AVAILABLE,
                "rvc_available": RVC_AVAILABLE,
                "models_count": len(models),
                "gpu_enabled": gpu_enabled,
                "gpu_info": gpu_info
            },
            "config": {
                "max_text_length": config["max_text_length"],
                "available_voices": len(EDGE_VOICES)
            }
        }
    )

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main page with simple interface"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>VICTOR-TTS UNIFIED</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .title {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
            .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            textarea {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
            select, button {{ padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; }}
            button {{ background: #3498db; color: white; cursor: pointer; }}
            button:hover {{ background: #2980b9; }}
            .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .gpu-info {{ background: #e2f3fe; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">🎙️ VICTOR-TTS UNIFIED</h1>
            <p style="text-align: center; color: #666;">Complete TTS + Voice Conversion Platform</p>
            
            <div class="gpu-info">
                <strong>GPU Status:</strong> {"Enabled ✅" if config["gpu"]["enabled"] and GPU_AVAILABLE else "Disabled ❌"}
                {f'<br><strong>Device:</strong> GPU {config["gpu"]["device_id"]} - {torch.cuda.get_device_name(config["gpu"]["device_id"])}' if config["gpu"]["enabled"] and GPU_AVAILABLE else ""}
            </div>
            
            <div class="section">
                <h3>📝 Text to Speech</h3>
                <textarea id="text" rows="5" placeholder="Enter text to convert to speech..."></textarea>
                <br>
                <select id="voice">
                    {"".join(f'<option value="{k}">{v["name"]}</option>' for k, v in EDGE_VOICES.items())}
                </select>
                <input type="range" id="speed" min="0.5" max="2" step="0.1" value="1" onchange="updateSpeed(this.value)">
                <span id="speedValue">Speed: 1.0x</span>
                <br>
                <button onclick="generateTTS()">🎵 Generate TTS</button>
            </div>
            
            <div class="section">
                <h3>🎭 Voice Conversion (Optional)</h3>
                <input type="checkbox" id="enableRVC"> Enable Voice Conversion
                <br>
                <select id="rvcModel" disabled>
                    <option value="">Loading models...</option>
                </select>
                <input type="range" id="transpose" min="-12" max="12" value="0" disabled onchange="updateTranspose(this.value)">
                <span id="transposeValue">Transpose: 0</span>
            </div>
            
            <div class="section">
                <h3>🎧 Result</h3>
                <div id="status"></div>
                <audio id="result" controls style="width: 100%; display: none;"></audio>
            </div>
            
            <div class="section">
                <h3>📋 API Information</h3>
                <p><strong>Docs:</strong> <a href="/docs" target="_blank">/docs</a></p>
                <p><strong>Health:</strong> <a href="/health" target="_blank">/health</a></p>
                <p><strong>Models:</strong> <a href="/models" target="_blank">/models</a></p>
            </div>
        </div>
        
        <script>
            function updateSpeed(value) {{
                document.getElementById('speedValue').textContent = `Speed: ${{value}}x`;
            }}
            
            function updateTranspose(value) {{
                document.getElementById('transposeValue').textContent = `Transpose: ${{value}}`;
            }}
            
            document.getElementById('enableRVC').onchange = function() {{
                const enabled = this.checked;
                document.getElementById('rvcModel').disabled = !enabled;
                document.getElementById('transpose').disabled = !enabled;
            }};
            
            async function loadModels() {{
                try {{
                    const response = await fetch('/models');
                    const data = await response.json();
                    const select = document.getElementById('rvcModel');
                    select.innerHTML = '';
                    
                    if (data.success && data.data.models.length > 0) {{
                        data.data.models.forEach(model => {{
                            const option = document.createElement('option');
                            option.value = model;
                            option.textContent = model;
                            select.appendChild(option);
                        }});
                    }} else {{
                        select.innerHTML = '<option value="">No RVC models available</option>';
                    }}
                }} catch (error) {{
                    console.error('Error loading models:', error);
                }}
            }}
            
            async function generateTTS() {{
                const text = document.getElementById('text').value;
                const voice = document.getElementById('voice').value;
                const speed = parseFloat(document.getElementById('speed').value);
                const enableRVC = document.getElementById('enableRVC').checked;
                const status = document.getElementById('status');
                const result = document.getElementById('result');
                
                if (!text.trim()) {{
                    status.innerHTML = '<div class="error">Please enter some text</div>';
                    return;
                }}
                
                status.innerHTML = '<div>Processing...</div>';
                
                try {{
                    const requestData = {{
                        text: text,
                        tts_voice: voice,
                        speed: speed,
                        enable_rvc: enableRVC
                    }};
                    
                    if (enableRVC) {{
                        requestData.rvc_params = {{
                            model_name: document.getElementById('rvcModel').value,
                            transpose: parseInt(document.getElementById('transpose').value),
                            index_ratio: 0.75,
                            f0_method: "rmvpe"
                        }};
                    }}
                    
                    const response = await fetch('/unified', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(requestData)
                    }});
                    
                    const data = await response.json();
                    
                    if (data.success) {{
                        const audioBlob = new Blob([Uint8Array.from(atob(data.data.audio_base64), c => c.charCodeAt(0))], {{type: 'audio/wav'}});
                        const audioUrl = URL.createObjectURL(audioBlob);
                        result.src = audioUrl;
                        result.style.display = 'block';
                        status.innerHTML = '<div class="success">Audio generated successfully!</div>';
                    }} else {{
                        status.innerHTML = `<div class="error">Error: ${{data.message}}</div>`;
                    }}
                }} catch (error) {{
                    status.innerHTML = `<div class="error">Error: ${{error.message}}</div>`;
                }}
            }}
            
            // Load models on page load
            loadModels();
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/voices")
async def get_voices():
    """Get available TTS voices"""
    return APIResponse(
        success=True,
        message="Voices retrieved successfully",
        data={"voices": EDGE_VOICES}
    )

@app.get("/models")
async def get_models():
    """Get available RVC models"""
    models = get_available_models()
    return APIResponse(
        success=True,
        message=f"Found {len(models)} RVC models",
        data={
            "models": models,
            "rvc_available": RVC_AVAILABLE
        }
    )

@app.post("/tts")
async def text_to_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    """Text-to-speech only"""
    start_time = datetime.now()
    
    try:
        # Generate TTS
        audio_data = await generate_tts(request.text, request.voice, request.speed)
        
        # Encode to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_files)
        
        return APIResponse(
            success=True,
            message="TTS completed successfully",
            data={
                "audio_base64": audio_base64,
                "format": "wav",
                "voice": request.voice,
                "text_length": len(request.text),
                "audio_size": len(audio_data)
            },
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

@app.post("/voice_conversion")
async def voice_conversion_only(
    audio: UploadFile = File(...),
    request_data: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    """Voice conversion only"""
    start_time = datetime.now()
    
    try:
        # Parse request data
        rvc_params = VoiceConversionRequest(**json.loads(request_data))
        
        # Read uploaded audio
        audio_data = await audio.read()
        
        # Apply voice conversion
        converted_audio = apply_voice_conversion(audio_data, rvc_params)
        
        # Encode to base64
        audio_base64 = base64.b64encode(converted_audio).decode('utf-8')
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_files)
        
        return APIResponse(
            success=True,
            message="Voice conversion completed successfully",
            data={
                "audio_base64": audio_base64,
                "format": "wav",
                "model_used": rvc_params.model_name,
                "original_size": len(audio_data),
                "converted_size": len(converted_audio)
            },
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice conversion error: {str(e)}")

@app.post("/unified")
async def unified_processing(request: UnifiedRequest, background_tasks: BackgroundTasks):
    """Unified TTS + Voice Conversion"""
    start_time = datetime.now()
    
    try:
        # Generate TTS
        audio_data = await generate_tts(request.text, request.tts_voice, request.speed)
        
        # Apply voice conversion if enabled
        if request.enable_rvc and request.rvc_params:
            audio_data = apply_voice_conversion(audio_data, request.rvc_params)
        
        # Encode to base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_files)
        
        return APIResponse(
            success=True,
            message="Unified processing completed successfully",
            data={
                "audio_base64": audio_base64,
                "format": "wav",
                "text_length": len(request.text),
                "audio_size": len(audio_data),
                "voice_conversion_applied": request.enable_rvc and request.rvc_params is not None
            },
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unified processing error: {str(e)}")

@app.post("/full_tts")
async def full_tts_processing(request: dict, background_tasks: BackgroundTasks):
    """Full TTS processing with HTML-compatible format"""
    start_time = datetime.now()
    
    try:
        # Extract parameters from request
        text = request.get("text", "")
        tts_voice = request.get("tts_voice", "th-TH-PremwadeeNeural")
        tts_speed = request.get("tts_speed", 1.0)
        enable_rvc = request.get("enable_rvc", False)
        rvc_model = request.get("rvc_model", None)
        rvc_transpose = request.get("rvc_transpose", 0)
        rvc_index_ratio = request.get("rvc_index_ratio", 0.7)
        rvc_f0_method = request.get("rvc_f0_method", "rmvpe")
        
        # Validate input
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text is required")
        
        if not tts_voice:
            raise HTTPException(status_code=400, detail="TTS voice is required")
        
        # Use TTSRVCCore for processing
        from tts_rvc_core import create_core_instance
        
        core = create_core_instance()
        
        # Process unified TTS + RVC
        result = await core.process_unified(
            text=text,
            tts_voice=tts_voice,
            enable_rvc=enable_rvc,
            rvc_model=rvc_model,
            tts_speed=tts_speed,
            rvc_transpose=rvc_transpose,
            rvc_index_ratio=rvc_index_ratio,
            rvc_f0_method=rvc_f0_method
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
        
        # Encode to base64
        audio_base64 = base64.b64encode(result["audio_data"]).decode('utf-8')
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_temp_files)
        
        return APIResponse(
            success=True,
            message="Full TTS processing completed successfully",
            data={
                "audio_base64": audio_base64,
                "format": "wav",
                "text_length": len(text),
                "audio_size": len(result["audio_data"]),
                "voice_conversion_applied": "voice_conversion" in result.get("processing_steps", []),
                "processing_steps": result.get("processing_steps", []),
                "stats": result.get("stats", {})
            },
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Full TTS processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Full TTS processing error: {str(e)}")

@app.on_event("startup")  # TODO: Replace with lifespan
async def startup_event():
    """Initialize on startup"""
    logger.info("🚀 VICTOR-TTS UNIFIED API Starting...")
    
    # Load configuration
    load_config()
    
    # Cleanup temp files
    cleanup_temp_files()
    
    # Initialize RVC
    rvc_ready = initialize_rvc()
    models = get_available_models()
    
    # Log GPU status
    if config["gpu"]["enabled"] and GPU_AVAILABLE:
        logger.info(f"🖥️ Using GPU: {torch.cuda.get_device_name(config['gpu']['device_id'])}")
    else:
        logger.info("💻 Using CPU mode")
    
    logger.info(f"✅ System ready!")
    logger.info(f"📢 TTS voices: {len(EDGE_VOICES)}")
    logger.info(f"🎭 RVC models: {len(models)}")
    logger.info(f"🔥 Max text length: {config['max_text_length']:,} characters")

@app.on_event("shutdown")  # TODO: Replace with lifespan
async def shutdown_event():
    """Cleanup on shutdown"""
    cleanup_temp_files()
    logger.info("👋 VICTOR-TTS UNIFIED API Shutdown")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VICTOR-TTS UNIFIED API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, default=6969, help="Port number")
    parser.add_argument("--log-level", default="info", help="Log level")
    
    # Add GPU-related options
    parser.add_argument("--gpu", type=int, help="GPU ID to use (0, 1, 2, ...)")
    parser.add_argument("--cpu", action="store_true", help="Force CPU usage even if GPU is available")
    parser.add_argument("--memory-limit", type=int, default=0, help="GPU memory limit in MB")
    parser.add_argument("--fp16", action="store_true", help="Use mixed precision (FP16)")
    
    args = parser.parse_args()
    
    # Load configuration
    load_config()
    
    # Setup GPU
    setup_gpu(args)
    
    print(f"""
🎙️ VICTOR-TTS UNIFIED API Server
==================================
🔥 Simplified & Unified Platform
✅ TTS + Voice Conversion
✅ Clean Architecture  
✅ Easy to Use & Maintain
==================================
Host: {args.host}
Port: {args.port}
Log Level: {args.log_level}
Max Text: {config['max_text_length']:,} chars
==================================
🖥️ {'Using GPU: ' + (torch.cuda.get_device_name(config["gpu"]["device_id"]) if config["gpu"]["enabled"] and GPU_AVAILABLE else 'No') if GPU_AVAILABLE else 'GPU not available'}
==================================
🚀 Starting unified server...
""")
    
    uvicorn.run(
        "main_api_server:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
        reload=False
    )
