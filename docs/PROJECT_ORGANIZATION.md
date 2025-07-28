# 📁 VICTOR-TTS Project Organization

## 🎯 Overview

เอกสารนี้อธิบายการจัดระเบียบโครงสร้างโปรเจค VICTOR-TTS ที่ได้รับการปรับปรุงให้เป็นระเบียบและใช้งานง่ายขึ้น

## 📂 New Directory Structure

```
VICTOR-TTS/
├── 🔧 Core Application Files
│   ├── main_api_server.py           # FastAPI server
│   ├── web_interface.py             # Web UI
│   ├── tts_rvc_core.py              # Core logic
│   ├── rvc_api.py                   # RVC wrapper
│   ├── victor_tts_launcher.py       # Launcher
│   ├── requirements.txt             # Dependencies
│   └── setup.py                     # Installation
│
├── 🐳 Docker Files
│   ├── docker/Dockerfile            # Main container
│   ├── docker/docker-compose.yml    # Full deployment
│   ├── docker/docker-compose.simple.yml # Simple deployment
│   ├── docker/docker-compose.test.yml   # Test deployment
│   └── docker/nginx.conf            # Reverse proxy
│
├── 📜 Scripts
│   ├── start.bat                    # Windows launcher (root)
│   ├── scripts/docker_management.py # Docker management
│   ├── scripts/build_exe.bat        # EXE builder
│   ├── scripts/build_exe.ps1        # PowerShell EXE builder
│   ├── scripts/update_github.bat    # GitHub updater
│   ├── scripts/update_github.ps1    # PowerShell GitHub updater
│   └── scripts/*.ps1                # Other PowerShell scripts
│
├── 📊 Documentation
│   ├── docs/README.md               # Main documentation
│   ├── docs/DOCKER_N8N_GUIDE.md     # Docker & N8N guide
│   ├── docs/GPU_EXE_GUIDE.md        # GPU & EXE guide
│   ├── docs/NAGA_THEME_UPDATE.md    # UI theme guide
│   ├── docs/MODEL_MANAGEMENT_REPOSITION.md # Model management
│   ├── docs/JAVASCRIPT_SYNTAX_FIX.md # JavaScript fixes
│   ├── docs/START_BAT_GPU_UPDATE.md # Start script updates
│   ├── docs/GPU_SUPPORT_SUMMARY.md  # GPU support summary
│   ├── docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md # Performance
│   ├── docs/AUDIO_DISPLAY_IMPROVEMENT.md # Audio display
│   ├── docs/START_GUIDE.md          # Start guide
│   ├── docs/TTS_RVC_WORKFLOW_FIX.md # Workflow fixes
│   ├── docs/RVC_DISPLAY_FIX.md      # RVC display fixes
│   ├── docs/COMPACT_UI_IMPROVEMENT.md # UI improvements
│   ├── docs/MODEL_MANAGEMENT_IMPROVEMENT.md # Model management
│   ├── docs/README_LANGUAGE_TEST.md # Language testing
│   ├── docs/LANGUAGE_TEST_SUMMARY.md # Language summary
│   ├── docs/MULTI_LANGUAGE_FIX_SUMMARY.md # Multi-language
│   ├── docs/WEB_INTERFACE_FIX_SUMMARY.md # Web interface
│   ├── docs/RVC_FIX_SUMMARY.md      # RVC fixes
│   ├── docs/RVC_TEST_SUMMARY.md     # RVC testing
│   ├── docs/BUILD_EXE_GUIDE.md      # EXE building
│   ├── docs/BUILD_EXE_OPTIMIZED.md  # Optimized EXE
│   ├── docs/DOCKER_GUIDE.md         # Docker guide
│   ├── docs/CONTRIBUTING.md         # Contributing guide
│   ├── docs/GITHUB_READY.md         # GitHub setup
│   ├── docs/GITHUB_SETUP.md         # GitHub configuration
│   └── docs/PROJECT_ORGANIZATION.md # This file
│
├── 🧪 Tests
│   ├── tests/test_rvc_detailed.py   # Detailed RVC tests
│   ├── tests/test_rvc_mp3_fix.py    # RVC MP3 fix tests
│   ├── tests/test_rvc_quick.py      # Quick RVC tests
│   ├── tests/test_rvc_status.py     # RVC status tests
│   ├── tests/test_rvc_fixed.py      # Fixed RVC tests
│   ├── tests/test_tts_language.py   # TTS language tests
│   ├── tests/test_multi_language.py # Multi-language tests
│   └── tests/test_new_system.py     # New system tests
│
├── 🎭 RVC System
│   ├── rvc/                         # RVC models and code
│   ├── models/                      # Voice models
│   └── voice_models/                # Additional models
│
├── 🔄 N8N Integration
│   └── n8n_workflows/               # Workflow templates
│
├── 📁 Supporting Directories
│   ├── assets/                      # Static assets
│   ├── config/                      # Configuration files
│   ├── logs/                        # Log files
│   ├── storage/                     # Storage (output/temp)
│   ├── templates/                   # HTML templates
│   ├── voice_samples/               # Voice samples
│   ├── test_output/                 # Test outputs
│   ├── build/                       # Build artifacts
│   ├── dist/                        # Distribution files
│   ├── venv/                        # Virtual environment
│   └── env/                         # Alternative virtual environment
│
└── 🔧 System Files
    ├── .gitignore                   # Git ignore rules
    ├── .dockerignore                # Docker ignore rules
    ├── LICENSE                      # License file
    ├── ffmpeg.exe                   # FFmpeg binary
    └── ffprobe.exe                  # FFprobe binary
```

