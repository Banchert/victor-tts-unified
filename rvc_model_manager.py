#!/usr/bin/env python3
"""
🎭 RVC Model Manager - Enhanced
เครื่องมือจัดการโมเดล RVC ที่ปรับปรุงแล้ว
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger("RVC_MODEL_MANAGER")

@dataclass
class ModelInfo:
    """ข้อมูลโมเดล RVC"""
    name: str
    path: str
    pth_files: List[str]
    index_files: List[str]
    size_mb: float
    status: str
    created_date: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = None
    quality_rating: Optional[int] = None  # 1-5 stars

class RVCModelManager:
    """จัดการโมเดล RVC แบบครอบคลุม"""
    
    def __init__(self, models_dir: str = "logs", config_file: str = "config/model_config.json"):
        self.models_dir = Path(models_dir)
        self.config_file = Path(config_file)
        self.config = self.load_config()
        
        # สร้างโฟลเดอร์ที่จำเป็น
        self.models_dir.mkdir(exist_ok=True)
        (self.models_dir / "backups").mkdir(exist_ok=True)
        (self.models_dir / "imports").mkdir(exist_ok=True)
        
        logger.info(f"RVC Model Manager initialized: {self.models_dir}")
    
    def load_config(self) -> Dict[str, Any]:
        """โหลดการตั้งค่า"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # สร้างการตั้งค่าเริ่มต้น
                default_config = {
                    "auto_backup": True,
                    "backup_retention_days": 30,
                    "quality_check": True,
                    "auto_organize": True,
                    "favorite_models": [],
                    "model_metadata": {}
                }
                self.save_config(default_config)
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    def save_config(self, config: Dict[str, Any]):
        """บันทึกการตั้งค่า"""
        try:
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def scan_models(self) -> List[ModelInfo]:
        """สแกนหาโมเดลทั้งหมด"""
        models = []
        
        if not self.models_dir.exists():
            return models
        
        for model_dir in self.models_dir.iterdir():
            if not model_dir.is_dir() or model_dir.name.startswith('.'):
                continue
            
            # ข้าม backup และ import folders
            if model_dir.name in ['backups', 'imports']:
                continue
            
            try:
                model_info = self.analyze_model(model_dir)
                if model_info:
                    models.append(model_info)
            except Exception as e:
                logger.warning(f"Error analyzing model {model_dir.name}: {e}")
        
        # เรียงตามชื่อ
        models.sort(key=lambda x: x.name.lower())
        return models
    
    def analyze_model(self, model_dir: Path) -> Optional[ModelInfo]:
        """วิเคราะห์โมเดล"""
        try:
            model_name = model_dir.name
            
            # หาไฟล์ .pth และ .index
            all_pth_files = list(model_dir.glob("*.pth"))
            all_index_files = list(model_dir.glob("*.index"))
            
            # กรองไฟล์ .pth (ไม่เอาไฟล์ training)
            model_pth_files = [
                f for f in all_pth_files 
                if not (f.name.startswith('D_') or f.name.startswith('G_'))
            ]
            
            if not model_pth_files:
                return None
            
            # คำนวณขนาด
            total_size = sum(f.stat().st_size for f in model_pth_files + all_index_files)
            size_mb = total_size / (1024 * 1024)
            
            # กำหนดสถานะ
            status = "ready" if model_pth_files and all_index_files else "incomplete"
            if not all_index_files:
                status = "no_index"
            
            # ดึงข้อมูล metadata
            metadata = self.config.get("model_metadata", {}).get(model_name, {})
            
            return ModelInfo(
                name=model_name,
                path=str(model_dir),
                pth_files=[f.name for f in model_pth_files],
                index_files=[f.name for f in all_index_files],
                size_mb=round(size_mb, 2),
                status=status,
                created_date=metadata.get("created_date"),
                description=metadata.get("description"),
                tags=metadata.get("tags", []),
                quality_rating=metadata.get("quality_rating")
            )
            
        except Exception as e:
            logger.error(f"Error analyzing model {model_dir}: {e}")
            return None
    
    def get_model_summary(self) -> Dict[str, Any]:
        """ดึงสรุปข้อมูลโมเดล"""
        models = self.scan_models()
        
        total_size = sum(model.size_mb for model in models)
        status_counts = {}
        
        for model in models:
            status_counts[model.status] = status_counts.get(model.status, 0) + 1
        
        return {
            "total_models": len(models),
            "total_size_mb": round(total_size, 2),
            "total_size_gb": round(total_size / 1024, 2),
            "status_breakdown": status_counts,
            "ready_models": len([m for m in models if m.status == "ready"]),
            "incomplete_models": len([m for m in models if m.status != "ready"]),
            "average_size_mb": round(total_size / len(models), 2) if models else 0,
            "largest_model": max(models, key=lambda x: x.size_mb).name if models else None,
            "smallest_model": min(models, key=lambda x: x.size_mb).name if models else None
        }
    
    def backup_model(self, model_name: str, backup_name: str = None) -> bool:
        """สำรองโมเดล"""
        try:
            model_dir = self.models_dir / model_name
            if not model_dir.exists():
                logger.error(f"Model not found: {model_name}")
                return False
            
            # สร้างชื่อ backup
            if not backup_name:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{model_name}_{timestamp}"
            
            backup_dir = self.models_dir / "backups" / backup_name
            
            # สำรองข้อมูล
            shutil.copytree(model_dir, backup_dir)
            
            logger.info(f"Model backed up: {model_name} -> {backup_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up model {model_name}: {e}")
            return False
    
    def restore_model(self, backup_name: str, new_model_name: str = None) -> bool:
        """คืนโมเดลจาก backup"""
        try:
            backup_dir = self.models_dir / "backups" / backup_name
            if not backup_dir.exists():
                logger.error(f"Backup not found: {backup_name}")
                return False
            
            # กำหนดชื่อโมเดลใหม่
            if not new_model_name:
                new_model_name = backup_name.split('_')[0]  # เอาส่วนหน้าของชื่อ backup
            
            restore_dir = self.models_dir / new_model_name
            
            # ตรวจสอบว่ามีโมเดลชื่อนี้อยู่แล้วหรือไม่
            if restore_dir.exists():
                logger.error(f"Model already exists: {new_model_name}")
                return False
            
            # คืนข้อมูล
            shutil.copytree(backup_dir, restore_dir)
            
            logger.info(f"Model restored: {backup_name} -> {new_model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring model {backup_name}: {e}")
            return False
    
    def delete_model(self, model_name: str, create_backup: bool = True) -> bool:
        """ลบโมเดล"""
        try:
            model_dir = self.models_dir / model_name
            if not model_dir.exists():
                logger.error(f"Model not found: {model_name}")
                return False
            
            # สำรองก่อนลบ (ถ้าต้องการ)
            if create_backup:
                if not self.backup_model(model_name):
                    logger.warning(f"Could not create backup for {model_name}")
            
            # ลบโมเดล
            shutil.rmtree(model_dir)
            
            # ลบข้อมูล metadata
            if "model_metadata" in self.config and model_name in self.config["model_metadata"]:
                del self.config["model_metadata"][model_name]
                self.save_config(self.config)
            
            logger.info(f"Model deleted: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting model {model_name}: {e}")
            return False
    
    def set_model_metadata(self, model_name: str, description: str = None, 
                          tags: List[str] = None, quality_rating: int = None) -> bool:
        """ตั้งค่า metadata ของโมเดล"""
        try:
            # ตรวจสอบว่ามีโมเดลอยู่
            model_dir = self.models_dir / model_name
            if not model_dir.exists():
                logger.error(f"Model not found: {model_name}")
                return False
            
            # เตรียม metadata
            if "model_metadata" not in self.config:
                self.config["model_metadata"] = {}
            
            if model_name not in self.config["model_metadata"]:
                self.config["model_metadata"][model_name] = {}
            
            metadata = self.config["model_metadata"][model_name]
            
            # อัปเดตข้อมูล
            if description is not None:
                metadata["description"] = description
            if tags is not None:
                metadata["tags"] = tags
            if quality_rating is not None:
                if 1 <= quality_rating <= 5:
                    metadata["quality_rating"] = quality_rating
                else:
                    logger.warning("Quality rating must be between 1 and 5")
            
            # เพิ่มวันที่อัปเดต
            from datetime import datetime
            metadata["updated_date"] = datetime.now().isoformat()
            
            self.save_config(self.config)
            logger.info(f"Metadata updated for model: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting metadata for {model_name}: {e}")
            return False
    
    def search_models(self, query: str) -> List[ModelInfo]:
        """ค้นหาโมเดล"""
        models = self.scan_models()
        query_lower = query.lower()
        
        matching_models = []
        
        for model in models:
            # ค้นหาในชื่อ
            if query_lower in model.name.lower():
                matching_models.append(model)
                continue
            
            # ค้นหาใน description
            if model.description and query_lower in model.description.lower():
                matching_models.append(model)
                continue
            
            # ค้นหาใน tags
            if model.tags:
                for tag in model.tags:
                    if query_lower in tag.lower():
                        matching_models.append(model)
                        break
        
        return matching_models
    
    def get_favorites(self) -> List[str]:
        """ดึงรายการโมเดลโปรด"""
        return self.config.get("favorite_models", [])
    
    def add_favorite(self, model_name: str) -> bool:
        """เพิ่มโมเดลโปรด"""
        try:
            # ตรวจสอบว่ามีโมเดลอยู่
            if not (self.models_dir / model_name).exists():
                logger.error(f"Model not found: {model_name}")
                return False
            
            favorites = self.config.get("favorite_models", [])
            if model_name not in favorites:
                favorites.append(model_name)
                self.config["favorite_models"] = favorites
                self.save_config(self.config)
                logger.info(f"Added to favorites: {model_name}")
            
            return True
        except Exception as e:
            logger.error(f"Error adding favorite {model_name}: {e}")
            return False
    
    def remove_favorite(self, model_name: str) -> bool:
        """ลบโมเดลโปรด"""
        try:
            favorites = self.config.get("favorite_models", [])
            if model_name in favorites:
                favorites.remove(model_name)
                self.config["favorite_models"] = favorites
                self.save_config(self.config)
                logger.info(f"Removed from favorites: {model_name}")
            
            return True
        except Exception as e:
            logger.error(f"Error removing favorite {model_name}: {e}")
            return False
    
    def cleanup_old_backups(self, retention_days: int = 30) -> int:
        """ทำความสะอาด backup เก่า"""
        try:
            from datetime import datetime, timedelta
            
            backup_dir = self.models_dir / "backups"
            if not backup_dir.exists():
                return 0
            
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            deleted_count = 0
            
            for backup in backup_dir.iterdir():
                if backup.is_dir():
                    # ดูจากวันที่แก้ไขล่าสุด
                    backup_time = datetime.fromtimestamp(backup.stat().st_mtime)
                    if backup_time < cutoff_date:
                        shutil.rmtree(backup)
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {backup.name}")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            return 0

def main():
    """ทดสอบ Model Manager"""
    manager = RVCModelManager()
    
    print("🎭 RVC Model Manager Test")
    print("=" * 40)
    
    # สแกนโมเดล
    models = manager.scan_models()
    print(f"Found {len(models)} models:")
    
    for model in models[:5]:  # แสดง 5 โมเดลแรก
        print(f"  📁 {model.name}")
        print(f"     Status: {model.status}")
        print(f"     Size: {model.size_mb} MB")
        print(f"     Files: {len(model.pth_files)} pth, {len(model.index_files)} index")
    
    # สรุปข้อมูล
    summary = manager.get_model_summary()
    print(f"\n📊 Summary:")
    print(f"  Total models: {summary['total_models']}")
    print(f"  Total size: {summary['total_size_gb']:.2f} GB")
    print(f"  Ready models: {summary['ready_models']}")
    print(f"  Average size: {summary['average_size_mb']:.1f} MB")

if __name__ == "__main__":
    main()
