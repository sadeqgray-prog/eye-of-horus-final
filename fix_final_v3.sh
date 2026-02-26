#!/data/data/com.termux/files/usr/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
END='\033[0m'

echo -e "${BLUE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🚀 FIX FINAL V3 - ULTIMATE SOLUTION                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${END}"

# ==================== مرحله ۱: پاک کردن EVERYTHING ====================
echo -e "\n${YELLOW}[1/7] پاک کردن کامل اطلاعات گیت از سیستم...${END}"

rm -rf ~/.gitconfig
rm -rf ~/.git-credentials
rm -rf ~/.config/git
unset GIT_AUTHOR_NAME
unset GIT_AUTHOR_EMAIL
unset GIT_COMMITTER_NAME
unset GIT_COMMITTER_EMAIL

echo -e "${GREEN}✅ همه اطلاعات پاک شد${END}"

# ==================== مرحله ۲: تنظیم اطلاعات جدید ====================
echo -e "\n${YELLOW}[2/7] تنظیم اطلاعات حساب جدید...${END}"

git config --global user.name "sadeqgray-prog"
git config --global user.email "sadeqgray@gmail.com"

echo -e "${GREEN}✅ اطلاعات جدید تنظیم شد${END}"

# ==================== مرحله ۳: ساختن توکن جدید ====================
echo -e "\n${YELLOW}[3/7] لطفاً یه توکن جدید از گیت‌هاب بساز...${END}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}"
echo "1. برو به: https://github.com/settings/tokens"
echo "2. کلیک کن روی: Generate new token (classic)"
echo "3. تیک بزن: repo, workflow, write:packages"
echo "4. کلیک کن: Generate token"
echo "5. توکن جدید رو کپی کن (شبیه YOUR_TOKEN_HERE...) )"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}"
echo -e "${YELLOW}توکن جدید رو اینجا Paste کن (راست کلیک کن):${END} "
read -s NEW_TOKEN

if [ -z "$NEW_TOKEN" ]; then
    echo -e "${RED}❌ توکن وارد نشد!${END}"
    exit 1
fi

echo -e "${GREEN}✅ توکن دریافت شد${END}"

# ==================== مرحله ۴: پاک کردن توکن از فایل ====================
echo -e "\n${YELLOW}[4/7] پاک کردن توکن از final_fix.sh...${END}"

if [ -f "final_fix.sh" ]; then
    sed -i "s/YOUR_TOKEN_HERE.*/YOUR_GITHUB_TOKEN_HERE # REMOVED/" final_fix.sh
    echo -e "${GREEN}✅ توکن پاک شد${END}"
fi

# ==================== مرحله ۵: اضافه کردن فایل‌ها ====================
echo -e "\n${YELLOW}[5/7] آماده‌سازی فایل‌ها...${END}"

git add final_fix.sh 2>/dev/null
git add fix_final.sh 2>/dev/null
git add fix_final_v2.sh 2>/dev/null

git commit -m "final: clean version" 2>/dev/null

echo -e "${GREEN}✅ فایل‌ها آماده شدند${END}"

# ==================== مرحله ۶: روش نهایی - استفاده از SSH ====================
echo -e "\n${YELLOW}[6/7] تنظیم SSH Key (روش قطعی)...${END}"

# ساختن SSH Key
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "sadeqgray@gmail.com" 2>/dev/null

# نشون دادن کلید
echo -e "${BLUE}کلید عمومی SSH شما (این رو کپی کن):${END}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}"
cat ~/.ssh/id_ed25519.pub
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${END}"

echo -e "${YELLOW}حالا برو به این آدرس و کلید بالا رو اضافه کن:${END}"
echo "https://github.com/settings/ssh/new"
echo -e "${BLUE}بعد از اضافه کردن کلید، یه کلید Enter بزن تا ادامه بده...${END}"
read

# ==================== مرحله ۷: push با SSH ====================
echo -e "\n${YELLOW}[7/7] ارسال نهایی با SSH...${END}"

git remote remove origin
git remote add origin git@github.com:sadeqgray-prog/eye-of-horus.git

git push -u origin main --force

# ==================== بررسی نتیجه ====================
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✅✅✅ پوش با موفقیت انجام شد! ✅✅✅${END}"
    
    echo -e "\n${BLUE}⏱️  صبر کن ۲ دقیقه تا Railway دیپلوی کنه...${END}"
    echo -e "\n${YELLOW}بعد از ۲ دقیقه، این دستور رو بزن تا لاگ رو ببینی:${END}"
    echo -e "${BOLD}railway logs --service eye-of-horus --limit 30${END}"
    echo -e "\n${GREEN}ربات رو تست کن:${END}"
    echo -e "https://t.me/EyeOfHorusMiniBot"
else
    echo -e "\n${RED}❌ بازم خطا داد!${END}"
    echo -e "${YELLOW}روش دستی رو امتحان کن:${END}"
    echo -e "git push https://sadeqgray-prog:${NEW_TOKEN}@github.com/sadeqgray-prog/eye-of-horus.git main --force"
fi
