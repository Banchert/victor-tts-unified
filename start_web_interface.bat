@echo off
echo ========================================
echo    VICTOR-TTS Web Interface
echo ========================================
echo.

echo กำลังเปิดใช้งาน Virtual Environment...
call env\Scripts\activate.bat

echo.
echo กำลังเริ่มต้น Web Interface...
python web_interface.py

echo.
echo Web Interface หยุดทำงานแล้ว
pause 