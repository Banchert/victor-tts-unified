#!/usr/bin/env python3
"""
🚀 VICTOR-TTS UNIFIED - ตัวเริ่มต้นระบบหลัก
รวมทุกอย่างในที่เดียว ใช้งานง่าย
"""
import os
import sys
import argparse
import asyncio
from pathlib import Path

# เพิ่ม path ของโปรเจค
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def show_banner():
    """แสดง banner ของระบบ"""
    banner = """
    🎙️ VICTOR-TTS UNIFIED SYSTEM 🎙️
    =====================================
    🔥 Complete TTS + Voice Conversion
    ✅ Simplified & Organized
    ✅ Easy to Use & Maintain
    ✅ All-in-One Solution
    =====================================
    """
    print(banner)

def check_system():
    """ตรวจสอบระบบ"""
    print("🔍 ตรวจสอบระบบ...")
    
    checks = {
        "TTS-RVC Core": "tts_rvc_core.py",
        "API Server": "main_api_server.py", 
        "Web Interface": "web_interface.py",
        "Storage Directory": "storage",
        "Models Directory": ["models", "logs"],  # ลองหาทั้งสอง
        "Config": "config/unified_config.toml"
    }
    
    all_ok = True
    
    for name, path in checks.items():
        if isinstance(path, list):
            # ตรวจสอบหลาย path
            found = False
            for p in path:
                if Path(p).exists():
                    print(f"✅ {name}: {p}")
                    found = True
                    break
            if not found:
                print(f"❌ {name}: ไม่พบใน {', '.join(path)}")
                all_ok = False
        else:
            if Path(path).exists():
                print(f"✅ {name}: {path}")
            else:
                print(f"❌ {name}: {path} (ไม่พบ)")
                all_ok = False
    
    # ตรวจสอบ GPU
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print(f"✅ GPU: พบ {gpu_count} เครื่อง")
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print(f"   - GPU {i}: {gpu_name} ({gpu_memory:.2f} GB)")
        else:
            print("⚠️ GPU: ไม่พบ GPU ที่รองรับ CUDA")
    except ImportError:
        print("⚠️ GPU: ไม่สามารถตรวจสอบได้ (torch ไม่ได้ติดตั้ง)")
    
    return all_ok

def start_api_server(host="0.0.0.0", port=6969, gpu_id=None):
    """เริ่มต้น API Server"""
    try:
        print(f"🚀 เริ่มต้น API Server บน {host}:{port}...")
        
        # ตรวจสอบไฟล์
        if not Path("main_api_server.py").exists():
            print("❌ ไม่พบไฟล์ main_api_server.py")
            return False
        
        # รัน API Server พร้อมระบุ GPU
        cmd = f'python main_api_server.py --host {host} --port {port}'
        if gpu_id is not None:
            cmd += f' --gpu {gpu_id}'
        
        os.system(cmd)
        return True
        
    except KeyboardInterrupt:
        print("\\n👋 หยุด API Server")
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def start_web_interface(port=7000, gpu_id=None):
    """เริ่มต้น Web Interface"""
    try:
        print(f"🌐 เริ่มต้น Web Interface บน port {port}...")
        
        # ตรวจสอบไฟล์
        if not Path("web_interface.py").exists():
            print("❌ ไม่พบไฟล์ web_interface.py")
            return False
        
        # รัน Web Interface พร้อมระบุ GPU
        cmd = f'python web_interface.py --port {port}'
        if gpu_id is not None:
            cmd += f' --gpu {gpu_id}'
        
        os.system(cmd)
        return True
        
    except KeyboardInterrupt:
        print("\\n👋 หยุด Web Interface")
        return True
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

async def test_system():
    """ทดสอบระบบ"""
    print("🧪 ทดสอบระบบ...")
    
    # รันไฟล์ทดสอบ
    test_file = Path("tests/test_new_system.py")
    if test_file.exists():
        print("🔧 รันการทดสอบ...")
        result = os.system(f'python {test_file}')
        return result == 0
    else:
        print("⚠️ ไม่พบไฟล์ทดสอบ")
        return False

def show_status():
    """แสดงสถานะระบบ"""
    print("📊 สถานะระบบ VICTOR-TTS UNIFIED:")
    print("-" * 40)
    
    try:
        from tts_rvc_core import TTSRVCCore
        core = TTSRVCCore()
        status = core.get_system_status()
        
        print(f"🎵 TTS: {'✅ พร้อมใช้งาน' if status['tts_available'] else '❌ ไม่พร้อม'}")
        print(f"🎭 RVC: {'✅ พร้อมใช้งาน' if status['rvc_available'] else '❌ ไม่พร้อม'}")
        print(f"📁 โมเดล RVC: {status['rvc_models_count']} ตัว")
        
        if status['rvc_models_count'] > 0:
            print(f"🎯 โมเดลตัวอย่าง: {', '.join(status['rvc_models'][:3])}")
        
        print(f"📂 ไดเรกทอรี temp: {status['temp_dir']}")
        print(f"📂 ไดเรกทอรี models: {status['models_dir']}")
        
        # แสดงสถานะ GPU
        if 'gpu_enabled' in status:
            print(f"🖥️ GPU: {'✅ กำลังใช้งาน' if status['gpu_enabled'] else '❌ ไม่ได้ใช้'}")
            if status['gpu_enabled'] and 'gpu_info' in status:
                print(f"🎮 GPU ที่ใช้งาน: {status['gpu_info']}")
        
    except Exception as e:
        print(f"❌ ไม่สามารถตรวจสอบสถานะได้: {e}")

