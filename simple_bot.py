#!/usr/bin/env python3
import logging
import os
import time
from telegram import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('simple')

TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN not set")
    exit(1)

logger.info("✅ Simple test bot started")
logger.info(f"🤖 Bot token: {TOKEN[:10]}...")

# فقط یه بار یه پیام تست بده
import asyncio
import telegram

async def test():
    bot = telegram.Bot(TOKEN)
    me = await bot.get_me()
    logger.info(f"✅ Bot connected: @{me.username}")

asyncio.run(test())

# نگه داشتن
while True:
    logger.info("💓 Heartbeat...")
    time.sleep(60)
