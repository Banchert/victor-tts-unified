#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ VICTOR-TTS Start Script (Compatibility Wrapper)
Simple launcher for VICTOR-TTS UNIFIED system
"""

import sys
import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="VICTOR-TTS Unified Launcher")
    parser.add_argument("--web", action="store_true", help="Start web interface")
    parser.add_argument("--api", action="store_true", help="Start API server")
    parser.add_argument("--launcher", action="store_true", help="Start GUI launcher")
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--port", type=int, help="Port number")
    parser.add_argument("--gpu", type=int, help="GPU ID to use")
    parser.add_argument("--cpu", action="store_true", help="Force CPU usage")
    
    args = parser.parse_args()
    
    # If no mode specified, show help
    if not any([args.web, args.api, args.launcher]):
        print("""
🎙️ VICTOR-TTS UNIFIED Launcher
==============================
Usage:
  python start.py --api          # Start API server (for N8N)
  python start.py --web          # Start web interface  
  python start.py --launcher     # Start GUI launcher
  
Options:
  --host HOST     Host address (default: 0.0.0.0)
  --port PORT     Port number
  --gpu GPU_ID    GPU ID to use
  --cpu           Force CPU usage
  
Examples:
  python start.py --api --port 6969
  python start.py --web --port 7000
  python start.py --launcher
""")
        return
    
    # Build command arguments
    cmd_args = []
    if args.host:
        cmd_args.extend(["--host", args.host])
    if args.port:
        cmd_args.extend(["--port", str(args.port)])
    if args.gpu is not None:
        cmd_args.extend(["--gpu", str(args.gpu)])
    if args.cpu:
        cmd_args.append("--cpu")
    
    try:
        if args.api:
            print("🚀 Starting VICTOR-TTS API Server...")
            cmd = [sys.executable, "main_api_server.py"] + cmd_args
            subprocess.run(cmd)
            
        elif args.web:
            print("🌐 Starting VICTOR-TTS Web Interface...")
            cmd = [sys.executable, "web_interface_complete.py"] + cmd_args
            subprocess.run(cmd)
            
        elif args.launcher:
            print("🎛️ Starting VICTOR-TTS GUI Launcher...")
            cmd = [sys.executable, "victor_tts_launcher.py"] + cmd_args
            subprocess.run(cmd)
            
    except KeyboardInterrupt:
        print("\n👋 VICTOR-TTS stopped by user")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure you're in the correct directory with all required files.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
