@echo off
chcp 65001 >nul
echo 🚀 VICTOR-TTS GitHub Update Script
echo ================================================

echo.
echo 📋 กำลังตรวจสอบสถานะ Git...
git status

echo.
echo 🔄 กำลังเพิ่มไฟล์ทั้งหมด...
git add .

echo.
echo 💬 กำลังสร้าง commit...
git commit -m "🚀 Major Update: Docker & N8N Integration + UI Improvements

✨ New Features:
- 🐳 Docker & N8N Integration
- 📁 Model Management Repositioning
- 🎨 Naga Dragons Theme
- ⚡ Performance Optimization
- 🖥️ GPU Support Enhancement
- 🔧 JavaScript Syntax Fixes

📁 New Files:
- docker-compose.yml (Full version)
- docker-compose.simple.yml (Simple version)
- docker-compose.test.yml (Test version)
- Dockerfile (Updated)
- nginx.conf (Reverse proxy)
- docker_management.py (Docker management)
- DOCKER_N8N_GUIDE.md (Comprehensive guide)
- n8n_workflows/victor_tts_workflow.json
- MODEL_MANAGEMENT_REPOSITION.md
- NAGA_THEME_UPDATE.md
- JAVASCRIPT_SYNTAX_FIX.md
- GPU_EXE_GUIDE.md
- victor_tts_launcher.py

🔧 Updated Files:
- web_interface.py (UI improvements)
- tts_rvc_core.py (Performance & GPU)
- rvc_api.py (GPU optimization)
- start.bat (GPU support)
- main_api_server.py (Docker support)

🐛 Bug Fixes:
- JavaScript syntax errors
- GPU detection issues
- Model management layout
- Audio processing improvements

📊 Summary:
- Docker containers for easy deployment
- N8N workflow automation
- Enhanced UI/UX with Naga theme
- Better GPU support and performance
- Comprehensive documentation"

echo.
echo 📤 กำลัง push ไปยัง GitHub...
git push origin main

echo.
echo ✅ อัปเดต GitHub เสร็จสิ้น!
echo.
echo 🌐 GitHub Repository: https://github.com/your-username/victor-tts
echo 📖 Documentation: https://github.com/your-username/victor-tts#readme
echo.
pause 