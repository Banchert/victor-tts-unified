# 📁 ระบบการจัดการโมเดลเสียง (Model Management System)

## 🎯 ภาพรวมระบบ

ระบบการจัดการโมเดลเสียงของ VICTOR-TTS ประกอบด้วย 2 ส่วนหลัก:

### 1. **โมเดลระบบ (Core Models)**
- **ตำแหน่ง**: โฟลเดอร์ `logs/`
- **ประเภท**: โมเดล RVC ที่ติดตั้งมาพร้อมระบบ
- **จำนวน**: 16 โมเดล
- **สถานะ**: พร้อมใช้งานทันที

### 2. **โมเดลที่อัปโหลด (Uploaded Models)**
- **ตำแหน่ง**: โฟลเดอร์ `voice_models/`
- **ประเภท**: โมเดลที่ผู้ใช้อัปโหลดเพิ่มเติม
- **สถานะ**: ต้องอัปโหลดผ่านหน้าเว็บ

## 📂 โครงสร้างโฟลเดอร์

```
TTS FOR N8N/
├── logs/                          # โมเดลระบบ (16 โมเดล)
│   ├── al_bundy/
│   │   └── albundy.pth
│   ├── BoSunita/
│   │   └── BoSunita.pth
│   ├── boy_peacemaker/
│   │   └── boy_peacemaker.pth
│   ├── ChalermpolMalakham/
│   │   └── ChalermpolMalakham.pth
│   ├── DangHMD2010v2New/
│   │   └── DangHMD2010v2New.pth
│   ├── illslick/
│   │   └── illslick.pth
│   ├── JO/
│   │   └── JO_800e_36800s.pth
│   ├── knomjean/
│   │   └── knomjean.pth
│   ├── Law_By_Mike_e160_s4800/
│   │   └── Law_By_Mike.pth
│   ├── Michael/
│   │   └── MichaelRosen.pth
│   ├── MonkanKaenkoon/
│   │   └── MonkanKaenkoon.pth
│   ├── MusicV1Carti_300_Epochs/
│   │   └── MusicV1Carti_300_Epochs.pth
│   ├── pang/
│   │   └── pang.pth
│   ├── STS73/
│   │   └── STS73.pth
│   ├── VANXAI/
│   │   └── VANXAI.pth
│   └── YingyongYodbuangarm/
│       └── YingyongYodbuangarm.pth
│
└── voice_models/                  # โมเดลที่อัปโหลด
    ├── cache/                     # แคชโมเดล
    ├── profiles/                  # โปรไฟล์โมเดล
    └── [ไฟล์โมเดลที่อัปโหลด]      # .pth, .pt, .ckpt
```

## 🔧 ฟีเจอร์การจัดการโมเดล

### 1. **อัปโหลดโมเดลใหม่**
- **รองรับไฟล์**: `.pth`, `.pt`, `.ckpt`
- **ขนาดสูงสุด**: 500MB
- **ตำแหน่งบันทึก**: `voice_models/`
- **การตรวจสอบ**: ตรวจสอบนามสกุลไฟล์และขนาด

### 2. **แสดงรายการโมเดล**
- **โมเดลระบบ**: แสดงจาก `logs/`
- **โมเดลอัปโหลด**: แสดงจาก `voice_models/`
- **ข้อมูลแสดง**: ชื่อ, ขนาด, วันที่อัปโหลด, ประเภท

### 3. **ค้นหาโมเดล**
- ค้นหาด้วยชื่อโมเดล
- กรองผลลัพธ์แบบ real-time

### 4. **ทดสอบโมเดล**
- ทดสอบโมเดลที่อัปโหลด
- ตรวจสอบความสมบูรณ์ของไฟล์

### 5. **ลบโมเดล**
- ลบโมเดลที่อัปโหลด
- ยืนยันการลบ

## 💻 การทำงานของระบบ

### **Frontend (JavaScript)**
```javascript
// การอัปโหลดไฟล์
function uploadModel(file) {
    const formData = new FormData();
    formData.append('model', file);
    
    fetch('/upload_model', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('✅ อัปโหลดสำเร็จ', 'success');
            refreshModelList();
        }
    });
}
```

