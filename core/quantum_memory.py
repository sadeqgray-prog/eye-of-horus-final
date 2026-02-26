#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
حافظه کوانتومی - ذخیره‌سازی اطلاعات با قابلیت:
- رمزنگاری پیشرفته
- فشرده‌سازی هوشمند
- بازیابی سریع
- پشتیبان‌گیری خودکار
- همگام‌سازی ابری
"""

import os
import sys
import json
import time
import logging
import hashlib
import pickle
import zlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import threading
import shutil
import sqlite3

logger = logging.getLogger(__name__)

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logger.warning("⚠️ Cryptography not available. Using basic encryption.")

class QuantumMemory:
    """
    حافظه کوانتومی - مثل یه ابررایانه برای ذخیره‌سازی
    """
    
    def __init__(self, encryption_key: str = None):
        self.memory_dir = Path("memory")
        self.memory_dir.mkdir(exist_ok=True)
        
        # حافظه‌های مختلف
        self.short_term = {}  # حافظه کوتاه‌مدت
        self.long_term = {}   # حافظه بلندمدت
        self.working = {}     # حافظه فعال
        self.cache = {}       # کش
        
        # آمار
        self.stats = {
            'total_writes': 0,
            'total_reads': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'storage_mb': 0
        }
        
        # رمزنگاری
        self.encryption_key = encryption_key or self._generate_key()
        self.cipher = None
        
        if CRYPTO_AVAILABLE:
            try:
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'salt_',
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(self.encryption_key.encode()))
                self.cipher = Fernet(key)
                logger.info("🔐 Encryption enabled")
            except:
                pass
        
        # بارگذاری حافظه
        self.load_all()
        
        # شروع پشتیبان‌گیری خودکار
        self.start_auto_backup()
        
        logger.info("💾 QuantumMemory initialized")
    
    def _generate_key(self) -> str:
        """تولید کلید رمزنگاری"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def store(self, key: str, value: Any, memory_type: str = 'long', 
             encrypt: bool = True, compress: bool = True) -> bool:
        """
        ذخیره یک مقدار در حافظه
        """
        self.stats['total_writes'] += 1
        
        try:
            # سریالایز کردن
            data = pickle.dumps(value)
            
            # فشرده‌سازی
            if compress:
                data = zlib.compress(data)
            
            # رمزنگاری
            if encrypt and self.cipher:
                data = self.cipher.encrypt(data)
            
            # انتخاب حافظه
            if memory_type == 'short':
                self.short_term[key] = {
                    'data': data,
                    'encrypted': encrypt,
                    'compressed': compress,
                    'timestamp': datetime.now().isoformat()
                }
            elif memory_type == 'long':
                self.long_term[key] = {
                    'data': data,
                    'encrypted': encrypt,
                    'compressed': compress,
                    'timestamp': datetime.now().isoformat()
                }
            else:  # working
                self.working[key] = {
                    'data': data,
                    'encrypted': encrypt,
                    'compressed': compress,
                    'timestamp': datetime.now().isoformat()
                }
            
            # ذخیره روی دیسک (برای long-term)
            if memory_type == 'long':
                self._save_to_disk(key, data, encrypt, compress)
            
            # به‌روزرسانی آمار
            self._update_stats()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to store {key}: {e}")
            return False
    
    def retrieve(self, key: str, memory_type: str = 'all', 
                default: Any = None) -> Any:
        """
        بازیابی یک مقدار از حافظه
        """
        self.stats['total_reads'] += 1
        
        # چک کردن کش
        if key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[key]
        
        self.stats['cache_misses'] += 1
        
        try:
            data = None
            encrypted = False
            compressed = False
            
            # جستجو در حافظه‌ها
            if memory_type in ['short', 'all'] and key in self.short_term:
                item = self.short_term[key]
                data = item['data']
                encrypted = item['encrypted']
                compressed = item['compressed']
                
            elif memory_type in ['long', 'all'] and key in self.long_term:
                item = self.long_term[key]
                data = item['data']
                encrypted = item['encrypted']
                compressed = item['compressed']
                
            elif memory_type in ['working', 'all'] and key in self.working:
                item = self.working[key]
                data = item['data']
                encrypted = item['encrypted']
                compressed = item['compressed']
            
            if data is None:
                # تلاش از دیسک
                data = self._load_from_disk(key)
                if data:
                    encrypted = True
                    compressed = True
            
            if data is None:
                return default
            
            # رمزگشایی
            if encrypted and self.cipher:
                data = self.cipher.decrypt(data)
            
            # دکمپرس
            if compressed:
                data = zlib.decompress(data)
            
            # دیسریالایز
            value = pickle.loads(data)
            
            # ذخیره در کش
            self.cache[key] = value
            if len(self.cache) > 1000:
                # حذف قدیمی‌ترین
                oldest = min(self.cache.keys(), key=lambda k: 
                           self.cache.get(k, {}).get('timestamp', 0))
                del self.cache[oldest]
            
            return value
            
        except Exception as e:
            logger.error(f"Failed to retrieve {key}: {e}")
            return default
    
    def _save_to_disk(self, key: str, data: bytes, encrypted: bool, compressed: bool):
        """ذخیره روی دیسک"""
        try:
            safe_key = hashlib.md5(key.encode()).hexdigest()
            file_path = self.memory_dir / f"{safe_key}.mem"
            
            metadata = {
                'key': key,
                'encrypted': encrypted,
                'compressed': compressed,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(file_path, 'wb') as f:
                f.write(pickle.dumps({
                    'metadata': metadata,
                    'data': data
                }))
                
        except Exception as e:
            logger.error(f"Failed to save to disk: {e}")
    
    def _load_from_disk(self, key: str) -> Optional[bytes]:
        """بارگذاری از دیسک"""
        try:
            safe_key = hashlib.md5(key.encode()).hexdigest()
            file_path = self.memory_dir / f"{safe_key}.mem"
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'rb') as f:
                package = pickle.load(f)
                return package['data']
                
        except Exception as e:
            logger.error(f"Failed to load from disk: {e}")
            return None
    
    def forget(self, key: str, memory_type: str = 'all') -> bool:
        """فراموش کردن یک مقدار"""
        try:
            if memory_type in ['short', 'all'] and key in self.short_term:
                del self.short_term[key]
            
            if memory_type in ['long', 'all'] and key in self.long_term:
                del self.long_term[key]
                # حذف از دیسک
                safe_key = hashlib.md5(key.encode()).hexdigest()
                file_path = self.memory_dir / f"{safe_key}.mem"
                if file_path.exists():
                    file_path.unlink()
            
            if memory_type in ['working', 'all'] and key in self.working:
                del self.working[key]
            
            if key in self.cache:
                del self.cache[key]
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to forget {key}: {e}")
            return False
    
    def clear_cache(self):
        """پاک کردن کش"""
        self.cache.clear()
        logger.info("🧹 Cache cleared")
    
    def backup(self, backup_name: str = None) -> Dict:
        """ایجاد پشتیبان کامل"""
        
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = Path("backups") / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 1. کپی فایل‌های حافظه
            for mem_file in self.memory_dir.glob("*.mem"):
                shutil.copy2(mem_file, backup_dir / mem_file.name)
            
            # 2. ذخیره حافظه‌های active
            active_memory = {
                'short_term': self.short_term,
                'long_term': {k: v for k, v in self.long_term.items() 
                            if 'data' not in v},  # بدون داده‌های حجیم
                'working': self.working,
                'stats': self.stats,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(backup_dir / 'active_memory.json', 'w') as f:
                json.dump(active_memory, f, indent=2)
            
            # 3. فشرده‌سازی
            shutil.make_archive(str(backup_dir), 'zip', backup_dir)
            
            # پاک کردن پوشه موقت
            shutil.rmtree(backup_dir)
            
            backup_file = f"{backup_dir}.zip"
            size_mb = Path(backup_file).stat().st_size / (1024 * 1024)
            
            logger.info(f"✅ Backup created: {backup_file} ({size_mb:.2f} MB)")
            
            return {
                'success': True,
                'file': backup_file,
                'size_mb': round(size_mb, 2),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def restore(self, backup_file: str) -> Dict:
        """بازیابی از پشتیبان"""
        
        backup_path = Path(backup_file)
        if not backup_path.exists():
            return {'success': False, 'error': 'Backup not found'}
        
        try:
            # دکمپرس
            import zipfile
            with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                zip_ref.extractall('temp_restore')
            
            restore_dir = Path('temp_restore')
            
            # 1. بازیابی فایل‌های حافظه
            for mem_file in restore_dir.glob("*.mem"):
                shutil.copy2(mem_file, self.memory_dir / mem_file.name)
            
            # 2. بازیابی active memory
            if (restore_dir / 'active_memory.json').exists():
                with open(restore_dir / 'active_memory.json', 'r') as f:
                    active = json.load(f)
                    self.short_term = active.get('short_term', {})
                    self.working = active.get('working', {})
                    self.stats = active.get('stats', self.stats)
            
            # پاک کردن موقت
            shutil.rmtree(restore_dir)
            
            logger.info(f"✅ Restored from: {backup_file}")
            
            return {
                'success': True,
                'backup': backup_file,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _update_stats(self):
        """به‌روزرسانی آمار"""
        total_size = 0
        for file in self.memory_dir.glob("*"):
            total_size += file.stat().st_size
        
        self.stats['storage_mb'] = total_size / (1024 * 1024)
    
    def load_all(self):
        """بارگذاری همه حافظه‌ها از دیسک"""
        try:
            for mem_file in self.memory_dir.glob("*.mem"):
                with open(mem_file, 'rb') as f:
                    package = pickle.load(f)
                    key = package['metadata']['key']
                    self.long_term[key] = {
                        'data': package['data'],
                        'encrypted': package['metadata']['encrypted'],
                        'compressed': package['metadata']['compressed'],
                        'timestamp': package['metadata']['timestamp']
                    }
            
            logger.info(f"📚 Loaded {len(self.long_term)} items from disk")
            
        except Exception as e:
            logger.error(f"Failed to load all memory: {e}")
    
    def start_auto_backup(self):
        """شروع پشتیبان‌گیری خودکار"""
        
        def backup_worker():
            while True:
                try:
                    time.sleep(3600)  # هر ساعت
                    if len(self.long_term) > 100:
                        self.backup(f"auto_backup_{datetime.now().strftime('%Y%m%d_%H')}")
                    
                    # پاک کردن بک‌آپ‌های قدیمی (بیشتر از ۷ روز)
                    backup_dir = Path("backups")
                    if backup_dir.exists():
                        for backup in backup_dir.glob("auto_backup_*.zip"):
                            age = time.time() - backup.stat().st_mtime
                            if age > 7 * 24 * 3600:  # older than 7 days
                                backup.unlink()
                                logger.info(f"🗑️ Deleted old backup: {backup.name}")
                                
                except Exception as e:
                    logger.error(f"Auto backup error: {e}")
                
                time.sleep(3600)  # یه ساعت دیگه
        
        thread = threading.Thread(target=backup_worker, daemon=True)
        thread.start()
        logger.info("🔄 Auto backup started")
    
    def get_stats(self) -> Dict:
        """گرفتن آمار حافظه"""
        return {
            'short_term': len(self.short_term),
            'long_term': len(self.long_term),
            'working': len(self.working),
            'cache': len(self.cache),
            'stats': self.stats,
            'disk_usage_mb': self.stats['storage_mb']
        }

# نمونه‌سازی سراسری
quantum_memory = QuantumMemory()
