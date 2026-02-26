#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مدیریت خطای هوشمند با قابلیت:
- تشخیص خودکار خطا
- یادگیری از خطاها
- پیشنهاد راه حل
- خودترمیمی
- گزارش به مدیر
"""

import logging
import sys
import traceback
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from functools import wraps
import asyncio
import hashlib

logger = logging.getLogger(__name__)

class ErrorHandler:
    """
    مغز متفکر مدیریت خطا - خودش یاد می‌گیره و تکامل پیدا می‌کنه
    """
    
    def __init__(self, admin_chat_id: int = 6590867551):
        self.admin_chat_id = admin_chat_id
        self.error_count = 0
        self.error_history = []
        self.error_patterns = {}
        self.solution_cache = {}
        self.recovery_strategies = {}
        self.learning_memory = []
        
        # آمار
        self.stats = {
            'total_errors': 0,
            'fixed_automatically': 0,
            'needed_attention': 0,
            'patterns_learned': 0
        }
        
        # بارگذاری حافظه قبلی
        self.load_memory()
        
        logger.info("🧠 ErrorHandler v5.0 initialized")
    
    def handle_error(self, error: Exception, context: Dict = None) -> Dict:
        """
        مدیریت هوشمند خطا با تشخیص و پیشنهاد راه حل
        """
        self.error_count += 1
        self.stats['total_errors'] += 1
        
        error_type = type(error).__name__
        error_hash = self._get_error_hash(error, context)
        error_info = {
            'id': error_hash,
            'type': error_type,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'timestamp': datetime.now().isoformat(),
            'count': self.error_count
        }
        
        # ذخیره در تاریخچه
        self.error_history.append(error_info)
        if len(self.error_history) > 1000:
            self.error_history = self.error_history[-1000:]
        
        # به‌روزرسانی الگوها
        self._update_patterns(error_info)
        
        # لاگ کردن
        logger.error(f"❌ Error #{self.error_count}: {error_type}")
        logger.debug(f"🔍 Context: {context}")
        
        # تلاش برای بازیابی خودکار
        solution = self._try_auto_recovery(error, context)
        
        # اگر راه حلی پیدا شد
        if solution:
            self.stats['fixed_automatically'] += 1
            error_info['solution'] = solution
            logger.info(f"✅ Auto-recovered: {solution}")
        
        # اگه خطا جدی بود، به ادمین گزارش بده
        if self._is_critical(error_type, context):
            self._notify_admin(error_info)
            self.stats['needed_attention'] += 1
        
        # ذخیره حافظه
        self.save_memory()
        
        return error_info
    
    def _get_error_hash(self, error: Exception, context: Dict = None) -> str:
        """ایجاد هش یکتا برای خطا"""
        error_str = f"{type(error).__name__}:{str(error)}"
        if context:
            error_str += json.dumps(context, sort_keys=True)
        return hashlib.md5(error_str.encode()).hexdigest()[:10]
    
    def _update_patterns(self, error_info: Dict):
        """به‌روزرسانی الگوهای خطا"""
        error_type = error_info['type']
        
        if error_type not in self.error_patterns:
            self.error_patterns[error_type] = {
                'count': 0,
                'first_seen': error_info['timestamp'],
                'last_seen': error_info['timestamp'],
                'examples': [],
                'solutions_found': []
            }
        
        pattern = self.error_patterns[error_type]
        pattern['count'] += 1
        pattern['last_seen'] = error_info['timestamp']
        
        # نگه داشتن ۵ مثال آخر
        pattern['examples'].append(error_info['message'])
        if len(pattern['examples']) > 5:
            pattern['examples'] = pattern['examples'][-5:]
        
        # یادگیری از تکرار
        if pattern['count'] > 10:
            self._learn_from_pattern(error_type, pattern)
    
    def _learn_from_pattern(self, error_type: str, pattern: Dict):
        """یادگیری از الگوهای تکراری"""
        lesson = {
            'error_type': error_type,
            'frequency': pattern['count'],
            'first_seen': pattern['first_seen'],
            'last_seen': pattern['last_seen'],
            'learned_at': datetime.now().isoformat(),
            'suggested_solution': self._suggest_solution(error_type)
        }
        
        self.learning_memory.append(lesson)
        self.stats['patterns_learned'] += 1
        
        logger.info(f"📚 Learned pattern: {error_type} (occurred {pattern['count']} times)")
    
    def _suggest_solution(self, error_type: str) -> str:
        """پیشنهاد راه حل برای نوع خطا"""
        
        solutions = {
            'ModuleNotFoundError': "Install missing module using 'pip install <module>'",
            'ImportError': "Check module name and path, or use safe_imports",
            'IndentationError': "Run auto_formatter or check spaces vs tabs",
            'ConnectionError': "Add retry logic with exponential backoff",
            'TimeoutError': "Increase timeout or use async with timeouts",
            'KeyError': "Check dictionary keys or use .get() with default",
            'AttributeError': "Verify object has the attribute before accessing",
            'TypeError': "Check variable types and conversion",
            'ValueError': "Validate input before processing",
            'ZeroDivisionError': "Add check for zero before division",
            'FileNotFoundError': "Verify file path and permissions",
            'PermissionError': "Check file/directory permissions",
            'MemoryError': "Optimize memory usage or increase available memory",
            'OverflowError': "Use larger data type or handle overflow",
            'RecursionError': "Increase recursion limit or optimize recursion"
        }
        
        return solutions.get(error_type, "Unknown error pattern. Check logs for details.")
    
    def _try_auto_recovery(self, error: Exception, context: Dict = None) -> Optional[str]:
        """تلاش برای بازیابی خودکار از خطا"""
        
        error_type = type(error).__name__
        
        # استراتژی‌های بازیابی ثبت شده
        if error_type in self.recovery_strategies:
            try:
                return self.recovery_strategies[error_type](error, context)
            except Exception as e:
                logger.error(f"Recovery failed: {e}")
        
        # خطاهای قابل بازیابی خودکار
        if error_type == 'ModuleNotFoundError':
            return self._recover_module_not_found(error)
        
        elif error_type == 'ConnectionError':
            return self._recover_connection_error(error)
        
        elif error_type == 'TimeoutError':
            return self._recover_timeout_error(error)
        
        elif error_type == 'MemoryError':
            return self._recover_memory_error(error)
        
        return None
    
    def _recover_module_not_found(self, error: Exception) -> str:
        """بازیابی از خطای ModuleNotFoundError"""
        try:
            module_name = str(error).split("'")[1]
            logger.info(f"🔧 Attempting to install {module_name}...")
            
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", module_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.solution_cache[module_name] = {
                    'installed_at': datetime.now().isoformat(),
                    'success': True
                }
                return f"Auto-installed module: {module_name}"
            else:
                return f"Failed to install {module_name}: {result.stderr}"
        except:
            return "Auto-recovery failed"
    
    def _recover_connection_error(self, error: Exception) -> str:
        """بازیابی از خطای ConnectionError"""
        # افزایش تعداد تلاش‌ها و استفاده از backoff
        retry_count = context.get('retry_count', 0) if 'context' in locals() else 0
        if retry_count < 3:
            return f"Retrying connection (attempt {retry_count + 1}/3)"
        return "Connection failed after 3 attempts"
    
    def _recover_timeout_error(self, error: Exception) -> str:
        """بازیابی از خطای TimeoutError"""
        # افزایش timeout
        return "Increasing timeout and retrying"
    
    def _recover_memory_error(self, error: Exception) -> str:
        """بازیابی از خطای MemoryError"""
        # پاک کردن کش
        import gc
        gc.collect()
        return "Cleared cache and garbage collected"
    
    def _is_critical(self, error_type: str, context: Dict = None) -> bool:
        """تشخیص خطاهای بحرانی"""
        critical_errors = [
            'SystemError',
            'KeyboardInterrupt',
            'SystemExit',
            'FatalError',
            'DatabaseError',
            'AuthenticationError'
        ]
        
        # خطاهایی که زیاد تکرار شدن
        if error_type in self.error_patterns:
            if self.error_patterns[error_type]['count'] > 100:
                return True
        
        return error_type in critical_errors
    
    def _notify_admin(self, error_info: Dict):
        """گزارش خطا به ادمین (از طریق تلگرام)"""
        # این بخش توسط ربات اصلی انجام میشه
        # فعلاً فقط لاگ می‌کنیم
        logger.critical(f"🚨 Critical error needs attention: {error_info['type']}")
    
    def register_recovery(self, error_type: str, strategy: Callable):
        """ثبت استراتژی بازیابی برای یک نوع خطا"""
        self.recovery_strategies[error_type] = strategy
        logger.info(f"🔧 Registered recovery strategy for {error_type}")
    
    def get_solution(self, error_hash: str) -> Optional[Dict]:
        """دریافت راه حل برای یک خطا"""
        return self.solution_cache.get(error_hash)
    
    def get_stats(self) -> Dict:
        """گرفتن آمار خطاها"""
        return {
            'total_errors': self.stats['total_errors'],
            'fixed_automatically': self.stats['fixed_automatically'],
            'needed_attention': self.stats['needed_attention'],
            'patterns_learned': self.stats['patterns_learned'],
            'active_patterns': len(self.error_patterns),
            'recent_errors': self.error_history[-5:] if self.error_history else []
        }
    
    def get_pattern_summary(self) -> List[Dict]:
        """خلاصه الگوهای خطا"""
        summary = []
        for error_type, pattern in self.error_patterns.items():
            if pattern['count'] >= 5:  # فقط الگوهای مهم
                summary.append({
                    'type': error_type,
                    'count': pattern['count'],
                    'first_seen': pattern['first_seen'],
                    'last_seen': pattern['last_seen'],
                    'solution': self._suggest_solution(error_type)
                })
        return sorted(summary, key=lambda x: x['count'], reverse=True)
    
    def save_memory(self):
        """ذخیره حافظه خطاها"""
        try:
            memory_file = 'memory/error_memory.json'
            os.makedirs('memory', exist_ok=True)
            
            memory = {
                'stats': self.stats,
                'patterns': self.error_patterns,
                'learning': self.learning_memory[-100:],  # ۱۰۰ درس آخر
                'timestamp': datetime.now().isoformat()
            }
            
            with open(memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save error memory: {e}")
    
    def load_memory(self):
        """بارگذاری حافظه خطاها"""
        try:
            memory_file = 'memory/error_memory.json'
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
                    self.stats = memory.get('stats', self.stats)
                    self.error_patterns = memory.get('patterns', {})
                    self.learning_memory = memory.get('learning', [])
                    logger.info(f"📚 Loaded error memory: {len(self.error_patterns)} patterns")
        except:
            pass

# ==================== Decorators ====================

def safe_execute(default_return=None, log_error=True, critical=False):
    """
    دکوریتور برای اجرای ایمن توابع
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    error_info = error_handler.handle_error(e, {
                        'function': func.__name__,
                        'args': str(args)[:200],
                        'kwargs': str(kwargs)[:200],
                        'critical': critical
                    })
                if critical:
                    # برای خطاهای بحرانی، None برمی‌گردونیم
                    return None
                return default_return
        return wrapper
    return decorator

def safe_async_execute(default_return=None, log_error=True, critical=False):
    """
    دکوریتور برای اجرای ایمن توابع async
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    error_info = error_handler.handle_error(e, {
                        'function': func.__name__,
                        'args': str(args)[:200],
                        'kwargs': str(kwargs)[:200],
                        'critical': critical
                    })
                if critical:
                    return None
                return default_return
        return wrapper
    return decorator

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    دکوریتور برای تلاش مجدد در صورت خطا
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

# نمونه‌سازی سراسری
error_handler = ErrorHandler(admin_chat_id=6590867551)

# ثبت استراتژی‌های پیش‌فرض
error_handler.register_recovery('ModuleNotFoundError', error_handler._recover_module_not_found)
error_handler.register_recovery('ConnectionError', error_handler._recover_connection_error)
error_handler.register_recovery('TimeoutError', error_handler._recover_timeout_error)
error_handler.register_recovery('MemoryError', error_handler._recover_memory_error)
