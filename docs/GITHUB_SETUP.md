# 🚀 GitHub Setup Guide - VICTOR-TTS UNIFIED

คู่มือการตั้งค่าและ push โปรเจกต์ไปยัง GitHub

## 📋 Prerequisites

1. **GitHub Account** - สร้างบัญชีที่ [GitHub.com](https://github.com)
2. **Git** - ติดตั้ง Git บนเครื่อง
3. **GitHub CLI** (optional) - สำหรับการจัดการ repository ผ่าน command line

## 🔧 Step-by-Step Setup

### 1. สร้าง GitHub Repository

#### วิธีที่ 1: ผ่าน GitHub Website
1. ไปที่ [GitHub.com](https://github.com)
2. คลิกปุ่ม "New" หรือ "+" → "New repository"
3. กรอกข้อมูล:
   - **Repository name**: `victor-tts-unified`
   - **Description**: `Complete Text-to-Speech with Voice Conversion Platform`
   - **Visibility**: Public หรือ Private (ตามต้องการ)
   - **Initialize with**: ไม่ต้องเลือกอะไร
4. คลิก "Create repository"

#### วิธีที่ 2: ผ่าน GitHub CLI
```bash
gh repo create victor-tts-unified --public --description "Complete Text-to-Speech with Voice Conversion Platform"
```

### 2. ตั้งค่า Local Repository

#### วิธีที่ 1: ใช้ Script อัตโนมัติ
```bash
# Windows
push_to_github.bat

# PowerShell
.\push_to_github.ps1
```

#### วิธีที่ 2: ใช้คำสั่ง Git แบบ manual
```bash
# 1. ตั้งค่า Git user (ถ้ายังไม่ได้ตั้ง)
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# 2. เพิ่ม remote origin
git remote add origin https://github.com/yourusername/victor-tts-unified.git

# 3. Push ไปยัง GitHub
git branch -M main
git push -u origin main
```

### 3. อัพเดท Repository URLs

หลังจาก push ไป GitHub แล้ว ให้อัพเดท URLs ในไฟล์ต่างๆ:

#### ใน `README.md`
```markdown
# เปลี่ยนจาก
url="https://github.com/yourusername/victor-tts-unified"

# เป็น
url="https://github.com/your-actual-username/victor-tts-unified"
```

#### ใน `setup.py`
```python
# เปลี่ยนจาก
url="https://github.com/yourusername/victor-tts-unified",

# เป็น
url="https://github.com/your-actual-username/victor-tts-unified",
```

#### ใน `CONTRIBUTING.md`
```markdown
# เปลี่ยนจาก
git clone https://github.com/yourusername/victor-tts-unified.git

# เป็น
git clone https://github.com/your-actual-username/victor-tts-unified.git
```

## 🎯 Repository Features

### 1. GitHub Pages (Optional)
ตั้งค่า GitHub Pages เพื่อแสดงเว็บไซต์:

1. ไปที่ repository → Settings
2. เลื่อนลงไปหา "Pages"
3. Source: Deploy from a branch
4. Branch: main
5. Folder: / (root)
6. คลิก "Save"

### 2. GitHub Actions (Optional)
สร้าง workflow สำหรับ CI/CD:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/
```

### 3. Repository Settings

#### Topics
เพิ่ม topics เพื่อให้ค้นหาได้ง่าย:
- `tts`
- `voice-conversion`
- `rvc`
- `edge-tts`
- `fastapi`
- `gradio`
- `python`

#### Description
```
Complete Text-to-Speech with Voice Conversion Platform. Features Edge TTS integration, RVC voice conversion, FastAPI backend, Gradio web interface, and N8N integration.
```

#### Website
```
https://yourusername.github.io/victor-tts-unified
```

## 📊 Repository Statistics

### Badges (เพิ่มใน README.md)
```markdown
![GitHub release (latest by date)](https://img.shields.io/github/v/release/yourusername/victor-tts-unified)
![GitHub stars](https://img.shields.io/github/stars/yourusername/victor-tts-unified)
![GitHub forks](https://img.shields.io/github/forks/yourusername/victor-tts-unified)
![GitHub issues](https://img.shields.io/github/issues/yourusername/victor-tts-unified)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/victor-tts-unified)
![GitHub license](https://img.shields.io/github/license/yourusername/victor-tts-unified)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
```

## 🔄 การอัพเดท Repository

### เพิ่มการเปลี่ยนแปลงใหม่
```bash
# 1. เพิ่มไฟล์ที่เปลี่ยนแปลง
git add .

# 2. Commit การเปลี่ยนแปลง
git commit -m "feat: add new feature"

# 3. Push ไปยัง GitHub
git push origin main
```

### สร้าง Release
1. ไปที่ repository → Releases
2. คลิก "Create a new release"
3. กรอกข้อมูล:
   - **Tag version**: `v1.0.0`
   - **Release title**: `Version 1.0.0`
   - **Description**: รายละเอียดการเปลี่ยนแปลง
4. คลิก "Publish release"

## 🛠️ Troubleshooting

### ปัญหาที่พบบ่อย

#### 1. Authentication Error
```bash
# ใช้ Personal Access Token
git remote set-url origin https://your-token@github.com/yourusername/victor-tts-unified.git
```

#### 2. Large File Error
```bash
# ใช้ Git LFS สำหรับไฟล์ใหญ่
git lfs install
git lfs track "*.wav"
git lfs track "*.mp3"
git lfs track "*.pth"
```

#### 3. Branch Protection
ตั้งค่า branch protection rules:
1. Settings → Branches
2. Add rule
3. Branch name pattern: `main`
4. Require pull request reviews
5. Require status checks to pass

## 📞 Support

หากมีปัญหาการตั้งค่า GitHub:
- [GitHub Help](https://help.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- สร้าง Issue ใน repository

---

🎉 **เสร็จสิ้น! โปรเจกต์ของคุณพร้อมใช้งานบน GitHub แล้ว** 