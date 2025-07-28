@echo off
echo ========================================
echo    VICTOR-TTS UNIFIED - GitHub Push
echo ========================================
echo.

echo 1. ตรวจสอบ Git status...
git status
echo.

echo 2. เพิ่มไฟล์ทั้งหมด...
git add .
echo.

echo 3. Commit การเปลี่ยนแปลง...
git commit -m "feat: update VICTOR-TTS UNIFIED platform"
echo.

echo 4. ตั้งค่า remote origin (กรุณาใส่ URL ของ repository ของคุณ)...
echo กรุณาใส่ URL ของ GitHub repository ของคุณ:
set /p repo_url="GitHub Repository URL: "
git remote add origin %repo_url%
echo.

echo 5. Push ไปยัง GitHub...
git branch -M main
git push -u origin main
echo.

echo ========================================
echo    เสร็จสิ้น! โปรเจกต์ถูก push ไป GitHub แล้ว
echo ========================================
echo.
echo ขั้นตอนต่อไป:
echo 1. ไปที่ GitHub repository ของคุณ
echo 2. ตรวจสอบว่าทุกไฟล์ถูก push แล้ว
echo 3. อัพเดท README.md URL ในไฟล์ต่างๆ
echo 4. ตั้งค่า GitHub Pages (ถ้าต้องการ)
echo.
pause 