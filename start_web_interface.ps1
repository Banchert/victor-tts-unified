# VICTOR-TTS Web Interface Launcher
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    VICTOR-TTS Web Interface" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "กำลังเปิดใช้งาน Virtual Environment..." -ForegroundColor Yellow
& "env\Scripts\Activate.ps1"

Write-Host ""
Write-Host "กำลังเริ่มต้น Web Interface..." -ForegroundColor Yellow
python web_interface.py

Write-Host ""
Write-Host "Web Interface หยุดทำงานแล้ว" -ForegroundColor Green
Read-Host "กด Enter เพื่อปิด" 