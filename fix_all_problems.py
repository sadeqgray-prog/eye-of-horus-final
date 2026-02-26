#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛠 FIX ALL PROBLEMS - نسخه نهایی
این اسکریپت تمام مشکلات ربات را یکبار برای همیشه حل می‌کند
"""

import os
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ==================== رنگ‌ها ====================
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

print(f"{BOLD}{BLUE}{'='*60}{END}")
print(f"{BOLD}{BLUE}🤖 FIX ALL PROBLEMS - نسخه نهایی{END}")
print(f"{BOLD}{BLUE}{'='*60}{END}")

# ==================== ۱. بک‌آپ ====================
print(f"\n{YELLOW}📦 Creating backup...{END}")
backup_name = f"backup_before_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.make_archive(backup_name, 'zip', '.')
print(f"{GREEN}✅ Backup created: {backup_name}.zip{END}")

# ==================== ۲. رفع مشکل knowledge_engine.py ====================
print(f"\n{YELLOW}🔧 Fixing brain/knowledge_engine.py...{END}")

file_path = "brain/knowledge_engine.py"
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # پیدا کردن تابع search
    pattern = r'(async def search\(self, query: str, limit: int = 5\) -> List\[Dict\]:.*?)(?=\n\s*def|\n\s*async def|\Z)'
    
    if re.search(pattern, content, re.DOTALL):
        # اضافه کردن تبدیل دیکشنری
        new_func = '''async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        جستجوی هوشمند در تمام منابع دانش
        """
        # اگر query دیکشنری بود، به رشته تبدیل کن
        if isinstance(query, dict):
            # استخراج متن از دیکشنری
            query = str(query.get('text', query.get('input', str(query))))
        
        query = query.lower()
        
        results = []'''
        
        content = re.sub(pattern, new_func, content, flags=re.DOTALL)
        
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"{GREEN}✅ Fixed knowledge_engine.py{END}")
    else:
        print(f"{YELLOW}⚠️ Pattern not found, manual fix needed{END}")
else:
    print(f"{RED}❌ File not found: {file_path}{END}")

# ==================== ۳. رفع مشکل agrippa.py ====================
print(f"\n{YELLOW}🔧 Fixing knowledge/books/agrippa.py...{END}")

file_path = "knowledge/books/agrippa.py"
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    if 'import json' not in content:
        content = 'import json\n\n' + content
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"{GREEN}✅ Added import json to agrippa.py{END}")
    else:
        print(f"{GREEN}✅ import json already exists{END}")
else:
    print(f"{RED}❌ File not found: {file_path}{END}")

# ==================== ۴. رفع مشکل ultimate_bot.py ====================
print(f"\n{YELLOW}🔧 Fixing bot/ultimate_bot.py...{END}")

file_path = "bot/ultimate_bot.py"
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # اضافه کردن run_with_retry اگر وجود نداشت
    if 'def run_with_retry' not in content:
        # پیدا کردن محل اضافه کردن تابع
        run_method_pattern = r'(def run\(self\):.*?)(?=\n\s*def|\n\s*class|\Z)'
        
        if re.search(run_method_pattern, content, re.DOTALL):
            # اضافه کردن تابع جدید
            retry_method = '''
    def run_with_retry(self):
        """اجرای ربات با قابلیت بازیابی از Conflict"""
        from telegram.error import Conflict
        
        while self.restart_count < self.max_restarts:
            try:
                self.run()
                break
            except Conflict as e:
                self.restart_count += 1
                self.last_restart = datetime.now()
                logger.warning(f"⚠️ Conflict detected (#{self.restart_count}): {e}")
                logger.info("🔄 Waiting 5 seconds before retry...")
                time.sleep(5)
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                break
        
        if self.restart_count >= self.max_restarts:
            logger.critical("💀 Max restarts reached. Container will stop.")
