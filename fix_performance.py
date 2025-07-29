#!/usr/bin/env python3
"""
🔧 Performance Fix Script - แก้ไขปัญหาประสิทธิภาพและ RVC
แก้ไขปัญหาการเปิดโปรแกรมช้าและ RVC ที่ไม่ทำงาน
"""
import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PERFORMANCE_FIX")

class PerformanceFixer:
    """คลาสสำหรับแก้ไขปัญหาประสิทธิภาพ"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        self.storage_dir = self.project_root / "storage"
        
    def fix_performance_config(self) -> Dict[str, Any]:
        """แก้ไขการตั้งค่าประสิทธิภาพเพื่อเพิ่มความเร็ว"""
        config_file = self.config_dir / "performance_config.json"
        
        # การตั้งค่าใหม่ที่เน้นความเร็ว
        new_config = {
            "tts_batch_size": 1,
            "tts_chunk_size": 3000,  # ลดขนาด chunk
            "tts_max_concurrent": 2,  # ลด concurrent
            "rvc_batch_size": 1,
            "rvc_use_half_precision": True,  # เปิดใช้ half precision
            "rvc_optimize_memory": True,
            "rvc_cache_models": True,
            "audio_sample_rate": 44100,
            "audio_chunk_duration": 5,  # ลดเวลา chunk
            "audio_use_soxr": True,
            "use_multiprocessing": False,  # ปิด multiprocessing ชั่วคราว
            "max_workers": 1,  # ลด workers
            "memory_limit_gb": 4,  # ลด memory limit
            "gpu_memory_fraction": 0.6,  # ลด GPU memory
            "gpu_allow_growth": True,
            "gpu_mixed_precision": True,  # เปิดใช้ mixed precision
            "lazy_loading": True,  # เพิ่ม lazy loading
            "preload_models": False,  # ปิด preload
            "cache_tts_voices": True,
            "optimize_startup": True
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            
            logger.info("✅ Performance config updated for faster startup")
            return new_config
        except Exception as e:
            logger.error(f"❌ Failed to update performance config: {e}")
            return {}
    
    def create_optimized_core(self) -> str:
        """สร้างไฟล์ core ที่ปรับปรุงแล้ว"""
        optimized_core = '''#!/usr/bin/env python3
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
                     transpose: int = 0, index_ratio: float = 0.75) -> bytes:
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
            
            # แปลงเสียง
            result_path = self.rvc_instance.convert_voice(
                input_path=str(temp_input),
                output_path=str(temp_output),
                model_name=model_name,
                transpose=transpose,
                index_ratio=index_ratio
            )
            
            # อ่านผลลัพธ์
            with open(result_path, "rb") as f:
                converted_audio = f.read()
            
            # ลบไฟล์ชั่วคราว
            temp_input.unlink(missing_ok=True)
            temp_output.unlink(missing_ok=True)
            
            return converted_audio
        except Exception as e:
            logger.error(f"Voice conversion failed: {e}")
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
        return {
            "tts_available": self.tts_available,
            "rvc_available": self.rvc_available,
            "device": self.device,
            "rvc_loaded": self.rvc_loaded
        }

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
'''
        
        optimized_file = self.project_root / "tts_rvc_core_optimized.py"
        try:
            with open(optimized_file, 'w', encoding='utf-8') as f:
                f.write(optimized_core)
            
            logger.info("✅ Optimized core file created")
            return str(optimized_file)
        except Exception as e:
            logger.error(f"❌ Failed to create optimized core: {e}")
            return ""
    
    def create_fast_web_interface(self) -> str:
        """สร้าง web interface ที่เร็วขึ้น"""
        fast_web = '''#!/usr/bin/env python3
"""
🌐 Fast Web Interface - เวอร์ชันที่เร็วขึ้น
"""
import os
import sys
import json
import base64
import asyncio
import socket
from pathlib import Path
from datetime import datetime
import webbrowser
from typing import Optional, Dict, Any

# เพิ่ม path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import optimized core
try:
    from tts_rvc_core_optimized import create_optimized_core_instance, get_supported_voices
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("⚠️ Optimized Core not available")

class FastWebInterface:
    """Web Interface ที่เร็วขึ้น"""
    
    def __init__(self, port: int = 7000):
        self.port = self._find_available_port(port)
        self.core = None
        self.is_running = False
        
        if CORE_AVAILABLE:
            try:
                # ใช้ optimized core
                self.core = create_optimized_core_instance()
                print("✅ Optimized Core loaded")
            except Exception as e:
                print(f"⚠️ Failed to load Optimized Core: {e}")
                self.core = None
    
    def _find_available_port(self, start_port: int) -> int:
        """หาพอร์ตที่ว่าง"""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return start_port
    
    def generate_html_page(self) -> str:
        """สร้างหน้าเว็บหลักแบบเร็ว"""
        # ดึงข้อมูลระบบ
        if self.core:
            status = self.core.get_system_status()
            voices = get_supported_voices()
            models = self.core.get_available_rvc_models()
        else:
            status = {"tts_available": False, "rvc_available": False}
            voices = {}
            models = []
        
        voices_options = ""
        for voice_id, voice_info in voices.items():
            voices_options += f'<option value="{voice_id}">{voice_info["name"]}</option>'
        
        models_options = ""
        for model in models:
            models_options += f'<option value="{model}">{model}</option>'
        
        # HTML template แบบเร็ว
        html = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VICTOR-TTS FAST</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #333; text-align: center; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        textarea, select {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        button {{ background: #007bff; color: white; padding: 15px; border: none; border-radius: 5px; cursor: pointer; width: 100%; }}
        button:hover {{ background: #0056b3; }}
        .result {{ margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
        audio {{ width: 100%; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ VICTOR-TTS FAST</h1>
        
        <div class="form-group">
            <label for="text">ข้อความ:</label>
            <textarea id="text" rows="4" placeholder="ใส่ข้อความที่นี่..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="voice">เสียง TTS:</label>
            <select id="voice">
                {voices_options}
            </select>
        </div>
        
        <div class="form-group">
            <label for="rvc_model">โมเดล RVC (ไม่บังคับ):</label>
            <select id="rvc_model">
                <option value="">ไม่ใช้ RVC</option>
                {models_options}
            </select>
        </div>
        
        <button onclick="generateAudio()">สร้างเสียง</button>
        
        <div id="result" class="result" style="display: none;">
            <h3>ผลลัพธ์:</h3>
            <audio id="audio" controls></audio>
            <br>
            <a id="download" href="#" download="output.wav">ดาวน์โหลด</a>
        </div>
    </div>
    
    <script>
        async function generateAudio() {{
            const text = document.getElementById('text').value;
            const voice = document.getElementById('voice').value;
            const rvc_model = document.getElementById('rvc_model').value;
            
            if (!text || !voice) {{
                alert('กรุณาใส่ข้อความและเลือกเสียง');
                return;
            }}
            
            const button = document.querySelector('button');
            button.disabled = true;
            button.textContent = 'กำลังประมวลผล...';
            
            try {{
                const response = await fetch('/generate', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        text: text,
                        voice: voice,
                        rvc_model: rvc_model
                    }})
                }});
                
                const result = await response.json();
                
                if (result.success) {{
                    const audio = document.getElementById('audio');
                    const download = document.getElementById('download');
                    
                    audio.src = 'data:audio/wav;base64,' + result.audio_base64;
                    download.href = 'data:audio/wav;base64,' + result.audio_base64;
                    
                    document.getElementById('result').style.display = 'block';
                }} else {{
                    alert('เกิดข้อผิดพลาด: ' + result.error);
                }}
            }} catch (error) {{
                alert('เกิดข้อผิดพลาด: ' + error.message);
            }} finally {{
                button.disabled = false;
                button.textContent = 'สร้างเสียง';
            }}
        }}
    </script>
</body>
</html>
"""
        return html
    
    def create_simple_server(self):
        """สร้าง server แบบง่าย"""
        import http.server
        import socketserver
        
        class FastRequestHandler(http.server.BaseHTTPRequestHandler):
            def __init__(self, *args, web_interface=None, **kwargs):
                self.web_interface = web_interface
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    html = self.web_interface.generate_html_page()
                    self.wfile.write(html.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                if self.path == '/generate':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = json.loads(post_data.decode('utf-8'))
                        
                        # สร้างเสียง
                        async def generate():
                            try:
                                # TTS
                                audio_data = await self.web_interface.core.generate_tts(
                                    data['text'], data['voice']
                                )
                                
                                # RVC (ถ้ามี)
                                if data.get('rvc_model'):
                                    audio_data = self.web_interface.core.convert_voice(
                                        audio_data, data['rvc_model']
                                    )
                                
                                return {
                                    'success': True,
                                    'audio_base64': base64.b64encode(audio_data).decode('utf-8')
                                }
                            except Exception as e:
                                return {
                                    'success': False,
                                    'error': str(e)
                                }
                        
                        # รัน async function
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        result = loop.run_until_complete(generate())
                        loop.close()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        
                        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        
                        error_result = {'success': False, 'error': str(e)}
                        self.wfile.write(json.dumps(error_result, ensure_ascii=False).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
        
        class FastServer(socketserver.TCPServer):
            def __init__(self, server_address, handler_class, web_interface):
                self.web_interface = web_interface
                super().__init__(server_address, handler_class)
            
            def finish_request(self, request, client_address):
                self.RequestHandlerClass(request, client_address, self, web_interface=self.web_interface)
        
        return FastServer(('localhost', self.port), FastRequestHandler, self)
    
    def start(self, open_browser: bool = True):
        """เริ่มต้น server"""
        try:
            server = self.create_simple_server()
            self.is_running = True
            
            print(f"🌐 Fast Web Interface started on http://localhost:{self.port}")
            print("✅ Optimized for faster startup and performance")
            
            if open_browser:
                def open_browser_delayed():
                    import time
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{self.port}')
                
                import threading
                threading.Thread(target=open_browser_delayed, daemon=True).start()
            
            server.serve_forever()
        except KeyboardInterrupt:
            print("\\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Server error: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Starting Fast Web Interface...")
    
    interface = FastWebInterface()
    interface.start()

if __name__ == "__main__":
    main()
'''
        
        fast_web_file = self.project_root / "web_interface_fast.py"
        try:
            with open(fast_web_file, 'w', encoding='utf-8') as f:
                f.write(fast_web)
            
            logger.info("✅ Fast web interface created")
            return str(fast_web_file)
        except Exception as e:
            logger.error(f"❌ Failed to create fast web interface: {e}")
            return ""
    
    def create_fast_start_script(self) -> str:
        """สร้างสคริปต์เริ่มต้นแบบเร็ว"""
        fast_start = '''@echo off
REM 🚀 VICTOR-TTS FAST START
REM เวอร์ชันที่เร็วขึ้น

title VICTOR-TTS FAST

echo.
echo ========================================
echo 🎙️  VICTOR-TTS FAST SYSTEM  🎙️
echo ========================================
echo ✅ Optimized for Speed
echo ✅ Fast Startup
echo ✅ Reduced Memory Usage
echo ========================================
echo.

REM ตรวจสอบ Python
if exist "venv\\Scripts\\python.exe" (
    set PYTHON_CMD=venv\\Scripts\\python.exe
    echo ✅ Using Virtual Environment
) else (
    set PYTHON_CMD=python
    echo ⚠️  Using System Python
)

echo 📌 Python Info:
%PYTHON_CMD% --version

echo.
echo 🚀 Starting Fast Web Interface...
echo 🔗 URL: http://localhost:7000
echo.

%PYTHON_CMD% web_interface_fast.py

pause
'''
        
        fast_start_file = self.project_root / "start_fast.bat"
        try:
            with open(fast_start_file, 'w', encoding='utf-8') as f:
                f.write(fast_start)
            
            logger.info("✅ Fast start script created")
            return str(fast_start_file)
        except Exception as e:
            logger.error(f"❌ Failed to create fast start script: {e}")
            return ""
    
    def test_system(self):
        """ทดสอบระบบ"""
        logger.info("🧪 Testing system performance...")
        
        # ทดสอบการโหลด core
        start_time = time.time()
        try:
            from tts_rvc_core_optimized import create_optimized_core_instance
            core = create_optimized_core_instance()
            load_time = time.time() - start_time
            logger.info(f"✅ Core loaded in {load_time:.2f} seconds")
            
            # ทดสอบ TTS
            status = core.get_system_status()
            logger.info(f"✅ System status: {status}")
            
        except Exception as e:
            logger.error(f"❌ Core test failed: {e}")
    
    def run_fixes(self):
        """รันการแก้ไขทั้งหมด"""
        logger.info("🔧 Starting performance fixes...")
        
        # 1. แก้ไขการตั้งค่าประสิทธิภาพ
        logger.info("📝 Fixing performance config...")
        self.fix_performance_config()
        
        # 2. สร้าง optimized core
        logger.info("⚡ Creating optimized core...")
        optimized_core = self.create_optimized_core()
        
        # 3. สร้าง fast web interface
        logger.info("🌐 Creating fast web interface...")
        fast_web = self.create_fast_web_interface()
        
        # 4. สร้าง fast start script
        logger.info("🚀 Creating fast start script...")
        fast_start = self.create_fast_start_script()
        
        # 5. ทดสอบระบบ
        logger.info("🧪 Testing system...")
        self.test_system()
        
        logger.info("✅ All fixes completed!")
        logger.info(f"📁 Optimized core: {optimized_core}")
        logger.info(f"🌐 Fast web interface: {fast_web}")
        logger.info(f"🚀 Fast start script: {fast_start}")
        logger.info("🎯 Use 'start_fast.bat' for faster startup")

def main():
    """ฟังก์ชันหลัก"""
    print("🔧 VICTOR-TTS Performance Fixer")
    print("=" * 50)
    
    fixer = PerformanceFixer()
    fixer.run_fixes()

if __name__ == "__main__":
    main() 