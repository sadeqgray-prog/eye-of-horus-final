#!/data/data/com.termux/files/usr/bin/bash

# 📚 نصب سیستم مدیریت دانش

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  📚  INSTALL KNOWLEDGE MANAGEMENT SYSTEM  📚  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# نصب کتابخونه‌ها
echo -e "${YELLOW}[1/3] Installing Python packages...${NC}"
pip install -r requirements-knowledge.txt

# ایجاد پوشه‌ها
echo -e "${YELLOW}[2/3] Creating directories...${NC}"
mkdir -p knowledge/raw knowledge/processed knowledge/books

# دانلود NLTK data
echo -e "${YELLOW}[3/3] Downloading NLTK data...${NC}"
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ INSTALLATION COMPLETE!  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
