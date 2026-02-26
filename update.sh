#!/data/data/com.termux/files/usr/bin/bash

# 𓂀 EYE OF HORUS UPDATER 𓂀

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}𓂀 Updating Eye of Horus...${NC}"

# بک‌آپ قبل از آپدیت
echo -e "${YELLOW}📦 Creating pre-update backup...${NC}"
python -c "from core.eternal_backup import eternal_backup; eternal_backup.create_backup('complete', 'Pre-update backup')"

# آپدیت از git
echo -e "${YELLOW}🔄 Pulling latest changes...${NC}"
git pull origin main

# آپدیت پکیج‌ها
echo -e "${YELLOW}📦 Updating packages...${NC}"
source venv/bin/activate
pip install --upgrade -r requirements.txt

# بک‌آپ بعد از آپدیت
echo -e "${YELLOW}📦 Creating post-update backup...${NC}"
python -c "from core.eternal_backup import eternal_backup; eternal_backup.create_backup('consciousness', 'Post-update backup')"

echo -e "${GREEN}✅ Update complete!${NC}"
