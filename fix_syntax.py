#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def fix_web_interface():
    """Fix the syntax errors in web_interface.py"""
    
    # Read the file
    with open('web_interface.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First, fix quadruple braces
    content = re.sub(r'{{{{', '{', content)
    content = re.sub(r'}}}}', '}', content)
    
    # Then fix triple braces
    content = re.sub(r'{{{', '{', content)
    content = re.sub(r'}}}', '}', content)
    
    # Then fix double braces
    content = re.sub(r'{{', '{', content)
    content = re.sub(r'}}', '}', content)
    
    # Now we need to properly escape CSS braces in the f-string
    # Find the CSS section and escape the braces
    css_start = content.find('<style>')
    css_end = content.find('</style>')
    
    if css_start != -1 and css_end != -1:
        css_section = content[css_start:css_end]
        # Escape single braces in CSS
        css_section = re.sub(r'([^}])\{([^}])', r'\1{{\2', css_section)
        css_section = re.sub(r'([^{])\}([^{])', r'\1}}\2', css_section)
        content = content[:css_start] + css_section + content[css_end:]
    
    # Write the fixed content back
    with open('web_interface.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed web_interface.py syntax errors")

if __name__ == "__main__":
    fix_web_interface() 