# VICTOR-TTS UNIFIED - GitHub Push Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    VICTOR-TTS UNIFIED - GitHub Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. ตรวจสอบ Git status
Write-Host "1. ตรวจสอบ Git status..." -ForegroundColor Yellow
git status
Write-Host ""

# 2. เพิ่มไฟล์ทั้งหมด
Write-Host "2. เพิ่มไฟล์ทั้งหมด..." -ForegroundColor Yellow
git add .
Write-Host ""

# 3. Commit การเปลี่ยนแปลง
Write-Host "3. Commit การเปลี่ยนแปลง..." -ForegroundColor Yellow
git commit -m "feat: update VICTOR-TTS UNIFIED platform"
Write-Host ""

# 4. ตั้งค่า remote origin
Write-Host "4. ตั้งค่า remote origin..." -ForegroundColor Yellow
$repoUrl = Read-Host "กรุณาใส่ URL ของ GitHub repository ของคุณ"
git remote add origin $repoUrl
Write-Host ""

# 5. Push ไปยัง GitHub
Write-Host "5. Push ไปยัง GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "    เสร็จสิ้น! โปรเจกต์ถูก push ไป GitHub แล้ว" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "ขั้นตอนต่อไป:" -ForegroundColor Cyan
Write-Host "1. ไปที่ GitHub repository ของคุณ" -ForegroundColor White
Write-Host "2. ตรวจสอบว่าทุกไฟล์ถูก push แล้ว" -ForegroundColor White
Write-Host "3. อัพเดท README.md URL ในไฟล์ต่างๆ" -ForegroundColor White
Write-Host "4. ตั้งค่า GitHub Pages (ถ้าต้องการ)" -ForegroundColor White
Write-Host ""

Read-Host "กด Enter เพื่อปิด" 