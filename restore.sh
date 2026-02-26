#!/data/data/com.termux/files/usr/bin/bash

# 𓂀 EYE OF HORUS RESTORER 𓂀

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}𓂀 Eye of Horus Recovery Tool${NC}"
echo ""

# نمایش بک‌آپ‌ها
echo -e "${YELLOW}Available backups:${NC}"
python -c "
from core.eternal_backup import eternal_backup
backups = eternal_backup.list_backups(10)
for i, b in enumerate(backups):
    print(f\"  [{i+1}] {b['timestamp']} - {b['level']} - {b['description']}\")
"

echo ""
read -p "Enter backup number to restore (or 'latest'): " choice

if [ "$choice" == "latest" ]; then
    python -c "
from core.eternal_backup import eternal_backup
result = eternal_backup.restore()
if result['success']:
    print('${GREEN}✅ Restore successful!${NC}')
else:
    print('${RED}❌ Restore failed: ' + result.get('error', 'Unknown error') + '${NC}')
"
else
    python -c "
from core.eternal_backup import eternal_backup
backups = eternal_backup.list_backups(10)
if $choice <= len(backups):
    result = eternal_backup.restore(backups[$choice-1]['id'])
    if result['success']:
        print('${GREEN}✅ Restore successful!${NC}')
    else:
        print('${RED}❌ Restore failed: ' + result.get('error', 'Unknown error') + '${NC}')
"
fi
