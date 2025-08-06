#!/usr/bin/env python3
"""
🐳 Docker Management Script for VICTOR-TTS + N8N
สคริปต์จัดการ Docker containers แบบง่ายๆ
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
import requests

class DockerManager:
    """จัดการ Docker containers สำหรับ VICTOR-TTS และ N8N"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.docker_dir = self.project_dir / "docker"
        
    def check_docker(self):
        """ตรวจสอบว่า Docker พร้อมใช้งานหรือไม่"""
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker: {result.stdout.strip()}")
                return True
            else:
                print("❌ Docker not found")
                return False
        except FileNotFoundError:
            print("❌ Docker not installed")
            return False
    
    def check_docker_compose(self):
        """ตรวจสอบว่า Docker Compose พร้อมใช้งานหรือไม่"""
        try:
            result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker Compose: {result.stdout.strip()}")
                return True
            else:
                print("❌ Docker Compose not found")
                return False
        except FileNotFoundError:
            print("❌ Docker Compose not installed")
            return False
    
    def run_command(self, command, shell=False):
        """รันคำสั่ง Docker"""
        try:
            print(f"🔄 Running: {' '.join(command) if isinstance(command, list) else command}")
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            
            if result.returncode == 0:
                if result.stdout:
                    print(result.stdout)
                return True
            else:
                print(f"❌ Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def build_images(self, compose_file="docker-compose.simple.yml"):
        """Build Docker images"""
        print("\n🔨 Building Docker images...")
        
        os.chdir(self.project_dir)
        return self.run_command(["docker-compose", "-f", compose_file, "build"])
    
    def start_services(self, compose_file="docker-compose.simple.yml", detached=True):
        """เริ่มต้น services"""
        print(f"\n🚀 Starting services using {compose_file}...")
        
        os.chdir(self.project_dir)
        cmd = ["docker-compose", "-f", compose_file, "up"]
        if detached:
            cmd.append("-d")
        
        return self.run_command(cmd)
    
    def stop_services(self, compose_file="docker-compose.simple.yml"):
        """หยุด services"""
        print(f"\n🛑 Stopping services using {compose_file}...")
        
        os.chdir(self.project_dir)
        return self.run_command(["docker-compose", "-f", compose_file, "down"])
    
    def restart_services(self, compose_file="docker-compose.simple.yml"):
        """รีสตาร์ท services"""
        print(f"\n🔄 Restarting services using {compose_file}...")
        
        os.chdir(self.project_dir)
        return self.run_command(["docker-compose", "-f", compose_file, "restart"])
    
    def show_logs(self, compose_file="docker-compose.simple.yml", service=None, follow=True):
        """แสดง logs"""
        print(f"\n📋 Showing logs...")
        
        os.chdir(self.project_dir)
        cmd = ["docker-compose", "-f", compose_file, "logs"]
        if follow:
            cmd.append("-f")
        if service:
            cmd.append(service)
        
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n📋 Logs stopped")
    
    def show_status(self, compose_file="docker-compose.simple.yml"):
        """แสดงสถานะ services"""
        print(f"\n📊 Services status:")
        
        os.chdir(self.project_dir)
        return self.run_command(["docker-compose", "-f", compose_file, "ps"])
    
    def health_check(self):
        """ตรวจสอบ health ของ services"""
        print("\n🏥 Health checking services...")
        
        services = {
            "VICTOR-TTS API": "http://localhost:6969/health",
            "N8N": "http://localhost:5678",
            "VICTOR-TTS Web": "http://localhost:7000"
        }
        
        for name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: Healthy")
                else:
                    print(f"⚠️ {name}: Status {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"❌ {name}: Not responding")
    
    def cleanup(self):
        """ทำความสะอาด Docker system"""
        print("\n🧹 Cleaning up Docker system...")
        
        commands = [
            ["docker", "system", "prune", "-f"],
            ["docker", "volume", "prune", "-f"],
            ["docker", "network", "prune", "-f"]
        ]
        
        for cmd in commands:
            self.run_command(cmd)
    
    def show_menu(self):
        """แสดงเมนูหลัก"""
        while True:
            print("\n" + "=" * 50)
            print("🐳 VICTOR-TTS Docker Management")
            print("=" * 50)
            print("1. 🔨 Build images")
            print("2. 🚀 Start services (Simple)")
            print("3. 🚀 Start services (Full)")
            print("4. 🛑 Stop services")
            print("5. 🔄 Restart services")
            print("6. 📋 Show logs")
            print("7. 📊 Show status")
            print("8. 🏥 Health check")
            print("9. 🧹 Cleanup Docker")
            print("10. 📝 Show URLs")
            print("0. ❌ Exit")
            print("=" * 50)
            
            choice = input("เลือกตัวเลือก (0-10): ").strip()
            
            if choice == "1":
                self.build_images()
            elif choice == "2":
                self.start_services("docker-compose.simple.yml")
            elif choice == "3":
                self.start_services("docker-compose.yml")
            elif choice == "4":
                compose_choice = input("ใช้ compose file ไหน? (1=simple, 2=full): ").strip()
                compose_file = "docker-compose.simple.yml" if compose_choice == "1" else "docker-compose.yml"
                self.stop_services(compose_file)
            elif choice == "5":
                compose_choice = input("ใช้ compose file ไหน? (1=simple, 2=full): ").strip()
                compose_file = "docker-compose.simple.yml" if compose_choice == "1" else "docker-compose.yml"
                self.restart_services(compose_file)
            elif choice == "6":
                service = input("Service name (หรือ Enter สำหรับทั้งหมด): ").strip()
                service = service if service else None
                self.show_logs(service=service)
            elif choice == "7":
                self.show_status()
            elif choice == "8":
                self.health_check()
            elif choice == "9":
                confirm = input("ต้องการลบ unused Docker resources? (y/N): ").strip().lower()
                if confirm == "y":
                    self.cleanup()
            elif choice == "10":
                self.show_urls()
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")
            
            input("\nกด Enter เพื่อดำเนินการต่อ...")
    
    def show_urls(self):
        """แสดง URLs ที่สำคัญ"""
        print("\n🌐 Important URLs:")
        print("=" * 50)
        print("🤖 N8N Workflow:        http://localhost:5678")
        print("🎙️ VICTOR-TTS API:      http://localhost:6969")
        print("🌐 VICTOR-TTS Web:      http://localhost:7000")
        print("📊 API Documentation:   http://localhost:6969/docs")
        print("🏥 Health Check:        http://localhost:6969/health")
        print("🔄 API Status:          http://localhost:6969/status")
        print("=" * 50)
        print("\n📝 API Endpoints:")
        print("POST /unified           - TTS + RVC แบบรวม")
        print("POST /tts               - TTS เท่านั้น")
        print("POST /voice_conversion  - RVC เท่านั้น")
        print("GET  /voices            - รายการเสียง")
        print("GET  /models            - รายการโมเดล RVC")
    
    def quick_start(self):
        """เริ่มต้นอย่างรวดเร็ว"""
        print("🚀 VICTOR-TTS + N8N Quick Start")
        print("=" * 50)
        
        if not self.check_docker() or not self.check_docker_compose():
            print("❌ Docker หรือ Docker Compose ไม่พร้อมใช้งาน")
            return False
        
        print("\n1. เลือกการติดตั้ง:")
        print("   1) Simple (VICTOR-TTS + N8N เท่านั้น)")
        print("   2) Full (พร้อม PostgreSQL, Redis, Nginx)")
        
        choice = input("เลือก (1-2): ").strip()
        compose_file = "docker-compose.simple.yml" if choice == "1" else "docker-compose.yml"
        
        print(f"\n2. Building และ starting services...")
        self.build_images(compose_file)
        self.start_services(compose_file)
        
        print("\n3. รอ services เริ่มต้น...")
        time.sleep(10)
        
        print("\n4. ตรวจสอบ health...")
        self.health_check()
        
        print("\n✅ เสร็จสิ้น! สามารถใช้งานได้ที่:")
        self.show_urls()

def main():
    """ฟังก์ชันหลัก"""
    manager = DockerManager()
    
    # ตรวจสอบ arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            manager.quick_start()
        elif command == "start":
            compose_file = sys.argv[2] if len(sys.argv) > 2 else "docker-compose.simple.yml"
            manager.start_services(compose_file)
        elif command == "stop":
            compose_file = sys.argv[2] if len(sys.argv) > 2 else "docker-compose.simple.yml"
            manager.stop_services(compose_file)
        elif command == "build":
            compose_file = sys.argv[2] if len(sys.argv) > 2 else "docker-compose.simple.yml"
            manager.build_images(compose_file)
        elif command == "logs":
            service = sys.argv[2] if len(sys.argv) > 2 else None
            manager.show_logs(service=service)
        elif command == "status":
            manager.show_status()
        elif command == "health":
            manager.health_check()
        elif command == "cleanup":
            manager.cleanup()
        elif command == "urls":
            manager.show_urls()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: quick, start, stop, build, logs, status, health, cleanup, urls")
    else:
        # แสดงเมนู interactive
        manager.show_menu()

if __name__ == "__main__":
    main()
