#!/usr/bin/env python3
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = "8762873121:AAEnSClZaYQETAmJxQk6RNQo4Uauo2dSw-4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات کار می‌کنه!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 ربات ساده شروع به کار کرد...")
    app.run_polling()

if __name__ == "__main__":
    main()
