"""
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
