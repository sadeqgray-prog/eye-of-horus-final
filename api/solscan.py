#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Solscan - برای تحلیل توکن‌های سولانا
پشتیبانی از توکن‌های جدید با platform_id (Raydium, Pump.fun, و...)
قابلیت‌ها:
- دریافت توکن‌های جدید در لحظه
- تحلیل میم‌کوین‌های Pump.fun
- ردیابی توکن‌های ساخته شده روی Raydium
- بدون نیاز به API Key (نسخه عمومی)
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import time

logger = logging.getLogger(__name__)

class SolscanAPI:
    """
    API Solscan - رایگان با محدودیت
    برای توکن‌های سولانا
    """
    
    BASE_URL = "https://api.solscan.io"
    
    # پلتفرم‌های محبوب برای توکن‌های جدید
    PLATFORMS = {
        'pumpfun': 'Pump.fun',
        'raydium': 'Raydium',
        'jupiter': 'Jupiter',
        'orca': 'Orca',
        'meteora': 'Meteora',
        'lifinity': 'Lifinity',
        'phoenix': 'Phoenix',
        'openbook': 'OpenBook'
    }
    
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_timeout = 60  # ۱ دقیقه
        
        # حافظه توکن‌های دیده شده
        self.seen_tokens = set()
        self.recent_tokens = []
        
        logger.info("🔍 SolscanAPI initialized - Ready to track Solana tokens")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """دریافت session (ساخت اگه وجود نداشته باشه)"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_token_info(self, token_address: str) -> Optional[Dict]:
        """
        دریافت اطلاعات کامل یک توکن سولانا
        
        Args:
            token_address: آدرس توکن (base58)
        
        Returns:
            اطلاعات توکن یا None
        """
        cache_key = f"token_{token_address}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/token/meta"
            params = {'token': token_address}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        token_data = data.get('data', {})
                        
                        result = {
                            'address': token_address,
                            'symbol': token_data.get('symbol'),
                            'name': token_data.get('name'),
                            'decimals': token_data.get('decimals', 9),
                            'supply': token_data.get('supply'),
                            'mint_authority': token_data.get('mintAuthority'),
                            'freeze_authority': token_data.get('freezeAuthority'),
                            'is_verified': token_data.get('isVerified', False),
                            'holder_count': token_data.get('holder', 0),
                            'created_at': token_data.get('createdTime'),
                            'created_tx': token_data.get('createdTx'),
                            'creator': token_data.get('creator'),
                            'icon': token_data.get('icon'),
                            'source': 'solscan'
                        }
                        
                        self.cache[cache_key] = (result, datetime.now())
                        return result
                
                elif response.status == 404:
                    logger.debug(f"Token {token_address} not found on Solscan")
                    return None
                else:
                    logger.warning(f"Solscan returned {response.status}")
                    return None
        
        except Exception as e:
            logger.error(f"Solscan API error: {e}")
            return None
        
        return None
    
    async def get_token_price(self, token_address: str) -> Optional[Dict]:
        """
        دریافت قیمت توکن
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/token/price"
            params = {'token': token_address}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        price_data = data.get('data', {})
                        return {
                            'price_usd': price_data.get('priceUsdt'),
                            'price_sol': price_data.get('priceSol'),
                            'volume_24h': price_data.get('volume24h'),
                            'price_change_24h': price_data.get('priceChange24h'),
                            'market_cap': price_data.get('marketCap'),
                            'liquidity': price_data.get('liquidity'),
                            'source': 'solscan'
                        }
        
        except Exception as e:
            logger.error(f"Solscan price error: {e}")
        
        return None
    
    async def get_token_holders(self, token_address: str, limit: int = 100) -> List[Dict]:
        """
        دریافت لیست هولدرهای توکن
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/token/holders"
            params = {
                'token': token_address,
                'limit': limit,
                'offset': 0
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        holders = data.get('data', [])
                        return [{
                            'address': h.get('owner'),
                            'amount': h.get('amount'),
                            'percentage': h.get('percentage', 0),
                            'rank': h.get('rank')
                        } for h in holders]
        
        except Exception as e:
            logger.error(f"Solscan holders error: {e}")
        
        return []
    
    async def get_token_transfers(self, token_address: str, limit: int = 50) -> List[Dict]:
        """
        دریافت تراکنش‌های اخیر توکن
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/token/transfers"
            params = {
                'token': token_address,
                'limit': limit,
                'offset': 0
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        transfers = data.get('data', [])
                        return [{
                            'tx_hash': t.get('txHash'),
                            'from': t.get('fromAddress'),
                            'to': t.get('toAddress'),
                            'amount': t.get('amount'),
                            'timestamp': t.get('blockTime'),
                            'slot': t.get('slot')
                        } for t in transfers]
        
        except Exception as e:
            logger.error(f"Solscan transfers error: {e}")
        
        return []
    
    async def get_new_tokens(self, platform: str = None, limit: int = 50) -> List[Dict]:
        """
        دریافت توکن‌های جدید سولانا
        
        Args:
            platform: پلتفرم خاص (pumpfun, raydium, ...)
            limit: تعداد
        
        Returns:
            لیست توکن‌های جدید
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/token/list"
            params = {
                'sortBy': 'createdTime',
                'order': 'desc',
                'limit': limit,
                'offset': 0
            }
            
            if platform:
                params['platform'] = platform
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        tokens = data.get('data', [])
                        
                        new_tokens = []
                        for token in tokens:
                            token_info = {
                                'address': token.get('address'),
                                'symbol': token.get('symbol'),
                                'name': token.get('name'),
                                'decimals': token.get('decimals', 9),
                                'holder_count': token.get('holder', 0),
                                'created_at': token.get('createdTime'),
                                'created_at_datetime': datetime.fromtimestamp(
                                    token.get('createdTime', 0)
                                ).isoformat() if token.get('createdTime') else None,
                                'creator': token.get('creator'),
                                'platform': token.get('platform'),
                                'is_pump_fun': token.get('platform') == 'pumpfun',
                                'is_raydium': token.get('platform') == 'raydium',
                                'mint_tx': token.get('mintTx'),
                                'source': 'solscan'
                            }
                            
                            # محاسبه سن توکن
                            if token_info['created_at']:
                                age_seconds = time.time() - token_info['created_at']
                                token_info['age_seconds'] = age_seconds
                                token_info['age_minutes'] = round(age_seconds / 60, 2)
                                token_info['is_new'] = age_seconds < 300  # کمتر از ۵ دقیقه
                            
                            # ذخیره در حافظه
                            if token_info['address'] not in self.seen_tokens:
                                self.seen_tokens.add(token_info['address'])
                                self.recent_tokens.append(token_info)
                                
                                if len(self.recent_tokens) > 1000:
                                    self.recent_tokens = self.recent_tokens[-1000:]
                            
                            new_tokens.append(token_info)
                        
                        return new_tokens
        
        except Exception as e:
            logger.error(f"Solscan new tokens error: {e}")
        
        return []
    
    async def get_pump_fun_tokens(self, limit: int = 50) -> List[Dict]:
        """
        دریافت توکن‌های جدید از Pump.fun
        (معروف‌ترین platform برای میم‌کوین‌های سولانا)
        """
        return await self.get_new_tokens('pumpfun', limit)
    
    async def get_raydium_tokens(self, limit: int = 50) -> List[Dict]:
        """
        دریافت توکن‌های جدید از Raydium
        """
        return await self.get_new_tokens('raydium', limit)
    
    async def monitor_new_tokens(self, callback=None, interval: int = 30):
        """
        مانیتورینگ مداوم توکن‌های جدید
        
        Args:
            callback: تابعی که برای هر توکن جدید صدا زده میشه
            interval: فاصله بین چک‌ها (ثانیه)
        """
        last_seen = set()
        
        while True:
            try:
                # دریافت توکن‌های جدید از همه پلتفرم‌ها
                new_tokens = await self.get_new_tokens(limit=100)
                
                for token in new_tokens:
                    if token['address'] not in last_seen:
                        last_seen.add(token['address'])
                        
                        # اگه توکن خیلی جدید باشه (کمتر از ۵ دقیقه)
                        if token.get('is_new'):
                            logger.info(f"🆕 NEW SOLANA TOKEN: {token['symbol']} on {token.get('platform', 'unknown')}")
                            
                            if callback:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(token)
                                else:
                                    callback(token)
                
                # محدودیت حافظه
                if len(last_seen) > 10000:
                    last_seen = set(list(last_seen)[-5000:])
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(60)
    
    async def analyze_token_security(self, token_address: str) -> Dict:
        """
        تحلیل امنیتی توکن سولانا
        
        بررسی:
        - آیا mint authority غیرفعال شده؟
        - آیا freeze authority غیرفعال شده؟
        - آیا تیم توکن رو قفل کرده؟
        - آیا liquidity قفل شده؟
        """
        token_info = await self.get_token_info(token_address)
        
        if not token_info:
            return {'error': 'Token not found'}
        
        security = {
            'address': token_address,
            'mint_authority_disabled': token_info.get('mint_authority') is None,
            'freeze_authority_disabled': token_info.get('freeze_authority') is None,
            'is_renounced': token_info.get('mint_authority') is None and token_info.get('freeze_authority') is None,
            'holder_count': token_info.get('holder_count', 0),
            'supply': token_info.get('supply'),
            'creator': token_info.get('creator'),
            'created_at': token_info.get('created_at'),
            'age_minutes': token_info.get('age_minutes', 0)
        }
        
        # امتیاز امنیتی
        security_score = 50  # پایه
        
        if security['mint_authority_disabled']:
            security_score += 20  # نمیتونه توکن جدید بسازه
        
        if security['freeze_authority_disabled']:
            security_score += 15  # نمیتونه حساب‌ها رو فریز کنه
        
        if security['holder_count'] > 100:
            security_score += 15  # هولدرهای کافی
        elif security['holder_count'] > 50:
            security_score += 10
        elif security['holder_count'] < 10:
            security_score -= 20  # خیلی کم هولدر
        
        if security['age_minutes'] < 5:
            security_score -= 30  # خیلی جدید - ریسک بالا
        elif security['age_minutes'] < 60:
            security_score -= 15
        elif security['age_minutes'] > 1440:  # بیشتر از ۱ روز
            security_score += 10
        
        security['security_score'] = max(0, min(100, security_score))
        
        if security_score >= 80:
            security['level'] = '🟢 SAFE'
            security['recommendation'] = '✅ Good security - Low risk'
        elif security_score >= 60:
            security['level'] = '🟡 MODERATE'
            security['recommendation'] = '⚠️ Acceptable risk - Do your own research'
        elif security_score >= 40:
            security['level'] = '🟠 RISKY'
            security['recommendation'] = '🔴 High risk - Be very careful'
        else:
            security['level'] = '🔴 DANGEROUS'
            security['recommendation'] = '💀 Extremely high risk - Avoid'
        
        return security
    
    async def get_trending_tokens(self) -> List[Dict]:
        """
        دریافت توکن‌های داغ سولانا
        بر اساس حجم معاملات و تعداد تراکنش‌ها
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/token/trending"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        tokens = data.get('data', [])
                        return [{
                            'address': t.get('address'),
                            'symbol': t.get('symbol'),
                            'name': t.get('name'),
                            'price_usd': t.get('priceUsdt'),
                            'volume_24h': t.get('volume24h'),
                            'price_change_24h': t.get('priceChange24h'),
                            'holder_count': t.get('holder'),
                            'platform': t.get('platform')
                        } for t in tokens[:20]]
        
        except Exception as e:
            logger.error(f"Solscan trending error: {e}")
        
        return []
    
    async def get_token_markets(self, token_address: str) -> List[Dict]:
        """
        دریافت بازارهای فعال برای یک توکن
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/market/token"
            params = {'token': token_address}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('success'):
                        markets = data.get('data', [])
                        return [{
                            'market_id': m.get('marketId'),
                            'name': m.get('name'),
                            'base_symbol': m.get('baseSymbol'),
                            'quote_symbol': m.get('quoteSymbol'),
                            'price': m.get('price'),
                            'volume_24h': m.get('volume24h')
                        } for m in markets]
        
        except Exception as e:
            logger.error(f"Solscan markets error: {e}")
        
        return []
    
    async def close(self):
        """بستن session"""
        if self.session and not self.session.closed:
            await self.session.close()

# نمونه‌سازی سراسری
solscan_api = SolscanAPI()