### **Backend (Python)**
```python
# การรับไฟล์อัปโหลด
elif self.path == '/upload_model':
    form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD': 'POST'}
    )
    
    if 'model' in form:
        fileitem = form['model']
        # ตรวจสอบนามสกุลไฟล์
        allowed_extensions = ['.pth', '.pt', '.ckpt']
        file_ext = Path(fileitem.filename).suffix.lower()
        
        if file_ext in allowed_extensions:
            # สร้างโฟลเดอร์และบันทึกไฟล์
            models_dir = Path("voice_models")
            models_dir.mkdir(exist_ok=True)
            
            model_path = models_dir / fileitem.filename
            with open(model_path, 'wb') as f:
                shutil.copyfileobj(fileitem.file, f)
```

## 📊 การดึงข้อมูลโมเดล

### **จาก Core System**
```python
# ดึงโมเดลจาก logs/
core_models = self.server.web_interface.core.get_available_rvc_models()
```

### **จาก Uploaded Models**
```python
# ดึงโมเดลจาก voice_models/
models_dir = Path("voice_models")
uploaded_models = []

if models_dir.exists():
    for model_file in models_dir.glob("*.pth"):
        uploaded_models.append({
            "name": model_file.name,
            "size": f"{stat.st_size / (1024*1024):.1f} MB",
            "updated": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "type": "uploaded"
        })
```

## 🎨 UI/UX Features

### **Drag & Drop**
- ลากวางไฟล์โมเดลได้
- แสดงสถานะการลากวาง

### **Progress Bar**
- แสดงความคืบหน้าการอัปโหลด
- แสดงเปอร์เซ็นต์

### **Notifications**
- แจ้งเตือนผลการอัปโหลด
- แจ้งเตือนข้อผิดพลาด

### **Model List**
- แสดงรายการโมเดลแบบตาราง
- ปุ่มทดสอบและลบโมเดล
- ข้อมูลขนาดและวันที่

## 🔒 ความปลอดภัย

### **การตรวจสอบไฟล์**
- ตรวจสอบนามสกุลไฟล์
- ตรวจสอบขนาดไฟล์
- ป้องกันไฟล์อันตราย

### **การจัดการข้อผิดพลาด**
- จัดการไฟล์เสียหาย
- แจ้งเตือนข้อผิดพลาด
- Rollback เมื่อเกิดปัญหา

## 📈 สถิติระบบ

### **โมเดลระบบ**
- **จำนวน**: 16 โมเดล
- **ประเภท**: RVC Models
- **สถานะ**: พร้อมใช้งาน

### **โมเดลอัปโหลด**
- **จำนวน**: ตามการอัปโหลด
- **ประเภท**: .pth, .pt, .ckpt
- **สถานะ**: ต้องอัปโหลดก่อนใช้งาน

## 🚀 การใช้งาน

1. **เข้าเว็บอินเตอร์เฟซ**: `http://localhost:7002`
2. **ไปที่ส่วน "จัดการโมเดลเสียง"**
3. **คลิก "อัปโหลดโมเดลเสียงใหม่"**
4. **เลือกไฟล์โมเดล (.pth, .pt, .ckpt)**
5. **รอการอัปโหลดเสร็จ**
6. **โมเดลจะปรากฏในรายการ**

## ⚠️ ข้อจำกัด

- **ขนาดไฟล์สูงสุด**: 500MB
- **นามสกุลที่รองรับ**: .pth, .pt, .ckpt
- **ตำแหน่งบันทึก**: โฟลเดอร์ `voice_models/`
- **การใช้งาน**: ต้องรีสตาร์ทระบบหลังอัปโหลด

## 🔄 การอัปเดตระบบ

เมื่ออัปโหลดโมเดลใหม่:
1. ไฟล์จะถูกบันทึกใน `voice_models/`
2. รายการโมเดลจะอัปเดตอัตโนมัติ
3. สามารถใช้งานโมเดลใหม่ได้ทันที
4. ข้อมูลจะถูกเก็บไว้ถาวร 