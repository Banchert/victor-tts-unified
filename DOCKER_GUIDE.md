# 🐳 Docker Guide - VICTOR-TTS UNIFIED

คู่มือการใช้งาน Docker สำหรับ VICTOR-TTS UNIFIED และ N8N integration

## 📋 Prerequisites

- Docker Desktop (Windows/Mac) หรือ Docker Engine (Linux)
- Docker Compose
- อย่างน้อย 4GB RAM
- อย่างน้อย 10GB disk space

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Banchert/victor-tts-unified.git
cd victor-tts-unified
```

### 2. Build และ Run (Simple Version)
```bash
# Build และ run แบบง่าย
docker-compose -f docker-compose.simple.yml up --build

# หรือ run ใน background
docker-compose -f docker-compose.simple.yml up -d --build
```

### 3. Build และ Run (Full Version)
```bash
# Build และ run แบบเต็ม
docker-compose up --build

# หรือ run ใน background
docker-compose up -d --build
```

## 🌐 Access Services

### VICTOR-TTS API
- **URL**: http://localhost:6969
- **API Docs**: http://localhost:6969/docs
- **Health Check**: http://localhost:6969/health

### N8N Workflow Automation
- **URL**: http://localhost:5678
- **Default**: ไม่มี username/password

### Web Interface
- **URL**: http://localhost:7000

## 🔧 Docker Commands

### Build Image
```bash
# Build image
docker build -t victor-tts-unified .

# Build with no cache
docker build --no-cache -t victor-tts-unified .
```

### Run Containers
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Start specific service
docker-compose up victor-tts-api

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs victor-tts-api
docker-compose logs n8n

# Follow logs
docker-compose logs -f victor-tts-api
```

### Container Management
```bash
# List containers
docker ps

# Execute command in container
docker exec -it victor-tts-api bash

# View container resources
docker stats

# Remove containers
docker-compose down --rmi all
```

## 🔌 N8N Integration

### 1. สร้าง Workflow ใน N8N

1. เปิด N8N ที่ http://localhost:5678
2. สร้าง Workflow ใหม่
3. เพิ่ม HTTP Request node

### 2. TTS Request Example

**HTTP Request Node Configuration:**
- Method: `POST`
- URL: `http://victor-tts-api:6969/tts`
- Headers: `Content-Type: application/json`
- Body (JSON):
```json
{
  "text": "Hello from N8N!",
  "voice": "en-US-AndrewNeural",
  "speed": 1.0
}
```

### 3. Voice Conversion Request Example

**HTTP Request Node Configuration:**
- Method: `POST`
- URL: `http://victor-tts-api:6969/voice_conversion`
- Headers: `Content-Type: multipart/form-data`
- Body (Form Data):
  - `audio_file`: [File from previous step]
  - `request_data`: 
```json
{
  "model_name": "your_model",
  "transpose": 0,
  "index_ratio": 0.75,
  "f0_method": "rmvpe"
}
```

### 4. Unified Processing Example

**HTTP Request Node Configuration:**
- Method: `POST`
- URL: `http://victor-tts-api:6969/unified`
- Headers: `Content-Type: application/json`
- Body (JSON):
```json
{
  "text": "Hello from N8N!",
  "tts_voice": "en-US-AndrewNeural",
  "speed": 1.0,
  "enable_rvc": true,
  "rvc_params": {
    "model_name": "your_model",
    "transpose": 0,
    "index_ratio": 0.75,
    "f0_method": "rmvpe"
  }
}
```

## 📁 Volume Mounts

### Local Directories
```
./storage     → /app/storage     # Output files
./models      → /app/models      # RVC models
./logs        → /app/logs        # Log files
./config      → /app/config      # Configuration
./voice_models → /app/voice_models # Voice models
```

### N8N Data
```
n8n_data      → /home/node/.n8n  # N8N workflows
postgres_data → /var/lib/postgresql/data # Database
```

## 🔧 Configuration

### Environment Variables

**VICTOR-TTS API:**
```yaml
environment:
  - PYTHONPATH=/app
  - CUDA_VISIBLE_DEVICES=0  # GPU support
```

**N8N:**
```yaml
environment:
  - N8N_HOST=0.0.0.0
  - N8N_PORT=5678
  - N8N_PROTOCOL=http
  - N8N_USER_MANAGEMENT_DISABLED=true
  - N8N_BASIC_AUTH_ACTIVE=false
  - WEBHOOK_URL=http://localhost:5678/
  - GENERIC_TIMEZONE=Asia/Bangkok
```

### Custom Configuration

สร้างไฟล์ `.env` สำหรับ environment variables:
```env
# VICTOR-TTS API
PYTHONPATH=/app
CUDA_VISIBLE_DEVICES=0

# N8N
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_USER_MANAGEMENT_DISABLED=true
N8N_BASIC_AUTH_ACTIVE=false
WEBHOOK_URL=http://localhost:5678/
GENERIC_TIMEZONE=Asia/Bangkok
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :6969
netstat -ano | findstr :5678

# Kill process
taskkill /PID <process_id> /F
```

#### 2. Permission Issues
```bash
# Fix permissions
chmod -R 755 ./storage
chmod -R 755 ./models
chmod -R 755 ./logs
```

#### 3. Container Won't Start
```bash
# Check logs
docker-compose logs victor-tts-api

# Rebuild without cache
docker-compose build --no-cache

# Remove and recreate
docker-compose down -v
docker-compose up --build
```

#### 4. GPU Issues
```bash
# Check GPU availability
nvidia-smi

# Install NVIDIA Docker runtime
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
```

### Health Checks

**API Health Check:**
```bash
curl http://localhost:6969/health
```

**Container Health:**
```bash
docker ps
docker inspect victor-tts-api | grep Health -A 10
```

## 📊 Monitoring

### Resource Usage
```bash
# View resource usage
docker stats

# View disk usage
docker system df
```

### Logs
```bash
# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f victor-tts-api
docker-compose logs -f n8n
```

## 🔄 Updates

### Update Images
```bash
# Pull latest images
docker-compose pull

# Rebuild with latest code
docker-compose up --build
```

### Backup Data
```bash
# Backup N8N data
docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n_backup.tar.gz -C /data .

# Backup models
tar czf models_backup.tar.gz models/
```

## 🚀 Production Deployment

### Production Docker Compose
```yaml
version: '3.8'
services:
  victor-tts-api:
    image: victor-tts-unified:latest
    restart: always
    environment:
      - NODE_ENV=production
    volumes:
      - /data/storage:/app/storage
      - /data/models:/app/models
    networks:
      - victor-network

  n8n:
    image: n8nio/n8n:latest
    restart: always
    environment:
      - N8N_USER_MANAGEMENT_DISABLED=false
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password
    volumes:
      - /data/n8n:/home/node/.n8n
    networks:
      - victor-network
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:6969/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /n8n/ {
        proxy_pass http://localhost:5678/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

🎉 **เสร็จสิ้น! ตอนนี้คุณมี VICTOR-TTS UNIFIED และ N8N ทำงานใน Docker แล้ว** 