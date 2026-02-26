#!/data/data/com.termux/files/usr/bin/bash

# 🛠 FIX GLASSNODE IMPORT - WITHOUT SIMPLIFICATION
# این اسکریپت فقط خط مربوط به glassnode رو حذف می‌کنه
# هیچ چیز دیگه‌ای تغییر نمی‌کنه

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🔧 Fixing glassnode import issue...${NC}"

# ===== بک‌آپ =====
cp bot/ultimate_bot.py bot/ultimate_bot.py.glassnode_backup
echo -e "${GREEN}✅ Backup created: ultimate_bot.py.glassnode_backup${NC}"

# ===== حذف خط glassnode =====
grep -v "from api.glassnode import" bot/ultimate_bot.py > bot/ultimate_bot_temp.py
grep -v "glassnode_api" bot/ultimate_bot_temp.py > bot/ultimate_bot.py
rm bot/ultimate_bot_temp.py

echo -e "${GREEN}✅ Removed glassnode import${NC}"

# ===== چک کردن نتیجه =====
if grep -q "glassnode" bot/ultimate_bot.py; then
    echo -e "${RED}❌ Glassnode still exists!${NC}"
else
    echo -e "${GREEN}✅ Glassnode successfully removed${NC}"
fi

# ===== commit و push =====
echo -e "${YELLOW}📦 Committing changes...${NC}"
git add bot/ultimate_bot.py
git commit -m "FIX: remove glassnode import (module not exists)"
git push origin main

echo -e "${GREEN}✅ Done! Changes pushed to GitHub${NC}"
echo -e "${YELLOW}⏳ Waiting 2 minutes for Railway to deploy...${NC}"
