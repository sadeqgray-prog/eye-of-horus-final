#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سیستم خودترمیمی هوشمند با قابلیت:
- تشخیص خودکار مشکلات
- رفع خودکار باگ‌ها
- بهینه‌سازی کد
- یادگیری از تجربیات
- پیش‌بینی مشکلات آینده
"""

import os
import sys
import json
import time
import logging
import subprocess
import ast
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import shutil
import re

logger = logging.getLogger(__name__)

class SelfHealer:
    """
    هوش مصنوعی خودترمیم - مثل یه دکتر برای کد
    """
    
    def __init__(self):
        self.healing_history = []
        self.known_issues = {}
        self.successful_fixes = {}
        self.health_score = 100
        self.last_check = datetime.now()
        
        # آمار
        self.stats = {
            'total_heals': 0,
            'successful_heals': 0,
            'failed_heals': 0,
            'optimizations': 0
        }
        
        # بارگذاری حافظه
        self.load_memory()
        
        logger.info("🩺 SelfHealer v5.0 initialized")
    
    def check_health(self) -> Dict:
        """
        چک کردن سلامت کلی سیستم
        """
        issues = []
        fixes = []
        
        # 1. چک کردن فایل‌های ضروری
        required_files = [
            'core/safe_imports.py',
            'core/error_handler.py',
            'core/self_healer.py',
            'bot/ultimate_bot.py',
            'database/models.py',
            'main.py'
        ]
        
        for file in required_files:
            if not Path(file).exists():
                issues.append({
                    'type': 'missing_file',
                    'file': file,
                    'severity': 'high'
                })
                # تلاش برای بازیابی
                if self._recover_file(file):
                    fixes.append(f"Recovered {file}")
        
        # 2. چک کردن سینتکس
        syntax_issues = self._check_syntax()
        issues.extend(syntax_issues)
        
        # 3. چک کردن imports
        import_issues = self._check_imports()
        issues.extend(import_issues)
        
        # 4. چک کردن حافظه
        memory_issues = self._check_memory()
        issues.extend(memory_issues)
        
        # 5. چک کردن دیسک
        disk_issues = self._check_disk()
        issues.extend(disk_issues)
        
        # محاسبه امتیاز سلامت
        self.health_score = self._calculate_health_score(issues)
        
        # اعمال fixes خودکار
        for issue in issues:
            if issue.get('auto_fixable'):
                fix = self._apply_fix(issue)
                if fix:
                    fixes.append(fix)
                    self.stats['successful_heals'] += 1
                else:
                    self.stats['failed_heals'] += 1
        
        result = {
            'health_score': self.health_score,
            'issues_found': len(issues),
            'issues': issues,
            'fixes_applied': fixes,
            'timestamp': datetime.now().isoformat()
        }
        
        # ذخیره در تاریخچه
        self.healing_history.append(result)
        if len(self.healing_history) > 100:
            self.healing_history = self.healing_history[-100:]
        
        self.save_memory()
        
        return result
    
    def _check_syntax(self) -> List[Dict]:
        """چک کردن سینتکس همه فایل‌های پایتون"""
        issues = []
        
        for py_file in Path('.').rglob('*.py'):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                ast.parse(content)
                
            except SyntaxError as e:
                issues.append({
                    'type': 'syntax_error',
                    'file': str(py_file),
                    'line': e.lineno,
                    'message': str(e),
                    'severity': 'high',
                    'auto_fixable': self._can_fix_syntax(e)
                })
            except Exception as e:
                issues.append({
                    'type': 'file_error',
                    'file': str(py_file),
                    'message': str(e),
                    'severity': 'medium',
                    'auto_fixable': False
                })
        
        return issues
    
    def _check_imports(self) -> List[Dict]:
        """چک کردن imports"""
        issues = []
        imported_modules = set()
        
        for py_file in Path('.').rglob('*.py'):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # پیدا کردن importها
                import_lines = re.findall(r'^import (\w+)|^from (\w+) import', content, re.MULTILINE)
                for line in import_lines:
                    module = line[0] or line[1]
                    if module and module not in ['os', 'sys', 'time', 'datetime', 'json', 'logging']:
                        imported_modules.add(module)
                        
            except Exception as e:
                pass
        
        # چک کردن وجود ماژول‌ها
        for module in imported_modules:
            try:
                __import__(module)
            except ImportError:
                issues.append({
                    'type': 'missing_module',
                    'module': module,
                    'severity': 'medium',
                    'auto_fixable': True,
                    'fix_command': f"pip install {module}"
                })
        
        return issues
    
    def _check_memory(self) -> List[Dict]:
        """چک کردن حافظه"""
        issues = []
        
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            if memory.percent > 90:
                issues.append({
                    'type': 'high_memory_usage',
                    'percent': memory.percent,
                    'severity': 'high',
                    'auto_fixable': True
                })
            elif memory.percent > 80:
                issues.append({
                    'type': 'medium_memory_usage',
                    'percent': memory.percent,
                    'severity': 'medium',
                    'auto_fixable': False
                })
        except:
            pass
        
        return issues
    
    def _check_disk(self) -> List[Dict]:
        """چک کردن دیسک"""
        issues = []
        
        try:
            import shutil
            disk = shutil.disk_usage('.')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            used_percent = (disk.used / disk.total) * 100
            
            if used_percent > 90:
                issues.append({
                    'type': 'low_disk_space',
                    'free_gb': round(free_gb, 2),
                    'total_gb': round(total_gb, 2),
                    'severity': 'high',
                    'auto_fixable': True
                })
            elif used_percent > 80:
                issues.append({
                    'type': 'medium_disk_space',
                    'free_gb': round(free_gb, 2),
                    'total_gb': round(total_gb, 2),
                    'severity': 'medium',
                    'auto_fixable': False
                })
        except:
            pass
        
        return issues
    
    def _calculate_health_score(self, issues: List[Dict]) -> int:
        """محاسبه امتیاز سلامت"""
        score = 100
        
        for issue in issues:
            if issue['severity'] == 'high':
                score -= 15
            elif issue['severity'] == 'medium':
                score -= 5
            else:
                score -= 1
        
        return max(0, min(100, score))
    
    def _can_fix_syntax(self, error: SyntaxError) -> bool:
        """آیا می‌شه خطای سینتکس رو خودکار رفع کرد"""
        fixable_patterns = [
            'unexpected indent',
            'unindent does not match',
            'expected an indented block',
            'invalid syntax'
        ]
        
        msg = str(error).lower()
        return any(pattern in msg for pattern in fixable_patterns)
    
    def _apply_fix(self, issue: Dict) -> Optional[str]:
        """اعمال fix برای یک مشکل"""
        
        if issue['type'] == 'missing_module':
            return self._fix_missing_module(issue['module'])
        
        elif issue['type'] == 'syntax_error':
            return self._fix_syntax_error(issue)
        
        elif issue['type'] == 'high_memory_usage':
            return self._fix_memory_usage()
        
        elif issue['type'] == 'low_disk_space':
            return self._fix_disk_space()
        
        return None
    
    def _fix_missing_module(self, module: str) -> str:
        """نصب ماژول missing"""
        try:
            logger.info(f"📦 Installing missing module: {module}")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", module],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.stats['total_heals'] += 1
                self.successful_fixes[module] = datetime.now().isoformat()
                return f"Installed module: {module}"
            else:
                return f"Failed to install {module}: {result.stderr}"
        except Exception as e:
            return f"Installation error: {e}"
    
    def _fix_syntax_error(self, issue: Dict) -> Optional[str]:
        """رفع خطای سینتکس"""
        try:
            file_path = issue['file']
            line_num = issue['line']
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # رفع indent مشکل‌دار
            if 'indent' in issue['message'].lower():
                if line_num <= len(lines):
                    lines[line_num-1] = '        ' + lines[line_num-1].lstrip()
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    
                    self.stats['total_heals'] += 1
                    return f"Fixed indentation in {file_path}:{line_num}"
            
            return None
        except Exception as e:
            logger.error(f"Syntax fix failed: {e}")
            return None
    
    def _fix_memory_usage(self) -> str:
        """بهینه‌سازی مصرف حافظه"""
        try:
            import gc
            # پاک کردن garbage collector
            collected = gc.collect()
            
            # پاک کردن کش
            import shutil
            cache_dirs = ['__pycache__', '.pytest_cache', '.mypy_cache']
            for cache in cache_dirs:
                if Path(cache).exists():
                    shutil.rmtree(cache)
            
            self.stats['optimizations'] += 1
            return f"Cleared memory: {collected} objects collected"
        except Exception as e:
            return f"Memory optimization failed: {e}"
    
    def _fix_disk_space(self) -> str:
        """آزادسازی فضای دیسک"""
        try:
            freed_space = 0
            
            # پاک کردن لاگ‌های قدیمی
            log_dir = Path('logs')
            if log_dir.exists():
                for log_file in log_dir.glob('*.log'):
                    if log_file.stat().st_mtime < (time.time() - 7*24*3600):  # older than 7 days
                        size = log_file.stat().st_size
                        log_file.unlink()
                        freed_space += size
            
            # پاک کردن بک‌آپ‌های قدیمی
            backup_dir = Path('backups')
            if backup_dir.exists():
                for backup in backup_dir.glob('*.tar.gz'):
                    if backup.stat().st_mtime < (time.time() - 30*24*3600):  # older than 30 days
                        size = backup.stat().st_size
                        backup.unlink()
                        freed_space += size
            
            freed_mb = freed_space / (1024 * 1024)
            self.stats['optimizations'] += 1
            return f"Freed {freed_mb:.2f} MB disk space"
        except Exception as e:
            return f"Disk cleanup failed: {e}"
    
    def heal(self) -> Dict:
        """
        اجرای فرآیند کامل خودترمیمی
        """
        logger.info("🔄 Starting self-healing process...")
        
        # 1. چک سلامت
        health = self.check_health()
        
        # 2. بهینه‌سازی خودکار
        if self.health_score < 80:
            optimizations = self._optimize_system()
            health['optimizations'] = optimizations
        
        # 3. یادگیری از مشکلات
        if health['issues_found'] > 0:
            self._learn_from_issues(health['issues'])
        
        # 4. ذخیره نتیجه
        result = {
            'health_score': self.health_score,
            'issues_fixed': len(health['fixes_applied']),
            'fixes': health['fixes_applied'],
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Self-healing complete. Health score: {self.health_score}")
        
        return result
    
    def _optimize_system(self) -> List[str]:
        """بهینه‌سازی خودکار سیستم"""
        optimizations = []
        
        # 1. بهینه‌سازی دیتابیس
        db_file = Path('data/oracle.db')
        if db_file.exists():
            try:
                # VACUUM دیتابیس
                import sqlite3
                conn = sqlite3.connect(str(db_file))
                conn.execute("VACUUM")
                conn.close()
                optimizations.append("Optimized database")
            except:
                pass
        
        # 2. فشرده‌سازی فایل‌ها
        log_dir = Path('logs')
        if log_dir.exists():
            for log_file in log_dir.glob('*.log'):
                if log_file.stat().st_size > 10 * 1024 * 1024:  # > 10 MB
                    # rotate log
                    log_file.rename(log_file.with_suffix('.log.old'))
                    optimizations.append(f"Rotated {log_file.name}")
        
        return optimizations
    
    def _learn_from_issues(self, issues: List[Dict]):
        """یادگیری از مشکلات برای آینده"""
        for issue in issues:
            key = f"{issue['type']}_{issue.get('file', 'unknown')}"
            
            if key not in self.known_issues:
                self.known_issues[key] = {
                    'count': 0,
                    'first_seen': datetime.now().isoformat()
                }
            
            self.known_issues[key]['count'] += 1
            self.known_issues[key]['last_seen'] = datetime.now().isoformat()
    
    def predict_issues(self) -> List[Dict]:
        """پیش‌بینی مشکلات آینده بر اساس الگوها"""
        predictions = []
        
        now = datetime.now()
        
        for key, issue_data in self.known_issues.items():
            count = issue_data['count']
            first_seen = datetime.fromisoformat(issue_data['first_seen'])
            last_seen = datetime.fromisoformat(issue_data['last_seen'])
            
            days_active = (last_seen - first_seen).days + 1
            frequency = count / days_active if days_active > 0 else 0
            
            # اگه frequency بالا باشه، احتمال تکرار هست
            if frequency > 5:  # بیش از ۵ بار در روز
                predictions.append({
                    'issue_type': key,
                    'predicted_frequency': frequency,
                    'confidence': min(0.9, frequency / 10),
                    'next_expected': (now + timedelta(hours=24/frequency)).isoformat()
                })
        
        return sorted(predictions, key=lambda x: x['confidence'], reverse=True)
    
    def save_memory(self):
        """ذخیره حافظه"""
        try:
            memory_file = 'memory/healer_memory.json'
            os.makedirs('memory', exist_ok=True)
            
            memory = {
                'stats': self.stats,
                'known_issues': self.known_issues,
                'successful_fixes': self.successful_fixes,
                'health_score': self.health_score,
                'last_check': self.last_check.isoformat(),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save healer memory: {e}")
    
    def load_memory(self):
        """بارگذاری حافظه"""
        try:
            memory_file = 'memory/healer_memory.json'
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
                    self.stats = memory.get('stats', self.stats)
                    self.known_issues = memory.get('known_issues', {})
                    self.successful_fixes = memory.get('successful_fixes', {})
                    self.health_score = memory.get('health_score', 100)
                    if 'last_check' in memory:
                        self.last_check = datetime.fromisoformat(memory['last_check'])
                    logger.info(f"📚 Loaded healer memory: {len(self.known_issues)} known issues")
        except:
            pass

# نمونه‌سازی سراسری
self_healer = SelfHealer()
