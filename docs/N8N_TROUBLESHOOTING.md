# 🔧 N8N Troubleshooting Guide - ปัญหาการสร้างเสียงได้น้อย

## 🚨 ปัญหาที่พบบ่อย

### 1. **N8N สร้างเสียงได้น้อย ไม่ได้หมด**

#### **สาเหตุที่เป็นไปได้:**

1. **ขีดจำกัดข้อความของ Edge TTS**
   - Edge TTS มีขีดจำกัดข้อความประมาณ 10,000 ตัวอักษร
   - ข้อความยาวเกินไปจะทำให้เกิดข้อผิดพลาด

2. **Timeout ใน N8N**
   - การประมวลผลข้อความยาวใช้เวลานาน
   - N8N timeout ก่อนที่จะเสร็จสิ้น

3. **ขนาด Response ใหญ่เกินไป**
   - Audio Base64 มีขนาดใหญ่
   - N8N ไม่สามารถรับข้อมูลได้

4. **การตั้งค่า HTTP Request ไม่ถูกต้อง**
   - URL ไม่ถูกต้อง
   - JSON Body ไม่ตรงกับ API Schema

---

## 🔍 การวินิจฉัยปัญหา

### ขั้นตอนที่ 1: ตรวจสอบข้อความที่ส่ง

```bash
# ทดสอบด้วย curl
curl -X POST http://localhost:6969/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "ข้อความทดสอบของคุณ",
    "voice": "th-TH-PremwadeeNeural",
    "speed": 1.0
  }'
```

### ขั้นตอนที่ 2: ตรวจสอบความยาวข้อความ

```javascript
// ใน N8N Code node
const text = $json.text;
console.log(`ความยาวข้อความ: ${text.length} ตัวอักษร`);

if (text.length > 8000) {
  console.log("⚠️ ข้อความยาวเกินไป แนะนำให้แบ่งเป็นส่วนๆ");
}
```

### ขั้นตอนที่ 3: ตรวจสอบ Response

```javascript
// ใน N8N Code node หลังจาก HTTP Request
if ($json.success) {
  console.log(`✅ สำเร็จ - ขนาดเสียง: ${$json.data.audio_size} bytes`);
  console.log(`ความยาวข้อความ: ${$json.data.text_length} ตัวอักษร`);
} else {
  console.log(`❌ ล้มเหลว: ${$json.message}`);
}
```

---

## 🛠️ วิธีแก้ไข

### วิธีที่ 1: แบ่งข้อความเป็นส่วนๆ

#### **ใน N8N Workflow:**

```
Text Input → Split Text → HTTP Request (Loop) → Merge Audio
```

#### **Code Node สำหรับแบ่งข้อความ:**

```javascript
// แบ่งข้อความเป็นส่วนๆ
const text = $json.text;
const maxLength = 5000; // ขีดจำกัดต่อส่วน

if (text.length <= maxLength) {
  // ข้อความสั้น ใช้ส่วนเดียว
  return [{ text: text }];
} else {
  // แบ่งข้อความ
  const chunks = [];
  let currentChunk = "";
  
  // แบ่งตามประโยค
  const sentences = text.split(/[.!?]+/).filter(s => s.trim());
  
  for (const sentence of sentences) {
    if ((currentChunk + sentence).length <= maxLength) {
      currentChunk += sentence + ". ";
    } else {
      if (currentChunk) {
        chunks.push({ text: currentChunk.trim() });
      }
      currentChunk = sentence + ". ";
    }
  }
  
  if (currentChunk) {
    chunks.push({ text: currentChunk.trim() });
  }
  
  return chunks;
}
```

#### **HTTP Request Node:**

```json
{
  "text": "{{ $json.text }}",
  "voice": "th-TH-PremwadeeNeural",
  "speed": 1.0
}
```

#### **Code Node สำหรับรวมเสียง:**

```javascript
// รวมเสียงจากหลายส่วน
const audioChunks = $input.all();
let combinedAudio = "";

for (const chunk of audioChunks) {
  if (chunk.json.success && chunk.json.data.audio_base64) {
    combinedAudio += chunk.json.data.audio_base64;
  }
}

return {
  success: true,
  audio_base64: combinedAudio,
  total_chunks: audioChunks.length
};
```

### วิธีที่ 2: เพิ่ม Timeout ใน N8N

#### **การตั้งค่า HTTP Request Node:**

