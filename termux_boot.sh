#!/data/data/com.termux/files/usr/bin/bash

# این فایل رو در ~/.termux/boot/ قرار بده
# تا با بوت گوشی自动 اجرا بشه

# ==================== تنظیمات ====================
PROJECT_DIR="/data/data/com.termux/files/home/ultimate_oracle_bot"
LOG_FILE="$PROJECT_DIR/logs/boot.log"

# ==================== اجرا ====================

{
    echo "========================================="
    echo "🚀 Booting Eye of Horus at $(date)"
    echo "========================================="
    
    # صبر برای آماده شدن شبکه
    sleep 30
    
    # اجرای اسکریپت اصلی
    cd "$PROJECT_DIR"
    ./startup.sh
    
    echo "✅ Boot complete at $(date)"
    echo ""
} >> "$LOG_FILE" 2>&1
