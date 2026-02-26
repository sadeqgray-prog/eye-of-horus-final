#!/data/data/com.termux/files/usr/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
END='\033[0m'

echo -e "${BLUE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 FIX FINAL - EYE OF HORUS DEPLOYMENT                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${END}"

# ==================== مرحله ۱: پاک کردن توکن از فایل ====================
echo -e "\n${YELLOW}[1/5] پاک کردن توکن از final_fix.sh...${END}"

if [ -f "final_fix.sh" ]; then
    sed -i '26s/YOUR_TOKEN_HERE.*/YOUR_GITHUB_TOKEN_HERE # REMOVED FOR SECURITY/' final_fix.sh
    echo -e "${GREEN}✅ توکن پاک شد${END}"
else
    echo -e "${YELLOW}⚠️ فایل final_fix.sh وجود نداره، ادامه می‌دیم...${END}"
fi

# ==================== مرحله ۲: اضافه کردن به گیت ====================
echo -e "\n${YELLOW}[2/5] اضافه کردن فایل به گیت...${END}"
git add final_fix.sh 2>/dev/null
echo -e "${GREEN}✅ فایل اضافه شد${END}"

# ==================== مرحله ۳: کامیت کردن ====================
echo -e "\n${YELLOW}[3/5] کامیت کردن تغییرات...${END}"
git commit -m "fix: remove token and final deploy" 2>/dev/null
echo -e "${GREEN}✅ کامیت انجام شد${END}"

# ==================== مرحله ۴: تنظیم ذخیره توکن ====================
echo -e "\n${YELLOW}[4/5] تنظیم Git Credential Helper...${END}"
git config --global credential.helper store
echo -e "${GREEN}✅ Git تنظیم شد برای ذخیره توکن${END}"

# ==================== مرحله ۵: push نهایی ====================
echo -e "\n${YELLOW}[5/5] ارسال به گیت‌هاب...${END}"
echo -e "${BLUE}⚠️ الآن ازت username و password می‌خواد:${END}"
echo -e "${BOLD}Username:${END} sadeqgray-prog"
echo -e "${BOLD}Password:${END} YOUR_TOKEN_HERE"
echo -e "${RED}🔔 توجه: وقتی password رو وارد می‌کنی، چیزی نشون داده نمی‌شه - این طبیعیه!${END}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}\n"

git push origin main

# ==================== بررسی نتیجه ====================
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✅✅✅ پوش با موفقیت انجام شد! ✅✅✅${END}"
    echo -e "\n${BLUE}⏱️  صبر کن ۲ دقیقه تا Railway دیپلوی کنه...${END}"
    echo -e "\n${YELLOW}بعد از ۲ دقیقه، این دستور رو بزن تا لاگ رو ببینی:${END}"
    echo -e "${BOLD}railway logs --service eye-of-horus --limit 30${END}"
    echo -e "\n${GREEN}ربات رو تست کن:${END}"
    echo -e "https://t.me/EyeOfHorusMiniBot"
else
    echo -e "\n${RED}❌ خطا در پوش!${END}"
    echo -e "${YELLOW}ممکنه مشکل از اینترنت باشه یا توکن اشتباه باشه. دوباره تلاش کن:${END}"
    echo -e "git push origin main"
fi
