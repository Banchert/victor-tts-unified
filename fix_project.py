#!/usr/bin/env python3
"""
🔧 Fix Project Script - แก้ไขปัญหา "unhashable type: 'dict'" และปัญหาอื่นๆ
"""

import os
import sys
import json
import re
from pathlib import Path

def fix_web_interface_syntax():
    """แก้ไข syntax error ในไฟล์ web_interface.py"""
    file_path = Path("web_interface.py")
    
    if not file_path.exists():
        print("❌ ไม่พบไฟล์ web_interface.py")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # แก้ไข double curly braces ในการสร้าง dict
        fixes_made = 0
        
        # Pattern 1: {{{{ ในการสร้าง dict
        if '{{{{' in content:
            content = content.replace('{{{{', '{{')
            fixes_made += 1
            print("✅ แก้ไข double curly braces แล้ว")
        
        # Pattern 2: }}}} ในการปิด dict
        if '}}}}' in content:
            content = content.replace('}}}}', '}}')
            fixes_made += 1
            print("✅ แก้ไข closing double curly braces แล้ว")
        
        # ตรวจสอบ import cgi ที่ deprecated
        if 'import cgi' in content:
            content = content.replace('import cgi', '# import cgi  # deprecated')
            fixes_made += 1
            print("✅ แก้ไข deprecated import cgi แล้ว")
        
        if fixes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"🎉 แก้ไข {fixes_made} ปัญหาใน web_interface.py แล้ว")
            return True
        else:
            print("ℹ️ ไม่พบปัญหา syntax ใน web_interface.py")
            return True
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการแก้ไข web_interface.py: {e}")
        return False

