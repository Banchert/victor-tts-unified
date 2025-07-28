# VICTOR-TTS UNIFIED - Quick Push Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    VICTOR-TTS UNIFIED - Quick Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# รับข้อมูลจากผู้ใช้
$username = Read-Host "กรุณาใส่ GitHub username ของคุณ"
$repoName = Read-Host "กรุณาใส่ชื่อ repository (default: victor-tts-unified)"

if ([string]::IsNullOrEmpty($repoName)) {
    $repoName = "victor-tts-unified"
}

Write-Host ""
Write-Host "กำลังตั้งค่า remote origin..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$username/$repoName.git"
git remote add origin $remoteUrl

Write-Host ""
Write-Host "กำลัง push ไปยัง GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    เสร็จสิ้น! โปรเจกต์ถูก push ไป GitHub แล้ว" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Repository URL: https://github.com/$username/$repoName" -ForegroundColor Cyan
Write-Host ""

Read-Host "กด Enter เพื่อปิด" 