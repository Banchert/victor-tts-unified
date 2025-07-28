# VICTOR-TTS UNIFIED - Build Optimized EXE Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    VICTOR-TTS UNIFIED - Build Optimized EXE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "กำลังตรวจสอบ dependencies..." -ForegroundColor Yellow
try {
    $pyinstaller_version = python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null
    Write-Host "PyInstaller version: $pyinstaller_version" -ForegroundColor Green
} catch {
    Write-Host "❌ PyInstaller not found. Installing..." -ForegroundColor Red
    pip install pyinstaller
}

Write-Host ""
Write-Host "กำลังสร้าง VICTOR-TTS UNIFIED.exe (Optimized)..." -ForegroundColor Yellow
Write-Host "รวม: TTS + RVC + 16 Models + Web Interface" -ForegroundColor Yellow
Write-Host "ขนาดโดยประมาณ: 2-5 GB" -ForegroundColor Yellow
Write-Host "เวลา: 10-30 นาที" -ForegroundColor Yellow
Write-Host ""

# ลบไฟล์เก่า
if (Test-Path "build") { Remove-Item -Path "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item -Path "dist" -Recurse -Force }

Write-Host "กำลังสร้าง .exe แบบ optimize..." -ForegroundColor Yellow
pyinstaller --clean victor_tts.spec

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Build Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "ไฟล์ .exe อยู่ที่: dist\VICTOR-TTS-UNIFIED.exe" -ForegroundColor Green
Write-Host ""
Write-Host "วิธีการใช้งาน:" -ForegroundColor Yellow
Write-Host "1. เปิดไฟล์ dist\VICTOR-TTS-UNIFIED.exe" -ForegroundColor White
Write-Host "2. รอสักครู่ให้ระบบโหลด (1-2 นาที)" -ForegroundColor White
Write-Host "3. เปิดเว็บเบราว์เซอร์ไปที่ http://localhost:7000" -ForegroundColor White
Write-Host ""
Write-Host "Features ที่รวม:" -ForegroundColor Yellow
Write-Host "- Text-to-Speech (Edge TTS)" -ForegroundColor White
Write-Host "- Voice Conversion (RVC) - 16 models" -ForegroundColor White
Write-Host "- Web Interface" -ForegroundColor White
Write-Host "- Audio Processing" -ForegroundColor White
Write-Host ""

Read-Host "กด Enter เพื่อปิด" 