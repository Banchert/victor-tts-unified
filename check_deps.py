import sys
print("Python version:", sys.version)
print("Python executable:", sys.executable)

try:
    import edge_tts
    print("✅ edge_tts available")
except ImportError:
    print("❌ edge_tts not available")
    print("Installing edge_tts...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"])

try:
    import asyncio
    print("✅ asyncio available")
except ImportError:
    print("❌ asyncio not available")

print("Test completed")
