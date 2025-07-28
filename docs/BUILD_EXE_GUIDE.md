# 🚀 VICTOR-TTS UNIFIED - Build EXE Guide

## 🎯 **การสร้างไฟล์ .exe สำหรับ VICTOR-TTS UNIFIED**

### 📋 **ข้อกำหนดเบื้องต้น**

1. **Python 3.10+** ติดตั้งแล้ว
2. **Virtual Environment** พร้อมใช้งาน
3. **Dependencies** ทั้งหมดติดตั้งแล้ว
4. **PyInstaller** ติดตั้งแล้ว

### 🔧 **การติดตั้ง PyInstaller**

```bash
# เปิดใช้งาน virtual environment
env\Scripts\activate

# ติดตั้ง PyInstaller
pip install pyinstaller
```

## 🎯 **ตัวเลือกการสร้าง .exe**

### ✅ **ตัวเลือก 1: Full Version (รวม Models)**

**ไฟล์ที่ได้:** `VICTOR-TTS-UNIFIED.exe`
**ขนาด:** ~2-5 GB (ขึ้นอยู่กับจำนวน models)
**รวม:** ทุกอย่าง + RVC models

```bash
# ใช้ Batch Script
build_exe.bat

# หรือใช้ PowerShell Script
.\build_exe.ps1

# หรือใช้คำสั่งโดยตรง
pyinstaller --clean victor_tts.spec
```

### ✅ **ตัวเลือก 2: Simple Version (ไม่รวม Models)**

**ไฟล์ที่ได้:** `VICTOR-TTS-UNIFIED-SIMPLE.exe`
**ขนาด:** ~500MB-1GB
**รวม:** โปรแกรมหลัก (ไม่รวม models)

```bash
# ใช้ Batch Script
build_exe_simple.bat

# หรือใช้คำสั่งโดยตรง
pyinstaller --clean victor_tts_simple.spec
```

## 📁 **โครงสร้างไฟล์หลังสร้าง .exe**

### **Full Version:**
```
dist/
└── VICTOR-TTS-UNIFIED.exe
    ├── rvc/ (RVC system)
    ├── logs/ (RVC models)
    ├── voice_samples/ (Voice samples)
    ├── templates/ (Web templates)
    ├── config/ (Configuration)
    ├── assets/ (Assets)
    ├── ffmpeg.exe
    ├── ffprobe.exe
    └── [all dependencies]
```

### **Simple Version:**
```
dist/
└── VICTOR-TTS-UNIFIED-SIMPLE.exe
    ├── rvc/ (RVC system)
    ├── templates/ (Web templates)
    ├── config/ (Configuration)
    ├── assets/ (Assets)
    ├── ffmpeg.exe
    ├── ffprobe.exe
    └── [all dependencies]
    
logs/ (ต้องมีแยกต่างหาก)
└── [RVC models]
```

## 🚀 **วิธีการใช้งาน .exe**

### **1. Full Version**
```bash
# เปิดไฟล์ .exe
dist\VICTOR-TTS-UNIFIED.exe

# รอสักครู่ให้ระบบโหลด
# เปิดเว็บเบราว์เซอร์ไปที่ http://localhost:7000
```

### **2. Simple Version**
```bash
# ต้องมีโฟลเดอร์ logs พร้อม models
# คัดลอกโฟลเดอร์ logs ไปไว้ข้างไฟล์ .exe

# เปิดไฟล์ .exe
dist\VICTOR-TTS-UNIFIED-SIMPLE.exe

# รอสักครู่ให้ระบบโหลด
# เปิดเว็บเบราว์เซอร์ไปที่ http://localhost:7000
```

## ⚙️ **การปรับแต่ง .exe**

### **เพิ่ม Icon**
```python
# แก้ไขในไฟล์ .spec
exe = EXE(
    # ... other options ...
    icon='path/to/icon.ico',  # เพิ่มบรรทัดนี้
)
```

### **สร้าง .exe แบบไม่มี Console**
```python
# แก้ไขในไฟล์ .spec
exe = EXE(
    # ... other options ...
    console=False,  # เปลี่ยนจาก True เป็น False
)
```

### **เพิ่มไฟล์เพิ่มเติม**
```python
# แก้ไขในไฟล์ .spec
datas = [
    # ... existing files ...
    ('path/to/additional/file', 'destination/in/exe'),
]
```

## 🔍 **การแก้ไขปัญหา**

### **❌ ปัญหา: ModuleNotFoundError**
```bash
# เพิ่ม module ใน hiddenimports ในไฟล์ .spec
hiddenimports = [
    # ... existing imports ...
    'missing_module_name',
]
```

### **❌ ปัญหา: FileNotFoundError**
```bash
# เพิ่มไฟล์ใน datas ในไฟล์ .spec
datas = [
    # ... existing files ...
    ('path/to/missing/file', 'destination'),
]
```

### **❌ ปัญหา: .exe ใหญ่เกินไป**
```bash
# ใช้ Simple Version แทน
# หรือเพิ่ม excludes ในไฟล์ .spec
excludes = [
    # ... existing excludes ...
    'unused_module',
    'unused_package',
]
```

## 📊 **ขนาดไฟล์โดยประมาณ**

| Version | ขนาด | หมายเหตุ |
|---------|------|----------|
| Simple | 500MB-1GB | ไม่รวม models |
| Full (16 models) | 2-5GB | รวม models ทั้งหมด |
| Full (5 models) | 1-2GB | รวม models บางส่วน |

## 🎯 **คำแนะนำ**

### **สำหรับการแจกจ่าย:**
- ใช้ **Simple Version** เพื่อลดขนาด
- แจกจ่าย models แยกต่างหาก
- สร้าง installer script

### **สำหรับการใช้งานส่วนตัว:**
- ใช้ **Full Version** เพื่อความสะดวก
- รวมทุกอย่างในไฟล์เดียว

### **สำหรับการพัฒนา:**
- ใช้ **Simple Version** เพื่อความรวดเร็ว
- แยก models ออกมาเพื่อการทดสอบ

## 🎉 **ข้อสรุป**

**การสร้าง .exe สำเร็จแล้ว!**

- ✅ **Full Version**: พร้อมใช้งานทุกอย่าง
- ✅ **Simple Version**: ขนาดเล็ก ใช้งานง่าย
- ✅ **Launch Scripts**: สร้าง .exe ได้ง่าย
- ✅ **Documentation**: คู่มือครบถ้วน

**เลือกใช้ตามความต้องการครับ!** 🚀✨ 