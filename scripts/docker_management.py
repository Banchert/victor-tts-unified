#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐳 VICTOR-TTS Docker Management Script
จัดการ Docker containers และ N8N integration
"""

import os
import sys
import subprocess
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional

class DockerManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.docker_compose_files = {
            'simple': 'docker-compose.simple.yml',
            'full': 'docker-compose.yml',
            'test': 'docker-compose.test.yml'
        }
        
    def check_docker_installed(self) -> bool:
        """ตรวจสอบว่า Docker ติดตั้งแล้วหรือไม่"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Docker: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker ไม่ได้ติดตั้ง")
            return False
    
    def check_docker_compose_installed(self) -> bool:
        """ตรวจสอบว่า Docker Compose ติดตั้งแล้วหรือไม่"""
        try:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Docker Compose: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker Compose ไม่ได้ติดตั้ง")
            return False
    
    def build_image(self, compose_file: str = 'simple') -> bool:
        """สร้าง Docker image"""
        if compose_file not in self.docker_compose_files:
            print(f"❌ ไม่พบไฟล์ {compose_file}")
            return False
            
        file_path = self.docker_compose_files[compose_file]
        if not Path(file_path).exists():
            print(f"❌ ไม่พบไฟล์ {file_path}")
            return False
            
        print(f"🔨 กำลังสร้าง Docker image จาก {file_path}...")
        try:
            subprocess.run(['docker-compose', '-f', file_path, 'build'], 
                          check=True, cwd=self.project_root)
            print("✅ สร้าง Docker image สำเร็จ")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ สร้าง Docker image ล้มเหลว: {e}")
            return False
    
    def start_services(self, compose_file: str = 'simple') -> bool:
        """เริ่มต้น services"""
        if compose_file not in self.docker_compose_files:
            print(f"❌ ไม่พบไฟล์ {compose_file}")
            return False
            
        file_path = self.docker_compose_files[compose_file]
        if not Path(file_path).exists():
            print(f"❌ ไม่พบไฟล์ {file_path}")
            return False
            
        print(f"🚀 กำลังเริ่มต้น services จาก {file_path}...")
        try:
            subprocess.run(['docker-compose', '-f', file_path, 'up', '-d'], 
                          check=True, cwd=self.project_root)
            print("✅ เริ่มต้น services สำเร็จ")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ เริ่มต้น services ล้มเหลว: {e}")
            return False
    
    def stop_services(self, compose_file: str = 'simple') -> bool:
        """หยุด services"""
        if compose_file not in self.docker_compose_files:
            print(f"❌ ไม่พบไฟล์ {compose_file}")
            return False
            
        file_path = self.docker_compose_files[compose_file]
        if not Path(file_path).exists():
            print(f"❌ ไม่พบไฟล์ {file_path}")
            return False
            
        print(f"🛑 กำลังหยุด services จาก {file_path}...")
        try:
            subprocess.run(['docker-compose', '-f', file_path, 'down'], 
                          check=True, cwd=self.project_root)
            print("✅ หยุด services สำเร็จ")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ หยุด services ล้มเหลว: {e}")
            return False
    
    def check_service_health(self, service_name: str, port: int, timeout: int = 60) -> bool:
        """ตรวจสอบสถานะของ service"""
        print(f"🔍 ตรวจสอบ {service_name} ที่ port {port}...")
        
        for i in range(timeout):
            try:
                response = requests.get(f"http://localhost:{port}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {service_name} พร้อมใช้งาน")
                    return True
            except requests.RequestException:
                pass
            
            print(f"⏳ รอ {service_name}... ({i+1}/{timeout})")
            time.sleep(1)
        
        print(f"❌ {service_name} ไม่พร้อมใช้งาน")
        return False
    
    def get_container_status(self) -> Dict[str, str]:
        """ดูสถานะของ containers"""
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'], 
                                  capture_output=True, text=True, check=True)
            
            containers = {}
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        name = parts[0]
                        status = parts[1]
                        containers[name] = status
            
            return containers
        except subprocess.CalledProcessError:
            return {}
    
    def show_logs(self, service_name: str, lines: int = 50) -> None:
        """แสดง logs ของ service"""
        try:
            subprocess.run(['docker-compose', 'logs', '--tail', str(lines), service_name], 
                          cwd=self.project_root)
        except subprocess.CalledProcessError as e:
            print(f"❌ ไม่สามารถแสดง logs ได้: {e}")
    
    def test_n8n_integration(self) -> bool:
        """ทดสอบการเชื่อมต่อกับ N8N"""
        print("🧪 ทดสอบการเชื่อมต่อกับ N8N...")
        
        # ตรวจสอบ N8N
        try:
            response = requests.get("http://localhost:5678", timeout=10)
            if response.status_code == 200:
                print("✅ N8N พร้อมใช้งาน")
            else:
                print("❌ N8N ไม่พร้อมใช้งาน")
                return False
        except requests.RequestException:
            print("❌ ไม่สามารถเชื่อมต่อกับ N8N ได้")
            return False
        
        # ตรวจสอบ VICTOR-TTS API
        try:
            response = requests.get("http://localhost:6969/health", timeout=10)
            if response.status_code == 200:
                print("✅ VICTOR-TTS API พร้อมใช้งาน")
            else:
                print("❌ VICTOR-TTS API ไม่พร้อมใช้งาน")
                return False
        except requests.RequestException:
            print("❌ ไม่สามารถเชื่อมต่อกับ VICTOR-TTS API ได้")
            return False
        
        print("✅ การเชื่อมต่อทั้งหมดพร้อมใช้งาน")
        return True
    
    def show_usage_info(self) -> None:
        """แสดงข้อมูลการใช้งาน"""
        print("\n🌐 URLs สำหรับการใช้งาน:")
        print("   N8N: http://localhost:5678")
        print("   VICTOR-TTS API: http://localhost:6969")
        print("   VICTOR-TTS Web: http://localhost:7000")
        print("   Health Check: http://localhost:6969/health")
        
        print("\n📋 API Endpoints:")
        print("   POST /unified - TTS + RVC แบบรวม")
        print("   POST /tts - TTS เท่านั้น")
        print("   POST /voice_conversion - RVC เท่านั้น")
        print("   GET /voices - รายการเสียง")
        print("   GET /models - รายการโมเดล")
        
        print("\n🔧 คำสั่ง Docker:")
        print("   docker-compose -f docker-compose.simple.yml up -d")
        print("   docker-compose -f docker-compose.yml up -d")
        print("   docker-compose -f docker-compose.test.yml up -d")

