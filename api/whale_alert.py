#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Whale Alert - ردیابی تراکنش‌های بزرگ نهنگ‌ها
پشتیبانی از: Bitcoin, Ethereum, Solana, BSC و...
نیازمند API Key (رایگان با محدودیت)
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class WhaleAlertAPI:
    """
    API Whale Alert - ردیابی تراکنش‌های بزرگ
    رایگان: ۱۰۰۰ درخواست در روز
    """
    
    BASE_URL = "https://api.whale-alert.io/v1"
    
    # حداقل مقادیر برای تشخیص نهنگ (دلار)
    MIN_VALUES = {
        'btc': 500000,    # ۵۰۰k
        'eth': 300000,     # ۳۰۰k
        'sol': 100000,     # ۱۰۰k
        'bsc': 100000,     # ۱۰۰k
        'default': 50000   # ۵۰k برای بقیه
    }
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        self.stats = {
            'total_requests': 0,
            'remaining': 1000,
            'reset_time': time.time() + 86400
        }
        
        self.cache = {}
        self.cache_timeout = 60  # ۱ دقیقه
        
        logger.info("🐋 WhaleAlertAPI initialized")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ WhaleAlert API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ WhaleAlert global API key set")
    
    def has_key(self, user_id: int = None) -> bool:
        """بررسی وجود API Key"""
        if user_id and user_id in self.user_api_keys:
            return True
        return self.api_key is not None
    
    def get_api_key(self, user_id: int = None) -> Optional[str]:
        """دریافت API Key مناسب"""
        if user_id and user_id in self.user_api_keys:
            return self.user_api_keys[user_id]
        return self.api_key
    
    def get_api_request_message(self) -> str:
        """پیام درخواست API Key"""
        return (
            "🐋 **Whale Alert API Key Required**\n\n"
            "To track whale movements, I need your Whale Alert API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://whale-alert.io/api\n"
            "2. Sign up and get your API key\n\n"
            "**Send me:** `WHALEALERT: YOUR_API_KEY`\n\n"
            "Example: `WHALEALERT: abc123xyz789`"
        )
    
    async def _make_request(self, endpoint: str, params: Dict,
                           user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به Whale Alert"""
        
        api_key = self.get_api_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        # Rate limiting
        now = time.time()
        if now > self.stats['reset_time']:
            self.stats['remaining'] = 1000
            self.stats['reset_time'] = now + 86400
        
        if self.stats['remaining'] <= 0:
            wait_time = self.stats['reset_time'] - now
            logger.warning(f"WhaleAlert rate limit reached, waiting {wait_time/3600:.1f}h")
            return {'error': 'rate_limit', 'message': f'Rate limit reached. Resets in {wait_time/3600:.1f}h'}
        
        params['api_key'] = api_key
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        self.stats['total_requests'] += 1
        self.stats['remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("WhaleAlert rate limit exceeded")
                        return {'error': 'rate_limit', 'message': 'Rate limit exceeded'}
                    else:
                        logger.warning(f"WhaleAlert returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"WhaleAlert request error: {e}")
            return None
    
    async def get_transactions(self, min_value: int = 500000, limit: int = 50,
                               user_id: int = None) -> List[Dict]:
        """
        دریافت تراکنش‌های نهنگ‌ها
        """
        cache_key = f"txs_{min_value}_{limit}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        params = {
            'min_value': min_value,
            'limit': limit
        }
        
        result = await self._make_request('transactions', params, user_id)
        
        if result and 'transactions' in result:
            txs = []
            for tx in result['transactions']:
                txs.append({
                    'id': tx.get('id'),
                    'hash': tx.get('hash'),
                    'symbol': tx.get('symbol'),
                    'amount': tx.get('amount'),
                    'amount_usd': tx.get('amount_usd'),
                    'from_address': tx.get('from', {}).get('address'),
                    'from_owner': tx.get('from', {}).get('owner'),
                    'to_address': tx.get('to', {}).get('address'),
                    'to_owner': tx.get('to', {}).get('owner'),
                    'timestamp': datetime.fromtimestamp(tx.get('timestamp', 0)).isoformat(),
                    'blockchain': tx.get('blockchain'),
                    'transaction_type': self._classify_transaction(tx)
                })
            
            self.cache[cache_key] = (txs, datetime.now())
            return txs
        
        return []
    
    def _classify_transaction(self, tx: Dict) -> str:
        """طبقه‌بندی نوع تراکنش"""
        amount_usd = tx.get('amount_usd', 0)
        
        if amount_usd > 10000000:  # ۱۰ میلیون
            return "🐋 MEGA WHALE"
        elif amount_usd > 5000000:  # ۵ میلیون
            return "🐋 SUPER WHALE"
        elif amount_usd > 1000000:  # ۱ میلیون
            return "🐋 WHALE"
        elif amount_usd > 500000:   # ۵۰۰ هزار
            return "🐋 DOLPHIN"
        else:
            return "🐟 FISH"
    
    async def get_token_whales(self, token_symbol: str, hours: int = 24,
                               user_id: int = None) -> List[Dict]:
        """
        دریافت تراکنش‌های نهنگ برای یک توکن خاص
        """
        # دریافت همه تراکنش‌ها
        txs = await self.get_transactions(min_value=50000, limit=100, user_id=user_id)
        
        # فیلتر بر اساس توکن
        token_txs = [tx for tx in txs if tx['symbol'] == token_symbol.upper()]
        
        # فیلتر زمانی
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_txs = []
        
        for tx in token_txs:
            tx_time = datetime.fromisoformat(tx['timestamp'])
            if tx_time > cutoff:
                recent_txs.append(tx)
        
        return recent_txs
    
    async def analyze_whale_movement(self, token_symbol: str, hours: int = 24,
                                     user_id: int = None) -> Dict:
        """
        تحلیل حرکت نهنگ‌ها برای یک توکن
        """
        txs = await self.get_token_whales(token_symbol, hours, user_id)
        
        if not txs:
            return {
                'has_whale_activity': False,
                'total_volume': 0,
                'net_flow': 0,
                'buy_pressure': 0,
                'alert_level': 'LOW'
            }
        
        total_in = 0
        total_out = 0
        exchanges_in = 0
        exchanges_out = 0
        
        for tx in txs:
            amount = tx['amount_usd']
            
            # تشخیص جهت
            if 'exchange' in tx.get('to_owner', '').lower():
                total_in += amount
                exchanges_in += 1
            elif 'exchange' in tx.get('from_owner', '').lower():
                total_out += amount
                exchanges_out += 1
            else:
                # انتقال بین ولت‌های شخصی
                pass
        
        net_flow = total_in - total_out
        buy_pressure = total_in / max(total_out, 1)
        
        # سطح هشدار
        if net_flow > 10000000:  # ۱۰ میلیون
            alert = "🔴 EXTREME"
        elif net_flow > 5000000:  # ۵ میلیون
            alert = "🟠 HIGH"
        elif net_flow > 1000000:  # ۱ میلیون
            alert = "🟡 MEDIUM"
        elif net_flow > 0:
            alert = "🟢 LOW"
        else:
            alert = "⚫ NEGATIVE"
        
        return {
            'has_whale_activity': True,
            'total_volume': total_in + total_out,
            'net_flow': net_flow,
            'buy_pressure': buy_pressure,
            'buy_volume': total_in,
            'sell_volume': total_out,
            'transaction_count': len(txs),
            'exchanges_in': exchanges_in,
            'exchanges_out': exchanges_out,
            'alert_level': alert,
            'transactions': txs[:10]  # ۱۰ تای آخر
        }
    
    async def monitor_whales(self, callback=None, interval: int = 60,
                             user_id: int = None):
        """
        مانیتورینگ لحظه‌ای نهنگ‌ها
        """
        logger.info("🐋 Starting whale monitor...")
        
        last_seen = set()
        
        while True:
            try:
                txs = await self.get_transactions(limit=50, user_id=user_id)
                
                for tx in txs:
                    if tx['id'] not in last_seen:
                        last_seen.add(tx['id'])
                        
                        # اگه تراکنش مهم بود
                        if tx['amount_usd'] > 5000000:  # ۵ میلیون
                            logger.info(f"🐋 MEGA WHALE: {tx['symbol']} - ${tx['amount_usd']:,.0f}")
                            
                            if callback:
                                await callback(tx)
                
                # محدودیت حافظه
                if len(last_seen) > 10000:
                    last_seen = set(list(last_seen)[-5000:])
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Whale monitor error: {e}")
                await asyncio.sleep(interval * 2)
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared WhaleAlert key for user {user_id}")

# نمونه‌سازی سراسری
whale_alert_api = WhaleAlertAPI()
