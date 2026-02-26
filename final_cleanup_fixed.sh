#!/data/data/com.termux/files/usr/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
END='\033[0m'

echo -e "${BLUE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🧹 FINAL CLEANUP FIXED - REMOVE TOKEN FROM EVERYWHERE     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${END}"

# ==================== مرحله ۱: جستجوی فایل‌های حاوی توکن ====================
echo -e "\n${YELLOW}[1/6] جستجوی فایل‌های حاوی توکن...${END}"

FILES_WITH_TOKEN=$(grep -r "YOUR_TOKEN_HERE" --include="*.sh" --include="*.py" --include="*.txt" . 2>/dev/null | cut -d: -f1 | sort -u)

if [ -n "$FILES_WITH_TOKEN" ]; then
    echo -e "${RED}❌ فایل‌های زیر حاوی توکن هستند:${END}"
    echo "$FILES_WITH_TOKEN"
else
    echo -e "${GREEN}✅ فایل جدیدی با توکن پیدا نشد${END}"
fi

# ==================== مرحله ۲: پاکسازی همه فایل‌های شل ====================
echo -e "\n${YELLOW}[2/6] پاکسازی همه فایل‌های sh از توکن...${END}"

# استفاده از find به جای for
find . -maxdepth 1 -name "*.sh" -type f | while read file; do
    if [ -f "$file" ]; then
        sed -i 's/YOUR_TOKEN_HERE[a-zA-Z0-9]*/YOUR_TOKEN_HERE/g' "$file"
        echo -e "${GREEN}✅ پاکسازی: $file${END}"
    fi
done

# ==================== مرحله ۳: پاکسازی فایل‌های پایتون ====================
echo -e "\n${YELLOW}[3/6] پاکسازی فایل‌های py از توکن...${END}"

find . -name "*.py" -type f | while read file; do
    sed -i 's/YOUR_TOKEN_HERE[a-zA-Z0-9]*/YOUR_TOKEN_HERE/g' "$file"
done
echo -e "${GREEN}✅ فایل‌های پایتون پاکسازی شدند${END}"

# ==================== مرحله ۴: پاکسازی فایل‌های txt ====================
echo -e "\n${YELLOW}[4/6] پاکسازی فایل‌های txt از توکن...${END}"

find . -name "*.txt" -type f | while read file; do
    sed -i 's/YOUR_TOKEN_HERE[a-zA-Z0-9]*/YOUR_TOKEN_HERE/g' "$file"
done
echo -e "${GREEN}✅ فایل‌های txt پاکسازی شدند${END}"

# ==================== مرحله ۵: پاکسازی تاریخچه گیت ====================
echo -e "\n${YELLOW}[5/6] پاکسازی کامل تاریخچه گیت...${END}"

# حذف فایل از تاریخچه
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch final_fix.sh" \
  --prune-empty --tag-name-filter cat -- --all 2>/dev/null

# پاک کردن رفرنس‌های قدیمی
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --aggressive --prune=now

echo -e "${GREEN}✅ تاریخچه گیت پاکسازی شد${END}"

# ==================== مرحله ۶: اضافه کردن فایل‌ها و push نهایی ====================
echo -e "\n${YELLOW}[6/6] ارسال نهایی به گیت‌هاب...${END}"

git add .
git commit -m "final: complete cleanup of all tokens" 2>/dev/null

# push با SSH
git push origin main --force

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}${BOLD}✅✅✅ پوش نهایی با موفقیت انجام شد! ✅✅✅${END}"
    echo -e "\n${BLUE}⏱️  صبر کن ۲ دقیقه تا Railway دیپلوی کنه...${END}"
    echo -e "\n${YELLOW}بعد از ۲ دقیقه، این دستور رو بزن:${END}"
    echo -e "${BOLD}railway logs --service eye-of-horus --limit 30${END}"
    echo -e "\n${GREEN}ربات رو تست کن:${END}"
    echo -e "https://t.me/EyeOfHorusMiniBot"
else
    echo -e "\n${RED}❌ خطا در پوش!${END}"
    echo -e "${YELLOW}این دستور رو امتحان کن:${END}"
    echo "git push git@github.com:sadeqgray-prog/eye-of-horus.git main --force"
fi
