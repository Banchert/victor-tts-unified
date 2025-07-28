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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .status-bar {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
        }}
        
        .status-item {{
            text-align: center;
        }}
        
        .status-icon {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .status-text {{
            font-weight: bold;
            color: #333;
        }}
        
        .section {{
            margin-bottom: 30px;
            padding: 25px;
            border: 2px solid #e9ecef;
            border-radius: 15px;
            background: #fafbfc;
        }}
        
        .section h3 {{
            color: #495057;
            margin-bottom: 20px;
            font-size: 1.3em;
            border-bottom: 2px solid #dee2e6;
            padding-bottom: 10px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #495057;
        }}
        
        textarea {{
            width: 100%;
            padding: 15px;
            border: 2px solid #dee2e6;
            border-radius: 10px;
            font-size: 16px;
            resize: vertical;
            min-height: 120px;
            font-family: inherit;
        }}
        
        textarea:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        select, input[type="range"] {{
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 16px;
        }}
        
        select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .slider-container {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .slider {{
            flex: 1;
        }}
        
        .slider-value {{
            min-width: 80px;
            text-align: center;
            font-weight: bold;
            color: #667eea;
        }}
        
        .checkbox-container {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .checkbox-container input[type="checkbox"] {{
            width: 20px;
            height: 20px;
        }}
        
        .button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .button:disabled {{
            background: #6c757d;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }}
        
        .result-section {{
            background: #e7f3ff;
            border-color: #b8daff;
        }}
        
        .alert {{
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            font-weight: 500;
        }}
        
        .alert-success {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        
        .alert-error {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        
        .alert-info {{
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #e9ecef;
            border-radius: 5px;
            overflow: hidden;
            margin: 15px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 5px;
            transition: width 0.3s ease;
            width: 0%;
        }}
        
        .audio-player {{
            width: 100%;
            margin: 20px 0;
            border-radius: 10px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .stat-item {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 15px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .status-bar {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            max-width: 400px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease;
        }}
        
        .notification.success {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }}
        
        .notification.error {{
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        }}
        
        .notification.warning {{
            background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
            color: #212529;
        }}
        
        .notification.info {{
            background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        }}
        
        .alert {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            font-weight: 500;
        }}
        
        .alert-success {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
        }}
        
        .alert-error {{
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
        }}
        
        .alert-info {{
            background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
            color: white;
        }}
        
        .alert-warning {{
            background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
            color: #212529;
        }}
        
        .audio-player {{
            width: 100%;
            margin: 15px 0;
            border-radius: 10px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }}
        
        .result-section {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 2px solid #28a745;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .stat-item {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #28a745;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        .download-btn {{
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            margin: 10px 5px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        
        .download-btn:hover {{
            background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}
        
        .download-btn:active {{
            transform: translateY(0);
        }}
        
        #ttsAudioSection, #rvcAudioSection, #combinedAudioSection {{
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        #ttsAudioSection h4, #rvcAudioSection h4, #combinedAudioSection h4 {{
            margin: 0 0 10px 0;
            color: #333;
            font-size: 16px;
        }}
        
        @keyframes slideIn {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎙️ VICTOR-TTS Interface</h1>
            <p>ระบบแปลงข้อความเป็นเสียงพร้อมการแปลงเสียง</p>
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
                
                <!-- TTS Audio Player -->
                <div id="ttsAudioSection" style="display: none;">
                    <h4>🎵 เสียง TTS (ต้นฉบับ)</h4>
                    <audio id="ttsAudioPlayer" class="audio-player" controls></audio>
                    <button id="downloadTTSBtn" class="download-btn" onclick="downloadAudio('tts')">📥 ดาวน์โหลด TTS</button>
                </div>
                
                <!-- RVC Audio Player -->
                <div id="rvcAudioSection" style="display: none;">
                    <h4>🎭 เสียง RVC (แปลงแล้ว)</h4>
                    <audio id="rvcAudioPlayer" class="audio-player" controls></audio>
                    <button id="downloadRVCBtn" class="download-btn" onclick="downloadAudio('rvc')">📥 ดาวน์โหลด RVC</button>
                </div>
                
                <!-- Combined Audio Player (for backward compatibility) -->
                <div id="combinedAudioSection" style="display: none;">
                    <h4>🎧 เสียงรวม</h4>
                    <audio id="audioPlayer" class="audio-player" controls></audio>
                    <button id="downloadCombinedBtn" class="download-btn" onclick="downloadAudio('combined')">📥 ดาวน์โหลด</button>
                </div>
                
                <div class="stats" id="statsContainer"></div>
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
            
            // แสดงส่วน TTS
            let ttsSection = document.getElementById('ttsAudioSection');
            let ttsPlayer = document.getElementById('ttsAudioPlayer');
            ttsSection.style.display = 'block';
            ttsPlayer.src = 'data:audio/wav;base64,' + ttsAudioData;
            
            // แสดงส่วน RVC
            let rvcSection = document.getElementById('rvcAudioSection');
            let rvcPlayer = document.getElementById('rvcAudioPlayer');
            rvcSection.style.display = 'block';
            rvcPlayer.src = 'data:audio/wav;base64,' + rvcAudioData;
            
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
                        rvc_transpose: rvcTranspose
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
                        
                        // เก็บข้อมูลเสียงสำหรับดาวน์โหลด
                        window.ttsAudioData = result.tts_audio_data;
                        window.rvcAudioData = result.rvc_audio_data;
                        window.finalAudioData = result.final_audio_data;
                        window.currentProcessingSteps = steps;
                        
                        // แสดงไฟล์เสียงตามประเภท
                        if (result.rvc_audio_data) {{
                            // มีทั้ง TTS และ RVC - แสดงทั้งสองไฟล์
                            showTTSAndRVCAudio(result.tts_audio_data, result.rvc_audio_data, stats);
                            showNotification('✅ สร้างเสียงสำเร็จ (TTS + RVC)', 'success');
                        }} else {{
                            // มีแค่ TTS - แสดงไฟล์เดียว
                            showCombinedAudio(result.tts_audio_data, stats);
                            let statusText = '✅ สร้างเสียงสำเร็จ (TTS เท่านั้น)';
                            if (steps.includes('rvc_failed')) {{
                                statusText += ' - RVC ล้มเหลว';
                            }} else if (steps.includes('rvc_no_model')) {{
                                statusText += ' - ไม่ได้เลือกโมเดล RVC';
                            }}
                            showNotification(statusText, 'success');
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
                    if self.server.web_interface.core:
                        try:
                            models = self.server.web_interface.core.get_available_rvc_models()
                            models_data = [{"name": model} for model in models]
                            response = {"success": True, "data": models_data}
                        except Exception as e:
                            response = {"success": False, "error": str(e)}
                    else:
                        response = {"success": False, "error": "Core not available"}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                
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
                
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not Found')
            
            async def _process_request(self, request_data):
                """ประมวลผลคำขอ TTS/RVC"""
                try:
                    core = self.server.web_interface.core
                    
                    # สร้าง TTS ก่อน
                    tts_audio = await core.generate_tts(
                        text=request_data.get('text', ''),
                        voice=request_data.get('tts_voice', 'th-TH-PremwadeeNeural'),
                        speed=request_data.get('tts_speed', 1.0),
                        pitch="+0Hz"
                    )
                    
                    # แปลง TTS เป็น base64
                    tts_base64 = base64.b64encode(tts_audio).decode('utf-8')
                    
                    # ตรวจสอบว่าต้องการ RVC หรือไม่
                    enable_rvc = request_data.get('enable_rvc', False)
                    rvc_model = request_data.get('rvc_model')
                    
                    if enable_rvc and rvc_model:
                        # แปลงเสียงด้วย RVC
                        try:
                            rvc_audio = core.convert_voice(
                                audio_data=tts_audio,
                                model_name=rvc_model,
                                transpose=request_data.get('rvc_transpose', 0),
                                index_ratio=0.75,
                                f0_method="rmvpe"
                            )
                            rvc_base64 = base64.b64encode(rvc_audio).decode('utf-8')
                            
                            return {
                                "success": True,
                                "tts_audio_data": tts_base64,
                                "rvc_audio_data": rvc_base64,
                                "final_audio_data": rvc_base64,  # ใช้ RVC เป็นไฟล์สุดท้าย
                                "stats": {
                                    "text_length": len(request_data.get('text', '')),
                                    "tts_audio_size": len(tts_audio),
                                    "rvc_audio_size": len(rvc_audio),
                                    "final_audio_size": len(rvc_audio),
                                    "voice_conversion_applied": True,
                                    "device": core.device
                                },
                                "processing_steps": ["tts_generation", "voice_conversion"]
                            }
                        except Exception as rvc_error:
                            # RVC ล้มเหลว ใช้ TTS เท่านั้น
                            return {
                                "success": True,
                                "tts_audio_data": tts_base64,
                                "rvc_audio_data": None,
                                "final_audio_data": tts_base64,
                                "stats": {
                                    "text_length": len(request_data.get('text', '')),
                                    "tts_audio_size": len(tts_audio),
                                    "rvc_audio_size": 0,
                                    "final_audio_size": len(tts_audio),
                                    "voice_conversion_applied": False,
                                    "device": core.device
                                },
                                "processing_steps": ["tts_generation", "rvc_failed"],
                                "rvc_error": str(rvc_error)
                            }
                    else:
                        # ใช้ TTS เท่านั้น
                        return {
                            "success": True,
                            "tts_audio_data": tts_base64,
                            "rvc_audio_data": None,
                            "final_audio_data": tts_base64,
                            "stats": {
                                "text_length": len(request_data.get('text', '')),
                                "tts_audio_size": len(tts_audio),
                                "rvc_audio_size": 0,
                                "final_audio_size": len(tts_audio),
                                "voice_conversion_applied": False,
                                "device": core.device
                            },
                            "processing_steps": ["tts_generation"]
                        }
                        
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
