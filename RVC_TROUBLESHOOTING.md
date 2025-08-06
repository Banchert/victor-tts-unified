# 🔧 RVC Troubleshooting Guide

## ปัญหาที่พบบ่อยและวิธีแก้ไข

### 🚨 RVC ไม่ทำงาน

#### วิธีการตรวจสอบ:
```bash
# รันสคริปต์ทดสอบ
python test_rvc_simple.py
# หรือ
test_rvc.bat

# รันสคริปต์แก้ไขปัญหา
python fix_rvc.py
# หรือ
fix_rvc.bat
```

#### สาเหตุที่พบบ่อย:

1. **ไม่มี Dependencies ที่จำเป็น**
   ```bash
   pip install torch torchvision torchaudio
   pip install soundfile librosa faiss-cpu torchcrepe
   ```

2. **ไม่มีโมเดล RVC**
   - ตรวจสอบว่าโฟลเดอร์ `logs/` มีโมเดล RVC หรือไม่
   - แต่ละโมเดลต้องมีไฟล์ `.pth` และ `.index`

3. **ปัญหา CUDA/GPU**
   ```python
   import torch
   print(torch.cuda.is_available())  # ควรแสดง True ถ้าใช้ GPU
   ```

4. **ปัญหาเส้นทางไฟล์**
   - ตรวจสอบว่าโครงสร้างไฟล์ถูกต้อง:
   ```
   victor-tts-unified/
   ├── rvc/
   ├── logs/
   ├── rvc_api.py
   └── tts_rvc_core.py
   ```

### 🛠️ การแก้ไขปัญหาขั้นสูง

#### แก้ไข Import Error:
```python
# เพิ่ม path ถ้าจำเป็น
import sys
sys.path.append('path/to/victor-tts-unified')
```

#### แก้ไข CUDA Memory Error:
```python
# ลด GPU memory usage
import torch
torch.cuda.empty_cache()
```

#### แก้ไข Model Loading Error:
```python
# ตรวจสอบไฟล์โมเดล
import os
models_dir = "logs"
for model in os.listdir(models_dir):
    model_path = f"{models_dir}/{model}"
    pth_files = [f for f in os.listdir(model_path) if f.endswith('.pth')]
    index_files = [f for f in os.listdir(model_path) if f.endswith('.index')]
    print(f"{model}: {len(pth_files)} pth, {len(index_files)} index")
```

### 🎯 ขั้นตอนการตรวจสอบแบบละเอียด

1. **ตรวจสอบ Python Environment**
   ```bash
   python --version
   pip list | grep torch
   pip list | grep soundfile
   ```

2. **ตรวจสอบโมเดล RVC**
   ```bash
   ls -la logs/
   # หรือใน Windows
   dir logs\
   ```

3. **ทดสอบการ Import**
   ```python
   from rvc_api import RVCConverter
   rvc = RVCConverter()
   print(rvc.get_available_models())
   ```

4. **ทดสอบการแปลงเสียง**
   ```python
   # ใช้โมเดลแรกที่มี
   models = rvc.get_available_models()
   if models:
       print(f"Testing with model: {models[0]}")
   ```

### 📞 หากยังมีปัญหา

1. รันสคริปต์ `fix_rvc.py` เพื่อดูรายละเอียดปัญหา
2. ตรวจสอบ log ข้อผิดพลาดในคอนโซล
3. ตรวจสอบว่าโมเดล RVC ถูกต้องและครบถ้วน
4. ลองใช้ CPU mode แทน GPU mode

### 🚀 การปรับปรุงประสิทธิภาพ

```python
# ใน tts_rvc_core.py หรือ rvc_api.py
# เพิ่มการตั้งค่าเหล่านี้:

# สำหรับ GPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# สำหรับ Memory Management
torch.cuda.empty_cache()  # เคลียร์ memory หลังใช้งาน

# สำหรับ Batch Processing
batch_size = 1  # ลดขนาด batch ถ้า memory ไม่พอ
```

### ✅ หลังแก้ไขแล้ว

1. รีสตาร์ทแอปพลิเคชัน
2. ทดสอบด้วย `test_rvc_simple.py`
3. ลองใช้งาน RVC ผ่าน Web Interface

---

*อัปเดตล่าสุด: กุมภาพันธ์ 2024*
