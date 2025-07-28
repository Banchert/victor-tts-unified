# VICTOR-TTS UNIFIED - Docker Setup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    VICTOR-TTS UNIFIED - Docker Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ตรวจสอบ Docker
Write-Host "ตรวจสอบ Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker ไม่ได้ติดตั้ง กรุณาติดตั้ง Docker Desktop" -ForegroundColor Red
    Read-Host "กด Enter เพื่อปิด"
    exit 1
}

Write-Host ""
Write-Host "เลือกการรัน:" -ForegroundColor Cyan
Write-Host "1. Simple Version (VICTOR-TTS + N8N)" -ForegroundColor White
Write-Host "2. Full Version (VICTOR-TTS + N8N + PostgreSQL + Redis)" -ForegroundColor White
Write-Host "3. VICTOR-TTS Only" -ForegroundColor White
Write-Host "4. Stop All Services" -ForegroundColor White
Write-Host "5. View Logs" -ForegroundColor White
Write-Host ""

$choice = Read-Host "เลือกตัวเลือก (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "กำลังรัน Simple Version..." -ForegroundColor Yellow
        docker-compose -f docker-compose.simple.yml up --build
    }
    "2" {
        Write-Host ""
        Write-Host "กำลังรัน Full Version..." -ForegroundColor Yellow
        docker-compose up --build
    }
    "3" {
        Write-Host ""
        Write-Host "กำลังรัน VICTOR-TTS Only..." -ForegroundColor Yellow
        docker-compose -f docker-compose.simple.yml up victor-tts-api --build
    }
    "4" {
        Write-Host ""
        Write-Host "กำลังหยุด services..." -ForegroundColor Yellow
        docker-compose down
        docker-compose -f docker-compose.simple.yml down
    }
    "5" {
        Write-Host ""
        Write-Host "เลือก service ที่ต้องการดู logs:" -ForegroundColor Cyan
        Write-Host "1. VICTOR-TTS API" -ForegroundColor White
        Write-Host "2. N8N" -ForegroundColor White
        Write-Host "3. All Services" -ForegroundColor White
        Write-Host ""
        $logChoice = Read-Host "เลือก (1-3)"
        
        switch ($logChoice) {
            "1" { docker-compose logs -f victor-tts-api }
            "2" { docker-compose logs -f n8n }
            "3" { docker-compose logs -f }
            default { Write-Host "ตัวเลือกไม่ถูกต้อง" -ForegroundColor Red }
        }
    }
    default {
        Write-Host ""
        Write-Host "ตัวเลือกไม่ถูกต้อง" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    เสร็จสิ้น!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "- VICTOR-TTS API: http://localhost:6969" -ForegroundColor White
Write-Host "- N8N: http://localhost:5678" -ForegroundColor White
Write-Host "- Web Interface: http://localhost:7000" -ForegroundColor White
Write-Host ""

Read-Host "กด Enter เพื่อปิด" 