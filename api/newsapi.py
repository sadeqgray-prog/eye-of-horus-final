#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API NewsAPI - برای دریافت اخبار مرتبط با میم‌کوین‌ها
نیازمند API Key (رایگان با محدودیت)
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class NewsAPI:
    """
    API NewsAPI - نیاز به API Key
    رایگان: ۱۰۰ درخواست در روز
    """
    
    BASE_URL = "https://newsapi.org/v2"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        self.stats = {
            'total_requests': 0,
            'remaining': 100,
            'reset_time': time.time() + 86400  # ۲۴ ساعت
        }
        
        self.cache = {}
        self.cache_timeout = 600  # ۱۰ دقیقه
        
        logger.info("📰 NewsAPI initialized")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ NewsAPI key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ NewsAPI global key set")
    
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
            "🔑 **NewsAPI Key Required**\n\n"
            "To analyze crypto news, I need your NewsAPI key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://newsapi.org/register\n"
            "2. Create an account\n"
            "3. Copy your API key\n\n"
            "**Send me:** `NEWSAPI: YOUR_API_KEY`\n\n"
            "Example: `NEWSAPI: abc123xyz789`"
        )
    
    async def _make_request(self, endpoint: str, params: Dict,
                           user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به NewsAPI"""
        
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
            logger.warning(f"NewsAPI rate limit reached, waiting {wait_time/3600:.1f}h")
            return {'error': 'rate_limit', 'message': f'Rate limit reached. Resets in {wait_time/3600:.1f}h'}
        
        params['apiKey'] = api_key
        
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        self.stats['total_requests'] += 1
        self.stats['remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("NewsAPI rate limit exceeded")
                        return {'error': 'rate_limit', 'message': 'Rate limit exceeded'}
                    else:
                        logger.warning(f"NewsAPI returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"NewsAPI request error: {e}")
            return None
    
    async def get_crypto_news(self, query: str, page_size: int = 20,
                              user_id: int = None) -> List[Dict]:
        """
        دریافت اخبار مرتبط با کریپتو
        """
        cache_key = f"news_{query}_{page_size}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        # کلمات کلیدی کریپتو
        crypto_keywords = ['cryptocurrency', 'crypto', 'bitcoin', 'ethereum', 'solana', 'memecoin']
        
        full_query = f"({query}) AND ({' OR '.join(crypto_keywords)})"
        
        params = {
            'q': full_query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': min(page_size, 100)
        }
        
        result = await self._make_request('everything', params, user_id)
        
        if result and 'articles' in result:
            articles = []
            from textblob import TextBlob
            
            for article in result['articles']:
                # تحلیل احساسات
                title = article.get('title', '')
                description = article.get('description', '') or ''
                text = f"{title} {description}"
                
                blob = TextBlob(text)
                sentiment = (blob.sentiment.polarity + 1) / 2
                
                articles.append({
                    'title': title,
                    'description': description,
                    'url': article.get('url'),
                    'source': article.get('source', {}).get('name'),
                    'published_at': article.get('publishedAt'),
                    'sentiment': sentiment,
                    'content': article.get('content', '')[:500] if article.get('content') else ''
                })
            
            self.cache[cache_key] = (articles, datetime.now())
            return articles
        
        return []
    
    async def search_token_news(self, token_symbol: str, token_name: str = None,
                                user_id: int = None) -> List[Dict]:
        """
        جستجوی اخبار مرتبط با یک توکن
        """
        queries = [token_symbol]
        if token_name:
            queries.append(token_name)
        
        all_news = []
        for query in queries:
            news = await self.get_crypto_news(query, 20, user_id)
            all_news.extend(news)
            await asyncio.sleep(1)
        
        # حذف تکراری‌ها
        seen = set()
        unique_news = []
        for article in all_news:
            if article['url'] not in seen:
                seen.add(article['url'])
                unique_news.append(article)
        
        return unique_news[:30]
    
    async def get_news_sentiment(self, token_symbol: str, user_id: int = None) -> Dict:
        """
        تحلیل احساسات اخبار مرتبط با یک توکن
        """
        news = await self.search_token_news(token_symbol, user_id=user_id)
        
        if not news:
            return {
                'sentiment': 0.5,
                'volume': 0,
                'trending': False,
                'positive_count': 0,
                'negative_count': 0
            }
        
        sentiments = [a['sentiment'] for a in news]
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        positive = len([s for s in sentiments if s > 0.6])
        negative = len([s for s in sentiments if s < 0.4])
        
        return {
            'sentiment': avg_sentiment,
            'volume': len(news),
            'trending': len(news) > 10,
            'positive_count': positive,
            'negative_count': negative,
            'positive_percentage': (positive / len(news)) * 100,
            'negative_percentage': (negative / len(news)) * 100,
            'recent_news': news[:5]
        }
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared NewsAPI key for user {user_id}")

# نمونه‌سازی سراسری
news_api = NewsAPI()