def cleanup_system():
    """ทำความสะอาดระบบ"""
    print("🧹 ทำความสะอาดระบบ...")
    
    try:
        from tts_rvc_core import TTSRVCCore
        core = TTSRVCCore()
        core.cleanup_temp_files()
        print("✅ ทำความสะอาดเสร็จสิ้น")
    except Exception as e:
        print(f"⚠️ ไม่สามารถทำความสะอาดได้: {e}")

def main():
    """ฟังก์ชันหลัก"""
    parser = argparse.ArgumentParser(
        description="VICTOR-TTS UNIFIED - ระบบ TTS + Voice Conversion ที่จัดระเบียบใหม่",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ตัวอย่างการใช้งาน:
  python start.py                    # แสดงเมนู
  python start.py --api              # เริ่ม API Server
  python start.py --web              # เริ่ม Web Interface
  python start.py --test             # ทดสอบระบบ
  python start.py --status           # แสดงสถานะ
  python start.py --cleanup          # ทำความสะอาด
  python start.py --check            # ตรวจสอบระบบ
  python start.py --api --gpu 0      # เริ่ม API Server โดยใช้ GPU 0
  python start.py --api --cpu        # เริ่ม API Server โดยใช้ CPU
        """
    )
    
    parser.add_argument("--api", action="store_true", help="เริ่ม API Server")
    parser.add_argument("--web", action="store_true", help="เริ่ม Web Interface")
    parser.add_argument("--test", action="store_true", help="ทดสอบระบบ")
    parser.add_argument("--status", action="store_true", help="แสดงสถานะระบบ")
    parser.add_argument("--cleanup", action="store_true", help="ทำความสะอาดระบบ")
    parser.add_argument("--check", action="store_true", help="ตรวจสอบระบบ")
    parser.add_argument("--host", default="0.0.0.0", help="Host สำหรับ API Server")
    parser.add_argument("--port", type=int, default=6969, help="Port สำหรับ API Server")
    parser.add_argument("--web-port", type=int, default=7000, help="Port สำหรับ Web Interface")
    
    # เพิ่ม GPU options
    parser.add_argument("--gpu", type=int, help="กำหนด GPU ID ที่ต้องการใช้ (0, 1, 2, ...)")
    parser.add_argument("--cpu", action="store_true", help="บังคับใช้ CPU แม้มี GPU")
    parser.add_argument("--fp16", action="store_true", help="ใช้ mixed precision (FP16) เพื่อความเร็วและประหยัดหน่วยความจำ")
    parser.add_argument("--memory-limit", type=int, default=0, help="จำกัดหน่วยความจำ GPU (MB)")
    
    args = parser.parse_args()
    
    show_banner()
    
    # ตรวจสอบความขัดแย้งของ arguments
    if args.cpu and args.gpu is not None:
        print("❌ ข้อผิดพลาด: ไม่สามารถใช้ --cpu และ --gpu พร้อมกัน")
        return
    
    # กำหนด GPU ID ที่ใช้
    gpu_id = None
    if args.gpu is not None:
        gpu_id = args.gpu
    elif args.cpu:
        gpu_id = -1  # -1 หมายถึงใช้ CPU
    
    # ถ้าไม่มี argument ให้แสดงเมนู
    if not any([args.api, args.web, args.test, args.status, args.cleanup, args.check]):
        print("🎯 เลือกโหมดการทำงาน:")
        print("1. API Server (--api)")
        print("2. Web Interface (--web)")
        print("3. ทดสอบระบบ (--test)")
        print("4. แสดงสถานะ (--status)")
        print("5. ตรวจสอบระบบ (--check)")
        print("6. ทำความสะอาด (--cleanup)")
        print()
        print("💡 ใช้ --help เพื่อดูตัวอย่างการใช้งาน")
        return
    
    try:
        if args.check:
            system_ok = check_system()
            if not system_ok:
                print("\\n⚠️ พบปัญหาในระบบ กรุณาตรวจสอบ")
                sys.exit(1)
            else:
                print("\\n✅ ระบบพร้อมใช้งาน")
        
        if args.status:
            show_status()
        
        if args.cleanup:
            cleanup_system()
        
        if args.test:
            success = asyncio.run(test_system())
            if not success:
                print("\\n❌ การทดสอบไม่ผ่าน")
                sys.exit(1)
            else:
                print("\\n✅ การทดสอบผ่านทั้งหมด")
        
        if args.api:
            start_api_server(args.host, args.port, gpu_id)
        
        if args.web:
            start_web_interface(args.web_port, gpu_id)
    
    except KeyboardInterrupt:
        print("\\n👋 ยกเลิกการทำงาน")
    except Exception as e:
        print(f"\\n❌ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