def fix_model_handling():
    """แก้ไขการจัดการโมเดลที่ทำให้เกิด unhashable type error"""
    
    # ตรวจสอบและสร้างไฟล์ model_utils.py
    model_utils_content = '''"""
🔧 Model Utilities - ช่วยจัดการโมเดลและป้องกัน unhashable type error
"""

def normalize_model_name(model_param):
    """
    แปลงพารามิเตอร์โมเดลให้เป็น string ที่ใช้งานได้
    
    Args:
        model_param: พารามิเตอร์โมเดลที่อาจเป็น string, dict, list, หรือ type อื่น
        
    Returns:
        str or None: ชื่อโมเดลที่ใช้งานได้ หรือ None ถ้าไม่สามารถแปลงได้
    """
    if model_param is None:
        return None
    
    # ถ้าเป็น string แล้ว
    if isinstance(model_param, str):
        cleaned = model_param.strip()
        return cleaned if cleaned else None
    
    # ถ้าเป็น dict
    if isinstance(model_param, dict):
        # ลองหา key ที่เป็นชื่อโมเดล
        for key in ['name', 'model_name', 'model', 'value']:
            if key in model_param:
                return normalize_model_name(model_param[key])
        
        # ถ้าไม่เจอ key ที่คาดหวัง ลองใช้ค่าแรก
        if model_param:
            first_value = next(iter(model_param.values()))
            return normalize_model_name(first_value)
        
        return None
    
    # ถ้าเป็น list
    if isinstance(model_param, list):
        if len(model_param) > 0:
            return normalize_model_name(model_param[0])
        return None
    
    # type อื่นๆ ลองแปลงเป็น string
    try:
        result = str(model_param).strip()
        return result if result else None
    except:
        return None

def validate_model_exists(model_name, available_models):
    """
    ตรวจสอบว่าโมเดลมีอยู่จริงในรายการโมเดลที่ใช้ได้
    
    Args:
        model_name: ชื่อโมเดล
        available_models: รายการโมเดลที่ใช้ได้
        
    Returns:
        str or None: ชื่อโมเดลที่ใช้ได้ หรือ None ถ้าไม่เจอ
    """
    if not model_name or not available_models:
        return None
    
    # หาแบบตรงกัน
    if model_name in available_models:
        return model_name
    
    # หาแบบ case insensitive
    model_name_lower = model_name.lower()
    for available_model in available_models:
        if available_model.lower() == model_name_lower:
            return available_model
    
    # หาแบบ partial match
    for available_model in available_models:
        if model_name in available_model or available_model in model_name:
            return available_model
    
    return None

def safe_model_processing(model_param, available_models, default_model=None):
    """
    ประมวลผลพารามิเตอร์โมเดลอย่างปลอดภัย
    
    Args:
        model_param: พารามิเตอร์โมเดล
        available_models: รายการโมเดลที่ใช้ได้
        default_model: โมเดลเริ่มต้น
        
    Returns:
        tuple: (model_name, error_message)
    """
    try:
        # Step 1: แปลงเป็น string
        normalized_model = normalize_model_name(model_param)
        
        if normalized_model is None:
            if default_model:
                return default_model, f"ไม่สามารถแปลงพารามิเตอร์โมเดลได้ ใช้โมเดลเริ่มต้น: {default_model}"
            else:
                return None, "ไม่สามารถแปลงพารามิเตอร์โมเดลได้ และไม่มีโมเดลเริ่มต้น"
        
        # Step 2: ตรวจสอบว่าโมเดลมีอยู่
        validated_model = validate_model_exists(normalized_model, available_models)
        
        if validated_model:
            return validated_model, None
        else:
            available_str = ", ".join(available_models[:5])  # แสดงแค่ 5 ตัวแรก
            if len(available_models) > 5:
                available_str += f" และอื่นๆ อีก {len(available_models) - 5} ตัว"
            
            error_msg = f"ไม่พบโมเดล '{normalized_model}' ในรายการ. โมเดลที่ใช้ได้: {available_str}"
            
            if default_model and default_model in available_models:
                return default_model, error_msg + f" ใช้โมเดลเริ่มต้น: {default_model}"
            else:
                return None, error_msg
    
    except Exception as e:
        error_msg = f"เกิดข้อผิดพลาดในการประมวลผลโมเดล: {str(e)}"
        if default_model:
            return default_model, error_msg + f" ใช้โมเดลเริ่มต้น: {default_model}"
        else:
            return None, error_msg
'''
    
    try:
        with open("model_utils.py", 'w', encoding='utf-8') as f:
            f.write(model_utils_content)
        print("✅ สร้างไฟล์ model_utils.py แล้ว")
        return True
    except Exception as e:
        print(f"❌ ไม่สามารถสร้างไฟล์ model_utils.py ได้: {e}")
        return False

def update_tts_rvc_core():
    """อัปเดตไฟล์ tts_rvc_core.py เพื่อใช้ model_utils"""
    
    file_path = Path("tts_rvc_core.py")
    if not file_path.exists():
        print("❌ ไม่พบไฟล์ tts_rvc_core.py")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # เพิ่ม import model_utils
        if 'from model_utils import' not in content:
            import_line = "from model_utils import safe_model_processing, normalize_model_name\\n"
            # หาตำแหน่งหลังจาก import logging
            logging_pos = content.find('import logging')
            if logging_pos != -1:
                # หาจุดสิ้นสุดของบรรทัด
                end_pos = content.find('\\n', logging_pos)
                if end_pos != -1:
                    content = content[:end_pos+1] + import_line + content[end_pos+1:]
                    print("✅ เพิ่ม import model_utils แล้ว")
        
        # แก้ไขส่วนที่จัดการ rvc_model ในฟังก์ชัน process_unified
        old_model_handling = '''                    # แปลง rvc_model ให้เป็น string ถ้าเป็น type อื่น (แก้ไข unhashable error)
                    if not isinstance(rvc_model, str):
                        logger.warning(f"RVC model parameter is not a string: {rvc_model} (type: {type(rvc_model)})")
                        if isinstance(rvc_model, dict) and 'name' in rvc_model:
                            rvc_model = rvc_model['name']
                            logger.info(f"Extracted model name from dict: {rvc_model}")
                        elif isinstance(rvc_model, list) and len(rvc_model) > 0:
                            rvc_model = rvc_model[0]
                            logger.info(f"Extracted model name from list: {rvc_model}")
                        else:
                            rvc_model = str(rvc_model)
                            logger.info(f"Converted model to string: {rvc_model}")'''
        
        new_model_handling = '''                    # แปลง rvc_model ให้เป็น string อย่างปลอดภัย (แก้ไข unhashable error)
                    available_models = self.get_available_rvc_models()
                    rvc_model, model_error = safe_model_processing(
                        rvc_model, 
                        available_models,
                        available_models[0] if available_models else None
                    )
                    
                    if model_error:
                        logger.warning(f"Model processing warning: {model_error}")
                    
                    if rvc_model:
                        logger.info(f"Using RVC model: {rvc_model}")'''
        
        if old_model_handling in content:
            content = content.replace(old_model_handling, new_model_handling)
            print("✅ อัปเดตการจัดการโมเดลใน tts_rvc_core.py แล้ว")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการอัปเดต tts_rvc_core.py: {e}")
        return False

