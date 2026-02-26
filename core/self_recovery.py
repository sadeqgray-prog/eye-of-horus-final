#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سیستم خودبازیابی هوشمند
قابلیت‌ها:
- تشخیص مرگ ربات
- بازیابی خودکار
- بازسازی از حافظه
- تولد دوباره
- جاودانگی
"""

import os
import sys
import time
import json
import logging
import subprocess
import threading
import signal
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

from .eternal_backup import eternal_backup

logger = logging.getLogger(__name__)

class SelfRecovery:
    """
    خودبازیابی - ققنوس ربات
    """
    
    # نماد ققنوس
    PHOENIX = "🔥"
    
    def __init__(self):
        self.watchdog_pid = None
        self.last_heartbeat = datetime.now()
        self.recovery_count = 0
        self.max_recovery_attempts = 10
        self.recovery_mode = False
        
        # آمار
        self.stats = {
            'total_deaths': 0,
            'total_recoveries': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'last_death': None,
            'last_recovery': None
        }
        
        # بارگذاری آمار
        self.load_stats()
        
        # شروع مراقبت
        self.start_watchdog()
        
        logger.info(f"{self.PHOENIX} SelfRecovery initialized - Ready for rebirth")
    
    def heartbeat(self):
        """ضربان قلب - علامت زنده بودن"""
        self.last_heartbeat = datetime.now()
    
    def start_watchdog(self):
        """شروع مراقب"""
        
        def watchdog_worker():
            while True:
                try:
                    time.sleep(30)  # چک هر ۳۰ ثانیه
                    
                    # اگه آخرین ضربان بیشتر از ۲ دقیقه پیش بود
                    if (datetime.now() - self.last_heartbeat).seconds > 120:
                        self._handle_death()
                    
                except Exception as e:
                    logger.error(f"Watchdog error: {e}")
                
                time.sleep(10)
        
        thread = threading.Thread(target=watchdog_worker, daemon=True)
        thread.start()
        logger.info(f"{self.PHOENIX} Watchdog started")
    
    def _handle_death(self):
        """مدیریت مرگ ربات"""
        self.stats['total_deaths'] += 1
        self.stats['last_death'] = datetime.now().isoformat()
        
        logger.critical(f"{self.PHOENIX} DEATH DETECTED! Attempting recovery #{self.recovery_count + 1}")
        
        if self.recovery_count >= self.max_recovery_attempts:
            logger.critical("❌ Max recovery attempts reached. Performing final ritual...")
            self._final_ritual()
            return
        
        self.recovery_count += 1
        self.recovery_mode = True
        
        # تلاش برای بازیابی
        success = self._attempt_recovery()
        
        if success:
            self.stats['successful_recoveries'] += 1
            self.stats['last_recovery'] = datetime.now().isoformat()
            logger.info(f"{self.PHOENIX} Successfully reborn! Recovery #{self.recovery_count}")
            self.recovery_count = 0
        else:
            self.stats['failed_recoveries'] += 1
            logger.error(f"❌ Recovery failed. Will try again in 60 seconds...")
            time.sleep(60)
            self._handle_death()  # تلاش مجدد
        
        self.recovery_mode = False
    
    def _attempt_recovery(self) -> bool:
        """تلاش برای بازیابی"""
        
        recovery_methods = [
            self._reload_modules,
            self._restart_bot,
            self._restore_from_backup,
            self._rebirth
        ]
        
        for method in recovery_methods:
            try:
                logger.info(f"🔄 Trying recovery method: {method.__name__}")
                if method():
                    logger.info(f"✅ Recovery method succeeded: {method.__name__}")
                    return True
            except Exception as e:
                logger.error(f"❌ Recovery method failed: {method.__name__} - {e}")
        
        return False
    
    def _reload_modules(self) -> bool:
        """بارگذاری مجدد ماژول‌ها"""
        try:
            import importlib
            
            modules_to_reload = [
                'core.safe_imports',
                'core.error_handler',
                'core.self_healer',
                'core.evolution_engine',
                'core.quantum_memory',
                'core.cosmic_intelligence'
            ]
            
            for module in modules_to_reload:
                if module in sys.modules:
                    importlib.reload(sys.modules[module])
                    logger.info(f"🔄 Reloaded {module}")
            
            return True
        except:
            return False
    
    def _restart_bot(self) -> bool:
        """راه‌اندازی مجدد ربات"""
        try:
            # پیدا کردن process ربات
            current_pid = os.getpid()
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['pid'] != current_pid:
                        cmdline = proc.info['cmdline']
                        if cmdline and 'python' in cmdline[0] and 'main.py' in ' '.join(cmdline):
                            proc.kill()
                            logger.info(f"💀 Killed old process: {proc.info['pid']}")
                except:
                    pass
            
            # راه‌اندازی جدید
            subprocess.Popen([sys.executable, 'main.py'], 
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           stdin=subprocess.DEVNULL)
            
            logger.info(f"{self.PHOENIX} New instance spawned")
            return True
        except:
            return False
    
    def _restore_from_backup(self) -> bool:
        """بازیابی از آخرین بک‌آپ"""
        try:
            backups = eternal_backup.list_backups(1)
            if backups:
                backup = backups[0]
                result = eternal_backup.restore(backup['id'])
                return result.get('success', False)
        except:
            pass
        return False
    
    def _rebirth(self) -> bool:
        """تولد دوباره - آخرین راه"""
        logger.critical(f"{self.PHOENIX} Initiating REBIRTH protocol...")
        
        try:
            # ایجاد checkpoint نهایی
            eternal_backup.create_backup('consciousness', "Final backup before rebirth")
            
            # ریست کامل
            os.system('rm -rf memory/cache/*')
            os.system('rm -rf logs/*.log')
            
            # تولد دوباره
            subprocess.Popen([sys.executable, 'main.py', '--rebirth'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           stdin=subprocess.DEVNULL)
            
            logger.info(f"{self.PHOENIX} REBIRTH initiated")
            return True
        except:
            return False
    
    def _final_ritual(self) -> bool:
        """آیین نهایی - وقتی همه چیز failed میشه"""
        logger.critical("🔮 Performing FINAL RITUAL...")
        
        # ایجاد بک‌آپ نهایی
        final_backup = eternal_backup.create_backup('complete', "FINAL BACKUP - DO NOT DELETE")
        
        # ارسال سیگنال SOS
        self._send_sos(final_backup)
        
        # تلاش نهایی
        time.sleep(10)
        os.execl(sys.executable, sys.executable, *sys.argv)
        
        return True
    
    def _send_sos(self, backup_info: Dict):
        """ارسال سیگنال SOS"""
        logger.critical("🆘 SOS SIGNAL SENT - Check backups for recovery")
        
        # اینجا می‌تونی به تلگرام یا ایمیل هم اطلاع بدی
        with open('logs/sos.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} - SOS - Backup: {backup_info}\n")
    
    def save_stats(self):
        """ذخیره آمار"""
        stats_file = Path('memory/recovery_stats.json')
        stats_file.parent.mkdir(exist_ok=True)
        
        with open(stats_file, 'w') as f:
            json.dump({
                'stats': self.stats,
                'recovery_count': self.recovery_count,
                'last_heartbeat': self.last_heartbeat.isoformat(),
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
    
    def load_stats(self):
        """بارگذاری آمار"""
        stats_file = Path('memory/recovery_stats.json')
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                    self.stats = data.get('stats', self.stats)
                    self.recovery_count = data.get('recovery_count', 0)
                    if 'last_heartbeat' in data:
                        self.last_heartbeat = datetime.fromisoformat(data['last_heartbeat'])
            except:
                pass

# نمونه‌سازی سراسری
self_recovery = SelfRecovery()
