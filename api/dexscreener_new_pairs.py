#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ردیاب توکن‌های جدید - شناسایی میم‌کوین‌ها حتی یک دقیقه پس از ایجاد
پشتیبانی از:
- Ethereum
- BSC (BNB Chain)
- Solana
- Polygon
- Arbitrum
- Optimism
- Base
- Avalanche
- Fantom
- Cronos
- و تمام زنجیره‌های پشتیبانی شده توسط DexScreener
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import json
import time

logger = logging.getLogger(__name__)

class DexScreenerNewPairs:
    """
    ردیاب لحظه‌ای توکن‌های جدید - بدون نیاز به API Key
    از WebSocket و REST API DexScreener استفاده می‌کنه
    """
    
    # لیست تمام زنجیره‌های پشتیبانی شده
    SUPPORTED_CHAINS = {
        'ethereum': 'ethereum',
        'bsc': 'bsc',
        'solana': 'solana',
        'polygon': 'polygon',
        'arbitrum': 'arbitrum',
        'optimism': 'optimism',
        'base': 'base',
        'avalanche': 'avalanche',
        'fantom': 'fantom',
        'cronos': 'cronos',
        'celo': 'celo',
        'aurora': 'aurora',
        'moonriver': 'moonriver',
        'moonbeam': 'moonbeam',
        'harmony': 'harmony',
        'fuse': 'fuse',
        'boba': 'boba',
        'metis': 'metis',
        'kava': 'kava',
        'okx': 'okx',
        'pulsechain': 'pulsechain',
        'telos': 'telos',
        'kcc': 'kcc',
        'tomochain': 'tomochain',
        'velas': 'velas',
        'smartbch': 'smartbch'
    }
    
    # WebSocket URL برای دریافت لحظه‌ای
    WS_URL = "wss://io.dexscreener.com/dex/screener/pairs/h1/1"
    
    def __init__(self):
        self.ws_connection = None
        self.callbacks = []
        self.recent_pairs = []
        self.max_recent = 1000
        self.monitoring = False
        
        # کش برای جلوگیری از داپلیکیت
        self.seen_pairs = set()
        
        logger.info(f"🔍 DexScreenerNewPairs initialized - Monitoring {len(self.SUPPORTED_CHAINS)} chains")
    
    async def get_new_pairs_rest(self, chain: str = None, limit: int = 50) -> List[Dict]:
        """
        دریافت توکن‌های جدید از طریق REST API
        مناسب برای درخواست‌های یک‌بار
        """
        session = aiohttp.ClientSession()
        
        try:
            if chain and chain in self.SUPPORTED_CHAINS:
                url = f"https://api.dexscreener.com/latest/dex/search?q={chain}"
            else:
                url = "https://api.dexscreener.com/latest/dex/search?q="
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    
                    # مرتب‌سازی بر اساس زمان ایجاد (جدیدترین اول)
                    sorted_pairs = sorted(
                        pairs,
                        key=lambda p: int(p.get('pairCreatedAt', 0)),
                        reverse=True
                    )
                    
                    # تبدیل به فرمت استاندارد
                    result = []
                    for pair in sorted_pairs[:limit]:
                        processed = self._process_pair(pair)
                        if processed:
                            result.append(processed)
                            self.seen_pairs.add(processed['pair_address'])
                    
                    await session.close()
                    return result
                else:
                    logger.warning(f"DexScreener REST returned {response.status}")
                    await session.close()
                    return []
        
        except Exception as e:
            logger.error(f"Error getting new pairs via REST: {e}")
            await session.close()
            return []
    
    async def get_new_pairs_by_chain(self, chain: str, limit: int = 50) -> List[Dict]:
        """
        دریافت توکن‌های جدید برای یک زنجیره خاص
        """
        if chain not in self.SUPPORTED_CHAINS:
            logger.warning(f"Unsupported chain: {chain}")
            return []
        
        return await self.get_new_pairs_rest(chain, limit)
    
    async def get_new_pairs_all_chains(self, limit_per_chain: int = 10) -> Dict[str, List[Dict]]:
        """
        دریافت توکن‌های جدید از همه زنجیره‌ها
        """
        result = {}
        
        for chain in self.SUPPORTED_CHAINS:
            pairs = await self.get_new_pairs_by_chain(chain, limit_per_chain)
            if pairs:
                result[chain] = pairs
            await asyncio.sleep(0.5)  # جلوگیری از rate limit
        
        return result
    
    async def start_websocket_monitoring(self, callback: Callable = None):
        """
        شروع مانیتورینگ لحظه‌ای با WebSocket
        این متد توکن‌های جدید رو همون لحظه که ساخته می‌شن گزارش می‌ده
        """
        if self.monitoring:
            logger.warning("WebSocket monitoring already active")
            return
        
        self.monitoring = True
        
        if callback:
            self.callbacks.append(callback)
        
        asyncio.create_task(self._websocket_loop())
        
        logger.info("🔌 WebSocket monitoring started - Real-time token detection active")
    
    async def _websocket_loop(self):
        """حلقه اصلی WebSocket"""
        import websocket
        
        while self.monitoring:
            try:
                ws = websocket.WebSocket()
                ws.connect(self.WS_URL)
                
                logger.info("✅ WebSocket connected")
                
                while self.monitoring:
                    message = ws.recv()
                    
                    if message:
                        await self._process_websocket_message(message)
                    
                    await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await asyncio.sleep(5)  # تلاش مجدد بعد از ۵ ثانیه
    
    async def _process_websocket_message(self, message: str):
        """پردازش پیام WebSocket"""
        try:
            data = json.loads(message)
            
            # استخراج جفت‌های جدید
            pairs = data.get('pairs', [])
            
            for pair in pairs:
                pair_address = pair.get('pairAddress')
                
                # اگه قبلاً ندیدیم
                if pair_address and pair_address not in self.seen_pairs:
                    processed = self._process_pair(pair)
                    
                    if processed:
                        # محاسبه سن توکن
                        created_at = processed.get('created_at', 0)
                        age_seconds = (time.time() * 1000) - created_at if created_at else 0
                        age_minutes = age_seconds / 60000
                        
                        processed['age_seconds'] = age_seconds
                        processed['age_minutes'] = round(age_minutes, 2)
                        processed['is_new'] = age_minutes < 5  # کمتر از ۵ دقیقه
                        
                        # اضافه به لیست
                        self.recent_pairs.append(processed)
                        self.seen_pairs.add(pair_address)
                        
                        # محدودیت لیست
                        if len(self.recent_pairs) > self.max_recent:
                            self.recent_pairs = self.recent_pairs[-self.max_recent:]
                        
                        # اجرای callbackها
                        for callback in self.callbacks:
                            try:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(processed)
                                else:
                                    callback(processed)
                            except Exception as e:
                                logger.error(f"Callback error: {e}")
                        
                        # لاگ برای توکن‌های خیلی جدید
                        if processed['is_new']:
                            logger.info(f"🆕 NEW TOKEN DETECTED: {processed['symbol']} on {processed['chain']} ({age_minutes:.1f} minutes old)")
        
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}")
    
    def _process_pair(self, pair: Dict) -> Optional[Dict]:
        """تبدیل داده‌های خام به فرمت استاندارد"""
        try:
            base_token = pair.get('baseToken', {})
            quote_token = pair.get('quoteToken', {})
            
            # استخراج اطلاعات
            result = {
                'chain': pair.get('chainId'),
                'dex': pair.get('dexId'),
                'pair_address': pair.get('pairAddress'),
                'pair_url': pair.get('url'),
                'created_at': pair.get('pairCreatedAt'),
                'created_at_datetime': datetime.fromtimestamp(
                    int(pair.get('pairCreatedAt', 0)) / 1000
                ).isoformat() if pair.get('pairCreatedAt') else None,
                
                # توکن
                'token_address': base_token.get('address'),
                'token_symbol': base_token.get('symbol'),
                'token_name': base_token.get('name'),
                
                # کووت
                'quote_address': quote_token.get('address'),
                'quote_symbol': quote_token.get('symbol'),
                
                # قیمت
                'price_usd': float(pair.get('priceUsd') or 0),
                'price_native': float(pair.get('priceNative') or 0),
                
                # تغییرات
                'price_change_5m': float(pair.get('priceChange', {}).get('m5') or 0),
                'price_change_1h': float(pair.get('priceChange', {}).get('h1') or 0),
                'price_change_6h': float(pair.get('priceChange', {}).get('h6') or 0),
                'price_change_24h': float(pair.get('priceChange', {}).get('h24') or 0),
                
                # حجم
                'volume_5m': float(pair.get('volume', {}).get('m5') or 0),
                'volume_1h': float(pair.get('volume', {}).get('h1') or 0),
                'volume_6h': float(pair.get('volume', {}).get('h6') or 0),
                'volume_24h': float(pair.get('volume', {}).get('h24') or 0),
                
                # نقدینگی
                'liquidity_usd': float(pair.get('liquidity', {}).get('usd') or 0),
                'liquidity_base': float(pair.get('liquidity', {}).get('base') or 0),
                'liquidity_quote': float(pair.get('liquidity', {}).get('quote') or 0),
                
                # مارکت‌کپ
                'market_cap': float(pair.get('marketCap') or 0),
                'fdv': float(pair.get('fdv') or 0),
                
                # تراکنش‌ها
                'txns_5m': pair.get('txns', {}).get('m5', {}),
                'txns_1h': pair.get('txns', {}).get('h1', {}),
                'txns_6h': pair.get('txns', {}).get('h6', {}),
                'txns_24h': pair.get('txns', {}).get('h24', {}),
                
                # اطلاعات اضافی
                'labels': pair.get('labels', []),
                'info': pair.get('info', {})
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing pair: {e}")
            return None
    
    def get_recent_pairs(self, chain: str = None, min_age: int = None, limit: int = 50) -> List[Dict]:
        """
        دریافت جفت‌های اخیر از حافظه
        """
        pairs = self.recent_pairs.copy()
        
        # فیلتر بر اساس زنجیره
        if chain:
            pairs = [p for p in pairs if p['chain'] == chain]
        
        # فیلتر بر اساس سن
        if min_age is not None:
            now = time.time() * 1000
            pairs = [p for p in pairs if (now - p['created_at']) / 60000 <= min_age]
        
        # مرتب‌سازی بر اساس زمان (جدیدترین اول)
        pairs.sort(key=lambda x: x['created_at'], reverse=True)
        
        return pairs[:limit]
    
    def get_newest_pairs(self, chain: str = None, minutes: int = 5) -> List[Dict]:
        """
        دریافت جدیدترین توکن‌ها (کمتر از X دقیقه)
        """
        return self.get_recent_pairs(chain, minutes)
    
    async def wait_for_new_token(self, chain: str = None, timeout: int = 300) -> Optional[Dict]:
        """
        منتظر موندن برای توکن جدید - تا timeout ثانیه
        """
        future = asyncio.Future()
        
        def callback(pair):
            if not chain or pair['chain'] == chain:
                if not future.done():
                    future.set_result(pair)
        
        self.callbacks.append(callback)
        
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            return None
        finally:
            if callback in self.callbacks:
                self.callbacks.remove(callback)
    
    def stop_monitoring(self):
        """توقف مانیتورینگ WebSocket"""
        self.monitoring = False
        logger.info("🛑 WebSocket monitoring stopped")

# نمونه‌سازی سراسری
dexscreener_new_pairs = DexScreenerNewPairs()
