#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API ردیت - برای تحلیل احساسات در ساب‌ردیت‌های کریپتو
پشتیبانی از:
- r/CryptoCurrency
- r/Solana
- r/Ethereum
- r/memecoins
- و بقیه
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncpraw
import time

logger = logging.getLogger(__name__)

class RedditAPI:
    """
    API ردیت - نیاز به API Key
    """
    
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.user_agent = "UltimateOracleBot/1.0"
        self.reddit = None
        self.user_keys = {}
        
        # آمار
        self.stats = {
            'total_requests': 0,
            'last_request': None
        }
        
        # کش
        self.cache = {}
        self.cache_timeout = 300
        
        # ساب‌ردیت‌های مرتبط با کریپتو
        self.crypto_subs = [
            'CryptoCurrency',
            'CryptoMarkets',
            'Solana',
            'Ethereum',
            'Bitcoin',
            'memecoins',
            'SatoshiStreetBets',
            'CryptoMoonShots',
            'Altcoin',
            'Crypto_General'
        ]
        
        logger.info("👽 RedditAPI initialized")
    
    def set_credentials(self, client_id: str, client_secret: str, user_id: int = None):
        """تنظیم credentials"""
        if user_id:
            self.user_keys[user_id] = {
                'client_id': client_id,
                'client_secret': client_secret
            }
            logger.info(f"✅ Reddit credentials set for user {user_id}")
        else:
            self.client_id = client_id
            self.client_secret = client_secret
            logger.info("✅ Reddit global credentials set")
    
    def has_credentials(self, user_id: int = None) -> bool:
        """بررسی وجود credentials"""
        if user_id and user_id in self.user_keys:
            return True
        return self.client_id is not None and self.client_secret is not None
    
    def get_credentials(self, user_id: int = None) -> Optional[Dict]:
        """دریافت credentials مناسب"""
        if user_id and user_id in self.user_keys:
            return self.user_keys[user_id]
        return {'client_id': self.client_id, 'client_secret': self.client_secret}
    
    def get_api_request_message(self) -> str:
        """پیام درخواست API Key"""
        return (
            "🔑 **Reddit API Key Required**\n\n"
            "To analyze Reddit sentiment, I need your Reddit API credentials.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://www.reddit.com/prefs/apps\n"
            "2. Click 'create app'\n"
            "3. Get client_id and client_secret\n\n"
            "**Send me:** `REDDIT: CLIENT_ID:CLIENT_SECRET`\n\n"
            "Example: `REDDIT: abc123:xyz789`"
        )
    
    async def _get_reddit(self, user_id: int = None):
        """دریافت instance ردیت"""
        if self.reddit and not user_id:
            return self.reddit
        
        creds = self.get_credentials(user_id)
        if not creds:
            return None
        
        try:
            reddit = asyncpraw.Reddit(
                client_id=creds['client_id'],
                client_secret=creds['client_secret'],
                user_agent=self.user_agent
            )
            
            if not user_id:
                self.reddit = reddit
            
            return reddit
            
        except Exception as e:
            logger.error(f"Reddit auth error: {e}")
            return None
    
    async def search_subreddit(self, subreddit: str, query: str, limit: int = 50,
                               user_id: int = None) -> List[Dict]:
        """
        جستجو در یک ساب‌ردیت
        """
        cache_key = f"search_{subreddit}_{query}_{limit}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        reddit = await self._get_reddit(user_id)
        if not reddit:
            return []
        
        try:
            sub = await reddit.subreddit(subreddit)
            posts = []
            
            async for post in sub.search(query, limit=limit):
                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'text': post.selftext[:500] if post.selftext else '',
                    'url': post.url,
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc).isoformat(),
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': subreddit
                })
            
            self.cache[cache_key] = (posts, datetime.now())
            return posts
            
        except Exception as e:
            logger.error(f"Reddit search error: {e}")
            return []
    
    async def search_all_crypto(self, query: str, limit_per_sub: int = 20,
                                user_id: int = None) -> List[Dict]:
        """
        جستجو در همه ساب‌ردیت‌های کریپتو
        """
        all_posts = []
        
        for sub in self.crypto_subs:
            posts = await self.search_subreddit(sub, query, limit_per_sub, user_id)
            all_posts.extend(posts)
            await asyncio.sleep(1)  # جلوگیری از rate limit
        
        # مرتب‌سازی بر اساس امتیاز
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        
        return all_posts
    
    async def search_token(self, token_symbol: str, token_name: str = None,
                          user_id: int = None) -> List[Dict]:
        """
        جستجوی پست‌های مرتبط با یک توکن
        """
        queries = [f"${token_symbol}", token_symbol]
        if token_name:
            queries.append(token_name)
        
        all_posts = []
        for query in queries:
            posts = await self.search_all_crypto(query, 20, user_id)
            all_posts.extend(posts)
        
        # حذف تکراری‌ها
        seen = set()
        unique_posts = []
        for post in all_posts:
            if post['id'] not in seen:
                seen.add(post['id'])
                unique_posts.append(post)
        
        return unique_posts[:100]
    
    async def get_subreddit_sentiment(self, token_symbol: str, user_id: int = None) -> Dict:
        """
        تحلیل احساسات در ردیت
        """
        posts = await self.search_token(token_symbol, user_id=user_id)
        
        if not posts:
            return {
                'sentiment': 0.5,
                'volume': 0,
                'avg_score': 0,
                'avg_comments': 0,
                'trending': False
            }
        
        from textblob import TextBlob
        
        sentiments = []
        total_score = 0
        total_comments = 0
        
        for post in posts:
            text = f"{post['title']} {post['text']}"
            blob = TextBlob(text)
            sentiments.append(blob.sentiment.polarity)
            
            total_score += post['score']
            total_comments += post['num_comments']
        
        avg_sentiment = (sum(sentiments) / len(sentiments) + 1) / 2
        avg_score = total_score / len(posts)
        avg_comments = total_comments / len(posts)
        
        # تشخیص ترند
        trending = avg_score > 50 and avg_comments > 20 and avg_sentiment > 0.6
        
        return {
            'sentiment': avg_sentiment,
            'volume': len(posts),
            'avg_score': avg_score,
            'avg_comments': avg_comments,
            'trending': trending,
            'positive_ratio': len([s for s in sentiments if s > 0.1]) / len(sentiments),
            'negative_ratio': len([s for s in sentiments if s < -0.1]) / len(sentiments)
        }
    
    async def get_hot_posts(self, subreddit: str = 'CryptoCurrency', limit: int = 25,
                            user_id: int = None) -> List[Dict]:
        """
        دریافت پست‌های داغ یک ساب‌ردیت
        """
        cache_key = f"hot_{subreddit}_{limit}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < 60:  # ۱ دقیقه کش
                return data
        
        reddit = await self._get_reddit(user_id)
        if not reddit:
            return []
        
        try:
            sub = await reddit.subreddit(subreddit)
            posts = []
            
            async for post in sub.hot(limit=limit):
                posts.append({
                    'id': post.id,
                    'title': post.title,
                    'url': post.url,
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc).isoformat(),
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': subreddit
                })
            
            self.cache[cache_key] = (posts, datetime.now())
            return posts
            
        except Exception as e:
            logger.error(f"Error getting hot posts: {e}")
            return []
    
    async def get_trending_tokens(self, user_id: int = None) -> List[Dict]:
        """
        تشخیص توکن‌های داغ در ردیت
        """
        # دریافت پست‌های داغ از ساب‌ردیت‌های مختلف
        all_posts = []
        for sub in self.crypto_subs[:5]:  # ۵ ساب‌ردیت اول
            posts = await self.get_hot_posts(sub, 20, user_id)
            all_posts.extend(posts)
            await asyncio.sleep(1)
        
        # استخراج نمادها از تایتل‌ها
        import re
        
        token_pattern = r'\$([A-Z]{2,10})|\b([A-Z]{2,10})\b'
        token_counts = {}
        
        for post in all_posts:
            matches = re.findall(token_pattern, post['title'])
            for match in matches:
                symbol = match[0] or match[1]
                if symbol and len(symbol) <= 10 and symbol not in ['THE', 'AND', 'FOR', 'WITH']:
                    token_counts[symbol] = token_counts.get(symbol, 0) + post['score']
        
        # مرتب‌سازی
        trending = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return [{'symbol': s, 'score': sc} for s, sc in trending]
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_keys:
            del self.user_keys[user_id]
            logger.info(f"🗑️ Cleared Reddit credentials for user {user_id}")

# نمونه‌سازی سراسری
reddit_api = RedditAPI()
