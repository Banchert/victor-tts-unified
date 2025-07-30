#!/usr/bin/env python3
"""
Optimized Voice Selector for VICTOR-TTS EXE
"""
import os
import sys
from pathlib import Path

def select_voice_model():
    """Select voice model for optimized EXE"""
    print("🎤 VICTOR-TTS Optimized Voice Selector")
    print("=" * 50)
    
    voice_models = {
        "1": {
            "name": "Thai Female (Premwadee)",
            "voice_id": "th-TH-PremwadeeNeural",
            "language": "Thai"
        },
        "2": {
            "name": "Lao Female (Keomany)", 
            "voice_id": "lo-LA-KeomanyNeural",
            "language": "Lao"
        },
        "3": {
            "name": "English Female (Aria)",
            "voice_id": "en-US-AriaNeural", 
            "language": "English"
        }
    }
    
    print("Available voice models:")
    for key, model in voice_models.items():
        print(f"{key}. {model['name']} ({model['language']})")
    
    while True:
        choice = input("\nSelect voice model (1-3): ").strip()
        if choice in voice_models:
            selected_model = voice_models[choice]
            print(f"\n✅ Selected: {selected_model['name']}")
            return selected_model
        else:
            print("❌ Invalid choice. Please select 1-3.")

def main():
    """Main function"""
    try:
        selected_voice = select_voice_model()
        os.environ["DEFAULT_VOICE"] = selected_voice["voice_id"]
        print(f"\n🎯 Default voice set to: {selected_voice['name']}")
        print("🚀 Starting VICTOR-TTS...")
        
        # Import and start web interface
        from web_interface_complete import main as start_web_interface
        start_web_interface()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
