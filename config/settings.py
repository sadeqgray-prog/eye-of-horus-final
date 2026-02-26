# config/settings.py
"""
تنظیمات اصلی ربات - Eye of Horus
"""

import os
from pathlib import Path

# ===== BOT INFO =====
BOT_NAME = "Eye of Horus"
BOT_VERSION = "∞"
BOT_CREATOR = "Al Hashash"
BOT_SYMBOL = "𓂀"

# ===== TELEGRAM =====
TELEGRAM_TOKEN = "8292269920:AAHkuDlHKRSPFJNNsqiv5Cb4WRfOo04aocg"
ADMIN_CHAT_ID = 6590867551

# ===== WALLET =====
WALLET_ADDRESS = "0x11096bccfc635a5467ccfa1ef2970bfb95bd1474"

# ===== API KEYS =====
COINGECKO_API_KEY = "CG-k55SRvbcKVHfecnavyFuAMeg"
NEWS_API_KEY = "6b0fc77978664ed695d2a69e68d89f38"

# ===== PRICING =====
PRICE_PER_PREDICTION = 0.32  # USDT
FREE_PREDICTIONS_FOR_VIP = 100  # تعداد پیش‌بینی رایگان برای VIP

# ===== PATHS =====
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MEMORY_DIR = BASE_DIR / "memory"
BACKUP_DIR = BASE_DIR / "backups"

# ===== EVOLUTION =====
EVOLUTION_SPEED = 1.0  # سرعت تکامل
MAX_EVOLUTION_STAGE = 1000
AUTO_EVOLVE = True

# ===== BACKUP =====
BACKUP_INTERVAL = 300  # seconds
KEEP_BACKUP_DAYS = 30
ENABLE_CONTINUOUS_BACKUP = True

# ===== SECURITY =====
ENABLE_ENCRYPTION = True
RATE_LIMIT = 30  # پیام در دقیقه
MAX_PREDICTIONS_PER_DAY = 100
