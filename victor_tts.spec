# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# ข้อมูลโปรแกรม
app_name = 'VICTOR-TTS-UNIFIED'
app_version = '1.0.0'
app_description = 'VICTOR-TTS UNIFIED - Text-to-Speech with Voice Conversion (Optimized)'

# ไฟล์หลัก
main_script = 'web_interface.py'

# ไฟล์และโฟลเดอร์ที่ต้องรวม
datas = [
    # โฟลเดอร์สำคัญ
    ('rvc', 'rvc'),
    ('logs', 'logs'),
    ('voice_samples', 'voice_samples'),
    ('templates', 'templates'),
    ('config', 'config'),
    ('assets', 'assets'),
    
    # ไฟล์สำคัญ
    ('tts_rvc_core.py', '.'),
    ('rvc_api.py', '.'),
    ('main_api_server.py', '.'),
    ('start.py', '.'),
    ('requirements.txt', '.'),
    ('README.md', '.'),
    
    # FFmpeg binaries
    ('ffmpeg.exe', '.'),
    ('ffprobe.exe', '.'),
]

# ไฟล์และโฟลเดอร์ที่ต้องยกเว้น (Optimized)
excludes = [
    'tkinter',
    'matplotlib',
    'jupyter',
    'IPython',
    'pandas',
    'scipy',
    'pytest',
    'unittest',
    'test',
    'tests',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.git',
    '.gitignore',
    'venv',
    'env',
    'node_modules',
    '*.log',
    '*.tmp',
    'storage/temp/*',
    '*.md',  # ไม่รวม markdown files
    '*.bat',  # ไม่รวม batch files
    '*.ps1',  # ไม่รวม PowerShell files
    '*.spec',  # ไม่รวม spec files
    'Dockerfile',
    'docker-compose*.yml',
    '.dockerignore',
    'LICENSE',
    'CONTRIBUTING.md',
    'GITHUB_*.md',
    'DOCKER_GUIDE.md',
    'BUILD_EXE_GUIDE.md',
    'WEB_INTERFACE_FIX_SUMMARY.md',
    'RVC_*.md',
    '*.json',  # ไม่รวม test reports
    'test_*.py',  # ไม่รวม test files
]

# Hidden imports ที่ PyInstaller อาจไม่เจอ
hiddenimports = [
    # Core modules
    'tts_rvc_core',
    'rvc_api',
    'main_api_server',
    'web_interface',
    
    # TTS modules
    'edge_tts',
    'edge_playback',
    
    # RVC modules
    'rvc.infer.infer',
    'rvc.infer.pipeline',
    'rvc.lib.utils',
    'rvc.configs.config',
    'rvc.lib.algorithm',
    'rvc.lib.predictors',
    'rvc.lib.tools',
    
    # Audio processing
    'librosa',
    'soundfile',
    'noisereduce',
    'pedalboard',
    'soxr',
    'ffmpeg',
    'ffmpy',
    
    # ML/AI
    'torch',
    'torchaudio',
    'faiss',
    'numpy',
    'scipy',
    
    # Web/API
    'fastapi',
    'uvicorn',
    'aiohttp',
    'requests',
    
    # Utilities
    'asyncio',
    'aiofiles',
    'coloredlogs',
    'click',
    'toml',
    'yaml',
    'json',
    'base64',
    'tempfile',
    'pathlib',
    'logging',
    'socket',
    'webbrowser',
    'http.server',
    'socketserver',
    'urllib.parse',
    'urllib.request',
    
    # Windows specific
    'win32api',
    'win32con',
    'win32gui',
    'win32process',
    'pywintypes',
]

# ตัวแปรสภาพแวดล้อม
env_vars = [
    ('PYTHONPATH', '.'),
    ('VICTOR_TTS_HOME', '.'),
]

a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Optimize: strip debug symbols
    upx=True,    # Optimize: compress with UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version_file=None,
    uac_admin=False,
    uac_uiaccess=False,
) 