# 🤝 Contributing to VICTOR-TTS UNIFIED

ขอบคุณที่สนใจในการ contribute โปรเจกต์ VICTOR-TTS UNIFIED! 

## 🚀 Getting Started

### Prerequisites
- Python 3.10 หรือสูงกว่า
- Git
- FFMPEG

### Setup Development Environment

1. **Fork และ Clone Repository**
```bash
git clone https://github.com/yourusername/victor-tts-unified.git
cd victor-tts-unified
```

2. **สร้าง Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

## 📝 Development Guidelines

### Code Style
- ใช้ **Black** สำหรับ code formatting
- ใช้ **isort** สำหรับ import sorting
- ใช้ **flake8** สำหรับ linting
- เขียน docstring สำหรับทุก function และ class

### Commit Messages
ใช้ conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: ฟีเจอร์ใหม่
- `fix`: แก้ไข bug
- `docs`: เอกสาร
- `style`: formatting, missing semicolons, etc
- `refactor`: refactoring code
- `test`: adding tests
- `chore`: maintenance tasks

### Testing
- เขียน test สำหรับฟีเจอร์ใหม่
- รัน test ก่อน commit:
```bash
python -m pytest tests/
```

## 🐛 Reporting Bugs

### Bug Report Template
```markdown
**Bug Description**
คำอธิบายสั้นๆ เกี่ยวกับ bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
สิ่งที่ควรจะเกิดขึ้น

**Actual Behavior**
สิ่งที่เกิดขึ้นจริง

**Environment**
- OS: [Windows/Linux/macOS]
- Python Version: [3.10/3.11/3.12]
- GPU: [Yes/No]
- CUDA Version: [if applicable]

**Additional Information**
ข้อมูลเพิ่มเติม เช่น error logs, screenshots
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
คำอธิบายฟีเจอร์ที่ต้องการ

**Use Case**
กรณีการใช้งาน

**Proposed Solution**
แนวทางแก้ไข (ถ้ามี)

**Alternative Solutions**
ทางเลือกอื่น (ถ้ามี)

**Additional Information**
ข้อมูลเพิ่มเติม
```

## 🔧 Pull Request Process

1. **สร้าง Branch ใหม่**
```bash
git checkout -b feature/your-feature-name
```

2. **ทำการเปลี่ยนแปลง**
- เขียนโค้ด
- เพิ่ม test
- อัพเดทเอกสาร

3. **Commit และ Push**
```bash
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

4. **สร้าง Pull Request**
- ไปที่ GitHub repository
- คลิก "New Pull Request"
- เลือก branch ที่สร้าง
- กรอกข้อมูลตาม template

### PR Template
```markdown
## Description
คำอธิบายการเปลี่ยนแปลง

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 📚 Documentation

### Updating Documentation
- อัพเดท README.md ถ้าจำเป็น
- เพิ่ม docstring ในโค้ด
- อัพเดท API documentation

### Code Documentation
```python
def example_function(param1: str, param2: int) -> bool:
    """
    คำอธิบายฟังก์ชัน
    
    Args:
        param1 (str): คำอธิบาย parameter 1
        param2 (int): คำอธิบาย parameter 2
        
    Returns:
        bool: คำอธิบาย return value
        
    Raises:
        ValueError: เมื่อ parameter ไม่ถูกต้อง
        
    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

## 🎯 Areas for Contribution

### High Priority
- [ ] เพิ่ม unit tests
- [ ] ปรับปรุง error handling
- [ ] เพิ่ม logging
- [ ] ปรับปรุง performance

### Medium Priority
- [ ] เพิ่มฟีเจอร์ใหม่
- [ ] ปรับปรุง UI/UX
- [ ] เพิ่ม documentation
- [ ] Internationalization

### Low Priority
- [ ] Code refactoring
- [ ] Performance optimization
- [ ] Additional examples

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/victor-tts-unified/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/victor-tts-unified/discussions)
- **Email**: your-email@example.com

## 🙏 Recognition

ผู้ที่ contribute จะได้รับการระบุใน:
- README.md contributors section
- Release notes
- Project documentation

---

ขอบคุณสำหรับการ contribute! 🎉 