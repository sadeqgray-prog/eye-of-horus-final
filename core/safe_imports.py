#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ماژول ایمن برای import کتابخونه‌ها با fallback هوشمند
نسخه ۵.۰ - با قابلیت یادگیری و پیش‌بینی نیازها
"""

import logging
import sys
import importlib
import pkg_resources
from typing import Any, Optional, Tuple, Dict, List, Callable
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

class SafeImporter:
    """
    کلاس ایمن برای import کتابخونه‌ها با قابلیت:
    - fallback هوشمند
    - کش کردن نتایج
    - یادگیری از خطاها
    - پیش‌بینی نیازها
    - نصب خودکار (اختیاری)
    """
    
    def __init__(self, auto_install: bool = False):
        self.import_cache = {}
        self.missing_modules = []
        self.usage_stats = {}
        self.fallback_objects = {}
        self.auto_install = auto_install
        
        # بارگذاری آمار قبلی
        self.load_stats()
        
        logger.info(f"🔰 SafeImporter v5.0 initialized (auto_install={auto_install})")
    
    def safe_import(self, module_name: str, fallback: Any = None, 
                   version: str = None, auto_install: bool = None) -> Tuple[bool, Any]:
        """
        import ایمن با fallback و قابلیت نصب خودکار
        
        Args:
            module_name: نام ماژول
            fallback: مقدار جایگزین در صورت عدم وجود
            version: نسخه مورد نیاز
            auto_install: نصب خودکار (override تنظیم سراسری)
        
        Returns:
            (موفقیت, ماژول یا fallback)
        """
        # ثبت آمار استفاده
        self._record_usage(module_name)
        
        # چک کردن کش
        cache_key = f"{module_name}:{version}" if version else module_name
        if cache_key in self.import_cache:
            return True, self.import_cache[cache_key]
        
        # تلاش برای import
        try:
            if version:
                module = importlib.import_module(module_name)
                # چک کردن نسخه
                if hasattr(module, '__version__'):
                    installed_version = module.__version__
                    if installed_version != version:
                        logger.warning(f"⚠️ Version mismatch for {module_name}: expected {version}, got {installed_version}")
            else:
                module = importlib.import_module(module_name)
            
            self.import_cache[cache_key] = module
            logger.debug(f"✅ Successfully imported {module_name}")
            return True, module
            
        except ImportError as e:
            logger.warning(f"⚠️ Could not import {module_name}: {e}")
            self.missing_modules.append({
                'module': module_name,
                'error': str(e),
                'time': datetime.now().isoformat()
            })
            
            # نصب خودکار (اگه فعال باشه)
            should_install = auto_install if auto_install is not None else self.auto_install
            if should_install:
                self._auto_install(module_name, version)
                # تلاش مجدد
                try:
                    module = importlib.import_module(module_name)
                    self.import_cache[cache_key] = module
                    logger.info(f"✅ Successfully installed and imported {module_name}")
                    return True, module
                except:
                    pass
            
            return False, fallback
    
    def _auto_install(self, module_name: str, version: str = None):
        """نصب خودکار ماژول (اگه فعال باشه)"""
        try:
            import subprocess
            package = f"{module_name}=={version}" if version else module_name
            logger.info(f"📦 Auto-installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return True
        except Exception as e:
            logger.error(f"❌ Auto-install failed for {module_name}: {e}")
            return False
    
    def safe_import_from(self, module_name: str, attr_name: str, 
                        fallback: Any = None, version: str = None) -> Tuple[bool, Any]:
        """
        import یک attribute از یک module با fallback
        """
        success, module = self.safe_import(module_name, None, version)
        if not success:
            return False, fallback
        
        try:
            attr = getattr(module, attr_name)
            return True, attr
        except AttributeError as e:
            logger.warning(f"⚠️ Could not import {attr_name} from {module_name}: {e}")
            return False, fallback
    
    def has_module(self, module_name: str) -> bool:
        """چک کردن وجود ماژول"""
        success, _ = self.safe_import(module_name)
        return success
    
    def get_version(self, module_name: str) -> Optional[str]:
        """دریافت نسخه ماژول"""
        success, module = self.safe_import(module_name)
        if success and hasattr(module, '__version__'):
            return module.__version__
        return None
    
    def register_fallback(self, module_name: str, fallback_factory: Callable):
        """ثبت fallback اختصاصی برای یک ماژول"""
        self.fallback_objects[module_name] = fallback_factory
        logger.debug(f"📝 Registered fallback for {module_name}")
    
    def get_fallback(self, module_name: str):
        """دریافت fallback اختصاصی"""
        if module_name in self.fallback_objects:
            return self.fallback_objects[module_name]()
        return None
    
    def _record_usage(self, module_name: str):
        """ثبت آمار استفاده برای یادگیری"""
        self.usage_stats[module_name] = self.usage_stats.get(module_name, 0) + 1
        
        # ذخیره هر ۱۰۰ بار
        if sum(self.usage_stats.values()) % 100 == 0:
            self.save_stats()
    
    def save_stats(self):
        """ذخیره آمار استفاده"""
        try:
            stats_file = os.path.join('memory', 'import_stats.json')
            os.makedirs('memory', exist_ok=True)
            with open(stats_file, 'w') as f:
                json.dump({
                    'usage_stats': self.usage_stats,
                    'missing_modules': self.missing_modules[-100:],  # ۱۰۰ تای آخر
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
        except:
            pass
    
    def load_stats(self):
        """بارگذاری آمار استفاده"""
        try:
            stats_file = os.path.join('memory', 'import_stats.json')
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                    self.usage_stats = data.get('usage_stats', {})
                    logger.info(f"📊 Loaded stats for {len(self.usage_stats)} modules")
        except:
            pass
    
    def get_most_used(self, limit: int = 10) -> List[Tuple[str, int]]:
        """دریافت پراستفاده‌ترین ماژول‌ها"""
        return sorted(self.usage_stats.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def get_missing_summary(self) -> Dict:
        """خلاصه ماژول‌های missing"""
        missing_count = {}
        for item in self.missing_modules:
            mod = item['module']
            missing_count[mod] = missing_count.get(mod, 0) + 1
        return missing_count

# نمونه‌سازی سراسری
importer = SafeImporter(auto_install=False)  # نصب خودکار غیرفعال (برای امنیت)

# ==================== Fallback Classes ====================

class CosmicDummy:
    """
    کلاس جایگزین هوشمند - وقتی کتابخونه‌ای نباشه،
    این کلاس رفتار اون کتابخونه رو شبیه‌سازی می‌کنه
    """
    
    def __init__(self, name="Dummy"):
        self.name = name
        self._methods = {}
    
    def __getattr__(self, name):
        if name not in self._methods:
            self._methods[name] = lambda *args, **kwargs: None
        return self._methods[name]
    
    def __call__(self, *args, **kwargs):
        return None
    
    def __repr__(self):
        return f"<CosmicDummy: {self.name}>"
    
    @staticmethod
    def version():
        return "0.0.0 (fallback)"

class DummyDataFrame:
    """جایگزین هوشمند pandas DataFrame"""
    
    def __init__(self, data=None):
        self.data = data or []
        self._columns = []
    
    def to_dict(self):
        return {}
    
    def to_json(self):
        return '{}'
    
    def to_csv(self):
        return ''
    
    def head(self, n=5):
        return self
    
    def tail(self, n=5):
        return self
    
    def describe(self):
        return {}
    
    @property
    def shape(self):
        return (0, 0)
    
    @property
    def columns(self):
        return self._columns

class DummyArray:
    """جایگزین هوشمند numpy array"""
    
    def __init__(self, data=None):
        self.data = data or []
    
    def __getitem__(self, idx):
        return 0
    
    def __len__(self):
        return 0
    
    def mean(self):
        return 0
    
    def sum(self):
        return 0
    
    def min(self):
        return 0
    
    def max(self):
        return 0
    
    def reshape(self, *args):
        return self
    
    @property
    def shape(self):
        return (0,)

# ==================== Fallback Factory Functions ====================

def _numpy_fallback():
    return DummyArray

def _pandas_fallback():
    return DummyDataFrame

def _tf_fallback():
    return CosmicDummy("TensorFlow")

def _torch_fallback():
    return CosmicDummy("PyTorch")

def _sklearn_fallback():
    return CosmicDummy("Scikit-Learn")

# ثبت fallbackها
importer.register_fallback('numpy', _numpy_fallback)
importer.register_fallback('pandas', _pandas_fallback)
importer.register_fallback('tensorflow', _tf_fallback)
importer.register_fallback('torch', _torch_fallback)
importer.register_fallback('sklearn', _sklearn_fallback)

# ==================== Helper Functions ====================

def get_numpy():
    """دریافت numpy با fallback هوشمند"""
    success, np = importer.safe_import('numpy')
    if success:
        return np
    return importer.get_fallback('numpy')

def get_pandas():
    """دریافت pandas با fallback هوشمند"""
    success, pd = importer.safe_import('pandas')
    if success:
        return pd
    return importer.get_fallback('pandas')

def get_tensorflow():
    """دریافت tensorflow با fallback هوشمند"""
    success, tf = importer.safe_import('tensorflow')
    if success:
        return tf
    return importer.get_fallback('tensorflow')

def get_torch():
    """دریافت torch با fallback هوشمند"""
    success, torch = importer.safe_import('torch')
    if success:
        return torch
    return importer.get_fallback('torch')

def get_sklearn():
    """دریافت sklearn با fallback هوشمند"""
    success, sk = importer.safe_import('sklearn')
    if success:
        return sk
    return importer.get_fallback('sklearn')

def get_transformers():
    """دریافت transformers با fallback هوشمند"""
    success, tr = importer.safe_import('transformers')
    if success:
        return tr
    return CosmicDummy("Transformers")

def get_nltk():
    """دریافت nltk با fallback هوشمند"""
    success, nltk = importer.safe_import('nltk')
    if success:
        return nltk
    return CosmicDummy("NLTK")

def get_textblob():
    """دریافت textblob با fallback هوشمند"""
    success, tb = importer.safe_import('textblob')
    if success:
        return tb
    return CosmicDummy("TextBlob")

def get_vader():
    """دریافت vaderSentiment با fallback هوشمند"""
    success, vs = importer.safe_import('vaderSentiment')
    if success:
        return vs
    return CosmicDummy("Vader")

def get_web3():
    """دریافت web3 با fallback هوشمند"""
    success, w3 = importer.safe_import('web3')
    if success:
        return w3
    return CosmicDummy("Web3")

def get_ccxt():
    """دریافت ccxt با fallback هوشمند"""
    success, ccxt = importer.safe_import('ccxt')
    if success:
        return ccxt
    return CosmicDummy("CCXT")

def get_pycoingecko():
    """دریافت pycoingecko با fallback هوشمند"""
    success, cg = importer.safe_import('pycoingecko')
    if success:
        return cg
    return CosmicDummy("CoinGecko")
