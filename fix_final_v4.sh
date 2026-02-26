#!/data/data/com.termux/files/usr/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
END='\033[0m'

echo -e "${BLUE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 FIX FINAL V4 - SSH SETUP WITH GUIDANCE                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${END}"

# ==================== مرحله ۱: نشون دادن کلید SSH ====================
echo -e "\n${YELLOW}[1/4] نمایش کلید SSH برای اضافه کردن به گیت‌هاب...${END}"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${END}"
echo -e "${BOLD}🔑 کلید SSH شما (این رو کپی کن):${END}"
echo -e "${GREEN}$(cat ~/.ssh/id_ed25519.pub)${END}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${END}"

echo -e "\n${YELLOW}🌐 حالا این کارها رو انجام بده:${END}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}"
echo "1. برو به: https://github.com/settings/ssh/new"
echo "2. توی کادر Title یه اسم بذار: termux-ultimate"
echo "3. توی کادر Key، کلید بالا رو Paste کن (کلیک راست → Paste)"
echo "4. دکمه سبز Add SSH Key رو بزن"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}"

echo -e "\n${YELLOW}⏳ بعد از اضافه کردن کلید، اینجا Enter بزن...${END}"
read -p ""

# ==================== مرحله ۲: تست SSH ====================
echo -e "\n${YELLOW}[2/4] تست اتصال SSH به گیت‌هاب...${END}"
ssh -T git@github.com -o StrictHostKeyChecking=accept-new 2>&1 | grep -v "Warning"

if [ $? -eq 1 ]; then  # 1 یعنی success برای ssh -T
    echo -e "${GREEN}✅ SSH اتصال برقرار شد!${END}"
else
    echo -e "${RED}❌ SSH هنوز کار نمی‌کنه. دوباره تلاش کن.${END}"
    exit 1
fi

# ==================== مرحله ۳: تغییر remote به SSH ====================
echo -e "\n${YELLOW}[3/4] تغییر remote به SSH...${END}"
git remote remove origin
git remote add origin git@github.com:sadeqgray-prog/eye-of-horus.git
echo -e "${GREEN}✅ remote تغییر کرد${END}"

# ==================== مرحله ۴: push نهایی ====================
echo -e "\n${YELLOW}[4/4] ارسال به گیت‌هاب با SSH...${END}"
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✅✅✅ پوش با موفقیت انجام شد! ✅✅✅${END}"
    echo -e "\n${BLUE}⏱️  صبر کن ۲ دقیقه تا Railway دیپلوی کنه...${END}"
    echo -e "\n${YELLOW}بعد از ۲ دقیقه، این دستور رو بزن:${END}"
    echo -e "${BOLD}railway logs --service eye-of-horus --limit 30${END}"
    echo -e "\n${GREEN}ربات رو تست کن:${END} https://t.me/EyeOfHorusMiniBot"
else
    echo -e "\n${RED}❌ بازم خطا داد!${END}"
    echo -e "${YELLOW}از روش توکن مستقیم استفاده کن:${END}"
    echo -e "git push https://sadeqgray-prog:YOUR_TOKEN_HERE@github.com/sadeqgray-prog/eye-of-horus.git main --force"
fi