def main():
    """Main function"""
    manager = DockerManager()
    
    print("🐳 VICTOR-TTS Docker Management")
    print("=" * 50)
    
    # ตรวจสอบ Docker
    if not manager.check_docker_installed():
        return
    
    if not manager.check_docker_compose_installed():
        return
    
    # แสดงเมนู
    while True:
        print("\n📋 เลือกตัวเลือก:")
        print("1. 🔨 สร้าง Docker image")
        print("2. 🚀 เริ่มต้น services (Simple)")
        print("3. 🚀 เริ่มต้น services (Full)")
        print("4. 🚀 เริ่มต้น services (Test)")
        print("5. 🛑 หยุด services")
        print("6. 📊 ดูสถานะ containers")
        print("7. 📝 แสดง logs")
        print("8. 🧪 ทดสอบการเชื่อมต่อ")
        print("9. ℹ️  ข้อมูลการใช้งาน")
        print("0. ❌ ออกจากโปรแกรม")
        
        try:
            choice = input("\n👉 เลือกตัวเลือก (0-9): ").strip()
            
            if choice == "0":
                print("👋 ออกจากโปรแกรม")
                break
            elif choice == "1":
                compose_type = input("เลือกประเภท (simple/full/test): ").strip()
                manager.build_image(compose_type)
            elif choice == "2":
                manager.start_services('simple')
            elif choice == "3":
                manager.start_services('full')
            elif choice == "4":
                manager.start_services('test')
            elif choice == "5":
                compose_type = input("เลือกประเภท (simple/full/test): ").strip()
                manager.stop_services(compose_type)
            elif choice == "6":
                containers = manager.get_container_status()
                if containers:
                    print("\n📊 สถานะ Containers:")
                    for name, status in containers.items():
                        print(f"   {name}: {status}")
                else:
                    print("❌ ไม่พบ containers ที่ทำงานอยู่")
            elif choice == "7":
                service = input("ชื่อ service (victor-tts-api/n8n): ").strip()
                lines = input("จำนวนบรรทัด (default 50): ").strip()
                lines = int(lines) if lines.isdigit() else 50
                manager.show_logs(service, lines)
            elif choice == "8":
                manager.test_n8n_integration()
            elif choice == "9":
                manager.show_usage_info()
            else:
                print("❌ ตัวเลือกไม่ถูกต้อง")
                
        except KeyboardInterrupt:
            print("\n👋 ออกจากโปรแกรม")
            break
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main() 