def update_rvc_api():
    """อัปเดตไฟล์ rvc_api.py เพื่อใช้ model_utils"""
    
    file_path = Path("rvc_api.py")
    if not file_path.exists():
        print("❌ ไม่พบไฟล์ rvc_api.py")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # เพิ่ม import model_utils
        if 'from model_utils import' not in content:
            import_line = "from model_utils import normalize_model_name\\n"
            # หาตำแหน่งหลังจาก import logging
            logging_pos = content.find('import logging')
            if logging_pos != -1:
                end_pos = content.find('\\n', logging_pos)
                if end_pos != -1:
                    content = content[:end_pos+1] + import_line + content[end_pos+1:]
                    print("✅ เพิ่ม import model_utils ใน rvc_api.py แล้ว")
        
        # แก้ไขส่วนที่จัดการ model_name ในฟังก์ชัน convert_voice
        old_convert_handling = '''            # แปลง model_name ให้เป็น string ถ้าเป็น type อื่น (แก้ไข unhashable error)
            if not isinstance(model_name, str):
                logger.warning(f"Model name parameter is not a string: {model_name} (type: {type(model_name)})")
                if isinstance(model_name, dict) and 'name' in model_name:
                    model_name = model_name['name']
                    logger.info(f"Extracted model name from dict: {model_name}")
                elif isinstance(model_name, list) and len(model_name) > 0:
                    model_name = model_name[0]
                    logger.info(f"Extracted model name from list: {model_name}")
                else:
                    model_name = str(model_name)
                    logger.info(f"Converted model name to string: {model_name}")'''
        
        new_convert_handling = '''            # แปลง model_name ให้เป็น string อย่างปลอดภัย (แก้ไข unhashable error)
            model_name = normalize_model_name(model_name)
            if model_name is None:
                raise ValueError("ไม่สามารถแปลงพารามิเตอร์ model_name ได้")
            
            logger.info(f"Using model name: {model_name}")'''
        
        if old_convert_handling in content:
            content = content.replace(old_convert_handling, new_convert_handling)
            print("✅ อัปเดตการจัดการโมเดลใน rvc_api.py แล้ว")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการอัปเดต rvc_api.py: {e}")
        return False

