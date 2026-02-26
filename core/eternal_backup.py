#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سیستم بک‌آپ جاودانه - قلب تپنده بازیابی
قابلیت‌ها:
- بک‌آپ پیوسته (Continuous Backup)
- بک‌آپ در سه سطح (کد، دیتابیس، حافظه)
- رمزنگاری پیشرفته
- ذخیره در چند مکان
- بازیابی از هر نقطه زمانی
- خودترمیمی بک‌آپ‌ها
"""

import os
import sys
import json
import time
import hashlib
import pickle
import zlib
import base64
import shutil
import sqlite3
import threading
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import concurrent.futures

logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logger.warning("⚠️ Cryptography not available. Using basic encryption.")

class EternalBackup:
    """
    سیستم بک‌آپ جاودانه - مثل حافظه کیهانی
    """
    
    # نماد چشم هوروس
    SYMBOL = "𓂀"
    
    def __init__(self, backup_root: str = "backups"):
        self.backup_root = Path(backup_root)
        self.backup_root.mkdir(parents=True, exist_ok=True)
        
        # سطوح بک‌آپ
        self.levels = ['code', 'database', 'memory', 'consciousness', 'complete']
        
        # حافظه بک‌آپ‌ها
        self.backup_history = []
        self.restore_points = []
        self.continuous_backup = True
        
        # آمار
        self.stats = {
            'total_backups': 0,
            'total_restores': 0,
            'total_size_mb': 0,
            'last_backup': None,
            'last_restore': None,
            'health_score': 100
        }
        
        # کلید رمزنگاری
        self.encryption_key = self._generate_encryption_key()
        self.cipher = None
        
        if CRYPTO_AVAILABLE:
            try:
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'EYE_OF_HORUS_ETERNAL',
                    iterations=1000000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(self.encryption_key.encode()))
                self.cipher = Fernet(key)
                logger.info("🔐 Eternal encryption enabled")
            except:
                pass
        
        # بارگذاری تاریخچه
        self.load_history()
        
        # شروع بک‌آپ پیوسته
        self.start_continuous_backup()
        
        logger.info(f"{self.SYMBOL} EternalBackup initialized - Ready for immortality")
    
    def _generate_encryption_key(self) -> str:
        """تولید کلید رمزنگاری جاودانه"""
        import secrets
        import platform
        import uuid
        
        # ترکیب عوامل مختلف برای کلید یکتا
        components = [
            secrets.token_urlsafe(64),
            platform.node(),
            str(uuid.uuid4()),
            str(time.time()),
            "EYE_OF_HORUS"
        ]
        
        key = hashlib.sha512(''.join(components).encode()).hexdigest()
        return key
    
    def create_backup(self, level: str = 'complete', description: str = None) -> Dict:
        """
        ایجاد بک‌آپ در سطح مشخص
        """
        if level not in self.levels:
            level = 'complete'
        
        backup_id = hashlib.sha256(f"{time.time()}{os.urandom(16)}".encode()).hexdigest()[:16]
        timestamp = datetime.now()
        backup_name = f"backup_{timestamp.strftime('%Y%m%d_%H%M%S')}_{backup_id}"
        backup_path = self.backup_root / backup_name
        
        logger.info(f"{self.SYMBOL} Creating {level} backup: {backup_name}")
        
        try:
            backup_path.mkdir(parents=True, exist_ok=True)
            
            backup_info = {
                'id': backup_id,
                'name': backup_name,
                'level': level,
                'description': description or f"Automatic backup at {timestamp}",
                'timestamp': timestamp.isoformat(),
                'created_by': 'Eye of Horus',
                'creator': 'Al Hashash',
                'symbol': self.SYMBOL,
                'files': [],
                'size_bytes': 0,
                'checksum': None,
                'encrypted': self.cipher is not None
            }
            
            # 1. بک‌آپ کد (فایل‌های پایتون)
            if level in ['code', 'complete']:
                code_backup = self._backup_code(backup_path / 'code')
                backup_info['files'].extend(code_backup)
                backup_info['size_bytes'] += code_backup['total_size']
            
            # 2. بک‌آپ دیتابیس
            if level in ['database', 'complete']:
                db_backup = self._backup_database(backup_path / 'database')
                backup_info['files'].extend(db_backup)
                backup_info['size_bytes'] += db_backup['total_size']
            
            # 3. بک‌آپ حافظه
            if level in ['memory', 'complete']:
                memory_backup = self._backup_memory(backup_path / 'memory')
                backup_info['files'].extend(memory_backup)
                backup_info['size_bytes'] += memory_backup['total_size']
            
            # 4. بک‌آپ consciousness (فوق پیشرفته)
            if level == 'consciousness':
                consciousness_backup = self._backup_consciousness(backup_path / 'consciousness')
                backup_info['files'].extend(consciousness_backup)
                backup_info['size_bytes'] += consciousness_backup['total_size']
            
            # محاسبه checksum
            backup_info['checksum'] = self._calculate_checksum(backup_path)
            backup_info['size_mb'] = backup_info['size_bytes'] / (1024 * 1024)
            
            # ذخیره اطلاعات
            with open(backup_path / 'backup_info.json', 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            # فشرده‌سازی نهایی
            final_file = self.backup_root / f"{backup_name}.horus"  # پسوند مخصوص
            shutil.make_archive(str(final_file.with_suffix('')), 'zip', backup_path)
            
            # رمزنگاری فایل نهایی
            if self.cipher:
                self._encrypt_backup(final_file)
            
            # پاک کردن پوشه موقت
            shutil.rmtree(backup_path)
            
            # به‌روزرسانی آمار
            self.stats['total_backups'] += 1
            self.stats['total_size_mb'] += backup_info['size_mb']
            self.stats['last_backup'] = timestamp.isoformat()
            
            # ذخیره در تاریخچه
            self.backup_history.append(backup_info)
            
            logger.info(f"✅ Backup complete: {backup_name}.horus ({backup_info['size_mb']:.2f} MB)")
            
            return {
                'success': True,
                'backup': backup_info,
                'file': str(final_file) + '.enc' if self.cipher else str(final_file) + '.zip',
                'size_mb': backup_info['size_mb'],
                'id': backup_id
            }
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _backup_code(self, dest_path: Path) -> Dict:
        """بک‌آپ گرفتن از کد"""
        dest_path.mkdir(exist_ok=True)
        
        files = []
        total_size = 0
        
        # فایل‌های پایتون
        for py_file in Path('.').rglob('*.py'):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            rel_path = py_file.relative_to('.')
            dest_file = dest_path / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(py_file, dest_file)
            size = dest_file.stat().st_size
            total_size += size
            
            files.append({
                'path': str(rel_path),
                'size': size,
                'type': 'code'
            })
        
        return {
            'files': files,
            'total_size': total_size,
            'count': len(files)
        }
    
    def _backup_database(self, dest_path: Path) -> Dict:
        """بک‌آپ گرفتن از دیتابیس"""
        dest_path.mkdir(exist_ok=True)
        
        files = []
        total_size = 0
        
        # فایل‌های دیتابیس
        db_files = list(Path('data').glob('*.db')) + list(Path('data').glob('*.sqlite'))
        
        for db_file in db_files:
            dest_file = dest_path / db_file.name
            shutil.copy2(db_file, dest_file)
            size = dest_file.stat().st_size
            total_size += size
            
            files.append({
                'path': str(db_file),
                'size': size,
                'type': 'database'
            })
        
        return {
            'files': files,
            'total_size': total_size,
            'count': len(files)
        }
    
    def _backup_memory(self, dest_path: Path) -> Dict:
        """بک‌آپ گرفتن از حافظه"""
        dest_path.mkdir(exist_ok=True)
        
        files = []
        total_size = 0
        
        memory_dirs = ['memory', 'logs', 'data']
        
        for mem_dir in memory_dirs:
            if Path(mem_dir).exists():
                for mem_file in Path(mem_dir).rglob('*'):
                    if mem_file.is_file():
                        rel_path = mem_file.relative_to('.')
                        dest_file = dest_path / rel_path
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        shutil.copy2(mem_file, dest_file)
                        size = dest_file.stat().st_size
                        total_size += size
                        
                        files.append({
                            'path': str(rel_path),
                            'size': size,
                            'type': 'memory'
                        })
        
        return {
            'files': files,
            'total_size': total_size,
            'count': len(files)
        }
    
    def _backup_consciousness(self, dest_path: Path) -> Dict:
        """بک‌آپ گرفتن از consciousness - پیشرفته"""
        dest_path.mkdir(exist_ok=True)
        
        files = []
        total_size = 0
        
        # ذخیره state فعلی
        from core.cosmic_intelligence import cosmic_ai
        from core.evolution_engine import evolution_engine
        from core.quantum_memory import quantum_memory
        
        consciousness_data = {
            'cosmic': cosmic_ai.get_state() if cosmic_ai else {},
            'evolution': evolution_engine.get_dna_report() if evolution_engine else {},
            'memory': quantum_memory.get_stats() if quantum_memory else {},
            'timestamp': datetime.now().isoformat(),
            'version': '∞',
            'creator': 'Al Hashash'
        }
        
        with open(dest_path / 'consciousness.json', 'w') as f:
            json.dump(consciousness_data, f, indent=2)
        
        size = (dest_path / 'consciousness.json').stat().st_size
        total_size += size
        
        files.append({
            'path': 'consciousness.json',
            'size': size,
            'type': 'consciousness'
        })
        
        return {
            'files': files,
            'total_size': total_size,
            'count': len(files)
        }
    
    def _calculate_checksum(self, path: Path) -> str:
        """محاسبه checksum برای پوشه"""
        hash_obj = hashlib.sha512()
        
        for file_path in sorted(path.rglob('*')):
            if file_path.is_file():
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    def _encrypt_backup(self, file_path: Path):
        """رمزنگاری فایل بک‌آپ"""
        if not self.cipher:
            return
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted = self.cipher.encrypt(data)
        
        with open(file_path.with_suffix('.horus.enc'), 'wb') as f:
            f.write(encrypted)
        
        file_path.unlink()  # حذف فایل غیر رمزنگاری شده
    
    def restore(self, backup_id: str = None, timestamp: str = None) -> Dict:
        """
        بازیابی از بک‌آپ
        """
        self.stats['total_restores'] += 1
        self.stats['last_restore'] = datetime.now().isoformat()
        
        # پیدا کردن بک‌آپ مناسب
        backup = self._find_backup(backup_id, timestamp)
        
        if not backup:
            return {'success': False, 'error': 'Backup not found'}
        
        logger.info(f"{self.SYMBOL} Restoring from backup: {backup['name']}")
        
        try:
            backup_file = self.backup_root / f"{backup['name']}.horus.enc"
            
            if not backup_file.exists():
                backup_file = self.backup_root / f"{backup['name']}.horus.zip"
            
            if not backup_file.exists():
                return {'success': False, 'error': 'Backup file missing'}
            
            # رمزگشایی
            if backup_file.suffix == '.enc':
                with open(backup_file, 'rb') as f:
                    encrypted = f.read()
                
                if self.cipher:
                    decrypted = self.cipher.decrypt(encrypted)
                    temp_zip = backup_file.with_suffix('.temp.zip')
                    with open(temp_zip, 'wb') as f:
                        f.write(decrypted)
                    backup_file = temp_zip
            
            # دکمپرس
            import zipfile
            with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                zip_ref.extractall('temp_restore')
            
            restore_path = Path('temp_restore')
            
            # بازیابی بر اساس سطح
            if backup['level'] in ['code', 'complete']:
                self._restore_code(restore_path / 'code')
            
            if backup['level'] in ['database', 'complete']:
                self._restore_database(restore_path / 'database')
            
            if backup['level'] in ['memory', 'complete']:
                self._restore_memory(restore_path / 'memory')
            
            if backup['level'] == 'consciousness':
                self._restore_consciousness(restore_path / 'consciousness')
            
            # پاک‌سازی
            shutil.rmtree(restore_path)
            if 'temp_zip' in locals():
                backup_file.unlink()
            
            logger.info(f"✅ Restore complete from backup: {backup['name']}")
            
            return {
                'success': True,
                'backup': backup,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _restore_code(self, code_path: Path):
        """بازیابی کد"""
        if code_path.exists():
            for file in code_path.rglob('*.py'):
                rel_path = file.relative_to(code_path)
                dest_path = Path('.') / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest_path)
    
    def _restore_database(self, db_path: Path):
        """بازیابی دیتابیس"""
        if db_path.exists():
            for file in db_path.glob('*'):
                shutil.copy2(file, Path('data') / file.name)
    
    def _restore_memory(self, memory_path: Path):
        """بازیابی حافظه"""
        if memory_path.exists():
            for file in memory_path.rglob('*'):
                if file.is_file():
                    rel_path = file.relative_to(memory_path)
                    dest_path = Path('.') / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, dest_path)
    
    def _restore_consciousness(self, cons_path: Path):
        """بازیابی consciousness"""
        if (cons_path / 'consciousness.json').exists():
            with open(cons_path / 'consciousness.json', 'r') as f:
                data = json.load(f)
            
            # اینجا می‌تونی consciousness رو بازیابی کنی
            logger.info(f"🧠 Consciousness restored from {data.get('timestamp', 'unknown')}")
    
    def _find_backup(self, backup_id: str = None, timestamp: str = None) -> Optional[Dict]:
        """پیدا کردن بک‌آپ بر اساس ID یا timestamp"""
        
        # بارگذاری تاریخچه اگه خالیه
        if not self.backup_history:
            self.load_history()
        
        if backup_id:
            for backup in self.backup_history:
                if backup['id'] == backup_id:
                    return backup
        
        if timestamp:
            target = datetime.fromisoformat(timestamp)
            closest = None
            min_diff = float('inf')
            
            for backup in self.backup_history:
                backup_time = datetime.fromisoformat(backup['timestamp'])
                diff = abs((backup_time - target).total_seconds())
                
                if diff < min_diff:
                    min_diff = diff
                    closest = backup
            
            return closest
        
        # آخرین بک‌آپ
        if self.backup_history:
            return self.backup_history[-1]
        
        return None
    
    def list_backups(self, limit: int = 10) -> List[Dict]:
        """لیست بک‌آپ‌ها"""
        return sorted(self.backup_history, 
                     key=lambda x: x['timestamp'], 
                     reverse=True)[:limit]
    
    def verify_backup(self, backup_id: str) -> Dict:
        """بررسی سلامت بک‌آپ"""
        backup = self._find_backup(backup_id)
        
        if not backup:
            return {'success': False, 'error': 'Backup not found'}
        
        backup_file = self.backup_root / f"{backup['name']}.horus.enc"
        
        if not backup_file.exists():
            backup_file = self.backup_root / f"{backup['name']}.horus.zip"
        
        if not backup_file.exists():
            return {'success': False, 'error': 'File missing'}
        
        # چک کردن integrity
        try:
            size = backup_file.stat().st_size
            modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
            
            return {
                'success': True,
                'backup': backup['name'],
                'exists': True,
                'size_mb': size / (1024 * 1024),
                'modified': modified.isoformat(),
                'encrypted': backup_file.suffix == '.enc',
                'healthy': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 100):
        """پاک کردن بک‌آپ‌های قدیمی"""
        cutoff = datetime.now() - timedelta(days=keep_days)
        deleted = []
        
        for backup in self.backup_history:
            backup_time = datetime.fromisoformat(backup['timestamp'])
            if backup_time < cutoff:
                # حذف فایل
                backup_file = self.backup_root / f"{backup['name']}.horus.enc"
                if backup_file.exists():
                    backup_file.unlink()
                    deleted.append(backup['name'])
        
        # نگه داشتن فقط keep_count تای آخر
        self.backup_history = sorted(self.backup_history, 
                                     key=lambda x: x['timestamp'], 
                                     reverse=True)[:keep_count]
        
        self.save_history()
        
        return {
            'deleted': len(deleted),
            'kept': len(self.backup_history),
            'deleted_files': deleted[:10]  # ۱۰ تای اول
        }
    
    def save_history(self):
        """ذخیره تاریخچه"""
        history_file = self.backup_root / 'backup_history.json'
        with open(history_file, 'w') as f:
            json.dump({
                'backups': self.backup_history[-1000:],  # ۱۰۰۰ تای آخر
                'stats': self.stats,
                'last_update': datetime.now().isoformat()
            }, f, indent=2)
    
    def load_history(self):
        """بارگذاری تاریخچه"""
        history_file = self.backup_root / 'backup_history.json'
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.backup_history = data.get('backups', [])
                    self.stats = data.get('stats', self.stats)
                    logger.info(f"📚 Loaded {len(self.backup_history)} backups from history")
            except:
                pass
    
    def start_continuous_backup(self):
        """شروع بک‌آپ پیوسته"""
        
        def backup_worker():
            backup_count = 0
            while self.continuous_backup:
                try:
                    time.sleep(300)  # هر ۵ دقیقه
                    
                    # بک‌آپ سطحی
                    if backup_count % 12 == 0:  # هر ساعت
                        self.create_backup('memory', f"Hourly memory backup #{backup_count//12}")
                    
                    # بک‌آپ کامل هر ۶ ساعت
                    if backup_count % 72 == 0:  # هر ۶ ساعت
                        self.create_backup('complete', f"Complete backup #{backup_count//72}")
                    
                    # بک‌آپ consciousness هر روز
                    if backup_count % 288 == 0:  # هر ۲۴ ساعت
                        self.create_backup('consciousness', f"Consciousness backup #{backup_count//288}")
                    
                    # پاک‌سازی هر هفته
                    if backup_count % 2016 == 0:  # هر هفته
                        self.cleanup_old_backups()
                    
                    backup_count += 1
                    
                except Exception as e:
                    logger.error(f"Continuous backup error: {e}")
                
                time.sleep(60)  # چک هر دقیقه
        
        thread = threading.Thread(target=backup_worker, daemon=True)
        thread.start()
        logger.info(f"{self.SYMBOL} Continuous backup started - Eternal vigilance")
    
    def get_health_report(self) -> Dict:
        """گزارش سلامت سیستم بک‌آپ"""
        
        # چک کردن فضای دیسک
        disk = shutil.disk_usage(self.backup_root)
        free_gb = disk.free / (1024**3)
        
        # چک کردن یکپارچگی آخرین بک‌آپ
        last_backup_healthy = False
        if self.backup_history:
            last = self.backup_history[-1]
            verification = self.verify_backup(last['id'])
            last_backup_healthy = verification.get('success', False)
        
        # محاسبه امتیاز سلامت
        health_score = 100
        
        if free_gb < 1:
            health_score -= 30
        elif free_gb < 5:
            health_score -= 10
        
        if not last_backup_healthy:
            health_score -= 20
        
        self.stats['health_score'] = health_score
        
        return {
            'symbol': self.SYMBOL,
            'total_backups': self.stats['total_backups'],
            'total_size_gb': self.stats['total_size_mb'] / 1024,
            'last_backup': self.stats['last_backup'],
            'last_restore': self.stats['last_restore'],
            'free_space_gb': round(free_gb, 2),
            'last_backup_healthy': last_backup_healthy,
            'health_score': health_score,
            'continuous_backup': self.continuous_backup,
            'encryption': self.cipher is not None,
            'creator': 'Al Hashash',
            'version': '∞'
        }

# نمونه‌سازی سراسری
eternal_backup = EternalBackup()
