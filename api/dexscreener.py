#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API DexScreener - رایگان و بدون نیاز به کلید
منبع اصلی داده‌های لحظه‌ای توکن‌ها
پشتیبانی از: Ethereum, BSC, Polygon, Avalanche, Arbitrum, Optimism, Fantom, Cronos
"""

import aiohttp
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DexScreenerAPI:
    """
    API رایگان DexScreener - بهترین منبع برای داده‌های توکن
    """
    
    BASE_URL = "https://api.dexscreener.com/latest/dex"
    
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_timeout = 60  # 1 دقیقه
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """دریافت session (ساخت اگه وجود نداشته باشه)"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_token_info(self, token_address: str, chain: str = None) -> Optional[Dict]:
        """
        دریافت اطلاعات کامل توکن
        
        Args:
            token_address: آدرس توکن
            chain: زنجیره (اختیاری)
        
        Returns:
            اطلاعات توکن یا None
        """
        cache_key = f"token_{token_address}_{chain}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        session = await self._get_session()
        
        try:
            if chain:
                url = f"{self.BASE_URL}/tokens/{chain}/{token_address}"
            else:
                url = f"{self.BASE_URL}/tokens/{token_address}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    
                    if pairs:
                        # بهترین جفت (بیشترین نقدینگی)
                        best_pair = max(pairs, key=lambda p: float(p.get('liquidity', {}).get('usd', 0) or 0))
                        
                        result = self._parse_pair(best_pair)
                        self.cache[cache_key] = (result, datetime.now())
                        return result
                else:
                    logger.warning(f"DexScreener returned {response.status}")
        
        except Exception as e:
            logger.error(f"DexScreener error: {e}")
        
        return None
    
    async def search_token(self, query: str) -> List[Dict]:
        """
        جستجوی توکن بر اساس نماد یا نام
        """
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/search"
            params = {'q': query}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    return [self._parse_pair(p) for p in pairs[:20]]
        
        except Exception as e:
            logger.error(f"DexScreener search error: {e}")
        
        return []
    
    async def get_token_price(self, token_address: str, chain: str = None) -> Optional[float]:
        """دریافت فقط قیمت"""
        info = await self.get_token_info(token_address, chain)
        return info.get('price') if info else None
    
    async def get_token_pairs(self, token_address: str) -> List[Dict]:
        """دریافت همه جفت‌های یک توکن"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/tokens/{token_address}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [self._parse_pair(p) for p in data.get('pairs', [])]
        except Exception as e:
            logger.error(f"Error getting pairs: {e}")
        
        return []
    
    def _parse_pair(self, pair: Dict) -> Dict:
        """تبدیل داده‌های خام به فرمت یکسان"""
        return {
            'chain': pair.get('chainId'),
            'dex': pair.get('dexId'),
            'pair_address': pair.get('pairAddress'),
            'base_token': {
                'address': pair.get('baseToken', {}).get('address'),
                'symbol': pair.get('baseToken', {}).get('symbol'),
                'name': pair.get('baseToken', {}).get('name')
            },
            'quote_token': {
                'address': pair.get('quoteToken', {}).get('address'),
                'symbol': pair.get('quoteToken', {}).get('symbol'),
                'name': pair.get('quoteToken', {}).get('name')
            },
            'price': float(pair.get('priceUsd') or 0),
            'price_native': float(pair.get('priceNative') or 0),
            'price_change_5m': float(pair.get('priceChange', {}).get('m5') or 0),
            'price_change_1h': float(pair.get('priceChange', {}).get('h1') or 0),
            'price_change_6h': float(pair.get('priceChange', {}).get('h6') or 0),
            'price_change_24h': float(pair.get('priceChange', {}).get('h24') or 0),
            'volume_5m': float(pair.get('volume', {}).get('m5') or 0),
            'volume_1h': float(pair.get('volume', {}).get('h1') or 0),
            'volume_6h': float(pair.get('volume', {}).get('h6') or 0),
            'volume_24h': float(pair.get('volume', {}).get('h24') or 0),
            'liquidity': float(pair.get('liquidity', {}).get('usd') or 0),
            'market_cap': float(pair.get('marketCap') or 0),
            'txns_5m': pair.get('txns', {}).get('m5', {}),
            'txns_1h': pair.get('txns', {}).get('h1', {}),
            'txns_6h': pair.get('txns', {}).get('h6', {}),
            'txns_24h': pair.get('txns', {}).get('h24', {}),
            'url': pair.get('url'),
            'created_at': pair.get('pairCreatedAt'),
            'labels': pair.get('labels', []),
            'info': pair.get('info', {})
        }
    
    async def get_trending_tokens(self, chain: str = None) -> List[Dict]:
        """دریافت توکن‌های داغ"""
        # DexScreener Trending API نداره، از search استفاده می‌کنیم
        popular_pairs = []
        
        # توکن‌های محبوب معروف
        popular = ['WETH', 'USDC', 'USDT', 'WBTC', 'DAI']
        
        for token in popular:
            pairs = await self.search_token(token)
            if pairs:
                popular_pairs.extend(pairs[:3])
        
        return popular_pairs
    
    async def close(self):
        """بستن session"""
        if self.session and not self.session.closed:
            await self.session.close()

# نمونه‌سازی سراسری
dexscreener_api = DexScreenerAPI()
