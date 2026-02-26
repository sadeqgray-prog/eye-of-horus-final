#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔑 API REQUESTER - مدیریت درخواست‌های API
وقتی ربات به API نیاز دارد، از این بخش درخواست می‌کند
قابلیت:
- درخواست API Key از مدیر/کاربر
- ذخیره امن کلیدها
- بررسی اعتبار کلیدها
- مدیریت محدودیت نرخ
- پیشنهاد APIهای جایگزین
"""

import logging
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import time
import re

logger = logging.getLogger(__name__)

class APIRequester:
    """
    مدیریت درخواست‌های API
    """
    
    # لیست APIهای قابل درخواست
    AVAILABLE_APIS = {
        'etherscan': {
            'name': 'Etherscan',
            'url': 'https://etherscan.io/register',
            'free': True,
            'rate_limit': '5 requests/sec',
            'purpose': 'Ethereum token analysis',
            'needs_key': True
        },
        'bscscan': {
            'name': 'BSCScan',
            'url': 'https://bscscan.com/register',
            'free': True,
            'rate_limit': '5 requests/sec',
            'purpose': 'BSC token analysis',
            'needs_key': True
        },
        'twitter': {
            'name': 'Twitter API',
            'url': 'https://developer.twitter.com',
            'free': True,
            'rate_limit': 'Limited',
            'purpose': 'Sentiment analysis',
            'needs_key': True
        },
        'reddit': {
            'name': 'Reddit API',
            'url': 'https://www.reddit.com/prefs/apps',
            'free': True,
            'rate_limit': '60 requests/min',
            'purpose': 'Social analysis',
            'needs_key': True
        },
        'newsapi': {
            'name': 'NewsAPI',
            'url': 'https://newsapi.org/register',
            'free': True,
            'rate_limit': '100 requests/day',
            'purpose': 'News analysis',
            'needs_key': True
        },
        'whale_alert': {
            'name': 'Whale Alert',
            'url': 'https://whale-alert.io/api',
            'free': True,
            'rate_limit': '1000 requests/day',
            'purpose': 'Whale tracking',
            'needs_key': True
        },
        'coingecko': {
            'name': 'CoinGecko',
            'url': 'https://www.coingecko.com/en/api',
            'free': True,
            'rate_limit': '50 calls/min',
            'purpose': 'Market data',
            'needs_key': False  # رایگان بدون کلید
        },
        'dexscreener': {
            'name': 'DexScreener',
            'url': 'https://docs.dexscreener.com/',
            'free': True,
            'rate_limit': '300 requests/min',
            'purpose': 'DEX data',
            'needs_key': False
        }
    }
    
    def __init__(self):
        self.name = "API Requester"
        self.version = "1.0.0"
        
        # ذخیره API Keyها
        self.api_keys = {}
        self.pending_requests = {}
        
        # محدودیت نرخ
        self.rate_limits = {}
        
        # مسیر ذخیره‌سازی
        self.keys_path = Path("data/api_keys.json")
        self.keys_path.parent.mkdir(exist_ok=True)
        
        # بارگذاری کلیدهای ذخیره شده
        self._load_keys()
        
        logger.info("🔑 API Requester initialized")
    
    def _load_keys(self):
        """بارگذاری API Keyهای ذخیره شده"""
        try:
            if self.keys_path.exists():
                with open(self.keys_path, 'r') as f:
                    data = json.load(f)
                    self.api_keys = data.get('keys', {})
                    logger.info(f"📚 Loaded {len(self.api_keys)} API keys")
        except Exception as e:
            logger.error(f"Error loading API keys: {e}")
    
    def _save_keys(self):
        """ذخیره API Keyها"""
        try:
            with open(self.keys_path, 'w') as f:
                json.dump({'keys': self.api_keys}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving API keys: {e}")
    
    def request_api_key(self, api_name: str, user_id: int, reason: str = None) -> Dict:
        """
        درخواست API Key از کاربر
        """
        if api_name not in self.AVAILABLE_APIS:
            return {
                'success': False,
                'message': f"API {api_name} not supported"
            }
        
        api_info = self.AVAILABLE_APIS[api_name]
        
        # اگر API نیازی به کلید نداره
        if not api_info['needs_key']:
            return {
                'success': True,
                'message': f"{api_name} is free, no API key needed",
                'free': True
            }
        
        request_id = hashlib.md5(f"{api_name}{user_id}{datetime.now()}".encode()).hexdigest()[:8]
        
        request = {
            'id': request_id,
            'api_name': api_name,
            'user_id': user_id,
            'requested_at': datetime.now().isoformat(),
            'status': 'pending',
            'reason': reason or api_info['purpose'],
            'instructions': self._get_instructions(api_name)
        }
        
        self.pending_requests[request_id] = request
        
        return {
            'success': True,
            'request': request,
            'message': f"Please provide your {api_info['name']} API key"
        }
    
    def _get_instructions(self, api_name: str) -> str:
        """دریافت راهنمای دریافت API Key"""
        instructions = {
            'etherscan': (
                "1. Go to https://etherscan.io/register\n"
                "2. Create an account\n"
                "3. Go to API Keys section\n"
                "4. Create a new API key\n"
                "5. Send me: `ETHERSCAN: YOUR_API_KEY`"
            ),
            'bscscan': (
                "1. Go to https://bscscan.com/register\n"
                "2. Create an account\n"
                "3. Go to API Keys section\n"
                "4. Create a new API key\n"
                "5. Send me: `BSCSCAN: YOUR_API_KEY`"
            ),
            'twitter': (
                "1. Go to https://developer.twitter.com\n"
                "2. Apply for developer access\n"
                "3. Create a project and app\n"
                "4. Generate Bearer Token\n"
                "5. Send me: `TWITTER: YOUR_BEARER_TOKEN`"
            ),
            'reddit': (
                "1. Go to https://www.reddit.com/prefs/apps\n"
                "2. Click 'create app'\n"
                "3. Get client_id and client_secret\n"
                "4. Send me: `REDDIT: CLIENT_ID:CLIENT_SECRET`"
            )
        }
        
        return instructions.get(api_name, "Please provide your API key")
    
    def submit_api_key(self, user_id: int, api_name: str, api_key: str) -> Dict:
        """
        ثبت API Key دریافتی از کاربر
        """
        # بررسی الگوی کلید
        if not self._validate_key_format(api_name, api_key):
            return {
                'success': False,
                'message': "Invalid API key format"
            }
        
        # ذخیره کلید
        if str(user_id) not in self.api_keys:
            self.api_keys[str(user_id)] = {}
        
        self.api_keys[str(user_id)][api_name] = {
            'key': api_key,
            'added_at': datetime.now().isoformat(),
            'last_used': None,
            'valid': True
        }
        
        # به‌روزرسانی درخواست‌های pending
        for req_id, req in list(self.pending_requests.items()):
            if req['user_id'] == user_id and req['api_name'] == api_name:
                req['status'] = 'resolved'
                req['resolved_at'] = datetime.now().isoformat()
        
        self._save_keys()
        
        return {
            'success': True,
            'message': f"{api_name} API key saved successfully"
        }
    
    def _validate_key_format(self, api_name: str, api_key: str) -> bool:
        """بررسی فرمت API Key"""
        patterns = {
            'etherscan': r'^[A-Za-z0-9]{20,}$',
            'bscscan': r'^[A-Za-z0-9]{20,}$',
            'twitter': r'^[A-Za-z0-9%-]{40,}$',
            'reddit': r'^[A-Za-z0-9]{20,}:[A-Za-z0-9]{20,}$',
            'newsapi': r'^[A-Za-z0-9]{20,}$',
            'whale_alert': r'^[A-Za-z0-9]{20,}$'
        }
        
        pattern = patterns.get(api_name)
        if pattern:
            return bool(re.match(pattern, api_key))
        
        return len(api_key) > 10
    
    def get_api_key(self, user_id: int, api_name: str) -> Optional[str]:
        """
        دریافت API Key کاربر
        """
        try:
            user_keys = self.api_keys.get(str(user_id), {})
            key_data = user_keys.get(api_name)
            
            if key_data and key_data.get('valid'):
                # به‌روزرسانی آخرین استفاده
                key_data['last_used'] = datetime.now().isoformat()
                return key_data['key']
        except Exception as e:
            logger.error(f"Error getting API key: {e}")
        
        return None
    
    def has_api_key(self, user_id: int, api_name: str) -> bool:
        """آیا کاربر این API Key را دارد؟"""
        return self.get_api_key(user_id, api_name) is not None
    
    def get_pending_requests(self, user_id: int = None) -> List[Dict]:
        """دریافت لیست درخواست‌های pending"""
        if user_id:
            return [req for req in self.pending_requests.values() if req['user_id'] == user_id]
        return list(self.pending_requests.values())
    
    def check_rate_limit(self, api_name: str, user_id: int = None) -> Dict:
        """
        بررسی محدودیت نرخ
        """
        key = f"{api_name}_{user_id}" if user_id else api_name
        
        now = time.time()
        minute_ago = now - 60
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # پاک کردن درخواست‌های قدیمی
        self.rate_limits[key] = [t for t in self.rate_limits[key] if t > minute_ago]
        
        # محدودیت‌ها
        limits = {
            'etherscan': 5,  # 5 در ثانیه
            'bscscan': 5,
            'coingecko': 50,  # 50 در دقیقه
            'dexscreener': 300,  # 300 در دقیقه
        }
        
        limit = limits.get(api_name, 60)
        
        if len(self.rate_limits[key]) >= limit:
            return {
                'allowed': False,
                'reset_in': 60 - (now - minute_ago),
                'current': len(self.rate_limits[key]),
                'limit': limit
            }
        
        self.rate_limits[key].append(now)
        
        return {
            'allowed': True,
            'remaining': limit - len(self.rate_limits[key]),
            'limit': limit
        }
    
    def suggest_alternative(self, api_name: str) -> List[str]:
        """پیشنهاد API جایگزین"""
        alternatives = {
            'etherscan': ['bscscan', 'solscan', 'dexscreener'],
            'bscscan': ['etherscan', 'dexscreener'],
            'twitter': ['reddit', 'telegram_scraper'],
            'newsapi': ['cryptopanic'],
            'whale_alert': ['birdeye', 'dexscreener']
        }
        
        return alternatives.get(api_name, [])
    
    def get_api_info(self, api_name: str) -> Dict:
        """دریافت اطلاعات API"""
        return self.AVAILABLE_APIS.get(api_name, {
            'name': api_name,
            'needs_key': True,
            'free': 'unknown'
        })
    
    def get_user_keys_info(self, user_id: int) -> Dict:
        """دریافت اطلاعات کلیدهای یک کاربر"""
        user_keys = self.api_keys.get(str(user_id), {})
        
        info = {}
        for api_name, key_data in user_keys.items():
            info[api_name] = {
                'added': key_data['added_at'],
                'last_used': key_data['last_used'],
                'valid': key_data['valid']
            }
        
        return info

# نمونه‌سازی سراسری
api_requester = APIRequester()
