#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Ultimate Bot - Simple Class Version"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8762873121:AAEnSClZaYQETAmJxQk6RNQo4Uauo2dSw-4"

class UltimateBot:
    """کلاس اصلی ربات"""
    
    def __init__(self):
        self.token = TOKEN
        logger.info("✅ UltimateBot initialized")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /start"""
        await update.message.reply_text("✅ ربات کار می‌کند!")
    
    def run(self):
        """اجرای ربات"""
        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler("start", self.start_command))
        logger.info("🚀 ربات شروع به کار کرد...")
        app.run_polling()

if __name__ == "__main__":
    bot = UltimateBot()
    bot.run()
