# 🚀 Quick Start Guide - VICTOR-TTS + N8N Integration

## คำตอบสำหรับคำถาม: "โปรแกรมทำงานได้แล้ว ตอนนี้ ผมอยากใช้โปรแกมนี้ด้วย n8n ผมต้องทำอะไรเพี่มไหม ช่วยดูให้หน่อย ว่าโปรแกมนี้ สามาดติดตั้งไปที่ Docker ได้ไหม"

## ✅ ข่าวดี! ระบบพร้อมใช้งานแล้ว

**คุณไม่ต้องทำอะไรเพิ่ม** เพราะระบบ Docker + N8N พร้อมใช้งานครบถ้วนแล้ว!

---

## 🐳 วิธีใช้งาน Docker (เลือก 1 วิธี)

### 🔹 วิธีที่ 1: ใช้งานแบบง่าย (แนะนำ)
```powershell
.\docker_setup.bat
```

### 🔹 วิธีที่ 2: คำสั่ง Docker โดยตรง
```powershell
# Simple Setup (N8N + VICTOR-TTS เท่านั้น)
docker-compose -f docker-compose.simple.yml up -d

# Full Setup (ครบครัน + Database + Nginx)
docker-compose -f docker-compose.yml up -d
```

### 🔹 วิธีที่ 3: เมนูจัดการแบบโต้ตอบ
```powershell
python docker_management.py
```

---

## 🌐 URLs ที่ใช้งานได้

| Service | URL | คำอธิบาย |
|---------|-----|----------|
| **N8N Workflow** | http://localhost:5678 | สร้างและจัดการ Workflow |
| **VICTOR-TTS API** | http://localhost:6969 | API สำหรับเรียกใช้ TTS |
| **VICTOR-TTS Web** | http://localhost:7000 | หน้าเว็บทดสอบ |
| **API Docs** | http://localhost:6969/docs | เอกสาร API อัตโนมัติ |
| **Health Check** | http://localhost:6969/health | ตรวจสอบสถานะระบบ |

---

## 🤖 วิธีใช้งาน N8N กับ VICTOR-TTS

### 1. เปิด N8N
```
http://localhost:5678
```

### 2. สร้าง Webhook ใหม่
- เพิ่ม Node: **Webhook Trigger**
- ตั้งค่า Path: `victor-tts-webhook`
- Method: `POST`

### 3. เชื่อมต่อกับ VICTOR-TTS API
- เพิ่ม Node: **HTTP Request**
- URL: `http://victor-tts-api:6969/unified`
- Method: `POST`
- Body: JSON จาก Webhook

### 4. ตัวอย่าง JSON สำหรับทดสอบ
```json
{
  "text": "สวัสดีครับ ทดสอบระบบ TTS",
  "tts_voice": "th-TH-PremwadeeNeural",
  "rvc_model": "BoSunita",
  "output_path": "output.wav"
}
```

---

## 🔧 การจัดการระบบ

### ดูสถานะ
```powershell
docker-compose ps
```

### ดู Log
```powershell
docker-compose logs -f
```

### หยุดระบบ
```powershell
docker-compose down
```

### รีสตาร์ท
```powershell
docker-compose restart
```

---

## 📋 Workflow ที่พร้อมใช้งาน

ในโฟลเดอร์ `n8n_workflows/` มี Workflow ตัวอย่าง:
- `victor_tts_workflow.json` - Workflow สำหรับ VICTOR-TTS
- `webhook_examples.json` - ตัวอย่าง Webhook
- `error_handling.json` - การจัดการ Error

### การ Import Workflow
1. เปิด N8N → Settings → Import
2. เลือกไฟล์ JSON จาก `n8n_workflows/`
3. คลิก Import

---

## 🎯 ทดสอบระบบ

### 1. ทดสอบ API โดยตรง
```powershell
curl -X POST http://localhost:6969/unified -H "Content-Type: application/json" -d "{\"text\":\"สวัสดี\",\"tts_voice\":\"th-TH-PremwadeeNeural\"}"
```

### 2. ทดสอบผ่าน N8N Webhook
```powershell
curl -X POST http://localhost:5678/webhook/victor-tts-webhook -H "Content-Type: application/json" -d "{\"text\":\"ทดสอบ N8N\",\"tts_voice\":\"th-TH-PremwadeeNeural\"}"
```

---

## 🔍 การแก้ไขปัญหา

### ถ้าระบบไม่ทำงาน
1. ตรวจสอบ Docker ทำงาน: `docker --version`
2. ตรวจสอบ Container: `docker-compose ps`
3. ดู Log: `docker-compose logs`

### ถ้า RVC ไม่ทำงาน
1. ตรวจสอบ Model ใน `/logs/` folder
2. รัน: `python test_rvc_simple.py`
3. ใช้: `python fix_rvc.py` เพื่อแก้ไข

---

## 📚 เอกสารเพิ่มเติม

| เอกสาร | ไฟล์ |
|---------|------|
| Setup Docker ละเอียด | `docs/DOCKER_N8N_GUIDE.md` |
| การใช้งาน RVC | `docs/RVC_TEST_SUMMARY.md` |
| การแก้ไขปัญหา | `RVC_TROUBLESHOOTING.md` |

---

## 🎉 สรุป

✅ **ระบบพร้อมใช้งานแล้ว!**
- Docker และ N8N ติดตั้งครบถ้วน
- API ทำงานได้ปกติ
- มี Tools จัดการง่าย
- มี Workflow ตัวอย่าง

**เพียงแค่รัน:** `.\docker_setup.bat` แล้วเลือกโหมดที่ต้องการ!