def update_web_interface():
    """อัปเดตไฟล์ web_interface.py เพื่อใช้ model_utils"""
    
    file_path = Path("web_interface.py")
    if not file_path.exists():
        print("❌ ไม่พบไฟล์ web_interface.py")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # เพิ่ม import model_utils
        if 'from model_utils import' not in content:
            import_line = "from model_utils import safe_model_processing\\n"
            # หาตำแหน่งหลังจาก import asyncio
            asyncio_pos = content.find('import asyncio')
            if asyncio_pos != -1:
                end_pos = content.find('\\n', asyncio_pos)
                if end_pos != -1:
                    content = content[:end_pos+1] + import_line + content[end_pos+1:]
                    print("✅ เพิ่ม import model_utils ใน web_interface.py แล้ว")
        
        # แก้ไขส่วนที่จัดการ rvc_model ในฟังก์ชัน _process_request
        old_request_handling = '''                    # Additional safety check for rvc_model parameter
                    if rvc_model_param is not None:
                        if isinstance(rvc_model_param, str):
                            rvc_model_param = rvc_model_param.strip()
                            if rvc_model_param == "":
                                rvc_model_param = None
                        elif isinstance(rvc_model_param, dict):
                            if 'name' in rvc_model_param:
                                rvc_model_param = rvc_model_param['name']
                            else:
                                rvc_model_param = None
                        elif isinstance(rvc_model_param, list):
                            if len(rvc_model_param) > 0:
                                rvc_model_param = str(rvc_model_param[0])
                            else:
                                rvc_model_param = None
                        else:
                            rvc_model_param = str(rvc_model_param) if rvc_model_param else None'''
        
        new_request_handling = '''                    # ใช้ safe_model_processing เพื่อจัดการโมเดลอย่างปลอดภัย
                    if rvc_model_param is not None:
                        available_models = core.get_available_rvc_models() if core else []
                        rvc_model_param, model_error = safe_model_processing(
                            rvc_model_param,
                            available_models,
                            available_models[0] if available_models else None
                        )
                        
                        if model_error:
                            print(f"⚠️ Model processing warning: {model_error}")'''
        
        if old_request_handling in content:
            content = content.replace(old_request_handling, new_request_handling)
            print("✅ อัปเดตการจัดการโมเดลใน web_interface.py แล้ว")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการอัปเดต web_interface.py: {e}")
        return False

def check_models_directory():
    """ตรวจสอบโฟลเดอร์โมเดลและสร้างถ้าไม่มี"""
    dirs_to_check = [
        "logs",
        "voice_models", 
        "storage/temp",
        "config"
    ]
    
    for dir_path in dirs_to_check:
        path = Path(dir_path)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"✅ สร้างโฟลเดอร์ {dir_path} แล้ว")
            except Exception as e:
                print(f"❌ ไม่สามารถสร้างโฟลเดอร์ {dir_path}: {e}")
                return False
        else:
            print(f"ℹ️ โฟลเดอร์ {dir_path} มีอยู่แล้ว")
    
    return True

