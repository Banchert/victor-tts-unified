# RVC Models Directory

This directory contains RVC (Retrieval-based Voice Conversion) model files.

## Structure
Each model should have its own subdirectory with:
- `*.pth` files: The main model weights
- `*.index` files: Index files for voice matching (optional but recommended)

## Example
```
logs/
├── my_voice_model/
│   ├── my_voice_model.pth
│   └── my_voice_model.index
└── another_model/
    ├── another_model_v2.pth
    └── another_model_v2.index
```

## Usage
1. Place your trained RVC models in subdirectories here
2. The system will automatically detect and load available models
3. Use the web interface or API to select and use models

## Note
- Model files are typically large (50MB-500MB) and are excluded from git
- This directory contains only test/dummy files for system validation
- Replace with your actual trained RVC models for voice conversion 