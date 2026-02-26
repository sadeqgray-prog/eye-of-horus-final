#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
𓂀 EYE OF HORUS - THE LIVING ORACLE - VERSION FINAL 𓂀
نسخه نهایی با تمام بخش‌های متصل
"""

import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# ===== تنظیم لاگ =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('main')

# ===== اضافه کردن مسیر =====
sys.path.append(str(Path(__file__).parent))

def main():
    """تابع اصلی"""
    logger.info("="*50)
    logger.info("🚀 Eye of Horus Bot Started")
    logger.info("="*50)
    
    # چک کردن توکن
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        logger.error("❌ TELEGRAM_TOKEN not found!")
        return
    
    logger.info(f"✅ TELEGRAM_TOKEN found (length: {len(token)})")
    
    try:
        # ایمپورت ربات اصلی
        from bot.ultimate_bot import UltimateBot
        bot = UltimateBot()
        bot.run()
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.info("💡 Make sure bot/ultimate_bot.py exists")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
