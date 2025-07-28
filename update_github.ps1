# VICTOR-TTS GitHub Update Script
Write-Host "🚀 VICTOR-TTS GitHub Update Script" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

Write-Host ""
Write-Host "📋 กำลังตรวจสอบสถานะ Git..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "🔄 กำลังเพิ่มไฟล์ทั้งหมด..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "💬 กำลังสร้าง commit..." -ForegroundColor Yellow
$commitMessage = @"
🚀 Major Update: Docker & N8N Integration + UI Improvements

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
- Comprehensive documentation
"@

git commit -m $commitMessage

Write-Host ""
Write-Host "📤 กำลัง push ไปยัง GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "✅ อัปเดต GitHub เสร็จสิ้น!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 GitHub Repository: https://github.com/your-username/victor-tts" -ForegroundColor Cyan
Write-Host "📖 Documentation: https://github.com/your-username/victor-tts#readme" -ForegroundColor Cyan
Write-Host ""
Read-Host "กด Enter เพื่อปิด..." 