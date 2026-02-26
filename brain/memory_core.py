#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
💾 MEMORY CORE - هسته حافظه بی‌نهایت
مدیریت تمام خاطرات و تجربیات ربات
قابلیت:
- ذخیره خاطرات کوتاه‌مدت و بلندمدت
- بازیابی هوشمند بر اساس ارتباط
- بک‌آپ خودکار
- فشرده‌سازی و بهینه‌سازی
- یادآوری خاطرات قدیمی
"""

import logging
import json
import hashlib
import asyncio
import pickle
import zlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import threading
import time

logger = logging.getLogger(__name__)

class MemoryCore:
    """
    هسته حافظه - جایی که تمام تجربیات ذخیره می‌شود
    ربات هیچ چیز را فراموش نمی‌کند
    """
    
    def __init__(self):
        self.name = "Memory Core"
        self.version = "1.0.0"
        
        # مسیر ذخیره‌سازی
        self.memory_path = Path("memory")
        self.memory_path.mkdir(exist_ok=True)
        
        # حافظه‌های مختلف
        self.short_term = {}  # حافظه کوتاه‌مدت (موقت)
        self.long_term = {}   # حافظه بلندمدت (دائمی)
        self.working = {}     # حافظه فعال (برای پردازش)
        self.emotional = {}   # حافظه عاطفی (تجربیات مهم)
        
        # ایندکس‌ها
        self.index = {
            'by_time': [],
            'by_topic': {},
            'by_user': {},
            'by_importance': []
        }
        
        # آمار
        self.stats = {
            'total_memories': 0,
            'short_term_count': 0,
            'long_term_count': 0,
            'emotional_count': 0,
            'last_backup': None,
            'memory_size_mb': 0
        }
        
        # تنظیمات
        self.settings = {
            'short_term_limit': 1000,  # حداکثر حافظه کوتاه‌مدت
            'auto_backup': True,
            'backup_interval': 3600,  # هر ساعت
            'compress': True,
            'encrypt': False
        }
        
        # بارگذاری حافظه
        self._load_memory()
        
        # شروع بک‌آپ خودکار
        if self.settings['auto_backup']:
            self._start_auto_backup()
        
        logger.info("💾 Memory Core initialized")
    
    def _load_memory(self):
        """بارگذاری حافظه از دیسک"""
        try:
            # حافظه بلندمدت
            long_file = self.memory_path / "long_term.pkl"
            if long_file.exists():
                with open(long_file, 'rb') as f:
                    self.long_term = pickle.load(f)
                logger.info(f"📚 Loaded {len(self.long_term)} long-term memories")
            
            # ایندکس
            index_file = self.memory_path / "index.json"
            if index_file.exists():
                with open(index_file, 'r') as f:
                    self.index = json.load(f)
            
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
    
    def _save_memory(self):
        """ذخیره حافظه روی دیسک"""
        try:
            # حافظه بلندمدت
            with open(self.memory_path / "long_term.pkl", 'wb') as f:
                pickle.dump(self.long_term, f)
            
            # ایندکس
            with open(self.memory_path / "index.json", 'w') as f:
                json.dump(self.index, f, indent=2)
            
            logger.info("💾 Memory saved to disk")
            
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def _start_auto_backup(self):
        """شروع بک‌آپ خودکار"""
        def backup_worker():
            while True:
                try:
                    time.sleep(self.settings['backup_interval'])
                    self.backup()
                except:
                    pass
        
        thread = threading.Thread(target=backup_worker, daemon=True)
        thread.start()
        logger.info("🔄 Auto backup started")
    
    async def store(self, key: str, value: Any, memory_type: str = 'long', 
                   importance: float = 0.5, metadata: Dict = None) -> str:
        """
        ذخیره یک خاطره
        
        Args:
            key: کلید خاطره
            value: مقدار خاطره
            memory_type: نوع حافظه ('short', 'long', 'emotional')
            importance: اهمیت (0-1)
            metadata: فراداده اضافی
        """
        memory_id = hashlib.md5(f"{key}{datetime.now()}".encode()).hexdigest()[:16]
        
        memory = {
            'id': memory_id,
            'key': key,
            'value': value,
            'type': memory_type,
            'importance': importance,
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'access_count': 0
        }
        
        # ذخیره بر اساس نوع
        if memory_type == 'short':
            self.short_term[memory_id] = memory
            self.stats['short_term_count'] += 1
            
            # مدیریت محدودیت
            if len(self.short_term) > self.settings['short_term_limit']:
                self._prune_short_term()
        
        elif memory_type == 'emotional':
            self.emotional[memory_id] = memory
            self.stats['emotional_count'] += 1
        
        else:  # long
            self.long_term[memory_id] = memory
            self.stats['long_term_count'] += 1
        
        # به‌روزرسانی ایندکس
        self._update_index(memory)
        
        self.stats['total_memories'] += 1
        
        # بک‌آپ خودکار برای خاطرات مهم
        if importance > 0.8:
            await self._backup_important(memory)
        
        return memory_id
    
    def _update_index(self, memory: Dict):
        """به‌روزرسانی ایندکس جستجو"""
        # ایندکس زمانی
        self.index['by_time'].append({
            'id': memory['id'],
            'time': memory['created_at'],
            'importance': memory['importance']
        })
        
        # محدودیت ایندکس زمانی
        if len(self.index['by_time']) > 10000:
            self.index['by_time'] = self.index['by_time'][-10000:]
        
        # ایندکس بر اساس کاربر
        user_id = memory['metadata'].get('user_id')
        if user_id:
            if str(user_id) not in self.index['by_user']:
                self.index['by_user'][str(user_id)] = []
            self.index['by_user'][str(user_id)].append(memory['id'])
    
    def _prune_short_term(self):
        """پاکسازی حافظه کوتاه‌مدت"""
        # نگه داشتن مهم‌ترین‌ها
        sorted_memories = sorted(
            self.short_term.values(),
            key=lambda x: (x['importance'], x['last_accessed']),
            reverse=True
        )
        
        # حفظ ۸۰٪ از مهم‌ترین‌ها
        keep_count = int(self.settings['short_term_limit'] * 0.8)
        keep_ids = [m['id'] for m in sorted_memories[:keep_count]]
        
        self.short_term = {id: m for id, m in self.short_term.items() if id in keep_ids}
        self.stats['short_term_count'] = len(self.short_term)
    
    async def recall(self, query: str, limit: int = 10, 
                    memory_type: str = 'all') -> List[Dict]:
        """
        یادآوری خاطرات مرتبط با یک query
        """
        results = []
        query = query.lower()
        
        # انتخاب حافظه بر اساس نوع
        memories = {}
        if memory_type in ['all', 'short']:
            memories.update(self.short_term)
        if memory_type in ['all', 'long']:
            memories.update(self.long_term)
        if memory_type in ['all', 'emotional']:
            memories.update(self.emotional)
        
        # جستجو و محاسبه ارتباط
        scored_memories = []
        for mem_id, memory in memories.items():
            score = self._calculate_relevance(query, memory)
            if score > 0:
                scored_memories.append((score, memory))
        
        # مرتب‌سازی بر اساس ارتباط
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # به‌روزرسانی آخرین دسترسی
        for score, memory in scored_memories[:limit]:
            memory['last_accessed'] = datetime.now().isoformat()
            memory['access_count'] += 1
            results.append(memory)
        
        return results
    
    def _calculate_relevance(self, query: str, memory: Dict) -> float:
        """محاسبه میزان ارتباط خاطره با query"""
        score = 0
        
        # جستجو در key
        if query in memory['key'].lower():
            score += 0.3
        
        # جستجو در value (اگر متن باشد)
        if isinstance(memory['value'], str):
            if query in memory['value'].lower():
                score += 0.5
        elif isinstance(memory['value'], dict):
            if any(query in str(v).lower() for v in memory['value'].values()):
                score += 0.4
        
        # اهمیت خاطره
        score += memory['importance'] * 0.2
        
        # تعداد دسترسی (خاطرات پراستفاده)
        score += min(0.2, memory['access_count'] * 0.01)
        
        return min(1.0, score)
    
    async def remember_by_user(self, user_id: int, limit: int = 20) -> List[Dict]:
        """یادآوری خاطرات یک کاربر خاص"""
        memories = []
        
        if str(user_id) in self.index['by_user']:
            for mem_id in self.index['by_user'][str(user_id)][-limit:]:
                if mem_id in self.long_term:
                    memories.append(self.long_term[mem_id])
                elif mem_id in self.emotional:
                    memories.append(self.emotional[mem_id])
        
        return memories
    
    async def forget(self, memory_id: str, memory_type: str = 'all') -> bool:
        """فراموش کردن یک خاطره"""
        if memory_type in ['all', 'short'] and memory_id in self.short_term:
            del self.short_term[memory_id]
            self.stats['short_term_count'] -= 1
            return True
        
        if memory_type in ['all', 'long'] and memory_id in self.long_term:
            del self.long_term[memory_id]
            self.stats['long_term_count'] -= 1
            return True
        
        if memory_type in ['all', 'emotional'] and memory_id in self.emotional:
            del self.emotional[memory_id]
            self.stats['emotional_count'] -= 1
            return True
        
        return False
    
    async def clear_short_term(self):
        """پاک کردن حافظه کوتاه‌مدت"""
        self.short_term.clear()
        self.stats['short_term_count'] = 0
        logger.info("🧹 Short-term memory cleared")
    
    def backup(self) -> Dict:
        """
        ایجاد بک‌آپ کامل از حافظه
        """
        backup_id = hashlib.md5(f"backup_{datetime.now()}".encode()).hexdigest()[:10]
        backup_time = datetime.now()
        
        backup_data = {
            'id': backup_id,
            'timestamp': backup_time.isoformat(),
            'short_term': self.short_term,
            'long_term': self.long_term,
            'emotional': self.emotional,
            'index': self.index,
            'stats': self.stats
        }
        
        # فشرده‌سازی
        if self.settings['compress']:
            data = pickle.dumps(backup_data)
            compressed = zlib.compress(data)
        else:
            compressed = pickle.dumps(backup_data)
        
        # ذخیره بک‌آپ
        backup_file = self.memory_path / f"backup_{backup_id}.mem"
        with open(backup_file, 'wb') as f:
            f.write(compressed)
        
        self.stats['last_backup'] = backup_time.isoformat()
        
        size_mb = backup_file.stat().st_size / (1024 * 1024)
        logger.info(f"✅ Backup created: {backup_file.name} ({size_mb:.2f} MB)")
        
        return {
            'id': backup_id,
            'file': str(backup_file),
            'size_mb': round(size_mb, 2),
            'timestamp': backup_time.isoformat()
        }
    
    async def _backup_important(self, memory: Dict):
        """بک‌آپ خاطرات مهم به صورت جداگانه"""
        important_file = self.memory_path / "important_memories.json"
        
        try:
            if important_file.exists():
                with open(important_file, 'r') as f:
                    important = json.load(f)
            else:
                important = []
            
            important.append({
                'id': memory['id'],
                'key': memory['key'],
                'importance': memory['importance'],
                'time': memory['created_at']
            })
            
            # نگه داشتن ۱۰۰ تای آخر
            important = important[-100:]
            
            with open(important_file, 'w') as f:
                json.dump(important, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error backing up important memory: {e}")
    
    def restore(self, backup_id: str = None) -> bool:
        """
        بازیابی از بک‌آپ
        """
        if backup_id:
            backup_file = self.memory_path / f"backup_{backup_id}.mem"
        else:
            # آخرین بک‌آپ
            backups = list(self.memory_path.glob("backup_*.mem"))
            if not backups:
                logger.error("No backups found")
                return False
            backup_file = max(backups, key=lambda p: p.stat().st_mtime)
        
        try:
            with open(backup_file, 'rb') as f:
                compressed = f.read()
            
            # دکمپرس
            data = pickle.loads(zlib.decompress(compressed))
            
            self.short_term = data['short_term']
            self.long_term = data['long_term']
            self.emotional = data['emotional']
            self.index = data['index']
            self.stats = data['stats']
            
            logger.info(f"✅ Restored from backup: {backup_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """گرفتن آمار حافظه"""
        # محاسبه حجم
        total_size = 0
        for mem_dict in [self.short_term, self.long_term, self.emotional]:
            total_size += len(pickle.dumps(mem_dict))
        
        self.stats['memory_size_mb'] = total_size / (1024 * 1024)
        
        return {
            'stats': self.stats,
            'short_term': len(self.short_term),
            'long_term': len(self.long_term),
            'emotional': len(self.emotional),
            'index_size': {
                'by_time': len(self.index['by_time']),
                'by_user': len(self.index['by_user']),
                'by_topic': len(self.index['by_topic'])
            }
        }
    
    def get_memory_by_id(self, memory_id: str) -> Optional[Dict]:
        """دریافت یک خاطره با ID"""
        if memory_id in self.short_term:
            return self.short_term[memory_id]
        if memory_id in self.long_term:
            return self.long_term[memory_id]
        if memory_id in self.emotional:
            return self.emotional[memory_id]
        return None

# نمونه‌سازی سراسری
memory_core = MemoryCore()
