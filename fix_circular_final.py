#!/usr/bin/env python3
"""
🛠 FIX CIRCULAR IMPORT FINAL
"""

import os
import re

print("🔧 Fixing circular import in knowledge_engine.py...")

file_path = "brain/knowledge_engine.py"
with open(file_path, 'r') as f:
    content = f.read()

# حذف هرگونه import خودارجاعی
content = re.sub(r'from\s+\.\s*import\s+knowledge_engine', '', content)
content = re.sub(r'import\s+knowledge_engine', '', content)

# اضافه کردن import های لازم
if 'import importlib.util' not in content:
    content = 'import importlib.util\n' + content
if 'from pathlib import Path' not in content:
    content = 'from pathlib import Path\n' + content

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Circular import fixed")
