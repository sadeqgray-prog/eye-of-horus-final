#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 TEST BOT - نسخه تست برای اطمینان از کار کردن تلگرام
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.environ.get('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور start"""
    await update.message.reply_text("✅ ربات کار می‌کند!")

def main():
    """تابع اصلی"""
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN not found!")
        return
    
    print(f"✅ Token found: {TOKEN[:10]}...")
    
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلر
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Starting bot...")
    
    # اجرا
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
