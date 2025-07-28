# 🐳 VICTOR-TTS Docker & N8N Integration Guide

## 📋 Overview
คู่มือการใช้งาน VICTOR-TTS ร่วมกับ Docker และ N8N สำหรับการสร้าง workflow automation

## 🚀 Quick Start

### 1. การติดตั้ง Docker
```bash
# Windows
# ดาวน์โหลดและติดตั้ง Docker Desktop จาก https://www.docker.com/products/docker-desktop

# Linux
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. การเริ่มต้นใช้งาน
```bash
# เริ่มต้นแบบง่าย (แนะนำสำหรับการทดสอบ)
docker-compose -f docker-compose.simple.yml up -d

# เริ่มต้นแบบเต็ม (พร้อม PostgreSQL และ Redis)
docker-compose -f docker-compose.yml up -d

# เริ่มต้นแบบทดสอบ
docker-compose -f docker-compose.test.yml up -d
```

### 3. การใช้งาน Python Script
```bash
python docker_management.py
```

## 📁 ไฟล์ Docker ที่สำคัญ

### **Dockerfile**
- **Base Image**: `python:3.10-slim`
- **GPU Support**: PyTorch CUDA 11.8
- **Security**: Non-root user
- **Ports**: 6969, 7000, 8000

### **docker-compose.yml** (Full Version)
```yaml
services:
  victor-tts-api:    # VICTOR-TTS API Server
  n8n:              # N8N Workflow Automation
  postgres:         # PostgreSQL Database
  redis:            # Redis Cache
  nginx:            # Reverse Proxy (Optional)
```

### **docker-compose.simple.yml** (Simple Version)
```yaml
services:
  victor-tts-api:    # VICTOR-TTS API Server
  n8n:              # N8N Workflow Automation
```

### **docker-compose.test.yml** (Test Version)
```yaml
services:
  victor-tts-test:   # VICTOR-TTS API Server (Test Mode)
  n8n-test:         # N8N Test Instance
```

## 🌐 URLs และ Ports

### **Services URLs**
- **N8N**: http://localhost:5678
- **VICTOR-TTS API**: http://localhost:6969
- **VICTOR-TTS Web Interface**: http://localhost:7000
- **Health Check**: http://localhost:6969/health

### **API Endpoints**
```
POST /unified          # TTS + RVC แบบรวม
POST /tts              # TTS เท่านั้น
POST /voice_conversion # RVC เท่านั้น
GET  /voices           # รายการเสียง
GET  /models           # รายการโมเดล
GET  /health           # Health check
```

## 🔧 การตั้งค่า Environment Variables

### **VICTOR-TTS API**
```yaml
environment:
  - PYTHONPATH=/app
  - CUDA_VISIBLE_DEVICES=0
  - TZ=Asia/Bangkok
  - VICTOR_TTS_MODE=docker
  - VICTOR_TTS_N8N_INTEGRATION=true
```

### **N8N**
```yaml
environment:
  - N8N_HOST=0.0.0.0
  - N8N_PORT=5678
  - N8N_PROTOCOL=http
  - N8N_USER_MANAGEMENT_DISABLED=true
  - N8N_BASIC_AUTH_ACTIVE=false
  - N8N_VICTOR_TTS_URL=http://victor-tts-api:6969
  - N8N_VICTOR_TTS_WEB_URL=http://victor-tts-api:7000
```

## 📊 Volumes และ Data Persistence

### **VICTOR-TTS Volumes**
```yaml
volumes:
  - ./storage:/app/storage          # Output files
  - ./models:/app/models            # RVC models
  - ./logs:/app/logs                # Log files
  - ./config:/app/config            # Configuration
  - ./voice_models:/app/voice_models # Voice models
  - ./voice_samples:/app/voice_samples # Voice samples
```

### **N8N Volumes**
```yaml
volumes:
  - n8n_data:/home/node/.n8n        # N8N data
  - ./n8n_workflows:/home/node/.n8n/workflows # Workflow files
```

## 🔄 N8N Workflow Integration

### **Workflow Template**
ไฟล์ `n8n_workflows/victor_tts_workflow.json` มี workflow template สำหรับ:
- Webhook trigger
- Input validation
- VICTOR-TTS API call
- Response handling

### **การใช้งาน Workflow**
1. เปิด N8N ที่ http://localhost:5678
2. Import workflow จากไฟล์ `victor_tts_workflow.json`
3. Activate workflow
4. เรียกใช้ผ่าน webhook

### **Webhook Example**
```bash
curl -X POST http://localhost:5678/webhook/victor-tts-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "text": "สวัสดีครับ ยินดีต้อนรับสู่ระบบ VICTOR-TTS",
    "voice": "th-TH-NeeraNeural",
    "speed": 1.0,
    "enable_rvc": true,
    "rvc_params": {
      "model_name": "al_bundy",
      "transpose": 0
    }
  }'
