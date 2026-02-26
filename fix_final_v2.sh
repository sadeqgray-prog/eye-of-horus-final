#!/data/data/com.termux/files/usr/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
END='\033[0m'

echo -e "${BLUE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 FIX FINAL V2 - COMPLETE RESET                           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${END}"

# ==================== مرحله ۱: پاک کردن اطلاعات قبلی گیت ====================
echo -e "\n${YELLOW}[1/6] پاک کردن اطلاعات قبلی گیت...${END}"

git config --global --unset credential.helper 2>/dev/null
rm -f ~/.git-credentials
rm -f ~/.config/git/credentials

echo -e "${GREEN}✅ اطلاعات قبلی پاک شد${END}"

# ==================== مرحله ۲: تنظیم مجدد اطلاعات کاربر ====================
echo -e "\n${YELLOW}[2/6] تنظیم اطلاعات کاربر جدید...${END}"

git config --global user.name "sadeqgray-prog"
git config --global user.email "sadeqgray@gmail.com"

echo -e "${GREEN}✅ اطلاعات تنظیم شد${END}"

# ==================== مرحله ۳: پاک کردن توکن از فایل ====================
echo -e "\n${YELLOW}[3/6] پاک کردن توکن از final_fix.sh...${END}"

if [ -f "final_fix.sh" ]; then
    sed -i 's/YOUR_TOKEN_HERE.*/YOUR_GITHUB_TOKEN_HERE # REMOVED FOR SECURITY/' final_fix.sh
    echo -e "${GREEN}✅ توکن پاک شد${END}"
else
    echo -e "${YELLOW}⚠️ فایل final_fix.sh وجود نداره${END}"
fi

# ==================== مرحله ۴: اضافه کردن و کامیت ====================
echo -e "\n${YELLOW}[4/6] اضافه کردن فایل به گیت...${END}"
git add final_fix.sh 2>/dev/null
git commit -m "fix: final clean version" 2>/dev/null
echo -e "${GREEN}✅ فایل آماده شد${END}"

# ==================== مرحله ۵: تنظیم remote با توکن مستقیم (یکبار مصرف) ====================
echo -e "\n${YELLOW}[5/6] تنظیم remote با توکن...${END}"

TOKEN="YOUR_TOKEN_HERE"
git remote remove origin
git remote add origin https://sadeqgray-prog:${TOKEN}@github.com/sadeqgray-prog/eye-of-horus.git

echo -e "${GREEN}✅ remote تنظیم شد${END}"

# ==================== مرحله ۶: push نهایی ====================
echo -e "\n${YELLOW}[6/6] ارسال به گیت‌هاب...${END}"
echo -e "${BLUE}⚠️ این بار با توکن مستقیم توی URL امتحان می‌کنیم...${END}\n"

git push -u origin main --force

# ==================== بررسی نتیجه ====================
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✅✅✅ پوش با موفقیت انجام شد! ✅✅✅${END}"
    
    # برگردوندن remote به حالت عادی
    git remote remove origin
    git remote add origin https://github.com/sadeqgray-prog/eye-of-horus.git
    
    echo -e "\n${BLUE}⏱️  صبر کن ۲ دقیقه تا Railway دیپلوی کنه...${END}"
    echo -e "\n${YELLOW}بعد از ۲ دقیقه، این دستور رو بزن تا لاگ رو ببینی:${END}"
    echo -e "${BOLD}railway logs --service eye-of-horus --limit 30${END}"
    echo -e "\n${GREEN}ربات رو تست کن:${END}"
    echo -e "https://t.me/EyeOfHorusMiniBot"
else
    echo -e "\n${RED}❌ خطا در پوش!${END}"
    echo -e "${YELLOW}ممکنه مشکل از اینترنت باشه. این دستور رو امتحان کن:${END}"
    echo -e "git push https://sadeqgray-prog:YOUR_TOKEN_HERE@github.com/sadeqgray-prog/eye-of-horus.git main --force"
fi
