#!/usr/bin/env python3
"""
🌐 VICTOR-TTS Improved Web Interface - เวอร์ชันที่ปรับปรุงแล้ว
ผลลัพธ์อยู่ใกล้ปุ่มสร้างเสียง
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

class ImprovedWebInterface:
    """Web Interface ที่ปรับปรุงแล้ว"""
    
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
        """สร้างหน้าเว็บหลักแบบปรับปรุงแล้ว"""
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
        
        # HTML template แบบปรับปรุงแล้ว
        html = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VICTOR-TTS IMPROVED</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');
        
        body {{ 
            font-family: 'Sarabun', sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        h1 {{ 
            color: #333; 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .form-group {{ 
            margin-bottom: 20px; 
        }}
        
        label {{ 
            display: block; 
            margin-bottom: 8px; 
            font-weight: bold; 
            color: #555;
            font-size: 1.1em;
        }}
        
        textarea, select {{ 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e0e0e0; 
            border-radius: 10px; 
            font-size: 1em;
            font-family: 'Sarabun', sans-serif;
            transition: border-color 0.3s, box-shadow 0.3s;
        }}
        
        textarea:focus, select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .button-result-container {{
            margin-top: 30px;
            text-align: center;
        }}
        
        button {{ 
            background: linear-gradient(45deg, #667eea, #764ba2); 
            color: white; 
            padding: 18px 40px; 
            border: none; 
            border-radius: 50px; 
            cursor: pointer; 
            font-size: 1.2em;
            font-weight: bold;
            font-family: 'Sarabun', sans-serif;
            transition: all 0.3s;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }}
        
        button:hover {{ 
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        }}
        
        button:disabled {{
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }}
        
        .result {{ 
            margin-top: 20px; 
            padding: 25px; 
            background: linear-gradient(135deg, #e8f5e8, #f0f8ff); 
            border-radius: 15px; 
            border: 2px solid #4CAF50;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2);
            opacity: 0;
            transform: translateY(-20px);
            transition: all 0.5s ease;
        }}
        
        .result.show {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        .result h3 {{
            color: #2E7D32;
            margin-top: 0;
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.5em;
        }}
        
        audio {{ 
            width: 100%; 
            margin: 15px 0; 
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .download-btn {{
            display: inline-block;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-family: 'Sarabun', sans-serif;
            transition: all 0.3s;
            margin-top: 15px;
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        }}
        
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
        }}
        
        .status {{
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
        }}
        
        .status.success {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        
        .status.error {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        
        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
                margin: 10px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            button {{
                padding: 15px 30px;
                font-size: 1.1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ VICTOR-TTS IMPROVED</h1>
        
        <div class="form-group">
            <label for="text">📝 ข้อความ:</label>
            <textarea id="text" rows="5" placeholder="ใส่ข้อความที่นี่... (ไม่จำกัดความยาว)"></textarea>
        </div>
        
        <div class="form-group">
            <label for="voice">🎤 เสียง TTS:</label>
            <select id="voice">
                <option value="">-- เลือกเสียง --</option>
                {voices_options}
            </select>
        </div>
        
        <div class="form-group">
            <label for="rvc_model">🎭 โมเดล RVC (ไม่บังคับ):</label>
            <select id="rvc_model">
                <option value="">ไม่ใช้ RVC</option>
                {models_options}
            </select>
        </div>
        
        <div class="button-result-container">
            <button onclick="generateAudio()" id="generateBtn">🚀 สร้างเสียง</button>
            
            <div id="result" class="result">
                <h3>🎵 ผลลัพธ์</h3>
                <audio id="audio" controls></audio>
                <br>
                <a id="download" href="#" download="output.wav" class="download-btn">📥 ดาวน์โหลดไฟล์เสียง</a>
            </div>
        </div>
        
        <div id="status" class="status" style="display: none;"></div>
    </div>
    
    <script>
        async function generateAudio() {{
            const text = document.getElementById('text').value;
            const voice = document.getElementById('voice').value;
            const rvc_model = document.getElementById('rvc_model').value;
            
            if (!text || !voice) {{
                showStatus('กรุณาใส่ข้อความและเลือกเสียง', 'error');
                return;
            }}
            
            const button = document.getElementById('generateBtn');
            const resultDiv = document.getElementById('result');
            
            // ปิดปุ่มและแสดงสถานะ
            button.disabled = true;
            button.innerHTML = '<span class="loading"></span>กำลังประมวลผล...';
            hideStatus();
            
            // ซ่อนผลลัพธ์เก่า
            resultDiv.classList.remove('show');
            
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
                    
                    // แสดงผลลัพธ์
                    resultDiv.classList.add('show');
                    
                    // เลื่อนไปที่ผลลัพธ์
                    resultDiv.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                    
                    showStatus('✅ สร้างเสียงสำเร็จ!', 'success');
                }} else {{
                    showStatus('❌ เกิดข้อผิดพลาด: ' + result.error, 'error');
                }}
            }} catch (error) {{
                showStatus('❌ เกิดข้อผิดพลาด: ' + error.message, 'error');
            }} finally {{
                // เปิดปุ่มกลับ
                button.disabled = false;
                button.innerHTML = '🚀 สร้างเสียง';
            }}
        }}
        
        function showStatus(message, type) {{
            const statusDiv = document.getElementById('status');
            statusDiv.textContent = message;
            statusDiv.className = `status ${{type}}`;
            statusDiv.style.display = 'block';
            
            // ซ่อนสถานะหลังจาก 5 วินาที
            setTimeout(() => {{
                hideStatus();
            }}, 5000);
        }}
        
        function hideStatus() {{
            const statusDiv = document.getElementById('status');
            statusDiv.style.display = 'none';
        }}
        
        // เพิ่ม event listener สำหรับ Enter key
        document.getElementById('text').addEventListener('keydown', function(e) {{
            if (e.key === 'Enter' && e.ctrlKey) {{
                generateAudio();
            }}
        }});
    </script>
</body>
</html>
"""
        return html
    
    def create_simple_server(self):
        """สร้าง server แบบง่าย"""
        import http.server
        import socketserver
        
        class ImprovedRequestHandler(http.server.BaseHTTPRequestHandler):
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
        
        class ImprovedServer(socketserver.TCPServer):
            def __init__(self, server_address, handler_class, web_interface):
                self.web_interface = web_interface
                super().__init__(server_address, handler_class)
            
            def finish_request(self, request, client_address):
                self.RequestHandlerClass(request, client_address, self, web_interface=self.web_interface)
        
        return ImprovedServer(('localhost', self.port), ImprovedRequestHandler, self)
    
    def start(self, open_browser: bool = True):
        """เริ่มต้น server"""
        try:
            server = self.create_simple_server()
            self.is_running = True
            
            print(f"🌐 Improved Web Interface started on http://localhost:{self.port}")
            print("✅ Enhanced UI with better result positioning")
            
            if open_browser:
                def open_browser_delayed():
                    import time
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{self.port}')
                
                import threading
                threading.Thread(target=open_browser_delayed, daemon=True).start()
            
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Server error: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Starting Improved Web Interface...")
    
    interface = ImprovedWebInterface()
    interface.start()

if __name__ == "__main__":
    main() 