1. เปิด HTTP Request Node
2. ไปที่ **Settings** tab
3. เพิ่ม **Timeout** เป็น 300000 (5 นาที)
4. เพิ่ม **Response Format** เป็น **JSON**

### วิธีที่ 3: ใช้ Unified Endpoint

#### **แทนที่ TTS อย่างเดียวด้วย Unified:**

```json
{
  "text": "{{ $json.text }}",
  "tts_voice": "th-TH-PremwadeeNeural",
  "speed": 1.0,
  "enable_rvc": false
}
```

**URL:** `http://host.docker.internal:6969/unified`

### วิธีที่ 4: ใช้ Full TTS Endpoint

#### **สำหรับข้อความยาว:**

```json
{
  "text": "{{ $json.text }}",
  "tts_voice": "th-TH-PremwadeeNeural",
  "tts_speed": 1.0,
  "enable_rvc": false
}
```

**URL:** `http://host.docker.internal:6969/full_tts`

---

## ⚙️ การตั้งค่าที่แนะนำ

### 1. **การตั้งค่า HTTP Request Node**

```
Method: POST
URL: http://host.docker.internal:6969/unified
Headers:
  Content-Type: application/json
Timeout: 300000 (5 นาที)
Response Format: JSON
```

### 2. **การตั้งค่า JSON Body**

```json
{
  "text": "{{ $json.text }}",
  "tts_voice": "th-TH-PremwadeeNeural",
  "speed": 1.0,
  "enable_rvc": false
}
```

### 3. **การตั้งค่า Error Handling**

```javascript
// ใน Code Node หลัง HTTP Request
try {
  if ($json.success) {
    return {
      success: true,
      audio: $json.data.audio_base64,
      text_length: $json.data.text_length,
      processing_time: $json.processing_time
    };
  } else {
    throw new Error($json.message || "Unknown error");
  }
} catch (error) {
  return {
    success: false,
    error: error.message,
    timestamp: new Date().toISOString()
  };
}
```

---

## 📊 การตรวจสอบประสิทธิภาพ

### 1. **ทดสอบด้วยสคริปต์**

```bash
# รันสคริปต์ทดสอบ
python test_text_limits.py
```

### 2. **ตรวจสอบ Log**

```bash
# ดู log ของ TTS Server
tail -f logs/victor_tts.log
```

### 3. **ตรวจสอบ Memory Usage**

```bash
# ตรวจสอบการใช้ memory
nvidia-smi  # สำหรับ GPU
htop        # สำหรับ CPU
```

---

## 🎯 ตัวอย่าง Workflow ที่แก้ไขแล้ว

### Workflow 1: แบ่งข้อความอัตโนมัติ

```
Webhook → Code (Split Text) → HTTP Request (Loop) → Code (Merge) → Save File
```

### Workflow 2: ใช้ Unified Endpoint

```
Webhook → HTTP Request (Unified) → Code (Process Response) → Save File
```

### Workflow 3: Error Handling แบบสมบูรณ์

```
Webhook → Code (Validate) → HTTP Request → Code (Handle Response) → Save File
```

---

## 🔧 การตั้งค่าเพิ่มเติม

### 1. **เพิ่ม Memory Limit**

```bash
# ใน docker-compose.yml
environment:
  - VICTOR_TTS_MAX_TEXT_LENGTH=20000
  - VICTOR_TTS_CHUNK_SIZE=5000
```

### 2. **เพิ่ม Timeout**

```bash
# ใน N8N HTTP Request
Timeout: 600000  # 10 นาที
```

### 3. **เพิ่ม Retry Logic**

```javascript
// ใน Code Node
const maxRetries = 3;
let retryCount = 0;

while (retryCount < maxRetries) {
  try {
    // HTTP Request logic
    break;
  } catch (error) {
    retryCount++;
    if (retryCount >= maxRetries) {
      throw error;
    }
    // Wait before retry
    await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
  }
}
```

---

## 📞 การติดต่อและสนับสนุน

หากยังมีปัญหา:

1. **ตรวจสอบ Log:** `tail -f logs/victor_tts.log`
2. **ทดสอบ API:** `python test_text_limits.py`
3. **ตรวจสอบ Network:** `curl http://localhost:6969/health`
4. **ตรวจสอบ Config:** `cat config/unified_config.toml`

---

**🎉 ขอให้การแก้ไขปัญหาสำเร็จ!** 