#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API اختصاصی Pump.fun - ردیاب لحظه‌ای میم‌کوین‌های سولانا
Pump.fun بزرگترین platform برای ایجاد میم‌کوین در سولاناست
هر دقیقه ده‌ها توکن جدید روی اون ساخته میشه
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import json
import time
import base64

logger = logging.getLogger(__name__)

class PumpFunAPI:
    """
    API غیررسمی Pump.fun - ردیابی لحظه‌ای میم‌کوین‌های جدید
    بدون نیاز به API Key
    """
    
    BASE_URL = "https://pump.fun/api"
    
    # قراردادهای مهم
    PUMP_FUN_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
    RAYDIUM_PROGRAM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
    
    def __init__(self):
        self.session = None
        self.recent_tokens = []
        self.seen_tokens = set()
        self.callbacks = []
        self.monitoring = False
        
        logger.info("🦊 PumpFunAPI initialized - Ready to catch new meme coins")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """دریافت session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_recent_tokens(self, limit: int = 50) -> List[Dict]:
        """
        دریافت آخرین توکن‌های ساخته شده روی Pump.fun
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/coins/recent"
            params = {'limit': limit}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    tokens = []
                    for token in data:
                        processed = self._process_token(token)
                        
                        if processed['address'] not in self.seen_tokens:
                            self.seen_tokens.add(processed['address'])
                            self.recent_tokens.append(processed)
                            
                            if len(self.recent_tokens) > 1000:
                                self.recent_tokens = self.recent_tokens[-1000:]
                        
                        tokens.append(processed)
                    
                    return tokens
                else:
                    logger.warning(f"Pump.fun returned {response.status}")
                    return []
        
        except Exception as e:
            logger.error(f"Pump.fun API error: {e}")
            return []
    
    async def get_token_info(self, token_address: str) -> Optional[Dict]:
        """
        دریافت اطلاعات یک توکن خاص
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/coins/{token_address}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_token(data)
                else:
                    return None
        
        except Exception as e:
            logger.error(f"Error getting token info: {e}")
            return None
    
    async def get_token_trades(self, token_address: str, limit: int = 50) -> List[Dict]:
        """
        دریافت آخرین معاملات یک توکن
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/trades/{token_address}"
            params = {'limit': limit}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    trades = []
                    for trade in data:
                        trades.append({
                            'signature': trade.get('signature'),
                            'type': trade.get('type'),  # buy, sell
                            'amount': trade.get('amount'),
                            'price': trade.get('price'),
                            'timestamp': trade.get('timestamp'),
                            'user': trade.get('user'),
                            'market_cap': trade.get('marketCap')
                        })
                    
                    return trades
                else:
                    return []
        
        except Exception as e:
            logger.error(f"Error getting trades: {e}")
            return []
    
    async def get_token_chart(self, token_address: str, resolution: str = '1m') -> List[Dict]:
        """
        دریافت داده‌های نمودار
        resolution: 1m, 5m, 15m, 1h, 4h, 1d
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/charts/{token_address}"
            params = {'resolution': resolution}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    candles = []
                    for candle in data:
                        candles.append({
                            'timestamp': candle.get('timestamp'),
                            'open': candle.get('open'),
                            'high': candle.get('high'),
                            'low': candle.get('low'),
                            'close': candle.get('close'),
                            'volume': candle.get('volume')
                        })
                    
                    return candles
                else:
                    return []
        
        except Exception as e:
            logger.error(f"Error getting chart: {e}")
            return []
    
    async def get_king_of_the_hill(self) -> Optional[Dict]:
        """
        دریافت توکن "پادشاه تپه" - توکن با بیشترین حجم در ۱ ساعت
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/king-of-the-hill"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_token(data)
                else:
                    return None
        
        except Exception as e:
            logger.error(f"Error getting king: {e}")
            return None
    
    async def get_trending_tokens(self) -> List[Dict]:
        """
        دریافت توکن‌های داغ (بیشترین حجم در ۵ دقیقه)
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/trending"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [self._process_token(t) for t in data]
                else:
                    return []
        
        except Exception as e:
            logger.error(f"Error getting trending: {e}")
            return []
    
    async def monitor_new_tokens(self, callback: Callable = None, interval: float = 5.0):
        """
        مانیتورینگ لحظه‌ای توکن‌های جدید
        
        Args:
            callback: تابعی که برای هر توکن جدید صدا زده میشه
            interval: فاصله بین چک‌ها (ثانیه) - پیشنهادی ۵ ثانیه
        """
        if self.monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring = True
        
        if callback:
            self.callbacks.append(callback)
        
        logger.info(f"🔍 Starting Pump.fun monitor (interval: {interval}s)")
        
        last_check = datetime.now()
        
        while self.monitoring:
            try:
                # دریافت توکن‌های جدید
                tokens = await self.get_recent_tokens(limit=20)
                
                for token in tokens:
                    # محاسبه سن توکن
                    created_at = datetime.fromisoformat(token['created_at']) if token['created_at'] else datetime.now()
                    age_seconds = (datetime.now() - created_at).total_seconds()
                    
                    token['age_seconds'] = age_seconds
                    token['age_minutes'] = round(age_seconds / 60, 2)
                    token['is_new'] = age_seconds < 60  # کمتر از ۱ دقیقه
                    
                    # اگه خیلی جدید بود
                    if token['is_new']:
                        logger.info(f"🆕 NEW PUMP.FUN TOKEN: {token['symbol']} (${token['market_cap']:.0f}) - {age_seconds:.0f}s old")
                        
                        for callback in self.callbacks:
                            try:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(token)
                                else:
                                    callback(token)
                            except Exception as e:
                                logger.error(f"Callback error: {e}")
                
                # محاسبه زمان تا چک بعدی
                elapsed = (datetime.now() - last_check).total_seconds()
                if elapsed < interval:
                    await asyncio.sleep(interval - elapsed)
                
                last_check = datetime.now()
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(interval * 2)
    
    def stop_monitoring(self):
        """توقف مانیتورینگ"""
        self.monitoring = False
        logger.info("🛑 Pump.fun monitor stopped")
    
    def _process_token(self, token: Dict) -> Dict:
        """پردازش داده‌های خام توکن"""
        
        # محاسبات
        market_cap = float(token.get('marketCap', 0))
        volume_24h = float(token.get('volume24h', 0))
        liquidity = float(token.get('liquidity', 0))
        
        # امتیاز بر اساس معیارها
        score = 50  # پایه
        
        if market_cap > 100000:
            score += 20
        elif market_cap > 50000:
            score += 15
        elif market_cap > 10000:
            score += 10
        
        if volume_24h > market_cap * 0.5:
            score += 15
        
        if liquidity > 50000:
            score += 15
        elif liquidity > 10000:
            score += 10
        
        # سطح
        if score >= 80:
            level = "🚀 HOT"
        elif score >= 60:
            level = "🔥 WARM"
        elif score >= 40:
            level = "📊 NORMAL"
        else:
            level = "❄️ COLD"
        
        return {
            'address': token.get('mint'),
            'symbol': token.get('symbol'),
            'name': token.get('name'),
            'description': token.get('description'),
            'image': token.get('image'),
            'created_at': token.get('createdAt'),
            'creator': token.get('creator'),
            'market_cap': market_cap,
            'volume_24h': volume_24h,
            'liquidity': liquidity,
            'holder_count': token.get('holderCount', 0),
            'price': float(token.get('price', 0)),
            'price_change_5m': float(token.get('priceChange5m', 0)),
            'price_change_1h': float(token.get('priceChange1h', 0)),
            'price_change_24h': float(token.get('priceChange24h', 0)),
            'tx_count_5m': token.get('txCount5m', 0),
            'tx_count_1h': token.get('txCount1h', 0),
            'tx_count_24h': token.get('txCount24h', 0),
            'unique_wallets_24h': token.get('uniqueWallets24h', 0),
            'king_of_hill': token.get('isKing', False),
            'completed': token.get('isCompleted', False),  # آیا به Raydium مهاجرت کرده؟
            'score': score,
            'level': level,
            'platform': 'pump.fun',
            'url': f"https://pump.fun/coin/{token.get('mint')}",
            'source': 'pumpfun'
        }
    
    async def analyze_token_potential(self, token_address: str) -> Dict:
        """
        تحلیل پتانسیل یک توپن Pump.fun
        """
        token = await self.get_token_info(token_address)
        
        if not token:
            return {'error': 'Token not found'}
        
        # عوامل موفقیت
        factors = []
        
        # 1. سرعت رشد
        if token['price_change_5m'] > 50:
            factors.append(("🚀 Explosive growth", 0.9))
        elif token['price_change_5m'] > 20:
            factors.append(("📈 Strong growth", 0.8))
        elif token['price_change_5m'] > 10:
            factors.append(("📊 Moderate growth", 0.6))
        
        # 2. حجم معاملات
        if token['volume_24h'] > 100000:
            factors.append(("💎 High volume", 0.9))
        elif token['volume_24h'] > 50000:
            factors.append(("💰 Good volume", 0.7))
        elif token['volume_24h'] > 10000:
            factors.append(("📊 Average volume", 0.5))
        
        # 3. تعداد هولدرها
        if token['holder_count'] > 100:
            factors.append(("👥 Strong community", 0.8))
        elif token['holder_count'] > 50:
            factors.append(("👤 Growing community", 0.6))
        
        # 4. نقدینگی
        if token['liquidity'] > 50000:
            factors.append(("💧 High liquidity", 0.8))
        elif token['liquidity'] > 10000:
            factors.append(("💧 Good liquidity", 0.6))
        
        # 5. تعداد تراکنش‌ها
        if token['tx_count_24h'] > 500:
            factors.append(("🔄 Very active", 0.9))
        elif token['tx_count_24h'] > 200:
            factors.append(("🔄 Active", 0.7))
        
        # محاسبه امتیاز نهایی
        final_score = sum(f[1] for f in factors) / len(factors) if factors else 0.5
        
        # سطح پامپ
        if final_score >= 0.8:
            pump_level = "🚀🚀🚀 MEGA PUMP POTENTIAL"
        elif final_score >= 0.7:
            pump_level = "📈📈 STRONG PUMP POTENTIAL"
        elif final_score >= 0.6:
            pump_level = "📈 MODERATE PUMP POTENTIAL"
        elif final_score >= 0.5:
            pump_level = "👀 WATCHING"
        else:
            pump_level = "❄️ COLD"
        
        return {
            'token': token,
            'score': round(final_score * 100, 2),
            'pump_level': pump_level,
            'factors': [{'name': f[0], 'score': f[1]} for f in factors],
            'recommendation': self._get_recommendation(final_score),
            'analysis_time': datetime.now().isoformat()
        }
    
    def _get_recommendation(self, score: float) -> str:
        """توصیه بر اساس امتیاز"""
        if score >= 0.8:
            return "🚀 STRONG BUY - High potential for pump"
        elif score >= 0.7:
            return "📈 BUY - Good momentum"
        elif score >= 0.6:
            return "👀 WATCH - Wait for confirmation"
        elif score >= 0.5:
            return "⚖️ HOLD - Not clear yet"
        else:
            return "🛑 AVOID - Too risky"
    
    async def close(self):
        """بستن session"""
        if self.session and not self.session.closed:
            await self.session.close()

# نمونه‌سازی سراسری
pump_fun_api = PumpFunAPI()
