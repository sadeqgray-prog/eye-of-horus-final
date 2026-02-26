#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API CoinGecko - منبع اصلی داده‌های بازار
پشتیبانی از ۱۰۰۰۰+ ارز از جمله تمام میم‌کوین‌ها
با قابلیت شناسایی توکن‌های جدید
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class CoinGeckoAPI:
    """
    API CoinGecko - رایگان با محدودیت ۵۰ درخواست در دقیقه
    برای پروژه‌های جدی نیاز به API Key هست
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    PRO_BASE_URL = "https://pro-api.coingecko.com/api/v3"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        # آمار
        self.stats = {
            'total_requests': 0,
            'rate_limit_remaining': 50,
            'rate_limit_reset': time.time() + 60,
            'last_request': None
        }
        
        logger.info("📊 CoinGeckoAPI initialized")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key (اختیاری - برای درخواست بیشتر)"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ CoinGecko API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ CoinGecko global API key set")
    
    def has_key(self, user_id: int = None) -> bool:
        """بررسی وجود API Key"""
        if user_id and user_id in self.user_api_keys:
            return True
        return self.api_key is not None
    
    def get_base_url(self, user_id: int = None) -> str:
        """دریافت URL مناسب (با یا بدون API Key)"""
        if self.has_key(user_id):
            return self.PRO_BASE_URL
        return self.BASE_URL
    
    def get_api_key(self, user_id: int = None) -> Optional[str]:
        """دریافت API Key مناسب"""
        if user_id and user_id in self.user_api_keys:
            return self.user_api_keys[user_id]
        return self.api_key
    
    async def _make_request(self, endpoint: str, params: Dict = None, 
                           user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به CoinGecko با مدیریت rate limit"""
        
        # Rate limiting
        now = time.time()
        if now < self.stats['rate_limit_reset']:
            if self.stats['rate_limit_remaining'] <= 0:
                wait_time = self.stats['rate_limit_reset'] - now
                logger.warning(f"Rate limit reached, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
                self.stats['rate_limit_remaining'] = 50
                self.stats['rate_limit_reset'] = time.time() + 60
        else:
            self.stats['rate_limit_remaining'] = 50
            self.stats['rate_limit_reset'] = time.time() + 60
        
        base_url = self.get_base_url(user_id)
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        headers = {}
        api_key = self.get_api_key(user_id)
        if api_key:
            headers['x-cg-pro-api-key'] = api_key
        
        self.stats['total_requests'] += 1
        self.stats['last_request'] = datetime.now().isoformat()
        self.stats['rate_limit_remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    
                    # بررسی rate limit headers
                    if 'X-RateLimit-Remaining' in response.headers:
                        self.stats['rate_limit_remaining'] = int(response.headers['X-RateLimit-Remaining'])
                    
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("Rate limit exceeded, waiting...")
                        await asyncio.sleep(60)
                        return await self._make_request(endpoint, params, user_id)
                    else:
                        logger.warning(f"CoinGecko returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"CoinGecko request error: {e}")
            return None
    
    async def search_token(self, query: str, user_id: int = None) -> List[Dict]:
        """
        جستجوی توکن بر اساس نماد یا نام
        """
        result = await self._make_request('search', {'query': query}, user_id)
        
        if result:
            coins = result.get('coins', [])
            return [{
                'id': c.get('id'),
                'symbol': c.get('symbol'),
                'name': c.get('name'),
                'platforms': c.get('platforms', {}),
                'market_cap_rank': c.get('market_cap_rank'),
                'large_image': c.get('large'),
                'thumb_image': c.get('thumb')
            } for c in coins[:20]]
        
        return []
    
    async def get_token_price(self, token_id: str, vs_currency: str = 'usd',
                             user_id: int = None) -> Optional[Dict]:
        """
        دریافت قیمت لحظه‌ای توکن
        """
        result = await self._make_request('simple/price', {
            'ids': token_id,
            'vs_currencies': vs_currency,
            'include_24hr_vol': 'true',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_last_updated_at': 'true'
        }, user_id)
        
        if result and token_id in result:
            data = result[token_id]
            return {
                'price': data.get(f'{vs_currency}'),
                'volume_24h': data.get(f'{vs_currency}_24h_vol'),
                'price_change_24h': data.get(f'{vs_currency}_24h_change'),
                'market_cap': data.get(f'{vs_currency}_market_cap'),
                'last_updated': data.get('last_updated_at')
            }
        
        return None
    
    async def get_token_details(self, token_id: str, user_id: int = None) -> Optional[Dict]:
        """
        دریافت اطلاعات کامل توکن
        """
        result = await self._make_request(f'coins/{token_id}', {
            'localization': 'false',
            'tickers': 'true',
            'market_data': 'true',
            'community_data': 'true',
            'developer_data': 'true'
        }, user_id)
        
        if result:
            return {
                'id': result.get('id'),
                'symbol': result.get('symbol'),
                'name': result.get('name'),
                'description': result.get('description', {}).get('en'),
                'categories': result.get('categories', []),
                'market_data': {
                    'current_price': result.get('market_data', {}).get('current_price', {}),
                    'market_cap': result.get('market_data', {}).get('market_cap', {}),
                    'total_volume': result.get('market_data', {}).get('total_volume', {}),
                    'high_24h': result.get('market_data', {}).get('high_24h', {}),
                    'low_24h': result.get('market_data', {}).get('low_24h', {}),
                    'price_change_24h': result.get('market_data', {}).get('price_change_24h'),
                    'price_change_percentage_24h': result.get('market_data', {}).get('price_change_percentage_24h'),
                    'circulating_supply': result.get('market_data', {}).get('circulating_supply'),
                    'total_supply': result.get('market_data', {}).get('total_supply'),
                    'max_supply': result.get('market_data', {}).get('max_supply'),
                    'ath': result.get('market_data', {}).get('ath', {}),
                    'atl': result.get('market_data', {}).get('atl', {})
                },
                'community_data': {
                    'twitter_followers': result.get('community_data', {}).get('twitter_followers'),
                    'reddit_subscribers': result.get('community_data', {}).get('reddit_subscribers'),
                    'telegram_channel_user_count': result.get('community_data', {}).get('telegram_channel_user_count')
                },
                'developer_data': result.get('developer_data', {}),
                'platforms': result.get('platforms', {}),
                'genesis_date': result.get('genesis_date'),
                'sentiment_votes_up_percentage': result.get('sentiment_votes_up_percentage'),
                'sentiment_votes_down_percentage': result.get('sentiment_votes_down_percentage'),
                'last_updated': result.get('last_updated')
            }
        
        return None
    
    async def get_trending_tokens(self, user_id: int = None) -> List[Dict]:
        """
        دریافت توکن‌های داغ لحظه‌ای
        """
        result = await self._make_request('search/trending', user_id=user_id)
        
        if result:
            coins = result.get('coins', [])
            return [{
                'id': c['item'].get('id'),
                'coin_id': c['item'].get('coin_id'),
                'name': c['item'].get('name'),
                'symbol': c['item'].get('symbol'),
                'market_cap_rank': c['item'].get('market_cap_rank'),
                'thumb': c['item'].get('thumb'),
                'small': c['item'].get('small'),
                'large': c['item'].get('large'),
                'slug': c['item'].get('slug'),
                'price_btc': c['item'].get('price_btc'),
                'score': c['item'].get('score')
            } for c in coins]
        
        return []
    
    async def get_new_tokens(self, user_id: int = None) -> List[Dict]:
        """
        دریافت توکن‌های جدید اضافه شده به CoinGecko
        
        توجه: CoinGecko API مستقیم این قابلیت رو نداره
        از طریق categories و recently_added استفاده می‌کنیم
        """
        # این یک روش تقریبی هست
        # دریافت توکن‌های دسته‌بندی "Recently Added"
        result = await self._make_request('coins/markets', {
            'vs_currency': 'usd',
            'order': 'id_asc',
            'per_page': 100,
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }, user_id)
        
        if result:
            # مرتب‌سازی بر اساس id (که معمولاً تاریخ اضافه شدن رو منعکس می‌کنه)
            sorted_coins = sorted(result, key=lambda x: x['id'], reverse=True)
            return [{
                'id': c['id'],
                'symbol': c['symbol'],
                'name': c['name'],
                'image': c['image'],
                'current_price': c['current_price'],
                'market_cap': c['market_cap'],
                'market_cap_rank': c['market_cap_rank'],
                'price_change_24h': c['price_change_percentage_24h'],
                'is_new': True
            } for c in sorted_coins[:20]]
        
        return []
    
    async def get_token_ohlc(self, token_id: str, days: int = 1, 
                            vs_currency: str = 'usd', user_id: int = None) -> List[List]:
        """
        دریافت داده‌های OHLC برای تحلیل تکنیکال
        """
        result = await self._make_request(f'coins/{token_id}/ohlc', {
            'vs_currency': vs_currency,
            'days': days
        }, user_id)
        
        return result or []
    
    async def get_token_market_chart(self, token_id: str, days: int = 1,
                                     vs_currency: str = 'usd', user_id: int = None) -> Optional[Dict]:
        """
        دریافت نمودار بازار (قیمت، حجم، مارکت‌کپ)
        """
        result = await self._make_request(f'coins/{token_id}/market_chart', {
            'vs_currency': vs_currency,
            'days': days
        }, user_id)
        
        if result:
            return {
                'prices': result.get('prices', []),
                'market_caps': result.get('market_caps', []),
                'total_volumes': result.get('total_volumes', [])
            }
        
        return None
    
    async def get_tokens_by_category(self, category: str = 'meme-token',
                                     user_id: int = None) -> List[Dict]:
        """
        دریافت توکن‌های یک دسته‌بندی خاص
        category: 'meme-token', 'dex', 'layer-1', ...
        """
        result = await self._make_request('coins/markets', {
            'vs_currency': 'usd',
            'category': category,
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }, user_id)
        
        return result or []
    
    async def get_meme_coins(self, user_id: int = None) -> List[Dict]:
        """
        دریافت تمام میم‌کوین‌های معروف
        """
        return await self.get_tokens_by_category('meme-token', user_id)
    
    async def search_meme_coins(self, query: str, user_id: int = None) -> List[Dict]:
        """
        جستجوی میم‌کوین‌ها
        """
        results = await self.search_token(query, user_id)
        
        # فیلتر کردن میم‌کوین‌ها (بر اساس نماد)
        meme_keywords = ['dog', 'shib', 'pepe', 'woof', 'bonk', 'samoyed', 'floki', 'baby']
        
        meme_coins = []
        for token in results:
            symbol = token['symbol'].lower()
            if any(keyword in symbol for keyword in meme_keywords):
                meme_coins.append(token)
        
        return meme_coins
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared CoinGecko API key for user {user_id}")

# نمونه‌سازی سراسری
coingecko_api = CoinGeckoAPI()
