#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API CryptoPanic - اخبار اختصاصی ارزهای دیجیتال
پشتیبانی از فیلتر میم‌کوین‌ها
نیازمند API Key (رایگان)
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class CryptoPanicAPI:
    """
    API CryptoPanic - اخبار لحظه‌ای کریپتو
    رایگان: ۱۰۰ درخواست در روز
    """
    
    BASE_URL = "https://cryptopanic.com/api/v1"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        # فیلترهای خبری
        self.CURRENCIES = ['BTC', 'ETH', 'SOL', 'DOGE', 'SHIB', 'PEPE', 'BONK']
        self.FILTERS = ['hot', 'rising', 'bullish', 'bearish', 'important']
        
        self.stats = {
            'total_requests': 0,
            'remaining': 100,
            'reset_time': time.time() + 86400
        }
        
        self.cache = {}
        self.cache_timeout = 300  # ۵ دقیقه
        
        logger.info("📰 CryptoPanicAPI initialized")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ CryptoPanic API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ CryptoPanic global API key set")
    
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
            "🔑 **CryptoPanic API Key Required**\n\n"
            "To get real-time crypto news, I need your CryptoPanic API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://cryptopanic.com/developers/api/\n"
            "2. Sign up and get your API key\n\n"
            "**Send me:** `CRYPTOPANIC: YOUR_API_KEY`\n\n"
            "Example: `CRYPTOPANIC: abc123xyz789`"
        )
    
    async def _make_request(self, endpoint: str, params: Dict,
                           user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به CryptoPanic"""
        
        api_key = self.get_api_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        # Rate limiting
        now = time.time()
        if now > self.stats['reset_time']:
            self.stats['remaining'] = 100
            self.stats['reset_time'] = now + 86400
        
        if self.stats['remaining'] <= 0:
            wait_time = self.stats['reset_time'] - now
            logger.warning(f"CryptoPanic rate limit reached, waiting {wait_time/3600:.1f}h")
            return {'error': 'rate_limit', 'message': f'Rate limit reached. Resets in {wait_time/3600:.1f}h'}
        
        params['auth_token'] = api_key
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}/"
        
        self.stats['total_requests'] += 1
        self.stats['remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("CryptoPanic rate limit exceeded")
                        return {'error': 'rate_limit', 'message': 'Rate limit exceeded'}
                    else:
                        logger.warning(f"CryptoPanic returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"CryptoPanic request error: {e}")
            return None
    
    async def get_news(self, filter: str = 'hot', currencies: List[str] = None,
                       limit: int = 50, user_id: int = None) -> List[Dict]:
        """
        دریافت اخبار با فیلتر
        """
        cache_key = f"news_{filter}_{','.join(currencies or [])}_{limit}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        params = {
            'filter': filter,
            'limit': min(limit, 100),
            'kind': 'news'
        }
        
        if currencies:
            params['currencies'] = ','.join(currencies)
        
        result = await self._make_request('posts', params, user_id)
        
        if result and 'results' in result:
            news_items = []
            
            for item in result['results']:
                # تشخیص احساسات
                votes = item.get('votes', {})
                positive = votes.get('positive', 0)
                negative = votes.get('negative', 0)
                total = positive + negative
                
                sentiment = 0.5
                if total > 0:
                    sentiment = positive / total
                
                news_items.append({
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'source': item.get('source', {}).get('title'),
                    'published_at': item.get('published_at'),
                    'currencies': [c['code'] for c in item.get('currencies', [])],
                    'domain': item.get('domain'),
                    'votes': {
                        'positive': positive,
                        'negative': negative,
                        'total': total,
                        'sentiment': sentiment
                    },
                    'sentiment': sentiment,
                    'is_hot': item.get('votes', {}).get('important', 0) > 0
                })
            
            self.cache[cache_key] = (news_items, datetime.now())
            return news_items
        
        return []
    
    async def get_token_news(self, token_symbol: str, user_id: int = None) -> List[Dict]:
        """
        دریافت اخبار مرتبط با یک توکن
        """
        news = await self.get_news('important', [token_symbol], 30, user_id)
        return news
    
    async def get_meme_coin_news(self, user_id: int = None) -> List[Dict]:
        """
        دریافت اخبار میم‌کوین‌ها
        """
        meme_coins = ['DOGE', 'SHIB', 'PEPE', 'BONK', 'WIF', 'FLOKI']
        return await self.get_news('hot', meme_coins, 50, user_id)
    
    async def get_trending_topics(self, user_id: int = None) -> List[Dict]:
        """
        دریافت موضوعات داغ
        """
        news = await self.get_news('hot', limit=100, user_id=user_id)
        
        # آنالیز فراوانی
        from collections import Counter
        topics = []
        currencies_count = Counter()
        
        for item in news:
            for curr in item['currencies']:
                currencies_count[curr] += 1
        
        for curr, count in currencies_count.most_common(10):
            topics.append({
                'currency': curr,
                'mentions': count,
                'sentiment': self._calculate_avg_sentiment(news, curr)
            })
        
        return topics
    
    def _calculate_avg_sentiment(self, news: List[Dict], currency: str) -> float:
        """محاسبه میانگین احساسات برای یک ارز"""
        sentiments = []
        for item in news:
            if currency in item['currencies']:
                sentiments.append(item['sentiment'])
        
        return sum(sentiments) / len(sentiments) if sentiments else 0.5
    
    async def get_market_sentiment(self, user_id: int = None) -> Dict:
        """
        دریافت احساسات کلی بازار
        """
        news = await self.get_news('hot', limit=100, user_id=user_id)
        
        if not news:
            return {'sentiment': 0.5, 'confidence': 0}
        
        sentiments = [n['sentiment'] for n in news]
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        # محاسبه اعتماد
        import numpy as np
        std = np.std(sentiments) if len(sentiments) > 1 else 0
        confidence = 1 - min(std, 0.5) / 0.5
        
        # تشخیص روند
        if avg_sentiment > 0.6:
            trend = "🟢 Bullish"
        elif avg_sentiment < 0.4:
            trend = "🔴 Bearish"
        else:
            trend = "🟡 Neutral"
        
        return {
            'sentiment': avg_sentiment,
            'trend': trend,
            'confidence': confidence,
            'news_volume': len(news),
            'timestamp': datetime.now().isoformat()
        }
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared CryptoPanic key for user {user_id}")

# نمونه‌سازی سراسری
cryptopanic_api = CryptoPanicAPI()
