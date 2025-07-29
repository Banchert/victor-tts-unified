#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_web_interface():
    """Fix the web_interface.py file by properly structuring the f-string"""
    
    # Read the file
    with open('web_interface.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where the f-string should end (before the JavaScript code)
    # Look for the pattern where the HTML ends and JavaScript begins
    js_start_pattern = r'    <script>\s*let currentAudio = null;'
    match = re.search(js_start_pattern, content)
    
    if match:
        js_start_pos = match.start()
        
        # Find the f-string start
        fstring_start = content.find('html_content = f"""')
        if fstring_start != -1:
            # Extract the HTML part (everything before JavaScript)
            html_part = content[fstring_start + len('html_content = f"""'):js_start_pos]
            
            # Extract the JavaScript part
            js_part = content[js_start_pos:]
            
            # Find where the JavaScript ends and the return statement is
            return_pattern = r'\s*return html_content\s*'
            return_match = re.search(return_pattern, js_part)
            
            if return_match:
                js_end_pos = return_match.start()
                js_code = js_part[:js_end_pos]
                return_statement = js_part[js_end_pos:]
                
                # Reconstruct the file with proper f-string structure
                new_content = content[:fstring_start] + 'html_content = f"""' + html_part + '"""\n\n' + js_code + return_statement
                
                # Write the fixed content back
                with open('web_interface.py', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Fixed web_interface.py successfully!")
                return True
    
    print("❌ Could not find the proper structure to fix")
    return False

if __name__ == "__main__":
    fix_web_interface() 