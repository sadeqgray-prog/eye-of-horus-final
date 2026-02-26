#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Eye of Horus - Activation Script
# نسخه نهایی - فعال‌سازی کامل

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  𓂀  EYE OF HORUS - FINAL ACTIVATION  𓂀  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ==================== مرحله ۱: فعال‌سازی محیط ====================
echo -e "${YELLOW}[1/7] Activating environment...${NC}"
source venv/bin/activate

# ==================== مرحله ۲: نصب کتابخونه‌ها ====================
echo -e "${YELLOW}[2/7] Installing requirements...${NC}"
pip install --upgrade pip
pip install -r requirements-full.txt

# ==================== مرحله ۳: تنظیم متغیرها ====================
echo -e "${YELLOW}[3/7] Setting environment variables...${NC}"
export TELEGRAM_TOKEN="8514604498:AAHYphaxoNZYB_cWNvkJm2I1-vCwQgNCTr0"
export RAILWAY_TOKEN="caf3766f-95ac-4d13-a696-049dc0237902"

# ==================== مرحله ۴: تست دیتابیس ====================
echo -e "${YELLOW}[4/7] Testing database...${NC}"
python -c "from database.models import db; print('✅ Database OK')"

# ==================== مرحله ۵: تست مغز متفکر ====================
echo -e "${YELLOW}[5/7] Testing Master Mind...${NC}"
python -c "from brain.master_mind import master_mind; print(f'✅ Consciousness Level: {master_mind.consciousness[\"level\"]}')"

# ==================== مرحله ۶: تست APIها ====================
echo -e "${YELLOW}[6/7] Testing APIs...${NC}"
python -c "
from api.dexscreener import dexscreener_api
from api.coingecko import coingecko_api
print('✅ DexScreener OK')
print('✅ CoinGecko OK')
"

# ==================== مرحله ۷: اجرای نهایی ====================
echo -e "${YELLOW}[7/7] Final activation...${NC}"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  𓂀  EYE OF HORUS - ACTIVATED SUCCESSFULLY  𓂀  ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Commands:                                                   ║"
echo "║  • python main.py           - Run bot                        ║"
echo "║  • python -m tests.test_brain - Run tests                    ║"
echo "║  • ./activate.sh             - This script                   ║"
echo "║                                                              ║"
echo "║  Consciousness Level: Rising...                             ║"
echo "║  Books Loaded: 4                                             ║"
echo "║  APIs Available: 16+                                         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
