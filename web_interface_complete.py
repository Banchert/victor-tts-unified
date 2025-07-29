#!/usr/bin/env python3
"""
🌐 VICTOR-TTS COMPLETE Web Interface - เวอร์ชันครบถ้วน
รวมทุกฟีเจอร์และเครื่องมือจากเวอร์ชันเดิม พร้อมปรับปรุง UI
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

class CompleteWebInterface:
    """Web Interface ครบถ้วนสำหรับ TTS-RVC System"""
    
    def __init__(self, port: int = 7000):
        self.port = self._find_available_port(port)
        self.core = None
        self.is_running = False
        
        if CORE_AVAILABLE:
            try:
                self.core = create_core_instance()
                print("✅ TTS-RVC Core loaded in Complete Web Interface")
            except Exception as e:
                print(f"⚠️ Failed to load TTS-RVC Core: {e}")
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
        """สร้างหน้าเว็บหลักแบบครบถ้วน"""
        
        # ดึงข้อมูลระบบ
        if self.core:
            status = self.core.get_system_status()
            voices = get_supported_voices()
            models = self.core.get_available_rvc_models()
        else:
            status = {"tts_available": False, "rvc_available": False}
            voices = {}
            models = []
        
        # Debug logging
        print(f"🔍 Debug - Voices loaded: {len(voices)}")
        print(f"🔍 Debug - Models loaded: {len(models)}")
        
        # HTML template แบบครบถ้วน
        html = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VICTOR-TTS FULL UNLIMITED</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');

        body {{
            font-family: 'Sarabun', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(45deg, #4A90E2, #357ABD);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        header p {{
            margin: 10px 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}

        main {{
            padding: 30px;
        }}

        .card {{
            background: #fff;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}

        h2 {{
            margin-top: 0;
            color: #4A90E2;
            border-bottom: 3px solid #4A90E2;
            padding-bottom: 15px;
            margin-bottom: 25px;
            font-size: 1.8em;
        }}

        textarea {{
            width: 100%;
            min-height: 150px;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            font-size: 1.1em;
            font-family: 'Sarabun', sans-serif;
            margin-bottom: 25px;
            box-sizing: border-box;
            resize: vertical;
            transition: border-color 0.3s, box-shadow 0.3s;
        }}

        textarea:focus {{
            outline: none;
            border-color: #4A90E2;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 25px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }}

        label {{
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            font-size: 1.1em;
            color: #555;
        }}

        select {{
            width: 100%;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            font-size: 1.1em;
            background-color: white;
            transition: border-color 0.3s, box-shadow 0.3s;
            font-family: 'Sarabun', sans-serif;
        }}

        select:focus {{
            border-color: #4A90E2;
            outline: none;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
        }}

        select:disabled {{
            background-color: #f5f5f5;
            color: #888;
            cursor: not-allowed;
        }}

        .button-result-container {{
            text-align: center;
            margin-top: 30px;
        }}

        button {{
            background: linear-gradient(45deg, #50C878, #45a049);
            color: white;
            padding: 20px 40px;
            font-size: 1.3em;
            font-weight: bold;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Sarabun', sans-serif;
            box-shadow: 0 8px 25px rgba(80, 200, 120, 0.3);
            width: 100%;
            max-width: 300px;
        }}

        button:hover {{
            background: linear-gradient(45deg, #45a049, #3d8b40);
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(80, 200, 120, 0.4);
        }}
        
        button:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }}

        .result {{
            margin-top: 25px;
            padding: 30px;
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
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .download-btn {{
            display: inline-block;
            background: linear-gradient(45deg, #4A90E2, #357ABD);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-family: 'Sarabun', sans-serif;
            transition: all 0.3s;
            margin-top: 15px;
            box-shadow: 0 6px 20px rgba(74, 144, 226, 0.3);
        }}

        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4);
        }}

        footer {{
            text-align: center;
            padding: 25px;
            font-size: 1em;
            color: #888;
            background-color: #f9f9f9;
            border-top: 1px solid #e0e0e0;
        }}

        @media (max-width: 768px) {{
            .grid, .grid-3 {{
                grid-template-columns: 1fr;
            }}
            body {{
                padding: 10px;
            }}
            main {{
                padding: 20px;
            }}
            .container {{
                margin: 10px;
            }}
            header h1 {{
                font-size: 2em;
            }}
            button {{
                padding: 15px 30px;
                font-size: 1.2em;
            }}
        }}

        details {{
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-top: 25px;
            background: #fafafa;
        }}
        
        summary {{
            font-weight: bold;
            cursor: pointer;
            color: #4A90E2;
            font-size: 1.1em;
            padding: 10px 0;
        }}
        
        .effects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding-top: 20px;
        }}
        
        .checkbox-container {{
            display: flex;
            align-items: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s;
        }}
        
        .checkbox-container:hover {{
            border-color: #4A90E2;
            box-shadow: 0 4px 15px rgba(74, 144, 226, 0.1);
        }}
        
        .checkbox-container input {{
            margin-right: 15px;
            transform: scale(1.2);
        }}

        .status {{
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1.1em;
        }}

        .status.success {{
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }}

        .status.error {{
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }}

        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #4A90E2;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        .speed-control {{
            margin-top: 15px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
        }}

        .speed-slider {{
            width: 100%;
            margin: 10px 0;
        }}

        .speed-value {{
            text-align: center;
            font-weight: bold;
            color: #4A90E2;
            font-size: 1.2em;
            margin-top: 10px;
        }}

        .system-info {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 4px solid #4A90E2;
        }}

        .system-info h3 {{
            margin-top: 0;
            color: #1976d2;
        }}

        .system-info ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}

        .system-info li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎙️ VICTOR-TTS FULL UNLIMITED</h1>
            <p>Complete TTS + Voice Conversion Platform</p>
        </header>
        
        <main>
            <!-- System Information -->
            <div class="system-info">
                <h3>🔧 ข้อมูลระบบ</h3>
                <ul>
                    <li>🎵 TTS System: {'✅ Available' if status.get('tts_available') else '❌ Not Available'}</li>
                    <li>🎭 RVC System: {'✅ Available' if status.get('rvc_available') else '❌ Not Available'}</li>
                    <li>🖥️ Device: {status.get('device', 'Unknown')}</li>
                    <li>🎤 RVC Models: {status.get('rvc_models_count', 0)} models</li>
                </ul>
            </div>

            <div class="card">
                <h2>สร้างเสียงพูด (Text-to-Speech + RVC)</h2>
                <textarea id="text-input" placeholder="ใส่ข้อความที่นี่... (ไม่จำกัดความยาว)"></textarea>
                
                <div class="grid">
                    <div>
                        <label for="language-select">🌍 เลือกภาษา/ประเทศ:</label>
                        <select id="language-select">
                            <option value="">-- เลือกภาษา --</option>
                        </select>
                    </div>
                    <div>
                        <label for="tts-voice-select">🎤 เลือกเสียง TTS:</label>
                        <select id="tts-voice-select">
                            <option value="">-- เลือกเสียงก่อน --</option>
                        </select>
                    </div>
                </div>
                
                <div class="grid">
                    <div>
                        <label for="style-select">🎭 เลือกสไตล์การพูด:</label>
                        <select id="style-select">
                            <option value="">-- เลือกสไตล์ --</option>
                        </select>
                    </div>
                    <div>
                        <label for="speed-select">⚡ ความเร็วการพูด:</label>
                        <select id="speed-select">
                            <option value="0.3">🐌 ช้ามากมาก (0.3x)</option>
                            <option value="0.5">🐌 ช้ามาก (0.5x)</option>
                            <option value="0.7">🚶 ช้า (0.7x)</option>
                            <option value="0.8" selected>📖 ช้าเล็กน้อย (0.8x)</option>
                            <option value="0.9">📖 ปกติช้า (0.9x)</option>
                            <option value="1.0">🗣️ ปกติ (1.0x)</option>
                            <option value="1.1">⚡ เร็วเล็กน้อย (1.1x)</option>
                            <option value="1.3">🚀 เร็ว (1.3x)</option>
                            <option value="1.5">⚡⚡ เร็วมาก (1.5x)</option>
                        </select>
                        
                        <div class="speed-control">
                            <label for="speed-slider">🎚️ ปรับความเร็วแบบละเอียด:</label>
                            <input type="range" id="speed-slider" min="0.3" max="1.5" step="0.1" value="0.8" class="speed-slider">
                            <div id="speed-value" class="speed-value">0.8x</div>
                        </div>
                    </div>
                </div>
                
                <div class="grid">
                    <div>
                        <label for="rvc-model-select">🎭 เลือกโมเดล RVC (ไม่บังคับ):</label>
                        <select id="rvc-model-select">
                            <option value="">-- ไม่ใช้ RVC --</option>
                        </select>
                    </div>
                    <div>
                        <label for="rvc-transpose">🎵 ปรับ Pitch RVC:</label>
                        <select id="rvc-transpose">
                            <option value="-12">-12 (ต่ำมาก)</option>
                            <option value="-8">-8 (ต่ำมาก)</option>
                            <option value="-4">-4 (ต่ำ)</option>
                            <option value="-2">-2 (ต่ำเล็กน้อย)</option>
                            <option value="0" selected>0 (ปกติ)</option>
                            <option value="2">+2 (สูงเล็กน้อย)</option>
                            <option value="4">+4 (สูง)</option>
                            <option value="8">+8 (สูงมาก)</option>
                            <option value="12">+12 (สูงมากมาก)</option>
                        </select>
                    </div>
                </div>

                <details>
                    <summary>🎭 เอฟเฟกต์พิเศษ</summary>
                    <div class="effects-grid">
                        <div class="checkbox-container">
                            <input type="checkbox" id="demon-mode-check" name="demon_mode">
                            <label for="demon-mode-check">👹 โหมดปีศาจ</label>
                        </div>
                        <div class="checkbox-container">
                            <input type="checkbox" id="robot-mode-check" name="robot_mode">
                            <label for="robot-mode-check">🤖 โหมดหุ่นยนต์</label>
                        </div>
                        <div class="checkbox-container">
                            <input type="checkbox" id="echo-mode-check" name="echo_mode">
                            <label for="echo-mode-check">🔊 โหมดเอคโค่</label>
                        </div>
                        <div class="checkbox-container">
                            <input type="checkbox" id="reverb-mode-check" name="reverb_mode">
                            <label for="reverb-mode-check">🏛️ โหมดเสียงสะท้อน</label>
                        </div>
                    </div>
                </details>

                <div class="button-result-container">
                    <button id="generate-btn">🚀 สร้างเสียง</button>
                    
                    <div id="result" class="result">
                        <h3>🎵 ผลลัพธ์</h3>
                        <audio id="audio-output" controls></audio>
                        <br>
                        <a id="download-link" href="#" download="output.wav" class="download-btn">📥 ดาวน์โหลดไฟล์เสียง</a>
                    </div>
                </div>
            </div>
            
            <div id="status" class="status" style="display: none;"></div>
        </main>
        
        <footer>
            <p>Powered by FastAPI, RVC & Gradio. Crafted with ❤️ by VICTOR.</p>
        </footer>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const languageSelect = document.getElementById('language-select');
            const ttsVoiceSelect = document.getElementById('tts-voice-select');
            const styleSelect = document.getElementById('style-select');
            const speedSelect = document.getElementById('speed-select');
            const rvcModelSelect = document.getElementById('rvc-model-select');
            const rvcTransposeSelect = document.getElementById('rvc-transpose');
            const generateBtn = document.getElementById('generate-btn');
            const textInput = document.getElementById('text-input');
            const resultDiv = document.getElementById('result');
            const audioOutput = document.getElementById('audio-output');
            const downloadLink = document.getElementById('download-link');
            const demonModeCheck = document.getElementById('demon-mode-check');
            const robotModeCheck = document.getElementById('robot-mode-check');
            const echoModeCheck = document.getElementById('echo-mode-check');
            const reverbModeCheck = document.getElementById('reverb-mode-check');
            const speedSlider = document.getElementById('speed-slider');
            const speedValue = document.getElementById('speed-value');
            let lastAudioUrl = '';
            let allVoices = {{}}; // Store all voices data

            // Speed slider handler
            speedSlider.addEventListener('input', function() {{
                const value = parseFloat(this.value);
                speedValue.textContent = value.toFixed(1) + 'x';
                
                // Update dropdown to match slider
                const dropdown = document.getElementById('speed-select');
                const options = Array.from(dropdown.options);
                const closestOption = options.reduce((prev, curr) => {{
                    return Math.abs(parseFloat(curr.value) - value) < Math.abs(parseFloat(prev.value) - value) ? curr : prev;
                }});
                dropdown.value = closestOption.value;
            }});

            // Speed dropdown handler
            speedSelect.addEventListener('change', function() {{
                const value = parseFloat(this.value);
                speedSlider.value = value;
                speedValue.textContent = value.toFixed(1) + 'x';
            }});

            // Language mapping with country flags and names
            const languageMapping = {{
                'Thai': {{
                    name: '🇹🇭 ไทย (Thailand)',
                    code: 'th-TH',
                    flag: '🇹🇭',
                    rvcModels: ['niwat_thai', 'YingyongYodbuangarm', 'VANXAI', 'ChalermpolMalakham', 'MonkanKaenkoon', 'DangHMD2010v2New', 'BoSunita', 'pang', 'knomjean', 'illslick', 'al_bundy', 'boy_peacemaker', 'Michael', 'STS73', 'Law_By_Mike_e160_s4800', 'MusicV1Carti_300_Epochs', 'theestallion', 'JNANG', 'JO']
                }},
                'English': {{
                    name: '🇺🇸 อังกฤษ (English)',
                    code: 'en-US',
                    flag: '🇺🇸',
                    rvcModels: ['aria_english']
                }},
                'Chinese': {{
                    name: '🇨🇳 จีน (Chinese)',
                    code: 'zh-CN',
                    flag: '🇨🇳',
                    rvcModels: []
                }},
                'Japanese': {{
                    name: '🇯🇵 ญี่ปุ่น (Japanese)',
                    code: 'ja-JP',
                    flag: '🇯🇵',
                    rvcModels: []
                }},
                'Lao': {{
                    name: '🇱🇦 ลาว (Laos)',
                    code: 'lo-LA',
                    flag: '🇱🇦',
                    rvcModels: ['keomany_lao']
                }}
            }};

            // RVC Model categories
            const rvcModelCategories = {{
                'Thai Male': ['niwat_thai', 'YingyongYodbuangarm', 'VANXAI', 'ChalermpolMalakham', 'MonkanKaenkoon', 'DangHMD2010v2New', 'knomjean', 'illslick', 'al_bundy', 'boy_peacemaker', 'Michael', 'STS73', 'Law_By_Mike_e160_s4800', 'JNANG', 'JO'],
                'Thai Female': ['BoSunita', 'pang', 'theestallion'],
                'English': ['aria_english'],
                'Lao': ['keomany_lao'],
                'Music': ['MusicV1Carti_300_Epochs']
            }};

            let allRvcModels = []; // Store all RVC models

            // Fetch available voices and models
            async function fetchInitialData() {{
                try {{
                    // Fetch TTS voices
                    const voicesResponse = await fetch('/voices');
                    const voicesData = await voicesResponse.json();
                    if (voicesData.success && voicesData.data.voices) {{
                        allVoices = voicesData.data.voices;
                        
                        // Group voices by language
                        const voicesByLanguage = {{}};
                        for (const [key, voice] of Object.entries(allVoices)) {{
                            const lang = voice.language;
                            if (!voicesByLanguage[lang]) {{
                                voicesByLanguage[lang] = [];
                            }}
                            voicesByLanguage[lang].push({{key, ...voice}});
                        }}
                        
                        // Populate language select
                        for (const [language, mapping] of Object.entries(languageMapping)) {{
                            if (voicesByLanguage[language]) {{
                                const option = document.createElement('option');
                                option.value = language;
                                option.textContent = mapping.name;
                                languageSelect.appendChild(option);
                            }}
                        }}
                        
                        // Set default language to Thai if available
                        if (voicesByLanguage['Thai']) {{
                            languageSelect.value = 'Thai';
                            updateVoiceOptions('Thai');
                        }}
                    }}
                    
                    // Fetch Speaking Styles
                    const stylesResponse = await fetch('/styles');
                    const stylesData = await stylesResponse.json();
                    if (stylesData.success && stylesData.data.styles) {{
                        for (const [key, style] of Object.entries(stylesData.data.styles)) {{
                            const option = document.createElement('option');
                            option.value = key;
                            option.textContent = style.name;
                            styleSelect.appendChild(option);
                        }}
                    }}
                    
                    // Fetch RVC models
                    const modelsResponse = await fetch('/models');
                    const modelsData = await modelsResponse.json();
                    if (modelsData.success && modelsData.data.models) {{
                        allRvcModels = modelsData.data.models;
                        updateRvcModelOptions('Thai'); // Default to Thai
                    }}
                }} catch (error) {{
                    console.error('Error fetching initial data:', error);
                    showStatus('ไม่สามารถโหลดข้อมูลเสียงหรือโมเดลได้', 'error');
                }}
            }}

            // Update voice options based on selected language
            function updateVoiceOptions(selectedLanguage) {{
                // Clear current voice options
                ttsVoiceSelect.innerHTML = '<option value="">-- เลือกเสียง --</option>';
                
                if (!selectedLanguage || !allVoices) return;
                
                // Filter voices by language
                const filteredVoices = Object.entries(allVoices).filter(
                    ([key, voice]) => voice.language === selectedLanguage
                );
                
                // Add voices to select
                let isFirst = true;
                filteredVoices.forEach(([key, voice]) => {{
                    const option = document.createElement('option');
                    option.value = key;
                    
                    // Add gender emoji
                    const genderEmoji = voice.gender === 'Male' ? '👨' : '👩';
                    const languageFlag = languageMapping[voice.language]?.flag || '🗣️';
                    
                    option.textContent = `${{genderEmoji}} ${{voice.name}}`;
                    
                    // Set first voice as default
                    if (isFirst) {{
                        option.selected = true;
                        isFirst = false;
                    }}
                    
                    ttsVoiceSelect.appendChild(option);
                }});
                
                // Update placeholder if no voices found
                if (filteredVoices.length === 0) {{
                    ttsVoiceSelect.innerHTML = '<option value="">-- ไม่มีเสียงสำหรับภาษานี้ --</option>';
                }}
                
                // Update RVC models for selected language
                updateRvcModelOptions(selectedLanguage);
            }}

            // Update RVC model options based on selected language
            function updateRvcModelOptions(selectedLanguage) {{
                // Clear current RVC model options
                rvcModelSelect.innerHTML = '<option value="">-- ไม่ใช้ RVC --</option>';
                
                if (!selectedLanguage || !allRvcModels) return;
                
                const languageConfig = languageMapping[selectedLanguage];
                if (!languageConfig || !languageConfig.rvcModels) return;
                
                // Get available models for this language
                const availableModels = allRvcModels.filter(model => 
                    languageConfig.rvcModels.includes(model.name)
                );
                
                if (availableModels.length === 0) return;
                
                // Group models by category
                const modelsByCategory = {{}};
                availableModels.forEach(model => {{
                    let category = 'Other';
                    
                    // Determine category based on model name
                    for (const [catName, catModels] of Object.entries(rvcModelCategories)) {{
                        if (catModels.includes(model.name)) {{
                            category = catName;
                            break;
                        }}
                    }}
                    
                    if (!modelsByCategory[category]) {{
                        modelsByCategory[category] = [];
                    }}
                    modelsByCategory[category].push(model);
                }});
                
                // Add models grouped by category
                for (const [category, models] of Object.entries(modelsByCategory)) {{
                    // Add category header
                    const categoryOption = document.createElement('option');
                    categoryOption.value = '';
                    categoryOption.textContent = `--- ${{category}} ---`;
                    categoryOption.disabled = true;
                    rvcModelSelect.appendChild(categoryOption);
                    
                    // Add models in this category
                    models.forEach(model => {{
                        const option = document.createElement('option');
                        option.value = model.name;
                        
                        // Add emoji based on category
                        let emoji = '🎤';
                        if (category.includes('Male')) emoji = '👨';
                        else if (category.includes('Female')) emoji = '👩';
                        else if (category.includes('Lao')) emoji = '🇱🇦';
                        else if (category.includes('English')) emoji = '🇺🇸';
                        else if (category.includes('Music')) emoji = '🎵';
                        
                        option.textContent = `${{emoji}} ${{model.name}}`;
                        rvcModelSelect.appendChild(option);
                    }});
                }}
            }}

            // Language selection handler
            languageSelect.addEventListener('change', function() {{
                const selectedLanguage = this.value;
                updateVoiceOptions(selectedLanguage);
            }});

            // Generate audio with all features
            async function generateAudio() {{
                const text = textInput.value.trim();
                if (!text) {{
                    showStatus('กรุณาใส่ข้อความ', 'error');
                    return;
                }}
                
                const selectedVoice = ttsVoiceSelect.value;
                if (!selectedVoice) {{
                    showStatus('กรุณาเลือกเสียง TTS', 'error');
                    return;
                }}
                
                generateBtn.disabled = true;
                generateBtn.innerHTML = '<span class="loading"></span>กำลังประมวลผล...';
                hideStatus();
                
                // Hide previous result
                resultDiv.classList.remove('show');
                
                // Get selected speed
                const selectedSpeed = parseFloat(speedSlider.value);
                
                // Collect all effects
                const effects = {{
                    demon_mode: demonModeCheck.checked,
                    robot_mode: robotModeCheck.checked,
                    echo_mode: echoModeCheck.checked,
                    reverb_mode: reverbModeCheck.checked,
                }};
                
                const rvcModelName = rvcModelSelect.value;
                const rvcTranspose = parseInt(rvcTransposeSelect.value);
                
                const payload = {{
                    text: text,
                    tts_voice: selectedVoice,
                    tts_speed: selectedSpeed,
                    enable_rvc: !!rvcModelName,
                    rvc_model: rvcModelName,
                    rvc_transpose: rvcTranspose,
                    rvc_index_ratio: 0.7,
                    rvc_f0_method: "rmvpe",
                    effects: effects
                }};
                
                try {{
                    const response = await fetch('/full_tts', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify(payload),
                    }});
                    
                    if (!response.ok) {{
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'เกิดข้อผิดพลาดในการสร้างเสียง');
                    }}
                    
                    const result = await response.json();
                    
                    if (result.success && result.data.audio_base64) {{
                        const audioSrc = `data:audio/wav;base64,${{result.data.audio_base64}}`;
                        audioOutput.src = audioSrc;
                        downloadLink.href = audioSrc;
                        lastAudioUrl = audioSrc;
                        
                        // Show result with animation
                        resultDiv.classList.add('show');
                        
                        // Scroll to result
                        resultDiv.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                        
                        // Show success message
                        showSuccessMessage(result.data);
                        
                        console.log('Processing info:', result.data);
                    }} else {{
                        throw new Error(result.message || 'ไม่ได้รับข้อมูลเสียง');
                    }}
                }} catch (error) {{
                    console.error('Error generating audio:', error);
                    showStatus(`เกิดข้อผิดพลาด: ${{error.message}}`, 'error');
                }} finally {{
                    generateBtn.disabled = false;
                    generateBtn.innerHTML = '🚀 สร้างเสียง';
                }}
            }}

            // Show success message
            function showSuccessMessage(data) {{
                const selectedSpeed = parseFloat(speedSlider.value);
                const speedText = `${{selectedSpeed.toFixed(1)}}x`;
                
                const successDiv = document.createElement('div');
                successDiv.innerHTML = `
                    <div style="text-align: center; padding: 20px; background: #d4edda; border: 2px solid #c3e6cb; border-radius: 10px; margin: 20px 0; color: #155724;">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">✅ สร้างเสียงสำเร็จ!</div>
                        <div style="font-size: 16px;">
                            📝 ข้อความ: ${{data.text_length}} ตัวอักษร<br>
                            🎵 ขนาดไฟล์: ${{(data.audio_size / 1024).toFixed(1)}} KB<br>
                            ⚡ ความเร็ว: ${{speedText}}<br>
                            ${{data.voice_conversion_applied ? '🎭 ใช้ RVC: ใช่' : '🎭 ใช้ RVC: ไม่'}}
                        </div>
                    </div>
                `;
                
                resultDiv.parentNode.insertBefore(successDiv, resultDiv);
                
                // Auto-remove after 5 seconds
                setTimeout(() => {{
                    if (successDiv.parentNode) {{
                        successDiv.remove();
                    }}
                }}, 5000);
            }}

            // Show status message
            function showStatus(message, type) {{
                const statusDiv = document.getElementById('status');
                statusDiv.textContent = message;
                statusDiv.className = `status ${{type}}`;
                statusDiv.style.display = 'block';
                
                // Auto-hide after 5 seconds
                setTimeout(() => {{
                    hideStatus();
                }}, 5000);
            }}

            // Hide status message
            function hideStatus() {{
                const statusDiv = document.getElementById('status');
                statusDiv.style.display = 'none';
            }}

            // Event listeners
            generateBtn.addEventListener('click', generateAudio);
            
            downloadLink.addEventListener('click', function(e) {{
                if (!lastAudioUrl) {{
                    e.preventDefault();
                    showStatus('ไม่มีไฟล์เสียงที่สร้างล่าสุด', 'error');
                }}
            }});
            
            // Keyboard shortcuts
            textInput.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' && e.ctrlKey) {{
                    generateAudio();
                }}
            }});
            
            // Initialize the app
            fetchInitialData();
        }});
    </script>
</body>
</html>
"""
        return html
    
    def create_simple_server(self):
        """สร้าง server แบบครบถ้วน"""
        import http.server
        import socketserver
        
        class CompleteRequestHandler(http.server.BaseHTTPRequestHandler):
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
                elif self.path == '/voices':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    voices = get_supported_voices()
                    response = {
                        'success': True,
                        'data': {'voices': voices}
                    }
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                elif self.path == '/models':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    if self.web_interface.core:
                        models = self.web_interface.core.get_available_rvc_models()
                        model_list = [{'name': model} for model in models]
                    else:
                        model_list = []
                    
                    response = {
                        'success': True,
                        'data': {'models': model_list}
                    }
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                elif self.path == '/styles':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    styles = {
                        'normal': {'name': 'ปกติ'},
                        'excited': {'name': 'ตื่นเต้น'},
                        'calm': {'name': 'สงบ'},
                        'sad': {'name': 'เศร้า'},
                        'angry': {'name': 'โกรธ'}
                    }
                    
                    response = {
                        'success': True,
                        'data': {'styles': styles}
                    }
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                if self.path == '/full_tts':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = json.loads(post_data.decode('utf-8'))
                        
                        # สร้างเสียง
                        async def generate():
                            try:
                                # TTS
                                audio_data = await self.web_interface.core.generate_tts(
                                    data['text'], 
                                    data['tts_voice'],
                                    data.get('tts_speed', 1.0)
                                )
                                
                                # RVC (ถ้ามี)
                                if data.get('enable_rvc') and data.get('rvc_model'):
                                    audio_data = self.web_interface.core.convert_voice(
                                        audio_data, 
                                        data['rvc_model'],
                                        data.get('rvc_transpose', 0),
                                        data.get('rvc_index_ratio', 0.75),
                                        data.get('rvc_f0_method', 'rmvpe')
                                    )
                                
                                return {
                                    'success': True,
                                    'data': {
                                        'audio_base64': base64.b64encode(audio_data).decode('utf-8'),
                                        'text_length': len(data['text']),
                                        'audio_size': len(audio_data),
                                        'voice_conversion_applied': data.get('enable_rvc', False)
                                    }
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
        
        class CompleteServer(socketserver.TCPServer):
            def __init__(self, server_address, handler_class, web_interface):
                self.web_interface = web_interface
                super().__init__(server_address, handler_class)
            
            def finish_request(self, request, client_address):
                self.RequestHandlerClass(request, client_address, self, web_interface=self.web_interface)
        
        return CompleteServer(('localhost', self.port), CompleteRequestHandler, self)
    
    def start(self, open_browser: bool = True):
        """เริ่มต้น server"""
        try:
            server = self.create_simple_server()
            self.is_running = True
            
            print(f"🌐 Complete Web Interface started on http://localhost:{self.port}")
            print("✅ All features included: TTS, RVC, Effects, Speed Control")
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
    print("🚀 Starting Complete Web Interface...")
    
    interface = CompleteWebInterface()
    interface.start()

if __name__ == "__main__":
    main() 