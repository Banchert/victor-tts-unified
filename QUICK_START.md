# 🚀 VICTOR-TTS UNIFIED - Quick Start Guide

## ⚡ การเริ่มต้นอย่างรวดเร็ว

### 1. เริ่มต้น TTS Server
```bash
# วิธีที่ 1: Python โดยตรง
python main_api_server.py --port 6969

# วิธีที่ 2: Docker
docker-compose up -d
```

### 2. ตรวจสอบสถานะ
```bash
# Health Check
curl http://localhost:6969/health

# ทดสอบ API
python test_api.py
```

### 3. เชื่อมต่อ N8N

#### **TTS อย่างเดียว:**
```json
{
  "text": "{{ $json.text }}",
  "voice": "th-TH-PremwadeeNeural",
  "speed": 1.0
}
```
**URL:** `http://host.docker.internal:6969/tts`

#### **TTS + RVC:**
```json
{
  "text": "{{ $json.text }}",
  "tts_voice": "th-TH-PremwadeeNeural",
  "speed": 1.0,
  "enable_rvc": true,
  "rvc_params": {
    "model_name": "VANXAI",
    "transpose": 0,
    "index_ratio": 0.75,
    "f0_method": "rmvpe"
  }
}
```
**URL:** `http://host.docker.internal:6969/unified`

---

## 📁 ไฟล์ที่สำคัญ

| ไฟล์ | คำอธิบาย |
|------|----------|
| `N8N_INTEGRATION_GUIDE.md` | คู่มือการเชื่อมต่อ N8N แบบละเอียด |
| `n8n_examples.json` | ตัวอย่าง JSON สำหรับ N8N |
| `test_api.py` | สคริปต์ทดสอบ API |
| `docker-compose.yml` | การตั้งค่า Docker |

---

## 🎯 ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: TTS อย่างเดียว
```bash
curl -X POST http://localhost:6969/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "สวัสดีครับ",
    "voice": "th-TH-PremwadeeNeural",
    "speed": 1.0
  }'
```

### ตัวอย่างที่ 2: TTS + RVC
```bash
curl -X POST http://localhost:6969/unified \
  -H "Content-Type: application/json" \
  -d '{
    "text": "สวัสดีครับ",
    "tts_voice": "th-TH-PremwadeeNeural",
    "speed": 1.0,
    "enable_rvc": true,
    "rvc_params": {
      "model_name": "VANXAI",
      "transpose": 0,
      "index_ratio": 0.75,
      "f0_method": "rmvpe"
    }
  }'
```

---

## 🔧 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย:

1. **Connection Refused**
   - ตรวจสอบ: `curl http://localhost:6969/health`
   - แก้ไข: เริ่มต้น TTS Server

2. **Field Required Error**
   - ตรวจสอบ: JSON Body ให้ตรงกับ API Schema
   - แก้ไข: ใช้ field name ที่ถูกต้อง

3. **Port Already in Use**
   - ตรวจสอบ: `netstat -ano | findstr :6969`
   - แก้ไข: `taskkill /PID [PID] /F`

---

## 📞 การสนับสนุน

- **API Documentation:** `http://localhost:6969/docs`
- **Health Check:** `http://localhost:6969/health`
- **RVC Models:** `http://localhost:6969/models`
- **TTS Voices:** `http://localhost:6969/voices`

---

**�� พร้อมใช้งานแล้ว!** 