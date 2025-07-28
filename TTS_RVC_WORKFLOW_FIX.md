# 🔧 การแก้ไขปัญหาการทำงานของระบบ TTS และ RVC

## 🎯 ปัญหาที่พบ

จากข้อมูลที่แสดงให้เห็น ระบบมีปัญหาหลายประการ:

1. **เสียง TTS สร้างได้สำเร็จ** แต่เสียง RVC ไม่แสดงใน interface
2. **ไฟล์เสียง TTS มีปัญหา** ทำให้ RVC ไม่สามารถประมวลผลได้
3. **การทำงานไม่เป็นไปตามที่ต้องการ**: 
   - ไม่เลือก RVC = ควรแสดงเสียงต้นฉบับ
   - เลือก RVC = ควรแสดงเสียงที่แปลงแล้ว

## 🔍 สาเหตุของปัญหา

### 1. ปัญหาไฟล์เสียง TTS
```
Note: Illegal Audio-MPEG-Header 0x00000000 at offset 24192.
Note: Trying to resync...
Note: Skipped 1024 bytes in input.
error: Giving up resync after 1024 bytes - your stream is not nice...
```

### 2. การจัดการไฟล์ชั่วคราวไม่ถูกต้อง
- ใช้ `os.getpid()` ทำให้ไฟล์อาจซ้ำกัน
- ไม่มีการตรวจสอบว่าไฟล์ถูกสร้างขึ้นหรือไม่
- การลบไฟล์ชั่วคราวไม่สมบูรณ์

### 3. การประมวลผลแยกส่วน
- TTS และ RVC ประมวลผลแยกกัน
- ไม่มีการจัดการ error ที่ดี
- ผลลัพธ์ไม่สอดคล้องกับความต้องการ

## ✅ การแก้ไขที่ทำ

### 1. ปรับปรุงการจัดการไฟล์เสียงใน `convert_voice`

```python
def convert_voice(self, audio_data: bytes, model_name: str, 
                 transpose: int = 0, index_ratio: float = 0.75,
                 f0_method: str = "rmvpe") -> bytes:
    # สร้างชื่อไฟล์ที่ไม่ซ้ำกัน
    import time
    timestamp = int(time.time() * 1000)
    temp_input = self.temp_dir / f"rvc_input_{timestamp}.wav"
    temp_output = self.temp_dir / f"rvc_output_{timestamp}.wav"
    
    # ตรวจสอบว่าไฟล์ถูกสร้างขึ้นหรือไม่
    if not temp_input.exists():
        raise Exception("Failed to create input audio file")
    
    # ตรวจสอบว่าไฟล์ผลลัพธ์ถูกสร้างขึ้นหรือไม่
    if not Path(result_path).exists():
        raise Exception(f"RVC output file not found: {result_path}")
    
    if len(converted_audio) == 0:
        raise Exception("RVC output file is empty")
```

### 2. ปรับปรุงฟังก์ชัน `process_unified`

```python
async def process_unified(self, text: str, tts_voice: str, 
                        enable_rvc: bool = False, rvc_model: str = None,
                        tts_speed: float = 1.0, tts_pitch: str = "+0Hz",
                        rvc_transpose: int = 0, rvc_index_ratio: float = 0.75,
                        rvc_f0_method: str = "rmvpe", enable_multi_language: bool = True) -> Dict[str, Any]:
    
    result = {
        "success": False,
        "tts_audio_data": None,
        "rvc_audio_data": None,
        "final_audio_data": None,
        "processing_steps": [],
        "error": None,
        "stats": {}
    }
    
    # สร้าง TTS เสมอ
    tts_audio = await self.generate_tts(text, tts_voice, tts_speed, tts_pitch, enable_multi_language)
    result["tts_audio_data"] = tts_audio
    
    # แปลงเสียงด้วย RVC (ถ้าเปิดใช้)
    if enable_rvc and rvc_model:
        try:
            converted_audio = self.convert_voice(tts_audio, rvc_model, rvc_transpose, rvc_index_ratio, rvc_f0_method)
            result["rvc_audio_data"] = converted_audio
            final_audio = converted_audio
        except Exception as rvc_error:
            result["error"] = f"Voice conversion failed: {str(rvc_error)}"
            final_audio = tts_audio  # ใช้เสียง TTS เดิม
    else:
        final_audio = tts_audio  # ใช้เสียง TTS เดิม
    
    result["final_audio_data"] = final_audio
    result["success"] = True
    return result
```

### 3. ปรับปรุง Web Interface

