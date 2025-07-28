# 🎙️ VICTOR-TTS UNIFIED

**Complete Text-to-Speech with Voice Conversion Platform**

ระบบ TTS และ Voice Conversion ที่รวมทุกอย่างไว้ในที่เดียว ใช้งานง่าย มี API สำหรับ N8N และ Web Interface

## ✨ Features

- 🎯 **Edge TTS Integration** - คุณภาพเสียงสูงจาก Microsoft Edge TTS
- 🎭 **Retrieval-based Voice Conversion (RVC)** - เปลี่ยนเสียงด้วย AI
- 🔌 **N8N Integration** - เชื่อมต่อกับ N8N workflow automation
- 🌐 **Web Interface** - ใช้งานผ่านเว็บได้ง่าย
- ⚡ **GPU Acceleration** - รองรับ GPU สำหรับความเร็วสูง
- 🚀 **FastAPI Backend** - API ที่เร็วและใช้งานง่าย
- 📱 **RESTful API** - เชื่อมต่อกับแอปพลิเคชันอื่นๆ ได้

## 🛠️ Requirements

- Python 3.10 หรือสูงกว่า
- FFMPEG (สำหรับประมวลผลเสียง)
- NVIDIA GPU with CUDA support (optional, สำหรับความเร็วสูง)

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/victor-tts-unified.git
cd victor-tts-unified
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFMPEG
- **Windows**: ดาวน์โหลดจาก [FFmpeg.org](https://ffmpeg.org/download.html)
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

## 🚀 Quick Start

### Start API Server
```bash
python start.py --api
```
หรือ
```bash
python main_api_server.py
```

### Start Web Interface
```bash
python start.py --web
```
หรือ
```bash
python web_interface.py
```

### Use GPU Acceleration
```bash
python start.py --api --gpu 0  # ใช้ GPU 0
python start.py --web --gpu 1  # ใช้ GPU 1
```

## 🎮 Usage

### Web Interface
เปิดเบราว์เซอร์ไปที่: `http://localhost:7000`

### API Endpoints
- **Swagger UI**: `http://localhost:6969/docs`
- **ReDoc**: `http://localhost:6969/redoc`

### N8N Integration
ใช้ URL: `http://localhost:6969` ใน N8N HTTP Request node

## 📁 Project Structure

```
victor-tts-unified/
├── main_api_server.py      # FastAPI server
├── web_interface.py        # Gradio web interface
├── tts_rvc_core.py         # Core TTS + RVC logic
├── start.py               # Main launcher
├── requirements.txt       # Python dependencies
├── config/               # Configuration files
├── storage/              # Output and temp files
├── models/               # Model storage
├── logs/                 # RVC model storage
└── rvc/                  # RVC system files
```

## 🔧 Configuration

แก้ไขไฟล์ `config/unified_config.toml` สำหรับการตั้งค่าต่างๆ:

```toml
[server]
host = "0.0.0.0"
port = 6969

[gpu]
enabled = true
device_id = 0
memory_limit = 0
use_fp16 = true

[tts]
default_voice = "en-US-AndrewNeural"
default_rate = 0
default_volume = 0

[rvc]
default_pitch = 0
default_index_rate = 0.5
default_protect = 0.33
```

## 📚 API Documentation

### TTS Endpoint
```http
POST /tts
Content-Type: application/json

{
    "text": "Hello world",
    "voice": "en-US-AndrewNeural",
    "rate": 0,
    "volume": 0
}
```

### RVC Endpoint
```http
POST /rvc
Content-Type: multipart/form-data

{
    "audio_file": <audio_file>,
    "model_name": "model_name",
    "pitch": 0,
    "index_rate": 0.5,
    "protect": 0.33
}
```

### Combined TTS + RVC
```http
POST /tts-rvc
Content-Type: application/json

{
    "text": "Hello world",
    "voice": "en-US-AndrewNeural",
    "model_name": "model_name",
    "pitch": 0,
    "index_rate": 0.5,
    "protect": 0.33
}
```

## 🎯 Examples

### Python Client
```python
import requests

# TTS
response = requests.post("http://localhost:6969/tts", json={
    "text": "Hello from Python!",
    "voice": "en-US-AndrewNeural"
})

# RVC
with open("audio.wav", "rb") as f:
    response = requests.post("http://localhost:6969/rvc", files={
        "audio_file": f
    }, data={
        "model_name": "my_model"
    })
```

### N8N Workflow
1. เพิ่ม **HTTP Request** node
2. ตั้งค่า URL: `http://localhost:6969/tts-rvc`
3. Method: `POST`
4. Body: JSON
```json
{
    "text": "{{ $json.text }}",
    "voice": "en-US-AndrewNeural",
    "model_name": "{{ $json.model }}"
}
```

## 🔧 Troubleshooting

### Common Issues

1. **FFMPEG not found**
   - ติดตั้ง FFMPEG และเพิ่มใน PATH

2. **GPU not working**
   - ตรวจสอบ CUDA installation
   - ใช้ `--cpu` flag สำหรับ CPU only

3. **Port already in use**
   - เปลี่ยน port ใน config หรือ kill process ที่ใช้ port นั้น

### Logs
ตรวจสอบ logs ใน:
- Console output
- `storage/logs/` directory

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Edge-TTS](https://github.com/rany2/edge-tts) - Text-to-Speech system
- [RVC](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) - Voice conversion technology
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Gradio](https://gradio.app/) - Web interface framework

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/victor-tts-unified/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/victor-tts-unified/discussions)
- 📧 **Email**: your-email@example.com

---

⭐ **Star this repository if you find it helpful!**
