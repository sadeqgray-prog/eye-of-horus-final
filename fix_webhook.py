#!/usr/bin/env python3
"""
🛠 Auto-Fix Webhook for Railway
این اسکریپت خودکار فایل ربات رو برای Railway آماده می‌کنه
"""

import re
import os
from pathlib import Path

def fix_bot_file():
    """اصلاح خودکار فایل ultimate_bot.py برای Railway"""
    
    bot_file = Path("bot/ultimate_bot.py")
    
    if not bot_file.exists():
        print(f"❌ فایل {bot_file} پیدا نشد!")
        return False
    
    # خوندن فایل
    with open(bot_file, 'r') as f:
        content = f.read()
    
    # الگوی جستجو برای run_polling
    pattern = r'self\.application\.run_polling\(\)'
    
    if not re.search(pattern, content):
        print("✅ فایل از قبل اصلاح شده!")
        return True
    
    # پیدا کردن خطوط مربوط به run
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if 'def run(self):' in line:
            new_lines.append(line)
            i += 1
            
            # جمع‌آوری خطوط تا رسیدن به run_polling
            run_lines = []
            while i < len(lines) and 'run_polling' not in lines[i]:
                run_lines.append(lines[i])
                i += 1
            
            # رد شدن از خط run_polling
            if i < len(lines) and 'run_polling' in lines[i]:
                i += 1
            
            # اضافه کردن کد جدید webhook
            new_lines.extend(run_lines)
            new_lines.append('        # استفاده از webhook برای Railway')
            new_lines.append('        import os')
            new_lines.append('        port = int(os.getenv("PORT", 8080))')
            new_lines.append('        webhook_url = f"https://blissful-youthfulness.up.railway.app/{TOKEN}"')
            new_lines.append('        ')
            new_lines.append('        self.application.run_webhook(')
            new_lines.append('            listen="0.0.0.0",')
            new_lines.append('            port=port,')
            new_lines.append('            url_path=TOKEN,')
            new_lines.append('            webhook_url=webhook_url')
            new_lines.append('        )')
        else:
            new_lines.append(line)
            i += 1
    
    # ذخیره فایل جدید
    new_content = '\n'.join(new_lines)
    
    # بک‌آپ از فایل اصلی
    backup_file = bot_file.with_suffix('.py.backup')
    with open(backup_file, 'w') as f:
        f.write(content)
    print(f"✅ بک‌آپ ساخته شد: {backup_file}")
    
    # نوشتن فایل جدید
    with open(bot_file, 'w') as f:
        f.write(new_content)
    
    print("✅ فایل با موفقیت اصلاح شد!")
    return True

def check_telegram_token():
    """بررسی وجود توکن تلگرام"""
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("⚠️ توکن تلگرام تنظیم نشده!")
        token = "8514604498:AAHYphaxoNZYB_cWNvkJm2I1-vCwQgNCTr0"
        print(f"✅ توکن تنظیم شد: {token[:15]}...")
        return token
    return token

def add_to_git():
    """اضافه کردن تغییرات به گیت"""
    import subprocess
    
    try:
        subprocess.run(['git', 'add', 'bot/ultimate_bot.py'], check=True)
        subprocess.run(['git', 'commit', '-m', '🛠 auto-fix: change polling to webhook for Railway'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ تغییرات با موفقیت به گیت پوش شد!")
    except Exception as e:
        print(f"⚠️ خطا در پوش به گیت: {e}")

def main():
    print("=" * 50)
    print("🛠 Auto-Fix Webhook Tool v1.0")
    print("=" * 50)
    
    # ۱. چک کردن توکن
    token = check_telegram_token()
    
    # ۲. اصلاح فایل
    if fix_bot_file():
        print("\n✅ فایل با موفقیت اصلاح شد!")
        print("\n📝 تغییرات اعمال شده:")
        print("   - run_polling() → run_webhook()")
        print("   - اضافه شدن پورت 8080")
        print("   - تنظیم webhook_url")
        
        # ۳. پرسش برای پوش به گیت
        answer = input("\n❓ تغییرات به گیت پوش بشه؟ (y/n): ")
        if answer.lower() == 'y':
            add_to_git()
    
    print("\n✅ کار تمام شد! ربات ۲ دقیقه دیگه روی Railway راه می‌افته.")
    print("📱 برو به: https://t.me/EyeOfHorusProBot")

if __name__ == "__main__":
    main()
