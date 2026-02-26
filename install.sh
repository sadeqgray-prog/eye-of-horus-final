#!/data/data/com.termux/files/usr/bin/bash

# 𓂀 EYE OF HORUS INSTALLER 𓂀
# Created by: Al Hashash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  𓂀  EYE OF HORUS - THE ETERNAL ORACLE INSTALLER  𓂀  ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                  Created by: Al Hashash                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[1/8]${NC} Updating packages..."
pkg update && pkg upgrade -y

echo -e "${CYAN}[2/8]${NC} Installing Python and dependencies..."
pkg install python clang cmake libc++ ninja patchelf -y

echo -e "${CYAN}[3/8]${NC} Creating virtual environment..."
python -m venv venv
source venv/bin/activate

echo -e "${CYAN}[4/8]${NC} Upgrading pip..."
pip install --upgrade pip

echo -e "${CYAN}[5/8]${NC} Installing Python packages..."
pip install python-telegram-bot sqlalchemy alembic python-dotenv
pip install requests aiohttp beautifulsoup4
pip install numpy pandas scikit-learn
pip install nltk textblob vaderSentiment
pip install web3 eth-account ccxt pycoingecko
pip install tensorflow torch transformers
pip install cryptography psutil

echo -e "${CYAN}[6/8]${NC} Creating directory structure..."
mkdir -p logs data memory backups
mkdir -p modules/numerology modules/crypto modules/sports modules/events modules/ai modules/blockchain
mkdir -p knowledge/books knowledge/patterns knowledge/wisdom
mkdir -p api utils tests config

echo -e "${CYAN}[7/8]${NC} Setting up permissions..."
chmod +x main.py
chmod +x scripts/*.sh 2>/dev/null

echo -e "${CYAN}[8/8]${NC} Creating first backup..."
python -c "from core.eternal_backup import eternal_backup; eternal_backup.create_backup('complete', 'Initial installation')"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  𓂀  INSTALLATION COMPLETE!  𓂀  ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  To start the bot:                                          ║"
echo "║    source venv/bin/activate                                 ║"
echo "║    python main.py                                           ║"
echo "║                                                              ║"
echo "║  To run in background:                                      ║"
echo "║    nohup python main.py > bot.log 2>&1 &                    ║"
echo "║                                                              ║"
echo "║  First backup created successfully!                         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