```

## 🛠️ การจัดการ Docker

### **คำสั่งพื้นฐาน**
```bash
# สร้าง image
docker-compose -f docker-compose.simple.yml build

# เริ่มต้น services
docker-compose -f docker-compose.simple.yml up -d

# หยุด services
docker-compose -f docker-compose.simple.yml down

# ดู logs
docker-compose -f docker-compose.simple.yml logs -f

# ดูสถานะ
docker-compose -f docker-compose.simple.yml ps
```

### **การจัดการด้วย Python Script**
```bash
python docker_management.py
```

## 🔍 การ Troubleshooting

### **1. Container ไม่เริ่มต้น**
```bash
# ตรวจสอบ logs
docker-compose logs victor-tts-api

# ตรวจสอบสถานะ
docker ps -a

# Restart service
docker-compose restart victor-tts-api
```

### **2. GPU ไม่ทำงาน**
```bash
# ตรวจสอบ GPU
nvidia-smi

# ตรวจสอบ Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
```

### **3. Port ถูกใช้งาน**
```bash
# ตรวจสอบ port ที่ใช้งาน
netstat -tulpn | grep :6969

# เปลี่ยน port ใน docker-compose.yml
ports:
  - "6970:6969"  # เปลี่ยนจาก 6969 เป็น 6970
```

### **4. Permission Issues**
```bash
# แก้ไข permission
sudo chown -R $USER:$USER ./storage ./models ./logs

# หรือใช้ Docker volume
volumes:
  - victor_storage:/app/storage
```

## 📈 Performance Optimization

### **1. GPU Configuration**
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

### **2. Memory Limits**
```yaml
deploy:
  resources:
    limits:
      memory: 8G
    reservations:
      memory: 4G
```

### **3. CPU Limits**
```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'
    reservations:
      cpus: '2.0'
```

## 🔒 Security Considerations

### **1. Network Security**
```yaml
networks:
  victor-network:
    driver: bridge
    internal: true  # ไม่ expose ไป internet
```

### **2. User Permissions**
```dockerfile
# สร้าง non-root user
RUN useradd -m -u 1000 victor
USER victor
```

### **3. Environment Variables**
```yaml
# ใช้ .env file สำหรับ sensitive data
environment:
  - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
```

## 📝 การ Monitor และ Logging

### **1. Health Checks**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:6969/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### **2. Logging Configuration**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### **3. Monitoring Tools**
- **Docker Stats**: `docker stats`
- **Container Logs**: `docker-compose logs -f`
- **Resource Usage**: `docker system df`

## 🚀 Production Deployment

### **1. Production Docker Compose**
```yaml
version: '3.8'
services:
  victor-tts-api:
    image: victor-tts:latest
    restart: always
    environment:
      - VICTOR_TTS_MODE=production
    volumes:
      - victor_storage:/app/storage
    networks:
      - victor-network
```

### **2. Load Balancer**
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - victor-tts-api
```

### **3. SSL Configuration**
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... other SSL settings
}
```

## 📚 Additional Resources

### **1. N8N Documentation**
- [N8N Official Docs](https://docs.n8n.io/)
- [N8N Docker Guide](https://docs.n8n.io/hosting/installation/docker/)
- [N8N API Reference](https://docs.n8n.io/api/)

### **2. Docker Documentation**
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### **3. VICTOR-TTS Documentation**
- [API Documentation](http://localhost:6969/docs)
- [Web Interface](http://localhost:7000)
- [Health Check](http://localhost:6969/health)

## 🤝 Support

### **การรายงานปัญหา**
1. ตรวจสอบ logs: `docker-compose logs`
2. ตรวจสอบ health check: `curl http://localhost:6969/health`
3. รายงานปัญหาใน GitHub Issues

### **การขอความช่วยเหลือ**
- สร้าง issue ใน GitHub repository
- ระบุข้อมูลระบบและ error messages
- แนบ logs และ configuration files

---

**วันที่อัปเดต**: 29 กรกฎาคม 2025  
**เวอร์ชัน**: 1.0.0  
**ผู้พัฒนา**: VICTOR-TTS Team  
**ประเภท**: Docker & N8N Integration Guide 