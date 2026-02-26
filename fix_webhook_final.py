#!/usr/bin/env python3
"""
🛠 فیکس نهایی Webhook برای Railway
"""

import re

print("="*50)
print("🔧 Webhook Fixer - نسخه نهایی")
print("="*50)

# خوندن فایل
with open('bot/ultimate_bot.py', 'r') as f:
    content = f.read()

# پیدا کردن تابع run
if 'def run(self):' not in content:
    print("❌ تابع run پیدا نشد!")
    exit(1)

# پشتیبان گیری
with open('bot/ultimate_bot.py.backup', 'w') as f:
    f.write(content)
print("✅ بک‌آپ گرفته شد: bot/ultimate_bot.py.backup")

# جایگزینی run_polling با webhook
if 'self.application.run_polling()' in content:
    new_content = content.replace(
        'self.application.run_polling()',
        '''        # Webhook for Railway
        import os
        port = int(os.getenv('PORT', 8080))
        webhook_url = f"https://blissful-youthfulness.up.railway.app/{os.getenv('TELEGRAM_TOKEN')}"
        
        print(f"🌐 Starting webhook on port {port}")
        print(f"🔗 Webhook URL: {webhook_url}")
        
        self.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=os.getenv('TELEGRAM_TOKEN'),
            webhook_url=webhook_url
        )'''
    )
    
    with open('bot/ultimate_bot.py', 'w') as f:
        f.write(new_content)
    print("✅ فایل با موفقیت اصلاح شد (run_polling → run_webhook)")
else:
    print("⚠️ run_polling پیدا نشد! ممکنه قبلاً اصلاح شده باشه")

print("\n📋 مراحل بعدی:")
print("1. git add bot/ultimate_bot.py")
print("2. git commit -m 'fix: change to webhook for railway'")
print("3. git push origin main")
print("4. صبر کن ۲ دقیقه")
print("5. ربات تلگرام رو تست کن")
