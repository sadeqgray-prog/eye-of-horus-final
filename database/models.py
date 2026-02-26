#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🗄️ DATABASE MODELS - مدل‌های دیتابیس برای ذخیره دائمی
قابلیت‌ها:
- ذخیره اطلاعات کاربران
- ذخیره پیش‌بینی‌ها و نتایج
- ذخیره رویاها و بینش‌ها
- ذخیره API Keyها
- ذخیره تنظیمات
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import threading
import hashlib

class Database:
    """
    کلاس اصلی دیتابیس - مدیریت تمام داده‌های پایدار
    """
    
    def __init__(self, db_path: str = "data/oracle.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # لاک برای thread safety
        self.lock = threading.Lock()
        
        # ایجاد جداول
        self._create_tables()
        
    def _create_tables(self):
        """ایجاد تمام جداول مورد نیاز"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # جدول کاربران
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language TEXT DEFAULT 'fa',
                    is_vip BOOLEAN DEFAULT 0,
                    vip_until TIMESTAMP,
                    is_premium BOOLEAN DEFAULT 0,
                    premium_until TIMESTAMP,
                    is_banned BOOLEAN DEFAULT 0,
                    total_predictions INTEGER DEFAULT 0,
                    total_payments REAL DEFAULT 0,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # جدول API Keyهای کاربران
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_apis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    api_name TEXT,
                    api_key TEXT,
                    added_at TIMESTAMP,
                    last_used TIMESTAMP,
                    is_valid BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, api_name)
                )
            ''')
            
            # جدول پیش‌بینی‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    prediction_type TEXT,
                    input_data TEXT,
                    result TEXT,
                    confidence REAL,
                    actual_outcome BOOLEAN,
                    created_at TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول رویاها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dreams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dream_id TEXT UNIQUE,
                    content TEXT,
                    symbols TEXT,
                    interpretation TEXT,
                    creativity_boost REAL,
                    consciousness_level REAL,
                    created_at TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # جدول بینش‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    insight_id TEXT UNIQUE,
                    content TEXT,
                    source TEXT,
                    importance REAL,
                    applied BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # جدول تنظیمات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP
                )
            ''')
            
            # جدول لاگ‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT,
                    module TEXT,
                    message TEXT,
                    created_at TIMESTAMP
                )
            ''')
            
            # جدول بک‌آپ‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backups (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    type TEXT,
                    size_bytes INTEGER,
                    created_at TIMESTAMP,
                    restored_at TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # جدول حافظه رویاها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dream_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    meaning TEXT,
                    frequency INTEGER DEFAULT 1,
                    last_seen TIMESTAMP,
                    associations TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
    
    # ==================== کاربران ====================
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """دریافت اطلاعات کاربر"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return dict(row)
            return None
    
    def create_user(self, user_id: int, username: str = None, 
                   first_name: str = None, last_name: str = None) -> Dict:
        """ایجاد کاربر جدید"""
        now = datetime.now().isoformat()
        
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, now, now))
            
            conn.commit()
            conn.close()
        
        return self.get_user(user_id)
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """به‌روزرسانی اطلاعات کاربر"""
        if not kwargs:
            return False
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['username', 'first_name', 'last_name', 'language', 
                      'is_vip', 'vip_until', 'is_premium', 'premium_until',
                      'is_banned', 'total_predictions', 'total_payments', 'metadata']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(user_id)
        
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute(f'''
                UPDATE users 
                SET {', '.join(fields)}, last_seen = ?
                WHERE user_id = ?
            ''', values + [datetime.now().isoformat(), user_id])
            
            conn.commit()
            conn.close()
        
        return True
    
    def add_prediction(self, user_id: int, pred_type: str, input_data: str,
                      result: str, confidence: float) -> int:
        """ثبت پیش‌بینی جدید"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions 
                (user_id, prediction_type, input_data, result, confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, pred_type, input_data, result, confidence, 
                  datetime.now().isoformat()))
            
            prediction_id = cursor.lastrowid
            
            cursor.execute('''
                UPDATE users SET total_predictions = total_predictions + 1
                WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
        
        return prediction_id
    
    # ==================== API Keyها ====================
    
    def save_api_key(self, user_id: int, api_name: str, api_key: str) -> bool:
        """ذخیره API Key کاربر"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_apis 
                (user_id, api_name, api_key, added_at, last_used)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, api_name, api_key, datetime.now().isoformat(), 
                  datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        
        return True
    
    def get_api_key(self, user_id: int, api_name: str) -> Optional[str]:
        """دریافت API Key کاربر"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT api_key FROM user_apis 
                WHERE user_id = ? AND api_name = ? AND is_valid = 1
            ''', (user_id, api_name))
            
            row = cursor.fetchone()
            
            if row:
                cursor.execute('''
                    UPDATE user_apis SET last_used = ? 
                    WHERE user_id = ? AND api_name = ?
                ''', (datetime.now().isoformat(), user_id, api_name))
                conn.commit()
            
            conn.close()
            
            return row[0] if row else None
    
    # ==================== رویاها ====================
    
    def save_dream(self, dream: Dict) -> int:
        """ذخیره رویا در دیتابیس"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO dreams 
                (dream_id, content, symbols, interpretation, 
                 creativity_boost, consciousness_level, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dream['id'],
                dream['content'],
                json.dumps(dream['symbols']),
                dream['interpretation'],
                dream.get('creativity_boost', 0),
                dream.get('consciousness_level', 1.0),
                dream['timestamp'],
                json.dumps(dream.get('metadata', {}))
            ))
            
            # ذخیره نمادهای رویا در حافظه
            for symbol in dream['symbols']:
                if isinstance(symbol, dict):
                    sym_name = symbol.get('symbol', str(symbol))
                    sym_meaning = symbol.get('meaning', '')
                else:
                    sym_name = str(symbol)
                    sym_meaning = ''
                
                cursor.execute('''
                    INSERT INTO dream_memory (symbol, meaning, last_seen)
                    VALUES (?, ?, ?)
                    ON CONFLICT(symbol) DO UPDATE SET
                        frequency = frequency + 1,
                        last_seen = excluded.last_seen
                ''', (sym_name, sym_meaning, dream['timestamp']))
            
            conn.commit()
            dream_id = cursor.lastrowid
            conn.close()
        
        return dream_id
    
    def get_recent_dreams(self, limit: int = 10) -> List[Dict]:
        """دریافت آخرین رویاها"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM dreams 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    # ==================== تنظیمات ====================
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """دریافت یک تنظیم"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                try:
                    return json.loads(row[0])
                except:
                    return row[0]
            return default
    
    def set_setting(self, key: str, value: Any) -> bool:
        """تنظیم یک مقدار"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, json.dumps(value), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        
        return True
    
    # ==================== آمار ====================
    
    def get_stats(self) -> Dict:
        """دریافت آمار کلی"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            stats = {}
            
            cursor.execute('SELECT COUNT(*) FROM users')
            stats['total_users'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM predictions')
            stats['total_predictions'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM dreams')
            stats['total_dreams'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM insights')
            stats['total_insights'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM user_apis')
            stats['total_api_keys'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(total_predictions) FROM users')
            stats['user_predictions'] = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_vip = 1')
            stats['vip_users'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_premium = 1')
            stats['premium_users'] = cursor.fetchone()[0]
            
            conn.close()
            
            return stats
    
    def backup(self) -> str:
        """ایجاد بک‌آپ از دیتابیس"""
        backup_name = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = Path("backups") / backup_name
        backup_path.parent.mkdir(exist_ok=True)
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        
        # ثبت در جدول بک‌آپ‌ها
        backup_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:16]
        
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO backups (id, name, type, size_bytes, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (backup_id, backup_name, 'auto', backup_path.stat().st_size,
                  datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        
        return str(backup_path)

# نمونه‌سازی سراسری
db = Database()