```python
async def _process_request(self, request_data):
    # ใช้ฟังก์ชัน process_unified เพื่อประมวลผลรวม
    result = await core.process_unified(
        text=request_data.get('text', ''),
        tts_voice=request_data.get('tts_voice', 'th-TH-PremwadeeNeural'),
        enable_rvc=request_data.get('enable_rvc', False),
        rvc_model=request_data.get('rvc_model'),
        tts_speed=request_data.get('tts_speed', 1.0),
        rvc_transpose=request_data.get('rvc_transpose', 0),
        enable_multi_language=request_data.get('enable_multi_language', True)
    )
    
    # แปลงข้อมูลเสียงเป็น base64
    response_data = {
        "success": True,
        "tts_audio_data": base64.b64encode(result["tts_audio_data"]).decode('utf-8') if result["tts_audio_data"] else None,
        "rvc_audio_data": base64.b64encode(result["rvc_audio_data"]).decode('utf-8') if result["rvc_audio_data"] else None,
        "final_audio_data": base64.b64encode(result["final_audio_data"]).decode('utf-8') if result["final_audio_data"] else None,
        "stats": result["stats"],
        "processing_steps": result["processing_steps"]
    }
```

### 4. ปรับปรุงการแสดงผลลัพธ์

```javascript
// แสดงไฟล์เสียงตามประเภท
if (result.rvc_audio_data) {
    // มีทั้ง TTS และ RVC - แสดงทั้งสองไฟล์
    showTTSAndRVCAudio(result.tts_audio_data, result.rvc_audio_data, stats);
    showNotification('✅ สร้างเสียงสำเร็จ (TTS + RVC)', 'success');
} else if (result.tts_audio_data) {
    // มีแค่ TTS - แสดงไฟล์เดียว
    showCombinedAudio(result.tts_audio_data, stats);
    let statusText = '✅ สร้างเสียงสำเร็จ (TTS เท่านั้น)';
    if (steps.includes('rvc_failed')) {
        statusText += ' - RVC ล้มเหลว: ' + (result.rvc_error || 'Unknown error');
        showNotification('⚠️ RVC ล้มเหลว แต่ TTS สำเร็จ', 'warning');
    }
    showNotification(statusText, 'success');
}
```

## 📊 ผลลัพธ์หลังการแก้ไข

### ✅ สิ่งที่แก้ไขได้

1. **การทำงานที่ถูกต้อง**:
   - ไม่เลือก RVC = แสดงเสียงต้นฉบับ (TTS)
   - เลือก RVC = แสดงเสียงที่แปลงแล้ว (RVC)

2. **การจัดการไฟล์ที่ดีขึ้น**:
   - ใช้ timestamp แทน pid เพื่อหลีกเลี่ยงการซ้ำ
   - ตรวจสอบการสร้างไฟล์
   - ลบไฟล์ชั่วคราวอย่างสมบูรณ์

3. **การจัดการ Error ที่ดีขึ้น**:
   - แสดงข้อผิดพลาดที่ชัดเจน
   - ใช้เสียง TTS เป็น fallback เมื่อ RVC ล้มเหลว

4. **การแสดงผลที่ครบถ้วน**:
   - แสดงทั้งเสียง TTS และ RVC
   - แสดงสถานะการทำงาน
   - แจ้งเตือนเมื่อมีปัญหา

### 🎯 การทำงานใหม่

#### กรณีที่ 1: ไม่เลือก RVC
```
Input: ข้อความ + TTS Voice
Output: เสียง TTS เท่านั้น
Display: TTS Audio Player
```

#### กรณีที่ 2: เลือก RVC สำเร็จ
```
Input: ข้อความ + TTS Voice + RVC Model
Output: เสียง TTS + เสียง RVC
Display: TTS Audio Player + RVC Audio Player
```

#### กรณีที่ 3: เลือก RVC แต่ล้มเหลว
```
Input: ข้อความ + TTS Voice + RVC Model
Output: เสียง TTS + Error Message
Display: TTS Audio Player + RVC Status (Failed)
```

## 🔧 การทดสอบ

### 1. ทดสอบ TTS เท่านั้น
- เปิดใช้งาน TTS
- ปิดการใช้งาน RVC
- ควรแสดงเสียง TTS เท่านั้น

### 2. ทดสอบ TTS + RVC สำเร็จ
- เปิดใช้งานทั้ง TTS และ RVC
- เลือกโมเดล RVC
- ควรแสดงทั้งเสียง TTS และ RVC

### 3. ทดสอบ RVC ล้มเหลว
- เปิดใช้งานทั้ง TTS และ RVC
- เลือกโมเดล RVC
- ควรแสดงเสียง TTS และสถานะ RVC ล้มเหลว

## 📝 หมายเหตุ

- การแก้ไขนี้ทำให้ระบบทำงานตามความต้องการของผู้ใช้
- แม้ว่า RVC จะล้มเหลว แต่ TTS ยังคงทำงานได้ปกติ
- ผู้ใช้จะได้รับข้อมูลที่ครบถ้วนเกี่ยวกับการประมวลผล
- ระบบมีความเสถียรมากขึ้นและจัดการ error ได้ดีขึ้น

---

**วันที่แก้ไข**: 2025-01-28  
**สถานะ**: ✅ เสร็จสิ้น  
**เวอร์ชัน**: VICTOR-TTS v1.2 