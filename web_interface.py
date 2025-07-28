#!/usr/bin/env python3
"""
🌐 VICTOR-TTS Web Interface - เว็บอินเทอร์เฟซสำหรับใช้งาน TTS + RVC
อินเทอร์เฟซที่เรียบง่าย ใช้งานง่าย และครบถ้วน
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

# Import core system
try:
    from tts_rvc_core import TTSRVCCore, get_supported_voices, create_core_instance
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    print("⚠️ TTS-RVC Core not available")

class WebInterface:
    """Web Interface สำหรับ TTS-RVC System"""
    
    def __init__(self, port: int = 7000):
        self.port = self._find_available_port(port)
        self.core = None
        self.is_running = False
        
        if CORE_AVAILABLE:
            try:
                self.core = create_core_instance()
                print("✅ TTS-RVC Core loaded in Web Interface")
            except Exception as e:
                print(f"⚠️ Failed to load TTS-RVC Core: {e}")
                self.core = None
    
    def _find_available_port(self, start_port: int) -> int:
        """หาพอร์ตที่ว่างเริ่มต้นจาก start_port"""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return start_port  # ถ้าไม่เจอ port ว่างให้ใช้ port เดิม
    
    def generate_html_page(self) -> str:
        """สร้างหน้าเว็บหลัก"""
        
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
        
        html_content = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎙️ VICTOR-TTS Interface</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyMCIgaGVpZ2h0PSIxMDgwIiB2aWV3Qm94PSIwIDAgMTkyMCAxMDgwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZGVmcz4KPHJhZGlhbEdyYWRpZW50IGlkPSJteUdyYWRpZW50IiBjeD0iNTAlIiBjeT0iNTAlIiByPSI3MCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMDAwMDAwO3N0b3Atb3BhY2l0eTowLjgiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMDAwMDAwO3N0b3Atb3BhY2l0eTowLjQiLz4KPC9yYWRpYWxHcmFkaWVudD4KPC9kZWZzPgo8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI215R3JhZGllbnQpIi8+Cjx0ZXh0IHg9Ijk2MCIgeT0iNTQwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM0MEE3RjAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk5hZ2EgRHJhZ29ucyBCYWNrZ3JvdW5kPC90ZXh0Pgo8L3N2Zz4K') center center/cover no-repeat fixed, linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #333;
            position: relative;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyMCIgaGVpZ2h0PSIxMDgwIiB2aWV3Qm94PSIwIDAgMTkyMCAxMDgwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8ZGVmcz4KPHJhZGlhbEdyYWRpZW50IGlkPSJteUdyYWRpZW50IiBjeD0iNTAlIiBjeT0iNTAlIiByPSI3MCUiPgo8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMDAwMDAwO3N0b3Atb3BhY2l0eTowLjMiLz4KPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMDAwMDAwO3N0b3Atb3BhY2l0eTowLjEiLz4KPC9yYWRpYWxHcmFkaWVudD4KPC9kZWZzPgo8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI215R3JhZGllbnQpIi8+Cjx0ZXh0IHg9Ijk2MCIgeT0iNTQwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM0MEE3RjAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk5hZ2EgRHJhZ29ucyBCYWNrZ3JvdW5kPC90ZXh0Pgo8L3N2Zz4K') center center/cover no-repeat;
            opacity: 0.3;
            z-index: -1;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-top: 20px;
            margin-bottom: 20px;
            min-height: calc(100vh - 40px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 25px;
            border: 2px solid #4A90E2;
            box-shadow: 0 5px 15px rgba(74, 144, 226, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(74, 144, 226, 0.1) 50%, transparent 70%);
            animation: shimmer 3s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.2em;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .status-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(248, 249, 250, 0.9);
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border: 1px solid rgba(74, 144, 226, 0.3);
            backdrop-filter: blur(5px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .status-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
        }}
        
        .status-item.success {{
            color: #28a745;
        }}
        
        .status-item.info {{
            color: #17a2b8;
        }}
        
        .main-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 25px;
        }}
        
        .section {{
            background: rgba(248, 249, 250, 0.9);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(74, 144, 226, 0.3);
            backdrop-filter: blur(5px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .section h3 {{
            margin: 0 0 15px 0;
            color: #1a1a2e;
            font-size: 1.3em;
            border-bottom: 2px solid #4A90E2;
            padding-bottom: 8px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }}
        
        .form-group {{
            margin-bottom: 15px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #495057;
            font-size: 0.95em;
        }}
        
        .form-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        .form-row-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }}
        
        input[type="text"], input[type="number"], select, textarea {{
            width: 100%;
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }}
        
        input[type="text"]:focus, input[type="number"]:focus, select:focus, textarea:focus {{
            outline: none;
            border-color: #4A90E2;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
            background: rgba(255, 255, 255, 0.95);
        }}
        
        .button {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            padding: 12px 25px;
            border: 2px solid #4A90E2;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
            width: 100%;
            position: relative;
            overflow: hidden;
        }}
        
        .button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(74, 144, 226, 0.3), transparent);
            transition: left 0.5s;
        }}
        
        .button:hover::before {{
            left: 100%;
        }}
        
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4);
            border-color: #5BA0F2;
        }}
        
        .button:active {{
            transform: translateY(0);
        }}
        
        .button-secondary {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border-color: #95a5a6;
        }}
        
        .button-secondary:hover {{
            box-shadow: 0 5px 15px rgba(149, 165, 166, 0.4);
            border-color: #bdc3c7;
        }}
        
        .checkbox-group {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 15px;
        }}
        
        .checkbox-group input[type="checkbox"] {{
            width: auto;
            margin: 0;
        }}
        
        .slider-container {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .slider-container input[type="range"] {{
            flex: 1;
        }}
        
        .slider-container span {{
            min-width: 50px;
            text-align: center;
            font-weight: 500;
            color: #495057;
        }}
        
        .upload-area {{
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9fa;
        }}
        
        .upload-area:hover {{
            border-color: #667eea;
            background: #e3f2fd;
        }}
        
        .upload-icon {{
            font-size: 3em;
            margin-bottom: 10px;
            color: #6c757d;
        }}
        
        .upload-text {{
            font-size: 1.1em;
            color: #495057;
            margin-bottom: 5px;
        }}
        
        .upload-hint {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        .file-input {{
            display: none;
        }}
        
        .upload-progress {{
            width: 100%;
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
            display: none;
        }}
        
        .upload-progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            width: 0%;
            transition: width 0.3s;
        }}
        
        .btn-small {{
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .btn-success {{
            background: #28a745;
            color: white;
        }}
        
        .btn-danger {{
            background: #dc3545;
            color: white;
        }}
        
        .btn-primary {{
            background: #007bff;
            color: white;
        }}
        
        .btn-small:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        .model-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .model-table th {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            padding: 10px;
            text-align: left;
            border-radius: 8px 8px 0 0;
            font-size: 0.9em;
            border: 1px solid #4A90E2;
        }}
        
        .model-table td {{
            padding: 8px 10px;
            border-bottom: 1px solid #dee2e6;
            background: #f8f9fa;
            font-size: 0.85em;
        }}
        
        .model-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .model-table tr:nth-child(odd) {{
            background: #ffffff;
        }}
        
        .model-table tr:hover {{
            background: #e3f2fd !important;
        }}
        
        #modelSearchInput:focus {{
            outline: none;
            border-color: #4A90E2;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
        }}
        
        .model-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin-bottom: 10px;
            background: #f8f9fa;
        }}
        
        .model-info {{
            flex: 1;
        }}
        
        .model-name {{
            font-weight: 600;
            color: #495057;
            margin-bottom: 3px;
        }}
        
        .model-details {{
            font-size: 0.85em;
            color: #6c757d;
        }}
        
        .model-actions {{
            display: flex;
            gap: 5px;
        }}
        
        .compact-section {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
            margin-bottom: 15px;
        }}
        
        .compact-section h4 {{
            margin: 0 0 10px 0;
            color: #495057;
            font-size: 1.1em;
            border-bottom: 1px solid #667eea;
            padding-bottom: 5px;
        }}
        
        .compact-form-group {{
            margin-bottom: 10px;
        }}
        
        .compact-form-group label {{
            display: block;
            margin-bottom: 3px;
            font-weight: 500;
            color: #495057;
            font-size: 0.9em;
        }}
        
        .compact-input {{
            width: 100%;
            padding: 8px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 13px;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }}
        
        .compact-input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
        }}
        
        .compact-button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.3s;
            width: 100%;
        }}
        
        .compact-button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        }}
        
        .compact-form-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .compact-form-row-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .compact-checkbox-group {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        
        .compact-slider-container {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .compact-slider-container input[type="range"] {{
            flex: 1;
        }}
        
        .compact-slider-container span {{
            min-width: 40px;
            text-align: center;
            font-weight: 500;
            color: #495057;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            padding: 15px;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 1px solid #e9ecef;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 VICTOR-TTS Naga Interface</h1>
            <p>ระบบสร้างเสียงและแปลงเสียงด้วย AI - พลังแห่ง Naga Dragons</p>
        </div>
        
        <div class="content">
            <!-- Status Bar -->
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-icon">{"🎵" if status.get("tts_available") else "❌"}</div>
                    <div class="status-text">TTS: {"พร้อมใช้งาน" if status.get("tts_available") else "ไม่พร้อม"}</div>
                </div>
                <div class="status-item">
                    <div class="status-icon">{"🎭" if status.get("rvc_available") else "❌"}</div>
                    <div class="status-text">RVC: {"พร้อมใช้งาน" if status.get("rvc_available") else "ไม่พร้อม"}</div>
                </div>
                <div class="status-item">
                    <div class="status-icon">🎯</div>
                    <div class="status-text">โมเดล: {status.get("rvc_models_count", 0)} ตัว</div>
                </div>
            </div>
            

            
            <!-- System Control Panel -->
            <div class="section">
                <h3>⚙️ ควบคุมระบบ</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <button class="button" id="testSystemBtn" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                        🧪 ทดสอบระบบ
                    </button>
                    <button class="button" id="checkStatusBtn" style="background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);">
                        🔍 ตรวจสอบสถานะ
                    </button>
                    <button class="button" id="showModelsBtn" style="background: linear-gradient(135deg, #fd7e14 0%, #e83e8c 100%);">
                        📋 แสดงโมเดล
                    </button>
                    <button class="button" id="clearCacheBtn" style="background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);">
                        🧹 ล้างแคช
                    </button>
                    <button class="button" id="resetSettingsBtn" style="background: linear-gradient(135deg, #6c757d 0%, #495057 100%);">
                        🔄 รีเซ็ตการตั้งค่า
                    </button>
                    <button class="button" id="showHelpBtn" style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);">
                        ❓ คู่มือการใช้งาน
                    </button>
                </div>
                <div id="systemStatus" style="margin-top: 15px;"></div>
            </div>
            
            <!-- Text Input Section -->
            <div class="section">
                <h3>📝 ข้อความที่ต้องการแปลง</h3>
                <div class="form-group">
                    <label for="inputText">พิมพ์ข้อความที่ต้องการแปลงเป็นเสียง:</label>
                    <textarea id="inputText" placeholder="พิมพ์ข้อความของคุณที่นี่...

ตัวอย่าง:
- สวัสดีครับ ยินดีต้อนรับสู่ระบบ VICTOR-TTS
- Hello, welcome to our TTS system
- このシステムをお試しください"></textarea>
                </div>
                <div class="form-group">
                    <label>จำนวนตัวอักษร: <span id="charCount">0</span></label>
                </div>
            </div>
            
            <!-- Device Selection -->
            <div class="section">
                <h3>⚙️ การเลือกอุปกรณ์ประมวลผล</h3>
                <div class="form-group">
                    <label for="deviceSelect">เลือกอุปกรณ์:</label>
                    <select id="deviceSelect" onchange="changeDevice()">
                        <option value="cpu">🖥️ CPU Only (เสถียรที่สุด)</option>
                        <option value="auto">⚡ AUTO (เลือก GPU ที่ดีที่สุด)</option>
                    </select>
                    <div id="deviceStatus" style="margin-top: 5px; font-size: 0.9em; color: #6c757d;">
                        <span id="currentDevice">กำลังโหลด...</span>
                    </div>
                </div>
                <div class="form-group" style="margin-top: 10px; padding: 10px; background: #e8f5e8; border-radius: 8px; border-left: 4px solid #28a745;">
                    <small style="color: #155724;">
                        <strong>💡 คำแนะนำ:</strong> 
                        • <strong>CPU Only:</strong> เสถียรที่สุด เหมาะสำหรับการใช้งานทั่วไป<br>
                        • <strong>AUTO:</strong> ระบบจะเลือก GPU ที่ดีที่สุดอัตโนมัติ (เร็วขึ้น 3-5 เท่า)<br>
                        • การเปลี่ยนอุปกรณ์จะรีสตาร์ทระบบอัตโนมัติ
                    </small>
                </div>
            </div>
            
            <!-- TTS Settings -->
            <div class="section">
                <h3>🎵 การตั้งค่า Text-to-Speech</h3>
                <div class="form-group">
                    <label for="voiceSelect">เลือกเสียง:</label>
                    <select id="voiceSelect">
                        {voices_options}
                    </select>
                </div>
                <div class="form-group">
                    <label for="speedSlider">ความเร็วในการพูด:</label>
                    <div class="slider-container">
                        <input type="range" id="speedSlider" class="slider" min="0.5" max="2.0" step="0.1" value="1.0">
                        <div class="slider-value" id="speedValue">1.0x</div>
                    </div>
                </div>
                <div class="checkbox-container">
                    <input type="checkbox" id="enableMultiLanguage" checked>
                    <label for="enableMultiLanguage">🌐 เปิดใช้งานการประมวลผลหลายภาษา (แนะนำสำหรับข้อความผสมภาษา)</label>
                </div>
                <div class="form-group" style="margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff;">
                    <small style="color: #6c757d;">
                        <strong>💡 คำแนะนำ:</strong> เปิดใช้งานเพื่อให้ระบบตรวจจับและแยกการประมวลผลข้อความตามภาษา 
                        เช่น ข้อความภาษาลาวที่มีคำภาษาอังกฤษ จะถูกอ่านด้วยเสียงที่เหมาะสมสำหรับแต่ละภาษา
                    </small>
                </div>
                <div class="form-group" style="margin-top: 10px; padding: 10px; background: #e8f5e8; border-radius: 8px; border-left: 4px solid #28a745;">
                    <small style="color: #155724;">
                        <strong>🌍 ภาษาที่รองรับ:</strong><br>
                        🇹🇭 ไทย (Thai) | 🇱🇦 ลาว (Lao) | 🇺🇸 อังกฤษ (English)<br>
                        🇯🇵 ญี่ปุ่น (Japanese) | 🇨🇳 จีน (Chinese) | 🔢 ตัวเลข (Numbers)
                    </small>
                </div>
                <div class="form-group" style="margin-top: 10px; padding: 10px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">
                    <small style="color: #856404;">
                        <strong>🎯 ตัวอย่างการใช้งาน:</strong><br>
                        "สวัสดีครับ Hello world ສະບາຍດີ 123" → จะถูกแยกเป็น 4 ส่วนและอ่านด้วยเสียงที่เหมาะสม
                    </small>
                </div>
            </div>
            
            <!-- RVC Settings -->
            <div class="section">
                <h3>🎭 การตั้งค่าการแปลงเสียง (Voice Conversion)</h3>
                <div class="checkbox-container">
                    <input type="checkbox" id="enableRVC">
                    <label for="enableRVC">เปิดใช้งานการแปลงเสียง</label>
                </div>
                <div class="form-group">
                    <label for="modelSelect">เลือกโมเดลเสียง:</label>
                    <select id="modelSelect" disabled>
                        {models_options if models else '<option value="">ไม่มีโมเดลพร้อมใช้งาน</option>'}
                    </select>
                    <div id="rvcStatus" style="margin-top: 5px; font-size: 0.9em; color: #6c757d;"></div>
                </div>
                <div class="form-group">
                    <label for="transposeSlider">การปรับ Pitch:</label>
                    <div class="slider-container">
                        <input type="range" id="transposeSlider" class="slider" min="-12" max="12" step="1" value="0" disabled>
                        <div class="slider-value" id="transposeValue">0</div>
                    </div>
                </div>
            </div>
            
            <!-- Generate Button -->
            <div class="section" style="text-align: center;">
                <button class="button" id="generateBtn" onclick="generateAudio()">
                    🚀 สร้างเสียง
                </button>
                <div class="progress-bar" id="progressBar" style="display: none;">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
            
            <!-- Result Section -->
            <div class="section result-section" id="resultSection" style="display: none;">
                <h3>🎧 ผลลัพธ์</h3>
                <div id="statusMessage"></div>
                
                <!-- Language Detection Results -->
                <div id="languageDetectionSection" style="display: none; margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #17a2b8;">
                    <h4 style="margin-top: 0; color: #17a2b8;">🌍 การตรวจจับภาษา</h4>
                    <div id="languageDetectionResults"></div>
                </div>
                
                <!-- TTS Audio Player -->
                <div id="ttsAudioSection" style="display: none;">
                    <h4>🎵 เสียงต้นฉบับ (TTS)</h4>
                    <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">เสียงที่สร้างจากข้อความโดยตรง</p>
                    <audio id="ttsAudioPlayer" class="audio-player" controls></audio>
                    <button id="downloadTTSBtn" class="download-btn" onclick="downloadAudio('tts')">📥 ดาวน์โหลดเสียงต้นฉบับ</button>
                </div>
                
                <!-- RVC Audio Player -->
                <div id="rvcAudioSection" style="display: none;">
                    <h4>🎭 เสียงที่แปลงแล้ว (RVC)</h4>
                    <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">เสียงที่แปลงด้วยโมเดล RVC ที่เลือก</p>
                    <div id="rvcStatus" style="margin-bottom: 10px; padding: 8px; border-radius: 6px; background: #f8f9fa; border-left: 3px solid #007bff;">
                        <small style="color: #495057;">
                            <strong>สถานะ:</strong> <span id="rvcStatusText">พร้อมใช้งาน</span>
                        </small>
                    </div>
                    <audio id="rvcAudioPlayer" class="audio-player" controls></audio>
                    <button id="downloadRVCBtn" class="download-btn" onclick="downloadAudio('rvc')">📥 ดาวน์โหลดเสียงที่แปลงแล้ว</button>
                </div>
                
                <!-- Combined Audio Player (for backward compatibility) -->
                <div id="combinedAudioSection" style="display: none;">
                    <h4>🎧 เสียงรวม</h4>
                    <audio id="audioPlayer" class="audio-player" controls></audio>
                    <button id="downloadCombinedBtn" class="download-btn" onclick="downloadAudio('combined')">📥 ดาวน์โหลด</button>
                </div>
                
                <div class="stats" id="statsContainer"></div>
            </div>
            
            <!-- Model Management Section -->
            <div class="section">
                <h3>📁 จัดการโมเดลเสียง (Model Management)</h3>
                <div class="form-group">
                    <label>อัปโหลดโมเดลเสียงใหม่:</label>
                    <div class="upload-area" id="uploadArea" onclick="document.getElementById('modelFileInput').click()">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">คลิกเพื่อเลือกไฟล์ หรือ ลากวางไฟล์ที่นี่</div>
                        <div class="upload-hint">รองรับไฟล์ .pth, .pt, .ckpt (ขนาดสูงสุด 500MB)</div>
                        <input type="file" id="modelFileInput" class="file-input" accept=".pth,.pt,.ckpt" onchange="handleFileSelect(event)">
                    </div>
                    <div class="upload-progress" id="uploadProgress">
                        <div class="upload-progress-fill" id="uploadProgressFill"></div>
                    </div>
                </div>
                
                <!-- Model List Toggle -->
                <div class="form-group" style="margin-top: 20px;">
                    <button class="button" id="toggleModelListBtn" style="background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%); width: auto; padding: 10px 20px; font-size: 14px;">
                        📋 แสดงรายการโมเดล ({len(models)} ตัว)
                    </button>
                </div>
                
                <!-- Model List (Hidden by default) -->
                <div class="model-list" id="modelList" style="display: none;">
                    <h4>📋 โมเดลที่มีอยู่:</h4>
                    
                    <!-- Search Box -->
                    <div class="form-group" style="margin-bottom: 15px;">
                        <input type="text" id="modelSearchInput" placeholder="🔍 ค้นหาโมเดล..." 
                               style="width: 100%; padding: 10px; border: 2px solid #dee2e6; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <!-- Model Stats -->
                    <div style="margin-bottom: 15px; padding: 10px; background: #e7f3ff; border-radius: 8px; border-left: 4px solid #007bff;">
                        <small style="color: #495057;">
                            <strong>📊 สถิติ:</strong> พบโมเดลทั้งหมด <span id="modelCount">{len(models)}</span> ตัว
                        </small>
                    </div>
                    
                    <div id="modelItems">
                        {self._generate_model_list_html(models)}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentAudio = null;
        
        // Update character count
        document.getElementById('inputText').addEventListener('input', function() {{
            let text = this.value;
            document.getElementById('charCount').textContent = text.length;
        }});
        
        // Update speed value
        document.getElementById('speedSlider').addEventListener('input', function() {{
            document.getElementById('speedValue').textContent = this.value + 'x';
        }});
        
        // Update transpose value
        document.getElementById('transposeSlider').addEventListener('input', function() {{
            document.getElementById('transposeValue').textContent = this.value;
        }});
        
        // Enable/disable RVC controls
        document.getElementById('enableRVC').addEventListener('change', function() {{
            let enabled = this.checked;
            document.getElementById('modelSelect').disabled = !enabled;
            document.getElementById('transposeSlider').disabled = !enabled;
        }});
        
        // Toggle model list
        document.getElementById('toggleModelListBtn').addEventListener('click', function() {{
            let modelList = document.getElementById('modelList');
            let button = document.getElementById('toggleModelListBtn');
            
            if (modelList.style.display === 'none') {{
                modelList.style.display = 'block';
                button.innerHTML = '📋 ซ่อนรายการโมเดล';
                button.style.background = 'linear-gradient(135deg, #dc3545 0%, #fd7e14 100%)';
            }} else {{
                modelList.style.display = 'none';
                button.innerHTML = '📋 แสดงรายการโมเดล';
                button.style.background = 'linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%)';
            }}
        }});
        
        // Model search functionality
        document.getElementById('modelSearchInput').addEventListener('input', function() {{
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('#modelItems tbody tr');
            let visibleCount = 0;
            
            tableRows.forEach(row => {{
                const modelName = row.cells[1].textContent.toLowerCase();
                if (modelName.includes(searchTerm)) {{
                    row.style.display = '';
                    visibleCount++;
                }} else {{
                    row.style.display = 'none';
                }}
            }});
            
            // Update model count
            document.getElementById('modelCount').textContent = visibleCount;
        }});
        
        // File upload handling
        function handleFileSelect(event) {{
            const file = event.target.files[0];
            if (file) {{
                uploadModel(file);
            }}
        }}
        
        // Drag and drop functionality
        const uploadArea = document.getElementById('uploadArea');
        
        uploadArea.addEventListener('dragover', function(e) {{
            e.preventDefault();
            uploadArea.classList.add('dragover');
        }});
        
        uploadArea.addEventListener('dragleave', function(e) {{
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        }});
        
        uploadArea.addEventListener('drop', function(e) {{
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {{
                uploadModel(files[0]);
            }}
        }});
        
        // Upload model function
        function uploadModel(file) {{
            if (!file) return;
            
            // Check file type
            const allowedTypes = ['.pth', '.pt', '.ckpt'];
            const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
            if (!allowedTypes.includes(fileExtension)) {{
                showNotification('❌ ไฟล์ไม่ถูกต้อง กรุณาเลือกไฟล์ .pth, .pt, หรือ .ckpt', 'error');
                return;
            }}
            
            // Check file size (500MB limit)
            if (file.size > 500 * 1024 * 1024) {{
                showNotification('❌ ไฟล์ใหญ่เกินไป ขนาดสูงสุด 500MB', 'error');
                return;
            }}
            
            const formData = new FormData();
            formData.append('model', file);
            
            // Show progress bar
            const progressBar = document.getElementById('uploadProgress');
            const progressFill = document.getElementById('uploadProgressFill');
            progressBar.style.display = 'block';
            
            fetch('/upload_model', {{
                method: 'POST',
                body: formData
            }})
            .then(response => response.json())
            .then(data => {{
                progressBar.style.display = 'none';
                if (data.success) {{
                    showNotification('✅ อัปโหลดโมเดลสำเร็จ: ' + file.name, 'success');
                    refreshModelList();
                }} else {{
                    showNotification('❌ อัปโหลดล้มเหลว: ' + data.error, 'error');
                }}
            }})
            .catch(error => {{
                progressBar.style.display = 'none';
                showNotification('❌ เกิดข้อผิดพลาดในการอัปโหลด: ' + error.message, 'error');
            }});
            
            // Simulate progress (since we can't track actual upload progress with basic fetch)
            let progress = 0;
            const progressInterval = setInterval(() => {{
                progress += Math.random() * 10;
                if (progress > 90) progress = 90;
                progressFill.style.width = progress + '%';
            }}, 200);
            
            // Clear interval when upload completes
            setTimeout(() => {{
                clearInterval(progressInterval);
                progressFill.style.width = '100%';
            }}, 3000);
        }}
        
        // Refresh model list
        function refreshModelList() {{
            fetch('/models')
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    updateModelList(data.data);
                    updateModelSelect(data.data);
                }}
            }})
            .catch(error => {{
                console.error('Error refreshing model list:', error);
            }});
        }}
        
        // Update model list display
        function updateModelList(models) {{
            const modelItems = document.getElementById('modelItems');
            if (models.length === 0) {{
                modelItems.innerHTML = '<p style="color: #6c757d; text-align: center; padding: 20px;">ไม่มีโมเดลที่อัปโหลด</p>';
                return;
            }}
            
            let html = `
                <table class="model-table">
                    <thead>
                        <tr>
                            <th>ลำดับ</th>
                            <th>ชื่อโมเดล</th>
                            <th>ประเภท</th>
                            <th>สถานะ</th>
                            <th>การจัดการ</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            models.forEach((model, index) => {{
                html += `
                    <tr>
                        <td>${{index + 1}}</td>
                        <td><strong>${{model.name}}</strong></td>
                        <td>${{model.type || 'RVC Model'}}</td>
                        <td>${{model.size || 'ไม่ทราบ'}}</td>
                        <td>
                            <button class="btn-small btn-success" onclick="testModel('${{model.name}}')" style="margin-right: 5px;">🧪 ทดสอบ</button>
                            <button class="btn-small btn-danger" onclick="deleteModel('${{model.name}}')">🗑️ ลบ</button>
                        </td>
                    </tr>
                `;
            }});
            
            html += `
                    </tbody>
                </table>
            `;
            modelItems.innerHTML = html;
        }}
        
        // Update model select dropdown
        function updateModelSelect(models) {{
            const modelSelect = document.getElementById('modelSelect');
            let options = '';
            models.forEach(model => {{
                options += `<option value="${{model.name}}">${{model.name}}</option>`;
            }});
            modelSelect.innerHTML = options || '<option value="">ไม่มีโมเดลพร้อมใช้งาน</option>';
        }}
        
        // Test model
        function testModel(modelName) {{
            showNotification('🧪 กำลังทดสอบโมเดล: ' + modelName, 'info');
            fetch('/test_model', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{model: modelName}})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    showNotification('✅ ทดสอบโมเดลสำเร็จ: ' + modelName, 'success');
                }} else {{
                    showNotification('❌ ทดสอบโมเดลล้มเหลว: ' + data.error, 'error');
                }}
            }})
            .catch(error => {{
                showNotification('❌ เกิดข้อผิดพลาดในการทดสอบ: ' + error.message, 'error');
            }});
        }}
        
        // Delete model
        function deleteModel(modelName) {{
            if (!confirm('คุณแน่ใจหรือไม่ที่จะลบโมเดล "' + modelName + '"?')) {{
                return;
            }}
            
            fetch('/delete_model', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{model: modelName}})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    showNotification('✅ ลบโมเดลสำเร็จ: ' + modelName, 'success');
                    refreshModelList();
                }} else {{
                    showNotification('❌ ลบโมเดลล้มเหลว: ' + data.error, 'error');
                }}
            }})
            .catch(error => {{
                showNotification('❌ เกิดข้อผิดพลาดในการลบ: ' + error.message, 'error');
            }});
        }}
        
        // Progress bar animation
        function animateProgress(duration) {{
            let progressBar = document.getElementById('progressBar');
            let progressFill = document.getElementById('progressFill');
            
            progressBar.style.display = 'block';
            let progress = 0;
            let interval = setInterval(() => {{
                progress += 100 / (duration * 10); // Update every 100ms
                progressFill.style.width = Math.min(progress, 95) + '%';
                
                if (progress >= 95) {{
                    clearInterval(interval);
                }}
            }}, 100);
            
            return () => {{
                clearInterval(interval);
                progressFill.style.width = '100%';
                setTimeout(() => {{
                    progressBar.style.display = 'none';
                    progressFill.style.width = '0%';
                }}, 500);
            }};
        }}
        
        // Show status message
        function showStatus(message, type = 'info') {{
            let statusMessage = document.getElementById('statusMessage');
            statusMessage.className = 'alert alert-' + type;
            statusMessage.textContent = message;
            statusMessage.style.display = 'block';
        }}
        
        // Show statistics
        function showStats(stats) {{
            let statsContainer = document.getElementById('statsContainer');
            statsContainer.innerHTML = '';
            
            let statItems = [
                {{ label: 'ขนาดข้อความ', value: stats.text_length + ' ตัวอักษร' }},
                {{ label: 'ขนาดเสียง', value: Math.round(stats.final_audio_size / 1024) + ' KB' }},
                {{ label: 'การประมวลผล', value: stats.processing_steps?.join(', ') || 'ไม่มีข้อมูล' }},
                {{ label: 'แปลงเสียง', value: stats.voice_conversion_applied ? 'ใช่' : 'ไม่ใช่' }}
            ];
            
            statItems.forEach(item => {{
                let statDiv = document.createElement('div');
                statDiv.className = 'stat-item';
                statDiv.innerHTML = `
                    <div class="stat-value">${{item.value}}</div>
                    <div class="stat-label">${{item.label}}</div>
                `;
                statsContainer.appendChild(statDiv);
            }});
            
            statsContainer.style.display = 'grid';
        }}
        
        // แสดงไฟล์เสียง TTS และ RVC แยกกัน
        function showTTSAndRVCAudio(ttsAudioData, rvcAudioData, stats) {{
            // ซ่อนส่วนอื่น
            document.getElementById('combinedAudioSection').style.display = 'none';
            
            // แสดงส่วน TTS เสมอ
            let ttsSection = document.getElementById('ttsAudioSection');
            let ttsPlayer = document.getElementById('ttsAudioPlayer');
            ttsSection.style.display = 'block';
            ttsPlayer.src = 'data:audio/wav;base64,' + ttsAudioData;
            
            // แสดงส่วน RVC เสมอ (ไม่ว่าจะสำเร็จหรือล้มเหลว)
            let rvcSection = document.getElementById('rvcAudioSection');
            let rvcStatusText = document.getElementById('rvcStatusText');
            let rvcStatus = document.getElementById('rvcStatus');
            let rvcPlayer = document.getElementById('rvcAudioPlayer');
            
            rvcSection.style.display = 'block';
            
            if (rvcAudioData) {{
                // RVC สำเร็จ
                rvcPlayer.src = 'data:audio/wav;base64,' + rvcAudioData;
                rvcStatusText.textContent = '✅ แปลงเสียงสำเร็จ - ฟังเสียงที่แปลงแล้วด้านล่าง';
                rvcStatus.style.borderLeftColor = '#28a745';
                rvcStatus.style.background = '#d4edda';
                rvcPlayer.style.display = 'block';
            }} else {{
                // RVC ล้มเหลว
                rvcPlayer.style.display = 'none';
                rvcStatusText.textContent = '❌ แปลงเสียงล้มเหลว - ฟังเฉพาะเสียงต้นฉบับด้านบน';
                rvcStatus.style.borderLeftColor = '#dc3545';
                rvcStatus.style.background = '#f8d7da';
            }}
            
            // เก็บข้อมูลสำหรับดาวน์โหลด
            window.ttsAudioData = ttsAudioData;
            window.rvcAudioData = rvcAudioData;
        }}
        
        // แสดงไฟล์เสียงรวม (สำหรับ TTS เท่านั้น)
        function showCombinedAudio(audioData, stats) {{
            // ซ่อนส่วนอื่น
            document.getElementById('ttsAudioSection').style.display = 'none';
            document.getElementById('rvcAudioSection').style.display = 'none';
            
            // แสดงส่วนรวม
            let combinedSection = document.getElementById('combinedAudioSection');
            let combinedPlayer = document.getElementById('audioPlayer');
            combinedSection.style.display = 'block';
            combinedPlayer.src = 'data:audio/wav;base64,' + audioData;
            
            // เก็บข้อมูลสำหรับดาวน์โหลด
            window.combinedAudioData = audioData;
        }}
        
        // Show notification
        function showNotification(message, type = 'info') {{
            const notification = document.createElement('div');
            notification.className = `notification ${{type}}`;
            notification.textContent = message;
            notification.style.position = 'fixed';
            notification.style.top = '20px';
            notification.style.right = '20px';
            notification.style.padding = '15px 20px';
            notification.style.borderRadius = '8px';
            notification.style.color = 'white';
            notification.style.fontWeight = '500';
            notification.style.zIndex = '1000';
            notification.style.maxWidth = '400px';
            notification.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
            notification.style.animation = 'slideIn 0.3s ease';
            
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {{
                    document.body.removeChild(notification);
                }}, 300);
            }}, 3000);
        }}
        
        // ฟังก์ชันดาวน์โหลดไฟล์เสียง
        function downloadAudio(type) {{
            let audioData = null;
            let filename = '';
            
            switch(type) {{
                case 'tts':
                    audioData = window.ttsAudioData;
                    filename = 'tts_audio_' + new Date().getTime() + '.wav';
                    break;
                case 'rvc':
                    audioData = window.rvcAudioData;
                    filename = 'rvc_audio_' + new Date().getTime() + '.wav';
                    break;
                case 'combined':
                    audioData = window.combinedAudioData || window.ttsAudioData;
                    filename = 'audio_' + new Date().getTime() + '.wav';
                    break;
                default:
                    audioData = window.finalAudioData || window.ttsAudioData;
                    filename = 'audio_' + new Date().getTime() + '.wav';
            }}
            
            if (audioData) {{
                // แปลง base64 เป็น blob
                const byteCharacters = atob(audioData);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {{
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }}
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], {{ type: 'audio/wav' }});
                
                // สร้างลิงก์ดาวน์โหลด
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                showNotification('📥 ดาวน์โหลด ' + filename + ' สำเร็จ', 'success');
            }} else {{
                showNotification('❌ ไม่มีไฟล์เสียงให้ดาวน์โหลด', 'error');
            }}
        }}
        
        // ฟังก์ชันโหลดข้อมูลอุปกรณ์
        async function loadDeviceInfo() {{
            try {{
                let response = await fetch('/device_info');
                let result = await response.json();
                
                if (result.success) {{
                    let deviceInfo = result.data;
                    let deviceSelect = document.getElementById('deviceSelect');
                    let currentDevice = document.getElementById('currentDevice');
                    
                    // อัปเดตตัวเลือกอุปกรณ์
                    deviceSelect.innerHTML = '';
                    
                    deviceInfo.device_options.forEach(option => {{
                        let optionElement = document.createElement('option');
                        optionElement.value = option.value;
                        optionElement.textContent = option.label;
                        deviceSelect.appendChild(optionElement);
                    }});
                    
                    // ตั้งค่าตัวเลือกปัจจุบัน
                    deviceSelect.value = deviceInfo.current_device;
                    
                    // แสดงสถานะปัจจุบัน
                    let deviceLabel = deviceInfo.current_device;
                    if (deviceInfo.current_device === 'cpu') {{
                        deviceLabel = '🖥️ CPU Only';
                    }} else if (deviceInfo.current_device.startsWith('cuda:')) {{
                        let gpuId = deviceInfo.current_device.split(':')[1];
                        let gpuInfo = deviceInfo.gpu_info.find(g => g.id == gpuId);
                        if (gpuInfo) {{
                            deviceLabel = '🚀 GPU ' + gpuId + ': ' + gpuInfo.name + ' (' + gpuInfo.memory.toFixed(1) + 'GB)';
                        }} else {{
                            deviceLabel = '🚀 GPU ' + gpuId;
                        }}
                    }}
                    
                    currentDevice.textContent = 'อุปกรณ์ปัจจุบัน: ' + deviceLabel;
                    
                    // แสดงข้อมูล GPU
                    if (deviceInfo.gpu_available) {{
                        let gpuInfo = deviceInfo.gpu_info.map(g => 
                            'GPU ' + g.id + ': ' + g.name + ' (' + g.memory.toFixed(1) + 'GB)'
                        ).join(', ');
                        currentDevice.innerHTML += '<br><small>GPU ที่พบ: ' + gpuInfo + '</small>';
                    }} else {{
                        currentDevice.innerHTML += '<br><small>ไม่พบ GPU - ใช้ CPU เท่านั้น</small>';
                    }}
                    
                }} else {{
                    document.getElementById('currentDevice').textContent = 'ไม่สามารถโหลดข้อมูลอุปกรณ์ได้';
                }}
            }} catch (error) {{
                console.error('Error loading device info:', error);
                document.getElementById('currentDevice').textContent = 'เกิดข้อผิดพลาดในการโหลดข้อมูล';
            }}
        }}
        
        // ฟังก์ชันเปลี่ยนอุปกรณ์
        async function changeDevice() {{
            let deviceSelect = document.getElementById('deviceSelect');
            let selectedDevice = deviceSelect.value;
            let currentDevice = document.getElementById('currentDevice');
            
            // แสดงสถานะกำลังเปลี่ยน
            currentDevice.textContent = '🔄 กำลังเปลี่ยนอุปกรณ์...';
            deviceSelect.disabled = true;
            
            try {{
                let response = await fetch('/change_device', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{device: selectedDevice}})
                }});
                
                let result = await response.json();
                
                if (result.success) {{
                    showNotification('✅ เปลี่ยนอุปกรณ์เป็น ' + result.device + ' สำเร็จ', 'success');
                    
                    // รีโหลดข้อมูลอุปกรณ์
                    await loadDeviceInfo();
                    
                    // รีโหลดโมเดล RVC
                    await loadModels();
                    
                }} else {{
                    showNotification('❌ เปลี่ยนอุปกรณ์ล้มเหลว: ' + (result.error || 'ไม่ทราบสาเหตุ'), 'error');
                    
                    // รีโหลดข้อมูลอุปกรณ์เพื่อแสดงสถานะปัจจุบัน
                    await loadDeviceInfo();
                }}
                
            }} catch (error) {{
                console.error('Error changing device:', error);
                showNotification('❌ เกิดข้อผิดพลาดในการเปลี่ยนอุปกรณ์: ' + error.message, 'error');
                
                // รีโหลดข้อมูลอุปกรณ์เพื่อแสดงสถานะปัจจุบัน
                await loadDeviceInfo();
            }} finally {{
                deviceSelect.disabled = false;
            }}
        }}
        
        // ฟังก์ชันทดสอบระบบ
        async function testSystem() {{
            let button = document.getElementById('generateBtn');
            button.disabled = true;
            button.textContent = 'กำลังทดสอบ...';
            
            try {{
                let response = await fetch('/test', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{}})
                }});
                
                let result = await response.json();
                
                if (result.success) {{
                    showNotification('✅ ' + result.message, 'success');
                }} else {{
                    showNotification('❌ ' + (result.error || 'การทดสอบล้มเหลว'), 'error');
                }}
            }} catch (error) {{
                showNotification('❌ เกิดข้อผิดพลาดในการทดสอบ: ' + error.message, 'error');
            }} finally {{
                button.disabled = false;
                button.textContent = 'สร้างเสียง';
            }}
        }}
        
        // ฟังก์ชันแสดงผลการตรวจจับภาษา
        function showLanguageDetectionResults(segments) {{
            let container = document.getElementById('languageDetectionSection');
            let resultsDiv = document.getElementById('languageDetectionResults');
            
            if (!segments || segments.length === 0) {{
                container.style.display = 'none';
                return;
            }}
            
            let html = '<div style="margin-bottom: 10px;">';
            html += '<strong>📝 รายละเอียดการแยกข้อความ:</strong></div>';
            
            segments.forEach((segment, index) => {{
                let languageLabel = getLanguageLabel(segment.language);
                let voiceLabel = getVoiceLabel(segment.voice);
                
                html += `<div style="margin-bottom: 8px; padding: 8px; background: white; border-radius: 6px; border-left: 3px solid #17a2b8;">`;
                html += `<div style="font-weight: bold; color: #17a2b8;">ส่วนที่ ${{index + 1}}: ${{languageLabel}}</div>`;
                html += `<div style="margin-top: 4px; color: #495057;">"${{segment.text}}"</div>`;
                html += `<div style="margin-top: 2px; font-size: 0.85em; color: #6c757d;">🎤 เสียง: ${{voiceLabel}}</div>`;
                html += `</div>`;
            }});
            
            resultsDiv.innerHTML = html;
            container.style.display = 'block';
        }}
        
        // ฟังก์ชันแปลงรหัสภาษาเป็นชื่อภาษา
        function getLanguageLabel(language) {{
            const languageMap = {{
                'thai': '🇹🇭 ไทย',
                'lao': '🇱🇦 ลาว', 
                'english': '🇺🇸 อังกฤษ',
                'japanese': '🇯🇵 ญี่ปุ่น',
                'chinese': '🇨🇳 จีน',
                'numbers': '🔢 ตัวเลข',
                'punctuation': '📝 เครื่องหมาย',
                'unknown': '❓ ไม่ทราบ'
            }};
            return languageMap[language] || language;
        }}
        
        // ฟังก์ชันแปลงรหัสเสียงเป็นชื่อเสียง
        function getVoiceLabel(voice) {{
            const voiceMap = {{
                'th-TH-PremwadeeNeural': 'Premwadee (ไทย)',
                'th-TH-NiranNeural': 'Niran (ไทย)',
                'th-TH-NiwatNeural': 'Niwat (ไทย)',
                'lo-LA-KeomanyNeural': 'Keomany (ลาว)',
                'lo-LA-ChanthavongNeural': 'Chanthavong (ลาว)',
                'en-US-AriaNeural': 'Aria (อังกฤษ)',
                'en-US-GuyNeural': 'Guy (อังกฤษ)',
                'en-US-JennyNeural': 'Jenny (อังกฤษ)',
                'ja-JP-NanamiNeural': 'Nanami (ญี่ปุ่น)',
                'zh-CN-XiaoxiaoNeural': 'Xiaoxiao (จีน)'
            }};
            return voiceMap[voice] || voice;
        }}
        
        // ฟังก์ชันสร้างเสียง
        async function generateAudio() {{
            let button = document.getElementById('generateBtn');
            button.disabled = true;
            button.textContent = 'กำลังสร้างเสียง...';
            
            let text = document.getElementById('inputText').value;
            let ttsVoice = document.getElementById('voiceSelect').value;
            let enableRVC = document.getElementById('enableRVC').checked;
            let rvcModel = document.getElementById('modelSelect').value;
            let ttsSpeed = parseFloat(document.getElementById('speedSlider').value);
            let rvcTranspose = parseInt(document.getElementById('transposeSlider').value);
            let enableMultiLanguage = document.getElementById('enableMultiLanguage').checked;
            
            if (!text.trim()) {{
                showNotification('❌ กรุณาใส่ข้อความ', 'error');
                button.disabled = false;
                button.textContent = 'สร้างเสียง';
                return;
            }}
            
            // ตรวจสอบว่า RVC เปิดใช้งานแต่ไม่ได้เลือกโมเดล
            if (enableRVC && !rvcModel.trim()) {{
                showNotification('❌ กรุณาเลือกโมเดล RVC เมื่อเปิดใช้งานการแปลงเสียง', 'error');
                button.disabled = false;
                button.textContent = 'สร้างเสียง';
                return;
            }}
            
            try {{
                let response = await fetch('/generate', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        text: text,
                        tts_voice: ttsVoice,
                        enable_rvc: enableRVC,
                        rvc_model: rvcModel.trim() || null,
                        tts_speed: ttsSpeed,
                        rvc_transpose: rvcTranspose,
                        enable_multi_language: enableMultiLanguage
                    }})
                }});
                
                let result = await response.json();
                
                                    if (result.success) {{
                        // แสดงผลลัพธ์
                        let resultSection = document.getElementById('resultSection');
                        
                        // แสดง section ผลลัพธ์
                        resultSection.style.display = 'block';
                        
                        // แสดงสถิติ
                        let stats = result.stats || {{}};
                        let steps = result.processing_steps || [];
                        
                        // แสดงข้อมูลการตรวจจับภาษา
                        if (stats.detected_languages && stats.detected_languages.length > 0) {{
                            let languageInfo = `🌐 ตรวจพบภาษา: ${{stats.detected_languages.join(', ')}} (จำนวนส่วน: ${{stats.language_segments}})`; 
                            showNotification(languageInfo, 'info');
                            
                            // แสดงรายละเอียดการตรวจจับภาษา
                            showLanguageDetectionResults(stats.language_segments_detail || []);
                        }}
                        
                        // เก็บข้อมูลเสียงสำหรับดาวน์โหลด
                        window.ttsAudioData = result.tts_audio_data;
                        window.rvcAudioData = result.rvc_audio_data;
                        window.finalAudioData = result.final_audio_data;
                        window.currentProcessingSteps = steps;
                        
                        // แสดงไฟล์เสียงตามประเภท - แสดงทั้งต้นฉบับและ RVC เสมอ
                        if (result.tts_audio_data) {{
                            // แสดงเสียงต้นฉบับเสมอ
                            if (result.rvc_audio_data) {{
                                // มีทั้ง TTS และ RVC - แสดงทั้งสองไฟล์
                                showTTSAndRVCAudio(result.tts_audio_data, result.rvc_audio_data, stats);
                                showNotification('✅ สร้างเสียงสำเร็จ (TTS + RVC)', 'success');
                            }} else {{
                                // มีแค่ TTS - แสดงต้นฉบับและแจ้ง RVC ล้มเหลว
                                showTTSAndRVCAudio(result.tts_audio_data, null, stats);
                                let statusText = '✅ สร้างเสียงสำเร็จ (TTS เท่านั้น)';
                                if (steps.includes('rvc_failed')) {{
                                    statusText += ' - RVC ล้มเหลว: ' + (result.rvc_error || 'Unknown error');
                                    showNotification('⚠️ RVC ล้มเหลว แต่ TTS สำเร็จ', 'warning');
                                }} else if (steps.includes('rvc_no_model')) {{
                                    statusText += ' - ไม่ได้เลือกโมเดล RVC';
                                }} else if (steps.includes('rvc_unavailable')) {{
                                    statusText += ' - ระบบ RVC ไม่พร้อมใช้งาน';
                                }} else if (steps.includes('rvc_model_not_found')) {{
                                    statusText += ' - ไม่พบโมเดล RVC ที่เลือก';
                                }}
                                showNotification(statusText, 'success');
                            }}
                        }} else {{
                            showNotification('❌ ไม่สามารถสร้างเสียงได้', 'error');
                        }}
                        
                        // แสดงรายละเอียด
                        console.log('Processing steps:', steps);
                        console.log('Stats:', stats);
                        
                        // แสดงสถิติ
                        if (stats) {{
                            showStats(stats);
                        }}
                        
                    }} else {{
                        let errorMsg = result.error || 'การสร้างเสียงล้มเหลว';
                        if (errorMsg.includes('RVC enabled but no model specified')) {{
                            errorMsg = 'กรุณาเลือกโมเดล RVC เมื่อเปิดใช้งานการแปลงเสียง';
                        }}
                        showNotification('❌ ' + errorMsg, 'error');
                    }}
            }} catch (error) {{
                showNotification('❌ เกิดข้อผิดพลาด: ' + error.message, 'error');
            }} finally {{
                button.disabled = false;
                button.textContent = 'สร้างเสียง';
            }}
        }}
        
        // ฟังก์ชันล้างแคช
        async function clearCache() {{
            try {{
                let response = await fetch('/clear_cache', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{}})
                }});
                
                let result = await response.json();
                
                if (result.success) {{
                    showNotification('✅ ล้างแคชสำเร็จ', 'success');
                }} else {{
                    showNotification('❌ ' + (result.error || 'การล้างแคชล้มเหลว'), 'error');
                }}
            }} catch (error) {{
                showNotification('❌ เกิดข้อผิดพลาด: ' + error.message, 'error');
            }}
        }}
        
        // ฟังก์ชันแสดงการแจ้งเตือน
        function showNotification(message, type = 'info') {{
            let notification = document.createElement('div');
            notification.className = 'notification ' + type;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {{
                notification.remove();
            }}, 5000);
        }}
        
        // ฟังก์ชันแสดงสถานะระบบ
        function showSystemStatus(message, type = 'info') {{
            let systemStatus = document.getElementById('systemStatus');
            if (systemStatus) {{
                systemStatus.innerHTML = '<div class="alert alert-' + type + '">' + message + '</div>';
                setTimeout(() => {{
                    systemStatus.innerHTML = '';
                }}, 5000);
            }}
        }}
        
        // ฟังก์ชันแสดงโมเดล RVC
        async function showModels() {{
            try {{
                let response = await fetch('/models');
                let models = await response.json();
                
                if (models.success) {{
                    // จัดการข้อมูลโมเดล
                    let modelsList = [];
                    if (models.data && Array.isArray(models.data)) {{
                        modelsList = models.data;
                    }} else if (models.data && models.data.models && Array.isArray(models.data.models)) {{
                        modelsList = models.data.models;
                    }}
                    
                    if (modelsList.length > 0) {{
                        let modelList = modelsList.map(model => model.name).join(', ');
                        showNotification('📋 โมเดล RVC ที่พร้อมใช้งาน: ' + modelList, 'info');
                    }} else {{
                        showNotification('⚠️ ไม่มีโมเดล RVC พร้อมใช้งาน', 'warning');
                    }}
                }} else {{
                    showNotification('❌ ไม่สามารถโหลดรายชื่อโมเดลได้: ' + (models.error || 'Unknown error'), 'error');
                }}
            }} catch (error) {{
                showNotification('❌ เกิดข้อผิดพลาดในการโหลดโมเดล: ' + error.message, 'error');
            }}
        }}
        
        // ฟังก์ชันตรวจสอบสถานะ
        async function checkStatus() {{
            try {{
                let response = await fetch('/status');
                let status = await response.json();
                
                if (status.success) {{
                    let data = status.data;
                    showNotification('🔍 สถานะระบบ: TTS ' + (data.tts_available ? '✅' : '❌') + ', RVC ' + (data.rvc_available ? '✅' : '❌') + ' (' + data.rvc_models_count + ' models), Device: ' + data.device, 'info');
                }} else {{
                    showNotification('❌ ไม่สามารถตรวจสอบสถานะได้', 'error');
                }}
            }} catch (error) {{
                showNotification('❌ เกิดข้อผิดพลาดในการตรวจสอบสถานะ: ' + error.message, 'error');
            }}
        }}
        
        // ฟังก์ชันรีเซ็ตการตั้งค่า
        function resetSettings() {{
            if (confirm('คุณต้องการรีเซ็ตการตั้งค่าทั้งหมดหรือไม่?')) {{
                localStorage.removeItem('victor-tts-settings');
                location.reload();
            }}
        }}
        
        // ฟังก์ชันแสดงคู่มือ
        function showHelp() {{
            let helpText = `🎙️ คู่มือการใช้งาน VICTOR-TTS

1. 📝 พิมพ์ข้อความที่ต้องการแปลงเป็นเสียง
2. 🎵 เลือกเสียง TTS และปรับความเร็ว
3. 🎭 เปิดใช้งาน RVC และเลือกโมเดล (ถ้าต้องการ)
4. 🚀 กดปุ่ม "สร้างเสียง" เพื่อเริ่มการประมวลผล
5. 🎧 ฟังผลลัพธ์และดาวน์โหลดไฟล์เสียง

💡 เคล็ดลับ:
- ใช้ RVC เพื่อแปลงเสียงให้เหมือนกับเสียงต้นแบบ
- ปรับ Pitch เพื่อเปลี่ยนระดับเสียง
- ระบบรองรับข้อความยาวได้อัตโนมัติ`;
            
            alert(helpText);
        }}
        
        // โหลดข้อมูลเมื่อหน้าเว็บโหลดเสร็จ
        window.addEventListener('load', async function() {{
            // โหลดสถานะระบบ
            try {{
                let response = await fetch('/status');
                let status = await response.json();
                
                if (status.success) {{
                    let data = status.data;
                    document.getElementById('systemStatus').innerHTML = `
                        <div class="status-item">
                            <span class="status-label">TTS:</span>
                            <span class="status-value ${{data.tts_available ? 'success' : 'error'}}">
                                ${{data.tts_available ? '✅' : '❌'}}
                            </span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">RVC:</span>
                            <span class="status-value ${{data.rvc_available ? 'success' : 'error'}}">
                                ${{data.rvc_available ? '✅' : '❌'}} (${{data.rvc_models_count}} models)
                            </span>
                        </div>
                        <div class="status-item">
                            <span class="status-label">Device:</span>
                            <span class="status-value">${{data.device}}</span>
                        </div>
                    `;
                }}
            }} catch (error) {{
                console.error('Error loading status:', error);
            }}
            
            // โหลดรายชื่อโมเดล RVC
            try {{
                let response = await fetch('/models');
                let models = await response.json();
                
                if (models.success) {{
                    let rvcSelect = document.getElementById('modelSelect');
                    let enableRVC = document.getElementById('enableRVC');
                    
                    rvcSelect.innerHTML = '<option value="">เลือกโมเดล RVC</option>';
                    
                    // จัดการข้อมูลโมเดล
                    let modelsList = [];
                    if (models.data && Array.isArray(models.data)) {{
                        modelsList = models.data;
                    }} else if (models.data && models.data.models && Array.isArray(models.data.models)) {{
                        modelsList = models.data.models;
                    }}
                    
                    modelsList.forEach(model => {{
                        let option = document.createElement('option');
                        option.value = model.name;
                        option.textContent = model.name;
                        rvcSelect.appendChild(option);
                    }});
                    
                    if (modelsList.length === 0) {{
                        let option = document.createElement('option');
                        option.value = "";
                        option.textContent = "ไม่มีโมเดล RVC";
                        option.disabled = true;
                        rvcSelect.appendChild(option);
                        
                        // ปิดการใช้งาน RVC checkbox เมื่อไม่มีโมเดล
                        enableRVC.checked = false;
                        enableRVC.disabled = true;
                        document.getElementById('modelSelect').disabled = true;
                        document.getElementById('transposeSlider').disabled = true;
                        
                        // แสดงสถานะ
                        document.getElementById('rvcStatus').innerHTML = '⚠️ ไม่มีโมเดล RVC พร้อมใช้งาน';
                        document.getElementById('rvcStatus').style.color = '#dc3545';
                    }} else {{
                        // เปิดการใช้งาน RVC checkbox เมื่อมีโมเดล
                        enableRVC.disabled = false;
                        
                        // แสดงสถานะ
                        document.getElementById('rvcStatus').innerHTML = '✅ พบ ' + modelsList.length + ' โมเดล RVC พร้อมใช้งาน';
                        document.getElementById('rvcStatus').style.color = '#28a745';
                    }}
                }} else {{
                    console.error('Failed to load models:', models.error);
                    document.getElementById('rvcStatus').innerHTML = '❌ ไม่สามารถโหลดโมเดลได้: ' + (models.error || 'Unknown error');
                    document.getElementById('rvcStatus').style.color = '#dc3545';
                }}
            }} catch (error) {{
                console.error('Error loading models:', error);
                document.getElementById('rvcStatus').innerHTML = '❌ เกิดข้อผิดพลาดในการโหลดโมเดล';
                document.getElementById('rvcStatus').style.color = '#dc3545';
            }}
        }});
        
        // Auto-save settings to localStorage
        function saveSettings() {{
            let settings = {{
                voice: document.getElementById('voiceSelect').value,
                speed: document.getElementById('speedSlider').value,
                enableRVC: document.getElementById('enableRVC').checked,
                model: document.getElementById('modelSelect').value,
                transpose: document.getElementById('transposeSlider').value
            }};
            localStorage.setItem('victor-tts-settings', JSON.stringify(settings));
        }}
        
        // Load saved settings
        function loadSettings() {{
            try {{
                let settings = JSON.parse(localStorage.getItem('victor-tts-settings') || '{{}}');
                if (settings.voice) document.getElementById('voiceSelect').value = settings.voice;
                if (settings.speed) {{
                    document.getElementById('speedSlider').value = settings.speed;
                    document.getElementById('speedValue').textContent = settings.speed + 'x';
                }}
                if (settings.enableRVC !== undefined) {{
                    document.getElementById('enableRVC').checked = settings.enableRVC;
                    document.getElementById('modelSelect').disabled = !settings.enableRVC;
                    document.getElementById('transposeSlider').disabled = !settings.enableRVC;
                }}
                if (settings.model) document.getElementById('modelSelect').value = settings.model;
                if (settings.transpose) {{
                    document.getElementById('transposeSlider').value = settings.transpose;
                    document.getElementById('transposeValue').textContent = settings.transpose;
                }}
            }} catch (error) {{
                console.log('Could not load saved settings');
            }}
        }}
        
        // Save settings when changed
        ['voiceSelect', 'speedSlider', 'enableRVC', 'modelSelect', 'transposeSlider'].forEach(id => {{
            let element = document.getElementById(id);
            element.addEventListener('change', saveSettings);
        }});
        
        // Event listeners for control buttons
        document.addEventListener('DOMContentLoaded', function() {{
            // Test System Button
            let testSystemBtn = document.getElementById('testSystemBtn');
            if (testSystemBtn) {{
                testSystemBtn.addEventListener('click', testSystem);
            }}
            
            // Check Status Button
            let checkStatusBtn = document.getElementById('checkStatusBtn');
            if (checkStatusBtn) {{
                checkStatusBtn.addEventListener('click', checkStatus);
            }}
            
            // Show Models Button
            let showModelsBtn = document.getElementById('showModelsBtn');
            if (showModelsBtn) {{
                showModelsBtn.addEventListener('click', showModels);
            }}
            
            // Clear Cache Button
            let clearCacheBtn = document.getElementById('clearCacheBtn');
            if (clearCacheBtn) {{
                clearCacheBtn.addEventListener('click', clearCache);
            }}
            
            // Reset Settings Button
            let resetSettingsBtn = document.getElementById('resetSettingsBtn');
            if (resetSettingsBtn) {{
                resetSettingsBtn.addEventListener('click', resetSettings);
            }}
            
            // Show Help Button
            let showHelpBtn = document.getElementById('showHelpBtn');
            if (showHelpBtn) {{
                showHelpBtn.addEventListener('click', showHelp);
            }}
            
            // Load settings
            loadSettings();
            
            // Load device info
            loadDeviceInfo();
            
            // Show welcome message
            setTimeout(() => {{
                showNotification('ยินดีต้อนรับสู่ระบบ VICTOR-TTS Interface! พร้อมใช้งานแล้ว 🎉', 'success');
            }}, 500);
        }});
        
        // ฟังก์ชันแสดงสถานะระบบ
        function showSystemStatus(message, type = 'info') {{
            let statusDiv = document.getElementById('systemStatus');
            if (statusDiv) {{
                let alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-' + type;
                alertDiv.textContent = message;
                alertDiv.style.marginBottom = '10px';
                
                statusDiv.appendChild(alertDiv);
                
                // Auto-remove after 8 seconds
                setTimeout(() => {{
                    if (alertDiv.parentNode) {{
                        alertDiv.remove();
                    }}
                }}, 8000);
            }}
        }}
        
        // Reset settings
        function resetSettings() {{
            if (confirm('คุณต้องการรีเซ็ตการตั้งค่าทั้งหมดหรือไม่?')) {{
                localStorage.removeItem('victor-tts-settings');
                
                // Reset form values
                document.getElementById('voiceSelect').value = 'th-TH-PremwadeeNeural';
                document.getElementById('speedSlider').value = '0.8';
                document.getElementById('speedValue').textContent = '0.8x';
                document.getElementById('enableRVC').checked = false;
                document.getElementById('modelSelect').disabled = true;
                document.getElementById('transposeSlider').disabled = true;
                document.getElementById('transposeSlider').value = '0';
                document.getElementById('transposeValue').textContent = '0';
                
                showSystemStatus('✅ รีเซ็ตการตั้งค่าเสร็จสิ้น!', 'success');
            }}
        }}
        
        // Show help
        function showHelp() {{
            let helpContent = 
                '<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 15px 0;">' +
                    '<h3>📖 คู่มือการใช้งาน VICTOR-TTS</h3>' +
                    '<hr>' +
                    '<h4>🚀 การเริ่มต้นใช้งาน:</h4>' +
                    '<ul>' +
                        '<li>ใส่ข้อความที่ต้องการแปลงเป็นเสียง</li>' +
                        '<li>เลือกเสียง TTS และปรับความเร็ว</li>' +
                        '<li>เปิด RVC ถ้าต้องการแปลงเสียง</li>' +
                        '<li>กดปุ่ม "สร้างเสียง"</li>' +
                    '</ul>' +
                    
                    '<h4>⚙️ ปุ่มควบคุมระบบ:</h4>' +
                    '<ul>' +
                        '<li><strong>🧪 ทดสอบระบบ</strong>: ทดสอบ TTS และ RVC</li>' +
                        '<li><strong>🔍 ตรวจสอบสถานะ</strong>: ดูสถานะระบบ</li>' +
                        '<li><strong>📋 แสดงโมเดล</strong>: ดูโมเดล RVC ที่มี</li>' +
                        '<li><strong>🧹 ล้างแคช</strong>: ลบไฟล์ชั่วคราว</li>' +
                        '<li><strong>🔄 รีเซ็ตการตั้งค่า</strong>: กลับไปตั้งค่าเริ่มต้น</li>' +
                    '</ul>' +
                    
                    '<h4>🎯 เคล็ดลับ:</h4>' +
                    '<ul>' +
                        '<li>ใช้ความเร็ว 0.8x สำหรับการพูดที่ชัดเจน</li>' +
                        '<li>ข้อความไม่เกิน 500 ตัวอักษรต่อครั้ง</li>' +
                        '<li>ทดสอบระบบก่อนใช้งานจริง</li>' +
                        '<li>ใช้ Ctrl+Enter เพื่อสร้างเสียงเร็ว</li>' +
                    '</ul>' +
                    
                    '<p style="margin-top: 15px; font-weight: bold; color: #007bff;">' +
                        '📄 คู่มือเต็ม: <a href="WEB_APP_GUIDE.md" target="_blank">WEB_APP_GUIDE.md</a>' +
                    '</p>' +
                '</div>';
            
            showSystemStatus(helpContent, 'info');
        }}
        
        // Event listeners for control buttons
        document.addEventListener('DOMContentLoaded', function() {{
            // Test System Button
            document.getElementById('testSystemBtn').addEventListener('click', testSystem);
            
            // Check Status Button
            document.getElementById('checkStatusBtn').addEventListener('click', checkStatus);
            
            // Show Models Button
            document.getElementById('showModelsBtn').addEventListener('click', showModels);
            
            // Clear Cache Button
            document.getElementById('clearCacheBtn').addEventListener('click', clearCache);
            
            // Reset Settings Button
            document.getElementById('resetSettingsBtn').addEventListener('click', resetSettings);
            
            // Show Help Button
            document.getElementById('showHelpBtn').addEventListener('click', showHelp);
        }});
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey && e.key === 'Enter') {{
                generateAudio();
            }}
        }});
    </script>
</body>
</html>
        """
        
        return html_content
    
    def _generate_model_list_html(self, models):
        """สร้าง HTML สำหรับแสดงรายการโมเดล"""
        if not models:
            return '<p style="color: #6c757d; text-align: center; padding: 20px;">ไม่มีโมเดลที่อัปโหลด</p>'
        
        html = """
        <table class="model-table">
            <thead>
                <tr>
                    <th>ลำดับ</th>
                    <th>ชื่อโมเดล</th>
                    <th>ประเภท</th>
                    <th>สถานะ</th>
                    <th>การจัดการ</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for i, model in enumerate(models, 1):
            html += f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{model}</strong></td>
                    <td>RVC Model</td>
                    <td><span style="color: #28a745;">✅ พร้อมใช้งาน</span></td>
                    <td>
                        <button class="btn-small btn-success" onclick="testModel('{model}')" style="margin-right: 5px;">🧪 ทดสอบ</button>
                        <button class="btn-small btn-danger" onclick="deleteModel('{model}')">🗑️ ลบ</button>
                    </td>
                </tr>
            """
        
        html += """
            </tbody>
        </table>
        """
        return html
    
    def create_simple_server(self):
        """สร้าง HTTP server แบบง่าย"""
        import http.server
        import socketserver
        import json
        import urllib.parse
        
        class WebRequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    html_content = self.server.web_interface.generate_html_page()
                    self.wfile.write(html_content.encode('utf-8'))
                
                elif self.path == '/status':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    if self.server.web_interface.core:
                        try:
                            status = self.server.web_interface.core.get_system_status()
                            response = {"success": True, "data": status}
                        except Exception as e:
                            response = {"success": False, "error": str(e)}
                    else:
                        response = {"success": False, "error": "Core not available"}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                
                elif self.path == '/models':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    try:
                        from pathlib import Path
                        import os
                        from datetime import datetime
                        
                        # ดึงโมเดลจาก core system
                        core_models = []
                        if self.server.web_interface.core:
                            try:
                                core_models = self.server.web_interface.core.get_available_rvc_models()
                            except:
                                pass
                        
                        # ดึงโมเดลจากโฟลเดอร์ voice_models
                        models_dir = Path("voice_models")
                        uploaded_models = []
                        
                        if models_dir.exists():
                            for model_file in models_dir.glob("*.pth"):
                                stat = model_file.stat()
                                uploaded_models.append({
                                    "name": model_file.name,
                                    "size": f"{stat.st_size / (1024*1024):.1f} MB",
                                    "updated": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                                    "type": "uploaded"
                                })
                            
                            for model_file in models_dir.glob("*.pt"):
                                stat = model_file.stat()
                                uploaded_models.append({
                                    "name": model_file.name,
                                    "size": f"{stat.st_size / (1024*1024):.1f} MB",
                                    "updated": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                                    "type": "uploaded"
                                })
                            
                            for model_file in models_dir.glob("*.ckpt"):
                                stat = model_file.stat()
                                uploaded_models.append({
                                    "name": model_file.name,
                                    "size": f"{stat.st_size / (1024*1024):.1f} MB",
                                    "updated": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                                    "type": "uploaded"
                                })
                        
                        # รวมโมเดลทั้งหมด
                        all_models = []
                        
                        # เพิ่มโมเดลจาก core system
                        for model in core_models:
                            all_models.append({
                                "name": model,
                                "size": "ไม่ทราบ",
                                "updated": "ไม่ทราบ",
                                "type": "core"
                            })
                        
                        # เพิ่มโมเดลที่อัปโหลด
                        all_models.extend(uploaded_models)
                        
                        response = {"success": True, "data": all_models}
                        
                    except Exception as e:
                        response = {"success": False, "error": str(e)}
                    
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                
                elif self.path == '/device_info':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    try:
                        if self.server.web_interface.core:
                            device_info = self.server.web_interface.core.get_device_info()
                            response = {"success": True, "data": device_info}
                        else:
                            response = {"success": False, "error": "Core system not available"}
                    except Exception as e:
                        response = {"success": False, "error": str(e)}
                    
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not Found')
            
            def do_POST(self):
                if self.path == '/generate':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        request_data = json.loads(post_data.decode('utf-8'))
                        
                        # ประมวลผลคำขอ
                        if self.server.web_interface.core:
                            result = asyncio.run(self._process_request(request_data))
                        else:
                            result = {"success": False, "error": "Core system not available"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
                elif self.path == '/test':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        request_data = json.loads(post_data.decode('utf-8'))
                        
                        if self.server.web_interface.core:
                            # ทดสอบระบบ
                            test_result = asyncio.run(self._test_system())
                            result = {"success": True, "message": test_result}
                        else:
                            result = {"success": False, "error": "Core system not available"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
                elif self.path == '/clear_cache':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        request_data = json.loads(post_data.decode('utf-8'))
                        
                        if self.server.web_interface.core:
                            # ล้างแคช
                            files_removed = self._clear_cache()
                            result = {"success": True, "data": {"files_removed": files_removed}}
                        else:
                            result = {"success": False, "error": "Core system not available"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
                elif self.path == '/device_info':
                    try:
                        if self.server.web_interface.core:
                            device_info = self.server.web_interface.core.get_device_info()
                            result = {"success": True, "data": device_info}
                        else:
                            result = {"success": False, "error": "Core system not available"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
                
                elif self.path == '/change_device':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        request_data = json.loads(post_data.decode('utf-8'))
                        
                        if self.server.web_interface.core:
                            device_choice = request_data.get('device', 'cpu')
                            result = self.server.web_interface.core.change_device_auto(device_choice)
                        else:
                            result = {"success": False, "error": "Core system not available"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
                
                elif self.path == '/upload_model':
                    try:
                        import cgi
                        import tempfile
                        import shutil
                        from pathlib import Path
                        
                        # รับไฟล์ที่อัปโหลด
                        form = cgi.FieldStorage(
                            fp=self.rfile,
                            headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'}
                        )
                        
                        if 'model' not in form:
                            result = {"success": False, "error": "ไม่พบไฟล์โมเดล"}
                        else:
                            fileitem = form['model']
                            if fileitem.filename:
                                # ตรวจสอบนามสกุลไฟล์
                                allowed_extensions = ['.pth', '.pt', '.ckpt']
                                file_ext = Path(fileitem.filename).suffix.lower()
                                if file_ext not in allowed_extensions:
                                    result = {"success": False, "error": f"ไฟล์ไม่ถูกต้อง รองรับเฉพาะ {', '.join(allowed_extensions)}"}
                                else:
                                    # สร้างโฟลเดอร์สำหรับโมเดล
                                    models_dir = Path("voice_models")
                                    models_dir.mkdir(exist_ok=True)
                                    
                                    # บันทึกไฟล์
                                    model_path = models_dir / fileitem.filename
                                    with open(model_path, 'wb') as f:
                                        shutil.copyfileobj(fileitem.file, f)
                                    
                                    result = {"success": True, "message": f"อัปโหลดโมเดลสำเร็จ: {fileitem.filename}"}
                            else:
                                result = {"success": False, "error": "ไฟล์ว่างเปล่า"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
                elif self.path == '/delete_model':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        request_data = json.loads(post_data.decode('utf-8'))
                        
                        model_name = request_data.get('model')
                        if not model_name:
                            result = {"success": False, "error": "ไม่ระบุชื่อโมเดล"}
                        else:
                            # ลบไฟล์โมเดล
                            models_dir = Path("voice_models")
                            model_path = models_dir / model_name
                            
                            if model_path.exists():
                                model_path.unlink()
                                result = {"success": True, "message": f"ลบโมเดลสำเร็จ: {model_name}"}
                            else:
                                result = {"success": False, "error": f"ไม่พบโมเดล: {model_name}"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
                elif self.path == '/test_model':
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        request_data = json.loads(post_data.decode('utf-8'))
                        
                        model_name = request_data.get('model')
                        if not model_name:
                            result = {"success": False, "error": "ไม่ระบุชื่อโมเดล"}
                        else:
                            # ทดสอบโมเดล
                            models_dir = Path("voice_models")
                            model_path = models_dir / model_name
                            
                            if model_path.exists():
                                # ตรวจสอบว่าไฟล์ไม่เสียหาย
                                if model_path.stat().st_size > 0:
                                    result = {"success": True, "message": f"โมเดล {model_name} พร้อมใช้งาน"}
                                else:
                                    result = {"success": False, "error": f"ไฟล์โมเดลเสียหาย: {model_name}"}
                            else:
                                result = {"success": False, "error": f"ไม่พบโมเดล: {model_name}"}
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"success": False, "error": str(e)}
                        self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not Found')
            
            async def _process_request(self, request_data):
                """ประมวลผลคำขอ TTS/RVC"""
                try:
                    core = self.server.web_interface.core
                    
                    # ใช้ฟังก์ชัน process_unified เพื่อประมวลผลรวม
                    result = await core.process_unified(
                        text=request_data.get('text', ''),
                        tts_voice=request_data.get('tts_voice', 'th-TH-PremwadeeNeural'),
                        enable_rvc=request_data.get('enable_rvc', False),
                        rvc_model=request_data.get('rvc_model'),
                        tts_speed=request_data.get('tts_speed', 1.0),
                        tts_pitch="+0Hz",
                        rvc_transpose=request_data.get('rvc_transpose', 0),
                        rvc_index_ratio=0.75,
                        rvc_f0_method="rmvpe",
                        enable_multi_language=request_data.get('enable_multi_language', True)
                    )
                    
                    if result["success"]:
                        # แปลงข้อมูลเสียงเป็น base64
                        response_data = {
                            "success": True,
                            "tts_audio_data": base64.b64encode(result["tts_audio_data"]).decode('utf-8') if result["tts_audio_data"] else None,
                            "rvc_audio_data": base64.b64encode(result["rvc_audio_data"]).decode('utf-8') if result["rvc_audio_data"] else None,
                            "final_audio_data": base64.b64encode(result["final_audio_data"]).decode('utf-8') if result["final_audio_data"] else None,
                            "stats": result["stats"],
                            "processing_steps": result["processing_steps"]
                        }
                        
                        # เพิ่มข้อมูล error ถ้ามี
                        if result.get("error"):
                            response_data["rvc_error"] = result["error"]
                        
                        return response_data
                    else:
                        return {"success": False, "error": result.get("error", "Unknown error")}
                        
                except Exception as e:
                    return {"success": False, "error": str(e)}
            
            async def _test_system(self):
                """ทดสอบระบบ"""
                try:
                    core = self.server.web_interface.core
                    
                    # ทดสอบ TTS
                    test_text = "สวัสดีครับ นี่คือการทดสอบระบบ"
                    tts_result = await core.generate_tts(test_text, "th-TH-PremwadeeNeural", 1.0)
                    
                    # ทดสอบ RVC
                    rvc_models = core.get_available_rvc_models()
                    
                    return f"TTS: ✅ ({len(tts_result)} bytes), RVC Models: {len(rvc_models)} ตัว"
                    
                except Exception as e:
                    return f"การทดสอบล้มเหลว: {str(e)}"
            
            def _clear_cache(self):
                """ล้างแคช"""
                try:
                    import os
                    import glob
                    
                    # ลบไฟล์ชั่วคราว
                    temp_dir = Path("storage/temp")
                    if temp_dir.exists():
                        temp_files = list(temp_dir.glob("*"))
                        for file in temp_files:
                            try:
                                if file.is_file():
                                    file.unlink()
                            except:
                                pass
                        return len(temp_files)
                    return 0
                    
                except Exception as e:
                    return 0
        
        class WebServer(socketserver.TCPServer):
            def __init__(self, server_address, handler_class, web_interface):
                self.web_interface = web_interface
                super().__init__(server_address, handler_class)
                self.allow_reuse_address = True
        
        return WebServer(('localhost', self.port), WebRequestHandler, self)
    
    def start(self, open_browser: bool = True):
        """เริ่มต้น Web Interface"""
        try:
            print(f"🚀 Starting VICTOR-TTS Web Interface on port {self.port}...")
            
            server = self.create_simple_server()
            self.is_running = True
            
            if open_browser:
                import threading
                def open_browser_delayed():
                    import time
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{self.port}')
                
                threading.Thread(target=open_browser_delayed, daemon=True).start()
            
            print(f"✅ Web Interface started successfully!")
            print(f"🌐 Open: http://localhost:{self.port}")
            print(f"💡 System Status:")
            if self.core:
                status = self.core.get_system_status()
                print(f"   TTS: {'✅' if status['tts_available'] else '❌'}")
                print(f"   RVC: {'✅' if status['rvc_available'] else '❌'}")
                print(f"   Models: {status['rvc_models_count']}")
            else:
                print("   ❌ Core system not available")
            
            print("\\nPress Ctrl+C to stop the server...")
            
            server.serve_forever()
            
        except KeyboardInterrupt:
            print("\\n👋 Shutting down Web Interface...")
            self.is_running = False
        except Exception as e:
            print(f"❌ Error starting Web Interface: {e}")

def main():
    """เรียกใช้ Web Interface"""
    print("🌐 VICTOR-TTS Web Interface")
    print("=" * 40)
    
    # สร้าง Web Interface
    web_interface = WebInterface(port=7000)
    
    # เริ่มต้น server
    web_interface.start(open_browser=True)

if __name__ == "__main__":
    main()
