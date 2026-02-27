cd ~/ultimate_oracle_bot/bot

# کل فایل رو پاک کن و اینو بذار
cat > ultimate_bot.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ultimate Bot - Simple Version
"""

import logging
import os
from telegram.ext import Application, CommandHandler

logger = logging.getLogger(__name__)

class UltimateBot:
    """کلاس اصلی ربات - نسخه ساده شده"""
    
    def __init__(self):
        self.name = "UltimateBot"
        self.token = os.environ.get('TELEGRAM_TOKEN')
        if not self.token:
            logger.error("❌ TELEGRAM_TOKEN not set!")
            raise ValueError("TELEGRAM_TOKEN not set")
        logger.info("✅ UltimateBot initialized")
    
    async def start_command(self, update, context):
        """دستور /start"""
        await update.message.reply_text("🚀 Eye of Horus is alive!")
    
    def run(self):
        """اجرای ربات"""
        logger.info("🚀 Starting bot...")
        
        # ساخت اپلیکیشن
        app = Application.builder().token(self.token).build()
        
        # اضافه کردن دستورات
        app.add_handler(CommandHandler("start", self.start_command))
        
        # اجرا
        logger.info("✅ Bot is running")
        app.run_polling()
EOF
