#!/data/data/com.termux/files/usr/bin/bash

# 🚀 نصب خودکار سیستم دیپلوی

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  𓂀  INSTALL AUTO DEPLOYER  𓂀  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ==================== مرحله ۱: نصب پیش‌نیازها ====================
echo -e "${YELLOW}[1/7] Installing prerequisites...${NC}"

pkg update && pkg upgrade -y
pkg install python nodejs git openssh termux-services -y

# ==================== مرحله ۲: نصب Railway CLI ====================
echo -e "${YELLOW}[2/7] Installing Railway CLI...${NC}"

npm install -g @railway/cli

# ==================== مرحله ۳: نصب کتابخونه‌های پایتون ====================
echo -e "${YELLOW}[3/7] Installing Python packages...${NC}"

pip install deepseek-chat aiohttp python-telegram-bot

# ==================== مرحله ۴: تنظیم بوت خودکار ====================
echo -e "${YELLOW}[4/7] Setting up auto-boot...${NC}"

# نصب Termux:Boot
pkg install termux-services -y

# ایجاد پوشه boot
mkdir -p ~/.termux/boot

# کپی اسکریپت بوت
cp termux_boot.sh ~/.termux/boot/

chmod +x ~/.termux/boot/termux_boot.sh

# ==================== مرحله ۵: راه‌اندازی سرویس‌ها ====================
echo -e "${YELLOW}[5/7] Starting services...${NC}"

# فعال‌سازی SSH برای دسترسی از راه دور
sshd

# ==================== مرحله ۶: تنظیم Railway ====================
echo -e "${YELLOW}[6/7] Setting up Railway...${NC}"

railway login

# ==================== مرحله ۷: راه‌اندازی نهایی ====================
echo -e "${YELLOW}[7/7] Final setup...${NC}"

# ایجاد پوشه‌های لازم
mkdir -p logs memory backups

# اجرای تست
python -c "from auto_deployer import DeepSeekAutoDeployer; print('✅ AutoDeployer imported successfully')"

# ==================== پایان ====================
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✅ INSTALLATION COMPLETE!  ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Next steps:                                                ║"
echo "║  1. Run: ./startup.sh                                        ║"
echo "║  2. The bot will auto-start on every boot                   ║"
echo "║  3. AutoDeployer will monitor and fix errors                ║"
echo "║  4. Railway auto-deploy enabled                             ║"
echo "║                                                              ║"
echo "║  Commands:                                                   ║"
echo "║  • ./startup.sh          - Start manually                    ║"
echo "║  • ./startup.sh status   - Check status                      ║"
echo "║  • python auto_deployer.py - Run deployer manually           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
