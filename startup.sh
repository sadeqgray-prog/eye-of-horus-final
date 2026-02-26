#!/data/data/com.termux/files/usr/bin/bash

# 🚀 Eye of Horus - Startup Script
# اجرای خودکار پس از اتصال اینترنت

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  𓂀  EYE OF HORUS - AUTO STARTUP  𓂀  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ==================== تنظیمات ====================
PROJECT_DIR="/data/data/com.termux/files/home/ultimate_oracle_bot"
LOG_FILE="$PROJECT_DIR/logs/startup.log"
PID_FILE="$PROJECT_DIR/bot.pid"
AUTODEPLOYER_PID="$PROJECT_DIR/autodeployer.pid"

# ==================== توابع ====================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_internet() {
    ping -c 1 8.8.8.8 > /dev/null 2>&1
    return $?
}

wait_for_internet() {
    log "🌐 Waiting for internet connection..."
    while ! check_internet; do
        sleep 5
    done
    log "✅ Internet connected"
}

start_bot() {
    if [ -f "$PID_FILE" ]; then
        old_pid=$(cat "$PID_FILE")
        if kill -0 "$old_pid" 2>/dev/null; then
            log "⚠️ Bot already running (PID: $old_pid)"
            return
        fi
    fi
    
    log "🚀 Starting bot..."
    cd "$PROJECT_DIR"
    
    # فعال‌سازی محیط مجازی
    source venv/bin/activate
    
    # اجرا در پس‌زمینه
    nohup python main.py > logs/bot.out 2>&1 &
    echo $! > "$PID_FILE"
    
    log "✅ Bot started (PID: $!)"
}

start_autodeployer() {
    if [ -f "$AUTODEPLOYER_PID" ]; then
        old_pid=$(cat "$AUTODEPLOYER_PID")
        if kill -0 "$old_pid" 2>/dev/null; then
            log "⚠️ AutoDeployer already running (PID: $old_pid)"
            return
        fi
    fi
    
    log "🤖 Starting AutoDeployer..."
    cd "$PROJECT_DIR"
    
    source venv/bin/activate
    
    nohup python auto_deployer.py > logs/autodeployer.out 2>&1 &
    echo $! > "$AUTODEPLOYER_PID"
    
    log "✅ AutoDeployer started (PID: $!)"
}

check_status() {
    echo -e "\n${YELLOW}=== Status Report ===${NC}"
    
    # بات
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}✅ Bot: RUNNING (PID: $pid)${NC}"
            
            # آپ‌تایم
            if [ -f "/proc/$pid/stat" ]; then
                start_time=$(stat -c %Y "/proc/$pid")
                now=$(date +%s)
                uptime=$((now - start_time))
                hours=$((uptime / 3600))
                minutes=$(( (uptime % 3600) / 60 ))
                echo "   Uptime: ${hours}h ${minutes}m"
            fi
        else
            echo -e "${RED}❌ Bot: STOPPED${NC}"
        fi
    else
        echo -e "${RED}❌ Bot: NOT STARTED${NC}"
    fi
    
    # AutoDeployer
    if [ -f "$AUTODEPLOYER_PID" ]; then
        pid=$(cat "$AUTODEPLOYER_PID")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}✅ AutoDeployer: RUNNING (PID: $pid)${NC}"
        else
            echo -e "${RED}❌ AutoDeployer: STOPPED${NC}"
        fi
    else
        echo -e "${RED}❌ AutoDeployer: NOT STARTED${NC}"
    fi
    
    # اینترنت
    if check_internet; then
        echo -e "${GREEN}✅ Internet: CONNECTED${NC}"
    else
        echo -e "${RED}❌ Internet: DISCONNECTED${NC}"
    fi
    
    # آخرین بک‌آپ
    latest_backup=$(ls -t backups/backup_* 2>/dev/null | head -1)
    if [ -n "$latest_backup" ]; then
        backup_time=$(stat -c %y "$latest_backup" | cut -d. -f1)
        echo -e "${BLUE}💾 Last backup: $backup_time${NC}"
    fi
    
    # آخرین دیپلوی
    if [ -f "$PROJECT_DIR/.last_deploy" ]; then
        last_deploy=$(cat "$PROJECT_DIR/.last_deploy")
        echo -e "${BLUE}🚀 Last deploy: $last_deploy${NC}"
    fi
    
    echo ""
}

cleanup() {
    log "🧹 Cleaning up..."
    
    if [ -f "$PID_FILE" ]; then
        kill $(cat "$PID_FILE") 2>/dev/null
        rm "$PID_FILE"
    fi
    
    if [ -f "$AUTODEPLOYER_PID" ]; then
        kill $(cat "$AUTODEPLOYER_PID") 2>/dev/null
        rm "$AUTODEPLOYER_PID"
    fi
    
    log "👋 Goodbye!"
    exit 0
}

# ==================== اجرای اصلی ====================

trap cleanup SIGINT SIGTERM

# ایجاد پوشه لاگ
mkdir -p "$PROJECT_DIR/logs"

log "🔄 Starting Eye of Horus..."

# منتظر اینترنت
wait_for_internet

# شروع سرویس‌ها
start_autodeployer
sleep 2
start_bot

# نمایش وضعیت
check_status

# لاگ نهایی
log "✅ All systems operational"
echo -e "${GREEN}✅ Bot is running! Check logs/bot.out for output${NC}"
echo -e "${YELLOW}📊 Run './startup.sh status' to check status${NC}"
echo ""

# حلقه مانیتورینگ
while true; do
    sleep 60
    
    # چک اینترنت
    if check_internet; then
        # چک بات
        if [ -f "$PID_FILE" ]; then
            pid=$(cat "$PID_FILE")
            if ! kill -0 "$pid" 2>/dev/null; then
                log "⚠️ Bot died, restarting..."
                start_bot
            fi
        else
            start_bot
        fi
        
        # چک AutoDeployer
        if [ -f "$AUTODEPLOYER_PID" ]; then
            pid=$(cat "$AUTODEPLOYER_PID")
            if ! kill -0 "$pid" 2>/dev/null; then
                log "⚠️ AutoDeployer died, restarting..."
                start_autodeployer
            fi
        else
            start_autodeployer
        fi
    fi
done
