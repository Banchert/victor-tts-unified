#!/usr/bin/env python3
"""
🚀 VICTOR-TTS Docker Startup Script
Start both API server and Web Interface for Docker deployment
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

def start_api_server():
    """Start the API server"""
    print("📡 Starting VICTOR-TTS API Server on port 6969...")
    try:
        cmd = [sys.executable, "main_api_server.py", "--host", "0.0.0.0", "--port", "6969"]
        return subprocess.Popen(cmd)
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def start_web_interface():
    """Start the web interface"""
    print("🌐 Starting VICTOR-TTS Web Interface on port 7000...")
    try:
        # Try the simple fallback web server approach
        cmd = [sys.executable, "-c", """
import http.server
import socketserver
import socket

def find_port():
    for port in range(7000, 7010):
        try:
            s = socket.socket()
            s.bind(('0.0.0.0', port))
            s.close()
            return port
        except:
            continue
    return 7000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>VICTOR-TTS Web Interface</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 800px; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .api-link { background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
        a { color: #1976d2; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 VICTOR-TTS Web Interface</h1>
        <div class="status">
            <h3>✅ Docker Mode - Server is running!</h3>
            <p>The VICTOR-TTS system is successfully running in Docker container.</p>
        </div>
        
        <h3>� Available Services:</h3>
        <div class="api-link">
            <strong>🎙️ API Server:</strong> <a href="http://localhost:6969/docs" target="_blank">http://localhost:6969/docs</a><br>
            <strong>🏥 Health Check:</strong> <a href="http://localhost:6969/health" target="_blank">http://localhost:6969/health</a><br>
            <strong>🤖 N8N Workflow:</strong> <a href="http://localhost:5678" target="_blank">http://localhost:5678</a>
        </div>
        
        <h3>📝 API Usage:</h3>
        <p>Use the API endpoints for TTS and voice conversion:</p>
        <ul>
            <li><code>POST /unified</code> - Combined TTS + Voice Conversion</li>
            <li><code>POST /tts</code> - Text-to-Speech only</li>
            <li><code>POST /voice_conversion</code> - Voice conversion only</li>
            <li><code>GET /voices</code> - List available voices</li>
            <li><code>GET /models</code> - List RVC models</li>
        </ul>
        
        <p><em>🐳 This is the Docker web interface. The API is fully functional.</em></p>
    </div>
</body>
</html>
        '''
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        pass  # Suppress logs

port = find_port()
print(f'🌐 Web Interface starting on 0.0.0.0:{port}')
with socketserver.TCPServer(('0.0.0.0', port), Handler) as httpd:
    httpd.serve_forever()
"""]
        return subprocess.Popen(cmd)
    except Exception as e:
        print(f"❌ Failed to start web interface: {e}")
        return None

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    print("\n🛑 Received shutdown signal...")
    global api_process, web_process
    
    if api_process:
        print("📡 Stopping API server...")
        api_process.terminate()
    
    if web_process:
        print("🌐 Stopping web interface...")
        web_process.terminate()
    
    print("👋 VICTOR-TTS services stopped")
    sys.exit(0)

def main():
    """Main startup function"""
    global api_process, web_process
    
    print("🚀 VICTOR-TTS Docker Services Starting...")
    print("=" * 50)
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server, exiting...")
        sys.exit(1)
    
    # Wait a moment for API to initialize
    print("⏳ Waiting for API server to initialize...")
    time.sleep(10)
    
    # Start web interface
    web_process = start_web_interface()
    
    print("\n✅ VICTOR-TTS Services Started!")
    print("📡 API Server: http://0.0.0.0:6969")
    print("🌐 Web Interface: http://0.0.0.0:7000")
    print("💡 Services accessible from outside Docker container")
    print("\nPress Ctrl+C to stop all services")
    print("=" * 50)
    
    try:
        # Wait for processes
        while True:
            if api_process and api_process.poll() is not None:
                print("❌ API server stopped unexpectedly")
                break
            
            if web_process and web_process.poll() is not None:
                print("⚠️ Web interface stopped unexpectedly")
                # Try to restart web interface
                print("🔄 Attempting to restart web interface...")
                web_process = start_web_interface()
            
            time.sleep(5)
    
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    # Global process variables
    api_process = None
    web_process = None
    
    main()