## 🔄 Changes Made

### **1. Directory Organization**

#### **Before:**
```
VICTOR-TTS/
├── *.md (scattered documentation)
├── *.bat (scattered scripts)
├── *.py (mixed core and test files)
├── docker-compose*.yml (root level)
└── Dockerfile (root level)
```

#### **After:**
```
VICTOR-TTS/
├── docs/ (all documentation)
├── scripts/ (all scripts)
├── tests/ (all test files)
├── docker/ (all Docker files)
└── organized core files
```

### **2. File Categorization**

#### **📊 Documentation (`docs/`)**
- **All `.md` files** moved to `docs/`
- **Organized by topic**: Docker, GPU, UI, etc.
- **Easy to find and maintain**

#### **📜 Scripts (`scripts/`)**
- **All `.bat` and `.ps1` files** moved to `scripts/`
- **Python management scripts** included
- **Consistent naming and organization**

#### **🧪 Tests (`tests/`)**
- **All `test_*.py` files** moved to `tests/`
- **Organized by functionality**
- **Easy to run and maintain**

#### **🐳 Docker (`docker/`)**
- **All Docker-related files** moved to `docker/`
- **Compose files organized by purpose**
- **Clear separation of concerns**

### **3. Updated References**

#### **Start Script Updates**
- **`scripts/start.bat`** updated to reference new paths
- **Test file paths** updated to `tests/`
- **Docker management** updated to `scripts/`

#### **Documentation Updates**
- **README.md** reflects new structure
- **All internal links** updated
- **Clear navigation paths**

## 🎯 Benefits

### **1. Improved Organization**
- **Logical grouping** of related files
- **Easy to find** specific functionality
- **Clear separation** of concerns

### **2. Better Maintainability**
- **Reduced clutter** in root directory
- **Easier to manage** large number of files
- **Consistent structure** across project

### **3. Enhanced Developer Experience**
- **Faster navigation** to specific files
- **Clear understanding** of project structure
- **Easier onboarding** for new contributors

### **4. Professional Appearance**
- **Industry-standard** organization
- **Clean repository** structure
- **Professional documentation**

## 🔧 Usage After Reorganization

### **Starting the Application**
```bash
# Use the main start script
start.bat

# Or run directly
python web_interface.py
```

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_rvc_quick.py
```

### **Docker Operations**
```bash
# Use Docker management script
python scripts/docker_management.py

# Or use Docker Compose directly
docker-compose -f docker/docker-compose.simple.yml up -d
```

### **Documentation Access**
```bash
# View main documentation
docs/README.md

# View specific guides
docs/DOCKER_N8N_GUIDE.md
docs/GPU_EXE_GUIDE.md
```

## 📋 File Cleanup Summary

### **Files Moved:**
- **45+ documentation files** → `docs/`
- **15+ script files** → `scripts/`
- **10+ test files** → `tests/`
- **5+ Docker files** → `docker/`

### **Files Removed:**
- **Temporary JSON files** (test reports)
- **Old spec files** (PyInstaller)
- **Duplicate documentation**

### **Files Updated:**
- **`scripts/start.bat`** - Updated paths
- **`README.md`** - New structure
- **`.gitignore`** - Enhanced rules

## 🎉 Result

### **Before Reorganization:**
- **100+ files** in root directory
- **Difficult to navigate**
- **Mixed file types**
- **Poor organization**

### **After Reorganization:**
- **Clean root directory** with core files only
- **Logical organization** by functionality
- **Easy navigation** and maintenance
- **Professional structure**

## 📞 Support

หากมีคำถามเกี่ยวกับการจัดระเบียบโปรเจค:

1. **ดูเอกสารนี้** สำหรับรายละเอียด
2. **ตรวจสอบ `docs/`** สำหรับคู่มือเฉพาะ
3. **ใช้ `scripts/start.bat`** สำหรับการเริ่มต้น
4. **ติดต่อทีมพัฒนา** หากมีปัญหา

---

**🎯 การจัดระเบียบเสร็จสิ้น - โปรเจคพร้อมใช้งาน!** 