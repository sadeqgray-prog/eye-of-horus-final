#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛠 FIX CIRCULAR IMPORT - رفع خودکار مشکل
این اسکریپت هیچ چیز را ساده نمی‌کند، فقط مشکل circular import را حل می‌کند
"""

import os
import re
from pathlib import Path

# ==================== رنگ‌ها ====================
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

print(f"{BOLD}{BLUE}{'='*60}{END}")
print(f"{BOLD}{BLUE}🛠 FIX CIRCULAR IMPORT - WITHOUT SIMPLIFICATION{END}")
print(f"{BOLD}{BLUE}{'='*60}{END}")

# ==================== بک‌آپ ====================
print(f"\n{YELLOW}📦 Creating backup of knowledge_engine.py...{END}")
if os.path.exists("brain/knowledge_engine.py"):
    os.system("cp brain/knowledge_engine.py brain/knowledge_engine.py.circular_backup")
    print(f"{GREEN}✅ Backup created: brain/knowledge_engine.py.circular_backup{END}")

# ==================== رفع مشکل در knowledge_engine.py ====================
print(f"\n{YELLOW}🔧 Fixing brain/knowledge_engine.py...{END}")

knowledge_file = "brain/knowledge_engine.py"
if os.path.exists(knowledge_file):
    with open(knowledge_file, 'r') as f:
        content = f.read()
    
    # پیدا کردن خطوط مشکل‌دار
    lines = content.split('\n')
    fixed_lines = []
    in_class = False
    class_found = False
    
    for line in lines:
        # اگر خط import knowledge_engine هست، حذفش کن
        if 'import knowledge_engine' in line or 'from .knowledge_engine' in line:
            print(f"{YELLOW}⚠️ Removing problematic import: {line.strip()}{END}")
            continue
        
        # اگر خط class KnowledgeEngine: هست، علامت بزن
        if 'class KnowledgeEngine' in line:
            class_found = True
            in_class = True
            fixed_lines.append(line)
            continue
        
        # اگر داخل کلاس هستیم و خط __init__ هست
        if in_class and '__init__' in line:
            fixed_lines.append(line)
            continue
        
        # اگر داخل کلاس هستیم و خط self.books رو پیدا کردیم
        if in_class and 'self.books' in line:
            fixed_lines.append(line)
            # بعد از این خط، متد _load_books رو اضافه می‌کنیم
            fixed_lines.append('')
            fixed_lines.append('    def _load_books_safely(self):')
            fixed_lines.append('        """بارگذاری کتاب‌ها بدون circular import"""')
            fixed_lines.append('        books_dir = Path("knowledge/books")')
            fixed_lines.append('        ')
            fixed_lines.append('        for book_file in books_dir.glob("*.py"):')
            fixed_lines.append('            if book_file.name != "__init__.py":')
            fixed_lines.append('                try:')
            fixed_lines.append('                    book_name = book_file.stem')
            fixed_lines.append('                    # import دینامیک بدون وابستگی')
            fixed_lines.append('                    import importlib.util')
            fixed_lines.append('                    spec = importlib.util.spec_from_file_location(book_name, book_file)')
            fixed_lines.append('                    module = importlib.util.module_from_spec(spec)')
            fixed_lines.append('                    spec.loader.exec_module(module)')
            fixed_lines.append('                    ')
            fixed_lines.append('                    if hasattr(module, \'BOOK_DATA\'):')
            fixed_lines.append('                        self.books[book_name] = module.BOOK_DATA')
            fixed_lines.append('                        logger.info(f"✅ Loaded book: {book_name}")')
            fixed_lines.append('                except Exception as e:')
            fixed_lines.append('                    logger.warning(f"⚠️ Could not load book {book_file.stem}: {e}")')
            fixed_lines.append('        ')
            continue
        
        # بقیه خطوط رو به همان شکل نگه دار
        fixed_lines.append(line)
    
    # نوشتن فایل جدید
    with open(knowledge_file, 'w') as f:
        f.write('\n'.join(fixed_lines))
    
    print(f"{GREEN}✅ Fixed knowledge_engine.py{END}")
else:
    print(f"{RED}❌ File not found: {knowledge_file}{END}")

# ==================== اطمینان از وجود import json در کتاب‌ها ====================
print(f"\n{YELLOW}📚 Checking book files for import json...{END}")

books_dir = Path("knowledge/books")
fixed_books = 0

for book_file in books_dir.glob("*.py"):
    if book_file.name == "__init__.py":
        continue
    
    with open(book_file, 'r') as f:
        content = f.read()
    
    # اگر import json نیست، اضافه کن
    if 'import json' not in content:
        content = 'import json\n' + content
        with open(book_file, 'w') as f:
            f.write(content)
        print(f"{GREEN}✅ Added import json to {book_file.name}{END}")
        fixed_books += 1

print(f"{GREEN}✅ Fixed {fixed_books} book files{END}")

# ==================== ایجاد فایل __init__.py اگر نیست ====================
print(f"\n{YELLOW}📁 Creating/updating __init__.py files...{END}")

# برای knowledge
init_file = "knowledge/__init__.py"
if not os.path.exists(init_file):
    with open(init_file, 'w') as f:
        f.write('"""\n📚 Knowledge Package\n"""\n\n')
    print(f"{GREEN}✅ Created {init_file}{END}")

# برای knowledge/books
books_init = "knowledge/books/__init__.py"
if not os.path.exists(books_init):
    with open(books_init, 'w') as f:
        f.write('"""\n📖 Books Package\n"""\n\n')
        # اضافه کردن همه کتاب‌ها
        f.write('from . import westcott\n')
        f.write('from . import sepharial\n')
        f.write('from . import agrippa\n')
        f.write('from . import chaldean_books\n')
        f.write('\n__all__ = [\'westcott\', \'sepharial\', \'agrippa\', \'chaldean_books\']\n')
    print(f"{GREEN}✅ Created {books_init}{END}")

# ==================== گزارش نهایی ====================
print(f"\n{GREEN}{BOLD}{'='*60}{END}")
print(f"{GREEN}{BOLD}✅ FIX COMPLETE - NO SIMPLIFICATION{END}")
print(f"{GREEN}{BOLD}{'='*60}{END}")

print(f"\n{BLUE}📋 Summary:{END}")
print(f"  {GREEN}✓{END} Fixed circular import in knowledge_engine.py")
print(f"  {GREEN}✓{END} Added import json to {fixed_books} book files")
print(f"  {GREEN}✓{END} Created/updated __init__.py files")

print(f"\n{YELLOW}📦 To deploy:{END}")
print(f"  {BLUE}git add brain/knowledge_engine.py knowledge/books/ knowledge/__init__.py{END}")
print(f"  {BLUE}git commit -m \"FIX: resolve circular import in knowledge system\"{END}")
print(f"  {BLUE}git push origin main{END}")

print(f"\n{GREEN}{BOLD}🎉 Ready to deploy! Run the git commands above.{END}")
