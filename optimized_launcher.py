#!/usr/bin/env python3
"""
Optimized VICTOR-TTS Launcher for Windows EXE
"""
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def start_web_interface():
    """Start the web interface"""
    try:
        from web_interface_complete import CompleteWebInterface
        web_interface = CompleteWebInterface(port=7000)
        web_interface.start(open_browser=False)
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        input("Press Enter to exit...")

def open_browser_delayed():
    """Open browser after delay"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:7000")
    except:
        pass

def main():
    """Main launcher function"""
    print("🎤 VICTOR-TTS Optimized Launcher")
    print("=" * 40)
    print("🚀 Starting optimized TTS system...")
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start web interface
    start_web_interface()

if __name__ == "__main__":
    main()
