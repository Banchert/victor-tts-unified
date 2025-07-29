# 📥 Model Download Guide

## 🚨 Important Notice

Due to GitHub's file size limitations, some large model files have been removed from the repository. You need to download these files manually to use the RVC voice conversion features.

## 📋 Required Model Files

### RVC Predictor Models
These files are required for RVC voice conversion:

| File | Size | Description | Download Link |
|------|------|-------------|---------------|
| `rvc/models/predictors/fcpe.pt` | 65.81 MB | FCPE (Fast Context Prediction Encoder) | [Download](https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/fcpe.pt) |
| `rvc/models/predictors/rmvpe.pt` | 172.79 MB | RMVPE (Robust Multi-Voice Pitch Estimation) | [Download](https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt) |

## 📁 Installation Instructions

### Step 1: Create Directory Structure
```bash
# Navigate to your project directory
cd "TTS FOR N8N"

# Create the predictors directory if it doesn't exist
mkdir -p rvc/models/predictors
```

### Step 2: Download Model Files

#### Option A: Manual Download
1. Download the files from the links above
2. Place them in the `rvc/models/predictors/` directory
3. Ensure the file names match exactly:
   - `fcpe.pt`
   - `rmvpe.pt`

#### Option B: Using PowerShell (Windows)
```powershell
# Create directory
New-Item -ItemType Directory -Force -Path "rvc/models/predictors"

# Download fcpe.pt
Invoke-WebRequest -Uri "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/fcpe.pt" -OutFile "rvc/models/predictors/fcpe.pt"

# Download rmvpe.pt
Invoke-WebRequest -Uri "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt" -OutFile "rvc/models/predictors/rmvpe.pt"
```

#### Option C: Using curl (Linux/Mac)
```bash
# Create directory
mkdir -p rvc/models/predictors

# Download fcpe.pt
curl -L "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/fcpe.pt" -o "rvc/models/predictors/fcpe.pt"

# Download rmvpe.pt
curl -L "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt" -o "rvc/models/predictors/rmvpe.pt"
```

### Step 3: Verify Installation
After downloading, your directory structure should look like this:
```
rvc/
└── models/
    └── predictors/
        ├── fcpe.pt      (65.81 MB)
        └── rmvpe.pt     (172.79 MB)
```

## 🔍 Verification

You can verify the files are correctly installed by:

1. **Checking file sizes:**
   ```bash
   # Windows
   dir rvc\models\predictors\*.pt

   # Linux/Mac
   ls -lh rvc/models/predictors/*.pt
   ```

2. **Running the system:**
   ```bash
   python web_interface_complete.py
   ```
   
   You should see messages like:
   ```
   INFO:RVC_API:Loaded embedder: contentvec
   INFO:RVC_API:RVC Converter initialized on cuda:0
   ```

## 🚨 Troubleshooting

### File Not Found Errors
If you see errors like:
```
FileNotFoundError: [Errno 2] No such file or directory: 'rvc/models/predictors/fcpe.pt'
```

**Solution:** Download the missing files using the instructions above.

### Permission Errors
If you get permission errors when downloading:

**Windows:**
- Run PowerShell as Administrator
- Or download manually through your browser

**Linux/Mac:**
```bash
sudo chmod +w rvc/models/predictors/
```

### Download Speed Issues
If downloads are slow:

1. **Use a different browser**
2. **Try downloading during off-peak hours**
3. **Use a download manager**
4. **Alternative download links:**
   - [fcpe.pt Mirror](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/releases/download/v0.1.0/fcpe.pt)
   - [rmvpe.pt Mirror](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/releases/download/v0.1.0/rmvpe.pt)

## 📚 Additional Resources

- [RVC Project Repository](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- [Hugging Face Models](https://huggingface.co/lj1995/VoiceConversionWebUI)
- [VICTOR-TTS Documentation](docs/)

## 🤝 Support

If you encounter any issues:

1. Check the [troubleshooting section](#-troubleshooting) above
2. Review the [main documentation](docs/)
3. Create an issue on [GitHub](https://github.com/Banchert/victor-tts-unified/issues)

---

**Note:** These model files are essential for RVC voice conversion functionality. Without them, the RVC features will not work properly. 