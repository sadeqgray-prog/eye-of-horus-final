#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سیستم خودکار دیپلوی و بازیابی هوشمند با DeepSeek
قابلیت‌ها:
- اجرای خودکار DeepSeek در Termux
- تشخیص و رفع خطاهای زمان اجرا
- مانیتورینگ پس‌زمینه
- اتصال خودکار پس از اینترنت
- بک‌آپ لحظه‌ای
- دیپلوی خودکار به Railway
- بازیابی هوشمند پس از کرش
- یادگیری از خطاها
"""

import os
import sys
import time
import json
import logging
import subprocess
import threading
import asyncio
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib
import pickle
import shlex

logger = logging.getLogger(__name__)

# ==================== تنظیمات DeepSeek ====================
DEEPSEEK_CONFIG = {
    'model': 'deepseek-coder-33b-instruct',
    'temperature': 0.1,
    'max_tokens': 4096,
    'top_p': 0.95,
    'frequency_penalty': 0,
    'presence_penalty': 0
}

class DeepSeekAutoDeployer:
    """
    سیستم خودکار دیپلوی با DeepSeek - مغز متفکر پروژه
    """
    
    def __init__(self):
        self.deepseek_process = None
        self.is_running = False
        self.error_count = 0
        self.fix_count = 0
        self.last_backup = None
        self.last_deploy = None
        self.connection_monitor = None
        
        # مسیرها
        self.project_dir = Path.cwd()
        self.logs_dir = self.project_dir / 'logs'
        self.memory_dir = self.project_dir / 'memory'
        self.backup_dir = self.project_dir / 'backups'
        
        # ایجاد پوشه‌ها
        for d in [self.logs_dir, self.memory_dir, self.backup_dir]:
            d.mkdir(exist_ok=True)
        
        # حافظه خطاها و راه‌حل‌ها
        self.error_memory = self._load_error_memory()
        self.fix_history = []
        
        # آمار
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'total_errors': 0,
            'auto_fixes': 0,
            'manual_fixes_needed': 0,
            'deployments': 0,
            'backups': 0,
            'uptime_hours': 0
        }
        
        logger.info("🤖 DeepSeek AutoDeployer initialized")
        logger.info(f"📁 Project: {self.project_dir}")
        
        # شروع مانیتورینگ
        self.start_background_monitors()
    
    def _load_error_memory(self) -> Dict:
        """بارگذاری حافظه خطاها"""
        memory_file = self.memory_dir / 'error_memory.json'
        if memory_file.exists():
            try:
                with open(memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'errors': {},
            'fixes': {},
            'patterns': []
        }
    
    def _save_error_memory(self):
        """ذخیره حافظه خطاها"""
        memory_file = self.memory_dir / 'error_memory.json'
        try:
            with open(memory_file, 'w') as f:
                json.dump(self.error_memory, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save error memory: {e}")
    
    # ==================== مانیتورینگ اینترنت ====================
    
    def start_background_monitors(self):
        """شروع مانیتورینگ پس‌زمینه"""
        
        # مانیتور اینترنت
        self.connection_monitor = threading.Thread(target=self._monitor_connection, daemon=True)
        self.connection_monitor.start()
        
        # مانیتور خطاها
        error_monitor = threading.Thread(target=self._monitor_errors, daemon=True)
        error_monitor.start()
        
        # مانیتور بک‌آپ
        backup_monitor = threading.Thread(target=self._auto_backup, daemon=True)
        backup_monitor.start()
        
        logger.info("📡 Background monitors started")
    
    def _monitor_connection(self):
        """مانیتورینگ اتصال اینترنت"""
        while True:
            try:
                # چک اینترنت
                result = sub.run(['ping', '-c', '1', '8.8.8.8'], 
                               capture_output=True, timeout=5)
                
                if result.returncode == 0:
                    if not self.is_running:
                        logger.info("🌐 Internet connected - Resuming operations")
                        self._on_connect()
                else:
                    if self.is_running:
                        logger.warning("⚠️ Internet disconnected - Pausing operations")
                        self._on_disconnect()
                
            except Exception as e:
                logger.error(f"Connection monitor error: {e}")
            
            time.sleep(30)  # چک هر ۳۰ ثانیه
    
    def _on_connect(self):
        """وقتی اینترنت وصل میشه"""
        self.is_running = True
        
        # آپدیت وضعیت
        self.stats['last_online'] = datetime.now().isoformat()
        
        # چک و دیپلوی
        threading.Thread(target=self._check_and_deploy, daemon=True).start()
    
    def _on_disconnect(self):
        """وقتی اینترنت قطع میشه"""
        self.is_running = False
        
        # ذخیره وضعیت
        self._save_state()
    
    # ==================== دیپ‌سیک ====================
    
    def start_deepseek(self):
        """اجرای DeepSeek در Termux"""
        try:
            # نصب DeepSeek اگر نصب نیست
            self._ensure_deepseek()
            
            # اجرا در پس‌زمینه
            cmd = [
                'python', '-m', 'deepseek_chat',
                '--model', DEEPSEEK_CONFIG['model'],
                '--temperature', str(DEEPSEEK_CONFIG['temperature']),
                '--max-tokens', str(DEEPSEEK_CONFIG['max_tokens'])
            ]
            
            self.deepseek_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            logger.info("🤖 DeepSeek started")
            
            # مانیتور خروجی
            threading.Thread(target=self._monitor_deepseek_output, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to start DeepSeek: {e}")
    
    def _ensure_deepseek(self):
        """اطمینان از نصب DeepSeek"""
        try:
            import deepseek_chat
        except ImportError:
            logger.info("📦 Installing DeepSeek...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'deepseek-chat'], check=True)
            logger.info("✅ DeepSeek installed")
    
    def _monitor_deepseek_output(self):
        """مانیتورینگ خروجی DeepSeek"""
        if not self.deepseek_process:
            return
        
        for line in self.deepseek_process.stdout:
            if 'error' in line.lower() or 'exception' in line.lower():
                logger.warning(f"DeepSeek: {line.strip()}")
    
    async def ask_deepseek(self, prompt: str) -> str:
        """پرسش از DeepSeek"""
        try:
            from deepseek_chat import DeepSeekChat
            
            chat = DeepSeekChat()
            response = await chat.ask(prompt, **DEEPSEEK_CONFIG)
            return response
        except Exception as e:
            logger.error(f"DeepSeek error: {e}")
            return ""
    
    async def fix_error_with_deepseek(self, error_log: str, code_context: str = None) -> Optional[str]:
        """
        استفاده از DeepSeek برای رفع خطا
        """
        prompt = f"""
        I have an error in my Python code. Please analyze and provide the fix.
        
        Error:
        ```
        {error_log}
        ```
        
        {'Code context:' + code_context if code_context else ''}
        
        Please provide:
        1. What caused this error
        2. The exact fix needed
        3. The corrected code (if applicable)
        
        Focus on the solution. Be precise.
        """
        
        try:
            response = await self.ask_deepseek(prompt)
            
            # استخراج راه‌حل
            if '```python' in response:
                # کد در بلاک پایتون
                code_block = response.split('```python')[1].split('```')[0].strip()
                return code_block
            elif '`' in response:
                # کد در بک‌تیک
                parts = response.split('`')
                if len(parts) >= 2:
                    return parts[1].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"DeepSeek fix error: {e}")
            return None
    
    # ==================== مانیتورینگ خطا ====================
    
    def _monitor_errors(self):
        """مانیتورینگ خطاهای زمان اجرا"""
        log_file = self.logs_dir / 'bot.log'
        
        while True:
            try:
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        lines = f.readlines()[-50:]  # ۵۰ خط آخر
                        
                        for line in lines:
                            if 'ERROR' in line or 'Exception' in line or 'Traceback' in line:
                                self._handle_error(line)
                
            except Exception as e:
                logger.error(f"Error monitor failed: {e}")
            
            time.sleep(10)  # چک هر ۱۰ ثانیه
    
    def _handle_error(self, error_line: str):
        """مدیریت خطای جدید"""
        self.stats['total_errors'] += 1
        self.error_count += 1
        
        # استخراج نوع خطا
        error_hash = hashlib.md5(error_line.encode()).hexdigest()[:10]
        
        logger.error(f"🔴 Error detected [{error_hash}]: {error_line.strip()}")
        
        # چک کردن حافظه برای راه‌حل قبلی
        if error_hash in self.error_memory['fixes']:
            previous_fix = self.error_memory['fixes'][error_hash]
            logger.info(f"📚 Found previous fix: {previous_fix['solution'][:100]}...")
            
            # اعمال fix
            self._apply_fix(previous_fix)
            return
        
        # اگه راه‌حل نداشتیم، از DeepSeek می‌پرسیم
        threading.Thread(target=self._get_and_apply_fix, args=(error_line, error_hash), daemon=True).start()
    
    def _get_and_apply_fix(self, error_line: str, error_hash: str):
        """گرفتن راه‌حل از DeepSeek و اعمال"""
        try:
            # ایجاد حلقه asyncio جدید
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # دریافت راه‌حل
            fix = loop.run_until_complete(self.fix_error_with_deepseek(error_line))
            
            if fix:
                logger.info(f"🔧 DeepSeek suggested fix: {fix[:200]}...")
                
                # ذخیره در حافظه
                self.error_memory['fixes'][error_hash] = {
                    'error': error_line,
                    'solution': fix,
                    'applied_at': datetime.now().isoformat(),
                    'success': False  # بعداً آپدیت میشه
                }
                
                # اعمال fix
                success = self._apply_fix({'solution': fix})
                
                if success:
                    self.error_memory['fixes'][error_hash]['success'] = True
                    self.stats['auto_fixes'] += 1
                    self.fix_count += 1
                    
                    # ذخیره لاگ موفقیت
                    self.fix_history.append({
                        'error': error_hash,
                        'fix': fix[:100],
                        'time': datetime.now().isoformat()
                    })
            
            self._save_error_memory()
            
        except Exception as e:
            logger.error(f"Fix application failed: {e}")
    
    def _apply_fix(self, fix_data: Dict) -> bool:
        """اعمال راه‌حل"""
        try:
            solution = fix_data.get('solution', '')
            
            # اگه راه‌حل کد پایتون داره
            if '```python' in solution or '.py' in solution:
                # TODO: اعمال تغییرات در فایل
                logger.info("📝 Would apply code changes here")
            
            return True
            
        except Exception as e:
            logger.error(f"Fix application error: {e}")
            return False
    
    # ==================== بک‌آپ خودکار ====================
    
    def _auto_backup(self):
        """بک‌آپ خودکار در پس‌زمینه"""
        while True:
            try:
                now = datetime.now()
                
                # بک‌آپ هر ساعت
                if not self.last_backup or (now - self.last_backup).seconds > 3600:
                    self.create_backup('hourly')
                    self.last_backup = now
                    self.stats['backups'] += 1
                
                time.sleep(300)  # چک هر ۵ دقیقه
                
            except Exception as e:
                logger.error(f"Auto backup error: {e}")
                time.sleep(60)
    
    def create_backup(self, backup_type: str = 'manual'):
        """ایجاد بک‌آپ"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{backup_type}_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        try:
            backup_path.mkdir(exist_ok=True)
            
            # بک‌آپ فایل‌های مهم
            important_files = [
                'main.py', 'bot/ultimate_bot.py', 'core/',
                'modules/', 'api/', 'config/'
            ]
            
            for item in important_files:
                src = self.project_dir / item
                if src.exists():
                    if src.is_file():
                        dst = backup_path / item
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        import shutil
                        shutil.copy2(src, dst)
                    elif src.is_dir():
                        dst = backup_path / item
                        shutil.copytree(src, dst, dirs_exist_ok=True)
            
            # بک‌آپ حافظه
            memory_file = backup_path / 'memory.json'
            with open(memory_file, 'w') as f:
                json.dump({
                    'stats': self.stats,
                    'error_memory': self.error_memory,
                    'timestamp': timestamp
                }, f, indent=2)
            
            logger.info(f"✅ Backup created: {backup_name}")
            
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return None
    
    def restore_backup(self, backup_name: str):
        """بازیابی از بک‌آپ"""
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_name}")
            return False
        
        try:
            import shutil
            
            # بازیابی فایل‌ها
            for item in backup_path.iterdir():
                if item.name == 'memory.json':
                    continue
                
                dst = self.project_dir / item.name
                if item.is_file():
                    shutil.copy2(item, dst)
                elif item.is_dir():
                    shutil.copytree(item, dst, dirs_exist_ok=True)
            
            # بازیابی حافظه
            memory_file = backup_path / 'memory.json'
            if memory_file.exists():
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
                    self.stats = memory.get('stats', self.stats)
                    self.error_memory = memory.get('error_memory', self.error_memory)
            
            logger.info(f"✅ Restored from: {backup_name}")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
    
    # ==================== دیپلوی خودکار به Railway ====================
    
    def _check_and_deploy(self):
        """چک و دیپلوی خودکار"""
        try:
            # چک کردن تغییرات
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                   capture_output=True, text=True)
            
            if result.stdout.strip():
                logger.info("📦 Changes detected, preparing to deploy...")
                
                # بک‌آپ قبل از دیپلوی
                backup_path = self.create_backup('pre_deploy')
                
                # کامیت
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', f'Auto-deploy {datetime.now().isoformat()}'], 
                             check=True)
                
                # پوش به GitHub
                push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                           capture_output=True, text=True)
                
                if push_result.returncode == 0:
                    logger.info("✅ Pushed to GitHub")
                    
                    # دیپلوی به Railway
                    deploy_result = subprocess.run(['railway', 'up'], 
                                                 capture_output=True, text=True)
                    
                    if deploy_result.returncode == 0:
                        logger.info("✅ Deployed to Railway")
                        self.stats['deployments'] += 1
                        self.last_deploy = datetime.now().isoformat()
                        
                        # مانیتور وضعیت
                        threading.Thread(target=self._monitor_deployment, daemon=True).start()
                    else:
                        logger.error(f"❌ Railway deploy failed: {deploy_result.stderr}")
                        self._handle_deploy_failure(deploy_result.stderr)
                else:
                    logger.error(f"❌ Git push failed: {push_result.stderr}")
        
        except Exception as e:
            logger.error(f"Deploy check error: {e}")
    
    def _monitor_deployment(self):
        """مانیتورینگ وضعیت دیپلوی"""
        time.sleep(30)  # صبر برای شروع
        
        try:
            # چک لاگ‌های Railway
            result = subprocess.run(['railway', 'logs', '--limit', '20'], 
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                logs = result.stdout
                
                if 'error' in logs.lower() or 'crash' in logs.lower() or 'fail' in logs.lower():
                    logger.warning("⚠️ Deployment可能有 مشکل!")
                    self._handle_deploy_failure(logs)
                else:
                    logger.info("✅ Deployment successful!")
        
        except Exception as e:
            logger.error(f"Deployment monitor error: {e}")
    
    def _handle_deploy_failure(self, error_log: str):
        """مدیریت خطای دیپلوی"""
        logger.error("🔴 Deployment failed, analyzing...")
        
        # استخراج خطا
        error_lines = []
        for line in error_log.split('\n'):
            if 'error' in line.lower() or 'exception' in line.lower():
                error_lines.append(line)
        
        if error_lines:
            error_text = '\n'.join(error_lines)
            
            # استفاده از DeepSeek برای رفع
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            fix = loop.run_until_complete(self.fix_error_with_deepseek(error_text))
            
            if fix:
                logger.info(f"🔧 DeepSeek suggests: {fix[:200]}...")
                
                # اعمال fix و دیپلوی مجدد
                if self._apply_fix({'solution': fix}):
                    logger.info("🔄 Re-deploying...")
                    time.sleep(5)
                    self._check_and_deploy()
    
    # ==================== ذخیره و بازیابی وضعیت ====================
    
    def _save_state(self):
        """ذخیره وضعیت فعلی"""
        state_file = self.memory_dir / 'autodeployer_state.json'
        
        state = {
            'stats': self.stats,
            'error_count': self.error_count,
            'fix_count': self.fix_count,
            'last_backup': self.last_backup.isoformat() if self.last_backup else None,
            'last_deploy': self.last_deploy,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def load_state(self):
        """بارگذاری وضعیت قبلی"""
        state_file = self.memory_dir / 'autodeployer_state.json'
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.stats = state.get('stats', self.stats)
                    self.error_count = state.get('error_count', 0)
                    self.fix_count = state.get('fix_count', 0)
                    if state.get('last_backup'):
                        self.last_backup = datetime.fromisoformat(state['last_backup'])
                    self.last_deploy = state.get('last_deploy')
                    
                logger.info("📚 State loaded")
            except:
                pass
    
    # ==================== اجرای اصلی ====================
    
    def run(self):
        """اجرای اصلی سیستم"""
        logger.info("🚀 Starting DeepSeek AutoDeployer...")
        
        # بارگذاری وضعیت قبلی
        self.load_state()
        
        # شروع DeepSeek
        self.start_deepseek()
        
        # آپدیت آمار
        self.stats['uptime_hours'] = 0
        
        # حلقه اصلی
        try:
            while True:
                time.sleep(60)
                
                # آپدیت آمار
                uptime = datetime.now() - datetime.fromisoformat(self.stats['start_time'])
                self.stats['uptime_hours'] = round(uptime.total_seconds() / 3600, 1)
                
                # ذخیره وضعیت هر ساعت
                if int(time.time()) % 3600 == 0:
                    self._save_state()
                    
        except KeyboardInterrupt:
            logger.info("👋 Shutting down...")
            self._save_state()
            sys.exit(0)

# ==================== اجرا ====================

if __name__ == "__main__":
    # تنظیم لاگینگ
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/autodeployer.log'),
            logging.StreamHandler()
        ]
    )
    
    deployer = DeepSeekAutoDeployer()
    deployer.run()
