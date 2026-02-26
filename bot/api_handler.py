#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مدیریت API Keyهای دریافتی از کاربر
این فایل بین ربات و APIها ارتباط برقرار می‌کنه
"""

import logging
import re
import json
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

# ایمپورت همه APIها
from api import (
    birdeye_api, bscscan_api, coingecko_api, cryptopanic_api,
    dexscreener_api, dexscreener_new_pairs, etherscan_api,
    lunarcrush_api, news_api, pump_fun_api, reddit_api,
    santiment_api, solscan_api, telegram_scraper, twitter_api,
    whale_alert_api
)

logger = logging.getLogger(__name__)

class APIKeyManager:
    """
    مدیریت کلیدهای API کاربران
    """
    
    # نگاشت نام API به شیء مربوطه
    API_OBJECTS = {
        'birdeye': birdeye_api,
        'bscscan': bscscan_api,
        'coingecko': coingecko_api,
        'cryptopanic': cryptopanic_api,
        'etherscan': etherscan_api,
        'lunarcrush': lunarcrush_api,
        'newsapi': news_api,
        'reddit': reddit_api,
        'santiment': santiment_api,
        'twitter': twitter_api,
        'whale_alert': whale_alert_api
    }
    
    # APIهایی که نیاز به کلید دارن
    APIS_NEEDING_KEY = [
        'birdeye', 'bscscan', 'coingecko', 'cryptopanic',
        'etherscan', 'lunarcrush', 'newsapi', 'reddit',
        'santiment', 'twitter', 'whale_alert'
    ]
    
    # APIهای رایگان (بدون نیاز به کلید)
    FREE_APIS = [
        'dexscreener', 'dexscreener_new_pairs', 'pump_fun',
        'solscan', 'telegram_scraper'
    ]
    
    def __init__(self):
        self.user_keys = {}  # user_id -> {api_name: key_data}
        self.load_keys()
        logger.info("🔑 APIKeyManager initialized")
    
    def extract_key_from_message(self, text: str) -> Optional[Dict]:
        """
        استخراج API Key از پیام کاربر
        """
        text = text.strip()
        
        # الگوهای تشخیص
        patterns = {
            'etherscan': r'ETHERSCAN(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'bscscan': r'BSCSCAN(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'twitter': r'TWITTER(?:\s*):(?:\s*)([A-Za-z0-9_%-]{40,})',
            'reddit': r'REDDIT(?:\s*):(?:\s*)([A-Za-z0-9_]{20,}):([A-Za-z0-9_]{20,})',
            'newsapi': r'NEWSAPI(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'whale_alert': r'WHALEALERT(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'lunarcrush': r'LUNARCRUSH(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'santiment': r'SANTIMENT(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'birdeye': r'BIRDEYE(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'cryptopanic': r'CRYPTOPANIC(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})',
            'coingecko': r'COINGECKO(?:\s*):(?:\s*)([A-Za-z0-9_]{20,})'
        }
        
        for api_name, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if api_name == 'reddit':
                    return {
                        'api': api_name,
                        'client_id': match.group(1),
                        'client_secret': match.group(2),
                        'type': 'reddit'
                    }
                else:
                    return {
                        'api': api_name,
                        'key': match.group(1),
                        'type': 'normal'
                    }
        
        return None
    
    def save_user_key(self, user_id: int, api_data: Dict) -> bool:
        """
        ذخیره کلید کاربر
        """
        try:
            if user_id not in self.user_keys:
                self.user_keys[user_id] = {}
            
            api_name = api_data['api']
            
            if api_data['type'] == 'reddit':
                self.user_keys[user_id][api_name] = {
                    'client_id': api_data['client_id'],
                    'client_secret': api_data['client_secret'],
                    'added_at': datetime.now().isoformat()
                }
                # تنظیم در API مربوطه
                if api_name in self.API_OBJECTS:
                    self.API_OBJECTS[api_name].set_credentials(
                        api_data['client_id'],
                        api_data['client_secret'],
                        user_id
                    )
            else:
                self.user_keys[user_id][api_name] = {
                    'key': api_data['key'],
                    'added_at': datetime.now().isoformat()
                }
                # تنظیم در API مربوطه
                if api_name in self.API_OBJECTS:
                    self.API_OBJECTS[api_name].set_api_key(
                        api_data['key'],
                        user_id
                    )
            
            self.save_keys()
            logger.info(f"✅ {api_name} key saved for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving key: {e}")
            return False
    
    def get_user_key(self, user_id: int, api_name: str) -> Optional[Any]:
        """
        دریافت کلید کاربر برای یک API خاص
        """
        if user_id in self.user_keys and api_name in self.user_keys[user_id]:
            return self.user_keys[user_id][api_name]
        return None
    
    def has_api_key(self, user_id: int, api_name: str) -> bool:
        """
        بررسی اینکه کاربر این API رو داره یا نه
        """
        if api_name in self.FREE_APIS:
            return True  # APIهای رایگان همیشه در دسترسن
        return self.get_user_key(user_id, api_name) is not None
    
    def get_missing_apis(self, user_id: int, needed_apis: list) -> list:
        """
        دریافت لیست APIهایی که کاربر نداره
        """
        missing = []
        for api in needed_apis:
            if not self.has_api_key(user_id, api):
                missing.append(api)
        return missing
    
    def get_api_request_message(self, api_name: str) -> str:
        """
        دریافت پیام درخواست API
        """
        messages = {
            'etherscan': (
                "🔑 **Etherscan API Key Required**\n\n"
                "برای تحلیل توکن‌های اتریوم، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://etherscan.io/register برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ به بخش API Keys برو\n"
                "4️⃣ یه کلید جدید بساز\n\n"
                "📤 **برام بفرست:** `ETHERSCAN: YOUR_API_KEY`\n\n"
                "مثال: `ETHERSCAN: ABC123XYZ456DEF789`"
            ),
            'bscscan': (
                "🔑 **BSCScan API Key Required**\n\n"
                "برای تحلیل توکن‌های BSC (بایننس)، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://bscscan.com/register برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ به بخش API Keys برو\n"
                "4️⃣ یه کلید جدید بساز\n\n"
                "📤 **برام بفرست:** `BSCSCAN: YOUR_API_KEY`\n\n"
                "مثال: `BSCSCAN: ABC123XYZ456DEF789`"
            ),
            'twitter': (
                "🐦 **Twitter API Key Required**\n\n"
                "برای تحلیل احساسات توییتر، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://developer.twitter.com برو\n"
                "2️⃣ اکانت developer بساز\n"
                "3️⃣ یه پروژه جدید ایجاد کن\n"
                "4️⃣ Bearer Token رو کپی کن\n\n"
                "📤 **برام بفرست:** `TWITTER: YOUR_BEARER_TOKEN`\n\n"
                "مثال: `TWITTER: AAAAAAAAAAAAAAAAAAAAAA`"
            ),
            'reddit': (
                "👽 **Reddit API Key Required**\n\n"
                "برای تحلیل ردیت، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://www.reddit.com/prefs/apps برو\n"
                "2️⃣ روی 'create app' کلیک کن\n"
                "3️⃣ client_id و client_secret رو کپی کن\n\n"
                "📤 **برام بفرست:** `REDDIT: CLIENT_ID:CLIENT_SECRET`\n\n"
                "مثال: `REDDIT: abc123:xyz789`"
            ),
            'newsapi': (
                "📰 **NewsAPI Key Required**\n\n"
                "برای دریافت اخبار لحظه‌ای، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://newsapi.org/register برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `NEWSAPI: YOUR_API_KEY`\n\n"
                "مثال: `NEWSAPI: abc123xyz789`"
            ),
            'whale_alert': (
                "🐋 **Whale Alert API Key Required**\n\n"
                "برای ردیابی حرکت نهنگ‌ها، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://whale-alert.io/api برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `WHALEALERT: YOUR_API_KEY`\n\n"
                "مثال: `WHALEALERT: abc123xyz789`"
            ),
            'lunarcrush': (
                "🌕 **LunarCrush API Key Required**\n\n"
                "برای تحلیل اجتماعی پیشرفته، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://lunarcrush.com/developers برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `LUNARCRUSH: YOUR_API_KEY`\n\n"
                "مثال: `LUNARCRUSH: abc123xyz789`"
            ),
            'santiment': (
                "📊 **Santiment API Key Required**\n\n"
                "برای داده‌های on-chain، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://app.santiment.net/account برو\n"
                "2️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `SANTIMENT: YOUR_API_KEY`\n\n"
                "مثال: `SANTIMENT: abc123xyz789`"
            ),
            'birdeye': (
                "🐦 **BirdEye API Key Required**\n\n"
                "برای ردیابی هوشمند نهنگ‌ها، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://docs.birdeye.so/reference برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `BIRDEYE: YOUR_API_KEY`\n\n"
                "مثال: `BIRDEYE: abc123xyz789`"
            ),
            'cryptopanic': (
                "📰 **CryptoPanic API Key Required**\n\n"
                "برای اخبار اختصاصی کریپتو، به API Key نیاز دارم.\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://cryptopanic.com/developers/api/ برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `CRYPTOPANIC: YOUR_API_KEY`\n\n"
                "مثال: `CRYPTOPANIC: abc123xyz789`"
            ),
            'coingecko': (
                "🦎 **CoinGecko API Key Required**\n\n"
                "برای داده‌های بازار، به API Key نیاز دارم (اختیاری).\n\n"
                "📌 **دریافت رایگان:**\n"
                "1️⃣ به https://www.coingecko.com/en/api برو\n"
                "2️⃣ ثبت‌نام کن\n"
                "3️⃣ API key رو کپی کن\n\n"
                "📤 **برام بفرست:** `COINGECKO: YOUR_API_KEY`\n\n"
                "مثال: `COINGECKO: abc123xyz789`"
            )
        }
        
        return messages.get(api_name, f"API Key for {api_name} required.")
    
    def save_keys(self):
        """ذخیره کلیدها در فایل"""
        try:
            path = Path('data/api_keys.json')
            path.parent.mkdir(exist_ok=True)
            
            with open(path, 'w') as f:
                json.dump(self.user_keys, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save API keys: {e}")
    
    def load_keys(self):
        """بارگذاری کلیدها از فایل"""
        try:
            path = Path('data/api_keys.json')
            if path.exists():
                with open(path, 'r') as f:
                    self.user_keys = json.load(f)
                logger.info(f"📚 Loaded API keys for {len(self.user_keys)} users")
        except Exception as e:
            logger.error(f"Failed to load API keys: {e}")
    
    def get_user_api_status(self, user_id: int) -> Dict:
        """
        دریافت وضعیت APIهای کاربر
        """
        status = {}
        user_apis = self.user_keys.get(user_id, {})
        
        for api in self.APIS_NEEDING_KEY:
            status[api] = {
                'has_key': api in user_apis,
                'added_at': user_apis[api].get('added_at') if api in user_apis else None
            }
        
        return status

# نمونه‌سازی سراسری
api_key_manager = APIKeyManager()