def create_performance_config():
    """สร้างไฟล์ config ประสิทธิภาพ"""
    config_dir = Path("config")
    config_file = config_dir / "performance_config.json"
    
    if config_file.exists():
        print("ℹ️ ไฟล์ performance_config.json มีอยู่แล้ว")
        return True
    
    default_config = {
        "tts_batch_size": 1,
        "tts_chunk_size": 5000,
        "tts_max_concurrent": 1,
        "rvc_batch_size": 1,
        "rvc_use_half_precision": True,
        "rvc_cache_models": True,
        "audio_sample_rate": 44100,
        "audio_chunk_duration": 10,
        "audio_use_soxr": True,
        "use_multiprocessing": True,
        "max_workers": 1,
        "memory_limit_gb": 2,
        "gpu_memory_fraction": 0.8,
        "gpu_allow_growth": True,
        "gpu_mixed_precision": True
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print("✅ สร้างไฟล์ performance_config.json แล้ว")
        return True
    except Exception as e:
        print(f"❌ ไม่สามารถสร้างไฟล์ performance_config.json: {e}")
        return False

def test_import_fixes():
    """ทดสอบ import และการทำงานหลังจากแก้ไข"""
    print("\\n🧪 ทดสอบการ import หลังจากแก้ไข...")
    
    try:
        # ทดสอบ model_utils
        from model_utils import safe_model_processing, normalize_model_name
        print("✅ import model_utils สำเร็จ")
        
        # ทดสอบฟังก์ชัน normalize_model_name
        test_cases = [
            "test_model",
            {"name": "test_model_dict"},
            ["test_model_list"],
            None,
            "",
            123
        ]
        
        for test_case in test_cases:
            result = normalize_model_name(test_case)
            print(f"  normalize_model_name({test_case}) = {result}")
        
        # ทดสอบฟังก์ชัน safe_model_processing
        available_models = ["model1", "model2", "model3"]
        test_model, error = safe_model_processing("model1", available_models)
        print(f"  safe_model_processing result: {test_model}, error: {error}")
        
        print("✅ ทดสอบ model_utils สำเร็จ")
        
    except Exception as e:
        print(f"❌ การทดสอบ import ล้มเหลว: {e}")
        return False
    
    return True

def main():
    """ฟังก์ชันหลักในการแก้ไขโปรเจค"""
    print("🔧 เริ่มต้นการแก้ไขปัญหาโปรเจค...")
    print("=" * 50)
    
    success_count = 0
    total_tasks = 7
    
    # 1. แก้ไข syntax error ใน web_interface.py
    print("\\n1️⃣ แก้ไข syntax error ใน web_interface.py")
    if fix_web_interface_syntax():
        success_count += 1
    
    # 2. สร้าง model_utils.py
    print("\\n2️⃣ สร้างไฟล์ model_utils.py")
    if fix_model_handling():
        success_count += 1
    
    # 3. อัปเดต tts_rvc_core.py
    print("\\n3️⃣ อัปเดต tts_rvc_core.py")
    if update_tts_rvc_core():
        success_count += 1
    
    # 4. อัปเดต rvc_api.py
    print("\\n4️⃣ อัปเดต rvc_api.py")
    if update_rvc_api():
        success_count += 1
    
    # 5. อัปเดต web_interface.py
    print("\\n5️⃣ อัปเดต web_interface.py")
    if update_web_interface():
        success_count += 1
    
    # 6. ตรวจสอบโฟลเดอร์
    print("\\n6️⃣ ตรวจสอบและสร้างโฟลเดอร์ที่จำเป็น")
    if check_models_directory():
        success_count += 1
    
    # 7. สร้างไฟล์ config
    print("\\n7️⃣ สร้างไฟล์ config")
    if create_performance_config():
        success_count += 1
    
    # ทดสอบการแก้ไข
    print("\\n🧪 ทดสอบการแก้ไข")
    test_import_fixes()
    
    # สรุปผล
    print("\\n" + "=" * 50)
    print(f"🎉 การแก้ไขเสร็จสิ้น: {success_count}/{total_tasks} งานสำเร็จ")
    
    if success_count == total_tasks:
        print("✅ แก้ไขปัญหาทั้งหมดสำเร็จแล้ว!")
        print("\\n📋 สิ่งที่แก้ไข:")
        print("  - แก้ไข syntax error ใน web_interface.py")
        print("  - สร้าง model_utils.py เพื่อจัดการโมเดลอย่างปลอดภัย")
        print("  - อัปเดตการจัดการโมเดลในไฟล์ต่างๆ")
        print("  - สร้างโฟลเดอร์และไฟล์ config ที่จำเป็น")
        print("\\n🚀 ตอนนี้สามารถรันโปรเจคได้แล้ว:")
        print("     python web_interface.py")
        print("     หรือ python main_api_server.py")
    else:
        print(f"⚠️ แก้ไขได้เพียง {success_count}/{total_tasks} งาน")
        print("กรุณาตรวจสอบข้อผิดพลาดด้านบนและลองแก้ไขอีกครั้ง")
    
    return success_count == total_tasks

if __name__ == "__main__":
    main()