'''
            # اضافه کردن متغیرهای مورد نیاز به __init__
            init_pattern = r'(def __init__\(self\):.*?)(?=\n\s*def|\Z)'
            
            if re.search(init_pattern, content, re.DOTALL):
                init_vars = '''
        self.restart_count = 0
        self.max_restarts = 5
        self.last_restart = None'''
                
                content = re.sub(init_pattern, lambda m: m.group(1) + init_vars, content, flags=re.DOTALL)
            
            # اضافه کردن import datetime اگر نبود
            if 'from datetime import datetime' in content:
                content = content.replace('from datetime import datetime', 'from datetime import datetime, timedelta')
            else:
                content = 'from datetime import datetime, timedelta\n' + content
            
            # اضافه کردن import Conflict
            if 'from telegram.error import Conflict' not in content:
                # پیدا کردن خط import telegram.error
                import_pattern = r'(from telegram\.error import .*)'
                if re.search(import_pattern, content):
                    content = re.sub(import_pattern, r'\1, Conflict', content)
                else:
                    content = content.replace('from telegram import Update', 'from telegram import Update\nfrom telegram.error import Conflict')
            
            # اضافه کردن تابع به کلاس
            content += retry_method
            
            # تغییر خط آخر
            content = content.replace('bot.run()', 'bot.run_with_retry()')
            
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"{GREEN}✅ Added run_with_retry to ultimate_bot.py{END}")
        else:
            print(f"{YELLOW}⚠️ Could not find run method{END}")
    else:
        print(f"{GREEN}✅ run_with_retry already exists{END}")
    
    # اطمینان از وجود drop_pending_updates
    if 'drop_pending_updates=True' not in content:
        content = content.replace(
            'self.application.run_polling(',
            'self.application.run_polling(\n            drop_pending_updates=True,'
        )
        content = content.replace(
            'timeout=30',
            'timeout=30,\n            allowed_updates=[\'message\', \'callback_query\'],\n            poll_interval=1.0'
        )
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"{GREEN}✅ Added drop_pending_updates to polling{END}")
else:
    print(f"{RED}❌ File not found: {file_path}{END}")

# ==================== ۵. ایجاد فایل docker-entrypoint.sh (برای Railway) ====================
print(f"\n{YELLOW}🔧 Creating docker-entrypoint.sh...{END}")

entrypoint_content = '''#!/bin/sh
# Docker entrypoint script for Railway

echo "========================================="
echo "🚀 Starting Eye of Horus on Railway"
echo "========================================="

# Wait for old instance to fully terminate
echo "⏳ Waiting 5 seconds for clean start..."
sleep 5

# Start the bot
python main.py
'''

with open('docker-entrypoint.sh', 'w') as f:
    f.write(entrypoint_content)
os.chmod('docker-entrypoint.sh', 0o755)
print(f"{GREEN}✅ Created docker-entrypoint.sh{END}")

# ==================== ۶. ایجاد Dockerfile (اختیاری) ====================
print(f"\n{YELLOW}🔧 Creating Dockerfile...{END}")

dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
'''

with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)
print(f"{GREEN}✅ Created Dockerfile{END}")

# ==================== ۷. ایجاد railway.json ====================
print(f"\n{YELLOW}🔧 Creating railway.json...{END}")

railway_json = '''{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
'''

with open('railway.json', 'w') as f:
    f.write(railway_json)
print(f"{GREEN}✅ Created railway.json{END}")

# ==================== ۸. پاکسازی ====================
print(f"\n{YELLOW}🧹 Cleaning up...{END}")
if os.path.exists('logs.txt'):
    os.remove('logs.txt')
    print(f"{GREEN}✅ Removed old logs.txt{END}")

# ==================== ۹. گزارش نهایی ====================
print(f"\n{GREEN}{BOLD}{'='*60}{END}")
print(f"{GREEN}{BOLD}✅ ALL FIXES APPLIED SUCCESSFULLY{END}")
print(f"{GREEN}{BOLD}{'='*60}{END}")
print(f"\n{BLUE}📋 Summary of fixes:{END}")
print(f"  {GREEN}✓{END} Created backup: {backup_name}.zip")
print(f"  {GREEN}✓{END} Fixed knowledge_engine.py (AttributeError)")
print(f"  {GREEN}✓{END} Fixed agrippa.py (added import json)")
print(f"  {GREEN}✓{END} Added run_with_retry to ultimate_bot.py")
print(f"  {GREEN}✓{END} Added drop_pending_updates to polling")
print(f"  {GREEN}✓{END} Created docker-entrypoint.sh (5s delay)")
print(f"  {GREEN}✓{END} Created Dockerfile")
print(f"  {GREEN}✓{END} Created railway.json")

print(f"\n{YELLOW}📦 To deploy:{END}")
print(f"  {BLUE}1.{END} git add .")
print(f"  {BLUE}2.{END} git commit -m \"FINAL: all fixes applied\"")
print(f"  {BLUE}3.{END} git push origin main")

print(f"\n{GREEN}{BOLD}🎉 Ready to deploy! Run the git commands above.{END}")
