# 🚀 VICTOR-TTS Start Guide

## 📋 คู่มือการใช้งาน start.bat

### 🎯 ภาพรวม
`start.bat` เป็นตัวเรียกใช้งานหลักสำหรับระบบ VICTOR-TTS ที่รวมทุกฟังก์ชันไว้ในไฟล์เดียว

### ✅ ความสามารถ
- 🎤 **TTS (Text-to-Speech)** - แปลงข้อความเป็นเสียงพูด
- 🎵 **RVC (Voice Conversion)** - แปลงเสียงด้วย AI
- 🌍 **Multi-language Support** - รองรับหลายภาษา
- 🖥️ **GPU/CPU Support** - ใช้งานได้ทั้ง GPU และ CPU
- 🌐 **Web Interface** - หน้าเว็บใช้งานง่าย
- 📡 **API Server** - สำหรับ integration กับ N8N

### 🚀 วิธีใช้งาน

#### 1. เริ่มต้นใช้งาน
```batch
start.bat
```

#### 2. เมนูหลัก
```
[1] 🌐 Web Interface (Port 7000) - แนะนำ!
[2] 🖥️  Web Interface + เลือก GPU
[3] 📡 API Server (Port 6969)
[4] 🔄 Web + API (ทั้งสองโหมด)
```

#### 3. เมนูทดสอบ
```
[5] 🔍 ทดสอบระบบทั้งหมด
[6] 🎤 ทดสอบ RVC MP3 Fix
[7] 📋 ดูโมเดล RVC ที่มี
[8] 🌍 ทดสอบหลายภาษา
```

#### 4. ตัวเลือกขั้นสูง
```
[9] 📦 ติดตั้ง Dependencies
[10] 🏗️ สร้างไฟล์ EXE
```

### 📖 รายละเอียดแต่ละตัวเลือก

#### ตัวเลือก 1: Web Interface (แนะนำ)
- **URL**: http://localhost:7000
- **การใช้งาน**: เปิดเว็บบราวเซอร์อัตโนมัติ
- **ฟีเจอร์**: TTS + RVC ครบถ้วน
- **Device**: ตรวจจับ GPU/CPU อัตโนมัติ

#### ตัวเลือก 2: Web Interface + GPU
- เลือก GPU ที่ต้องการใช้ (0-3)
- หรือเลือก C สำหรับ CPU Only
- เหมาะสำหรับผู้ที่มีหลาย GPU

#### ตัวเลือก 3: API Server
- **API URL**: http://localhost:6969
- **API Docs**: http://localhost:6969/docs
- เหมาะสำหรับ integration กับ N8N หรือระบบอื่นๆ

#### ตัวเลือก 4: Web + API
- เปิดทั้ง Web Interface และ API Server พร้อมกัน
- ใช้สำหรับการพัฒนาหรือใช้งานเต็มรูปแบบ

### 🧪 การทดสอบระบบ

#### ทดสอบ RVC Status
```batch
python test_rvc_status.py
```

#### ทดสอบ MP3 Conversion
```batch
python test_rvc_mp3_fix.py
```

### 🛠️ แก้ปัญหาเบื้องต้น

#### ปัญหา: RVC ไม่ทำงาน
```batch
# เลือกตัวเลือก 9 เพื่อติดตั้ง dependencies
# หรือรันคำสั่ง:
python -m pip install -r requirements.txt
```

#### ปัญหา: ไม่พบ Python
- ตรวจสอบว่าติดตั้ง Python 3.10+ แล้ว
- เพิ่ม Python ใน PATH

#### ปัญหา: Port ถูกใช้งานอยู่
- ปิดโปรแกรมที่ใช้ port 7000 หรือ 6969
- หรือแก้ไข port ใน web_interface.py

### 📋 โมเดล RVC ที่มี
รันตัวเลือก 7 เพื่อดูรายชื่อโมเดลทั้งหมด (ปัจจุบันมี 16 โมเดล)

### 💡 Tips
- ใช้ตัวเลือก 1 สำหรับการใช้งานทั่วไป
- ใช้ตัวเลือก 3 สำหรับ N8N integration
- กด Ctrl+C เพื่อหยุดการทำงาน
- ดู logs ใน console เมื่อมีปัญหา

### 🌟 Features
- ✅ รองรับภาษาไทย/อังกฤษ และภาษาอื่นๆ
- ✅ แปลงเสียงด้วย RVC models
- ✅ ประมวลผลด้วย GPU (ถ้ามี)
- ✅ Web UI ใช้งานง่าย
- ✅ API สำหรับ automation

### 📞 ติดต่อ
หากพบปัญหาหรือต้องการความช่วยเหลือ ติดต่อผู้พัฒนา VICTOR 