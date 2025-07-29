# 🐉 VICTOR-TTS: Advanced Text-to-Speech with Voice Conversion

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![N8N](https://img.shields.io/badge/N8N-Integration-green.svg)](https://n8n.io/)
[![GPU](https://img.shields.io/badge/GPU-Supported-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Overview

**VICTOR-TTS** เป็นระบบ Text-to-Speech แบบครบวงจรที่รวมเทคโนโลยี RVC (Retrieval-Based Voice Conversion) เข้าด้วยกัน เพื่อสร้างเสียงพูดคุณภาพสูงพร้อมการแปลงเสียงแบบ AI

### ✨ Key Features

- 🎙️ **Edge TTS Integration** - เสียงพูดคุณภาพสูงจาก Microsoft
- 🎭 **RVC Voice Conversion** - แปลงเสียงด้วย AI
- 🐳 **Docker Support** - ติดตั้งง่ายด้วย Docker
- 🔄 **N8N Integration** - Workflow automation
- 🖥️ **GPU Acceleration** - รองรับ CUDA สำหรับความเร็วสูง
- 🎨 **Modern UI** - Enhanced Web Interface
- 🌐 **Multi-language Support** - รองรับหลายภาษา (อัตโนมัติ)
- ⚡ **Performance Optimized** - ปรับแต่งตามระบบ
- 🎭 **Special Effects** - เอฟเฟกต์พิเศษ (ปีศาจ, หุ่นยนต์)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/Banchert/victor-tts-unified.git
cd victor-tts-unified

# Start with Docker (Simple)
docker-compose -f docker/docker-compose.simple.yml up -d

# Or use Python management script
python scripts/docker_management.py
```

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/Banchert/victor-tts-unified.git
cd victor-tts-unified

# Install dependencies
pip install -r requirements.txt

# Start the application
start.bat
```

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **N8N** | http://localhost:5678 | Workflow Automation |
| **VICTOR-TTS API** | http://localhost:6969 | REST API |
| **VICTOR-TTS Web** | http://localhost:7000 | Enhanced Web Interface |
| **Health Check** | http://localhost:6969/health | System Status |

## 📁 Project Structure

```
VICTOR-TTS/
├── 🔧 Core Application
│   ├── main_api_server.py           # FastAPI server
│   ├── web_interface_complete.py    # Enhanced Web UI (Main)
│   ├── web_interface_improved.py    # Improved Web UI
│   ├── tts_rvc_core.py              # Core logic
│   ├── rvc_api.py                   # RVC wrapper
│   └── victor_tts_launcher.py       # Launcher
├── 🐳 Docker Files
│   ├── docker/Dockerfile            # Main container
│   ├── docker/docker-compose.yml    # Full deployment
│   ├── docker/docker-compose.simple.yml # Simple deployment
│   ├── docker/docker-compose.test.yml   # Test deployment
│   └── docker/nginx.conf            # Reverse proxy
├── 📜 Scripts
│   ├── start.bat                    # Main launcher
│   ├── start_complete.bat           # Complete interface launcher
│   ├── start_improved.bat           # Improved interface launcher
│   ├── scripts/docker_management.py # Docker management
│   └── scripts/*.ps1                # PowerShell scripts
├── 📊 Documentation
│   ├── docs/README.md               # Main documentation
│   ├── docs/DOCKER_N8N_GUIDE.md     # Docker & N8N guide
│   ├── docs/GPU_EXE_GUIDE.md        # GPU & EXE guide
│   ├── WEB_INTERFACE_GUIDE.md       # Web Interface Guide
│   └── docs/*.md                    # Other guides
├── 🧪 Tests
│   ├── tests/test_*.py              # Test files
│   └── tests/                       # Test utilities
├── 🎭 RVC System
│   ├── rvc/                         # RVC models
│   ├── models/                      # Voice models
│   └── voice_models/                # Additional models
└── 🔄 N8N Integration
    └── n8n_workflows/               # Workflow templates
```

## 🎯 Core Technologies

### **Text-to-Speech (TTS)**
- **Microsoft Edge TTS** - เสียงพูดคุณภาพสูง
- **Multi-language Support** - รองรับหลายภาษา (อัตโนมัติ)
- **Language Detection** - ตรวจจับและแยกข้อความตามภาษา
- **Voice Mapping** - เลือกเสียงที่เหมาะสมสำหรับแต่ละภาษา
- **Speed Control** - ปรับความเร็วการพูด

### **Voice Conversion (RVC)**
- **HuBERT/ContentVec** - Speaker embedding
- **F0 Extraction** - rmvpe, crepe, fcpe
- **Model Management** - อัปโหลดและจัดการโมเดล

### **System Architecture**
- **FastAPI** - REST API framework
- **PyTorch** - AI/ML framework
- **Docker** - Containerization
- **N8N** - Workflow automation

## 🔧 API Endpoints

### **Main Endpoints**
```http
POST /unified              # TTS + RVC combined
POST /tts                  # TTS only
POST /voice_conversion     # RVC only
GET  /voices              # Available voices
GET  /models              # Available models
GET  /health              # Health check
```

### **Example Usage**
```bash
# TTS + RVC
curl -X POST http://localhost:6969/unified \
  -H "Content-Type: application/json" \
  -d '{
    "text": "สวัสดีครับ ยินดีต้อนรับสู่ระบบ VICTOR-TTS",
    "tts_voice": "th-TH-NeeraNeural",
    "speed": 1.0,
    "enable_rvc": true,
    "rvc_params": {
      "model_name": "al_bundy",
      "transpose": 0
    }
  }'
```

## 🐳 Docker Deployment

### **Simple Deployment**
```bash
docker-compose -f docker/docker-compose.simple.yml up -d
```

### **Full Deployment**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

### **Test Deployment**
```bash
docker-compose -f docker/docker-compose.test.yml up -d
```

## 🔄 N8N Integration

### **Workflow Automation**
1. Import workflow จาก `n8n_workflows/victor_tts_workflow.json`
2. Activate workflow ใน N8N
3. เรียกใช้ผ่าน webhook

### **Webhook Example**
```bash
curl -X POST http://localhost:5678/webhook/victor-tts-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from N8N!",
    "voice": "en-US-JennyNeural",
    "enable_rvc": true
  }'
```

## 🖥️ GPU Support

### **Requirements**
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.8+
- PyTorch with CUDA

### **Configuration**
```bash
# Check GPU availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Set GPU device
export CUDA_VISIBLE_DEVICES=0
```

## 📊 Performance Optimization

### **Automatic Optimization**
- **CPU Detection** - ปรับแต่งตาม CPU cores
- **Memory Management** - จัดการ RAM อัตโนมัติ
- **GPU Utilization** - ใช้ GPU อย่างมีประสิทธิภาพ
- **Batch Processing** - ประมวลผลแบบ batch

### **Manual Configuration**
```python
# Performance settings
performance_config = {
    "tts_concurrent": 4,    # TTS concurrent processes
    "rvc_batch": 1,         # RVC batch size
    "gpu_memory_fraction": 0.8,  # GPU memory usage
    "half_precision": True  # Use FP16 for speed
}
```

## 🌍 Multi-Language Features

### **Supported Languages**
- 🇹🇭 **Thai** - ภาษาไทย
- 🇱🇦 **Lao** - ภาษาลาว  
- 🇺🇸 **English** - ภาษาอังกฤษ
- 🇯🇵 **Japanese** - ภาษาญี่ปุ่น
- 🇨🇳 **Chinese** - ภาษาจีน
- 🔢 **Numbers** - ตัวเลข

### **Automatic Language Detection**
```python
# ตัวอย่างการตรวจจับภาษา
text = "สวัสดีครับ Hello world ສະບາຍດີ こんにちは 你好 123"

# ผลลัพธ์:
# • "สวัสดีครับ" → thai (Voice: Premwadee)
# • "Hello world" → english (Voice: Aria)
# • "ສະບາຍດີ" → lao (Voice: Keomany)
# • "こんにちは" → japanese (Voice: Nanami)
# • "你好" → chinese (Voice: Xiaoxiao)
# • "123" → numbers (Voice: Premwadee)
```

### **Voice Mapping**
| ภาษา | Female Voice | Male Voice |
|------|--------------|------------|
| 🇹🇭 ไทย | `th-TH-PremwadeeNeural` | `th-TH-NiranNeural` |
| 🇱🇦 ลาว | `lo-LA-KeomanyNeural` | `lo-LA-ChanthavongNeural` |
| 🇺🇸 อังกฤษ | `en-US-AriaNeural` | `en-US-GuyNeural` |
| 🇯🇵 ญี่ปุ่น | `ja-JP-NanamiNeural` | - |
| 🇨🇳 จีน | `zh-CN-XiaoxiaoNeural` | - |

### **Usage**
```bash
# เปิดใช้งาน Multi-Language (เฉพาะภาษาลาว)
{
    "text": "ສະບາຍດີ Hello world ຂອບໃຈ",
    "enable_multi_language": true
}

# ปิดใช้งาน Multi-Language (ค่าเริ่มต้น)
{
    "text": "สวัสดีครับ Hello world",
    "enable_multi_language": false
}
```

## 🎨 User Interface

### **Naga Dragons Theme**
- **Dark Blue Gradient** - พื้นหลังสวยงาม
- **Glass Morphism** - เอฟเฟคแก้ว
- **Responsive Design** - รองรับทุกขนาดหน้าจอ
- **Interactive Elements** - ปุ่มและฟอร์มที่ใช้งานง่าย

### **Features**
- **Model Management** - จัดการโมเดลเสียง
- **Device Selection** - เลือก CPU/GPU
- **Real-time Processing** - ประมวลผลแบบ real-time
- **Audio Preview** - ฟังเสียงตัวอย่าง

## 📚 Documentation

### **Guides**
- [🐳 Docker & N8N Guide](docs/DOCKER_N8N_GUIDE.md)
- [🖥️ GPU & EXE Guide](docs/GPU_EXE_GUIDE.md)
- [🎨 UI Theme Guide](docs/NAGA_THEME_UPDATE.md)
- [📁 Model Management Guide](docs/MODEL_MANAGEMENT_REPOSITION.md)
- [🌍 Multi-Language Enhancement](docs/MULTI_LANGUAGE_ENHANCEMENT.md)

### **API Documentation**
- [FastAPI Docs](http://localhost:6969/docs)
- [Interactive API](http://localhost:6969/redoc)

## 🔧 Development

### **Setup Development Environment**
```bash
# Clone repository
git clone https://github.com/Banchert/victor-tts-unified.git
cd victor-tts-unified

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python web_interface.py
```

### **Testing**
```bash
# Run tests
python -m pytest tests/

# Test specific components
python tests/test_rvc_quick.py
python tests/test_tts_language.py
python tests/test_multi_language_enhanced.py

# หรือใช้ start.bat
start.bat
# เลือก [8] 🌍 ทดสอบหลายภาษา
# เลือก [9] 🌍 ทดสอบหลายภาษา (Enhanced)
```