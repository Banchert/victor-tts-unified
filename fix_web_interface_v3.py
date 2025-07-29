#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_web_interface():
    """Fix the web_interface.py file by putting JavaScript outside f-string"""
    
    # Read the file
    with open('web_interface.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the f-string start
    fstring_start = content.find('html_content = f"""')
    if fstring_start == -1:
        print("❌ Could not find f-string start")
        return False
    
    # Find where the f-string should end (before the JavaScript code)
    js_start_pattern = r'    <script>\s*let currentAudio = null;'
    match = re.search(js_start_pattern, content)
    
    if not match:
        print("❌ Could not find JavaScript start")
        return False
    
    js_start_pos = match.start()
    
    # Extract the HTML part (everything before JavaScript)
    html_part = content[fstring_start + len('html_content = f"""'):js_start_pos]
    
    # Extract the JavaScript part
    js_part = content[js_start_pos:]
    
    # Find where the JavaScript ends and the return statement is
    return_pattern = r'\s*return html_content\s*'
    return_match = re.search(return_pattern, js_part)
    
    if not return_match:
        print("❌ Could not find return statement")
        return False
    
    js_end_pos = return_match.start()
    js_code = js_part[:js_end_pos]
    return_statement = js_part[js_end_pos:]
    
    # Reconstruct the file with JavaScript outside the f-string
    new_content = content[:fstring_start] + 'html_content = f"""' + html_part + '"""\n\n' + js_code + return_statement
    
    # Write the fixed content back
    with open('web_interface.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Fixed web_interface.py successfully!")
    return True

if __name__ == "__main__":
    fix_web_interface() 