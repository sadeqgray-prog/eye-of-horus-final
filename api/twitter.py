#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API توییتر - برای تحلیل احساسات و روند میم‌کوین‌ها
قابلیت‌ها:
- جستجوی توییت‌های مرتبط با یک توکن
- تحلیل احساسات
- تشخیص ترندها
- ردیابی اینفلوئنسرها
- درخواست API Key از کاربر
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import json
import re
import time

logger = logging.getLogger(__name__)

class TwitterAPI:
    """
    API توییتر - نیاز به API Key
    """
    
    # نسخه‌های مختلف API
    API_V1 = "https://api.twitter.com/1.1"
    API_V2 = "https://api.twitter.com/2"
    
    def __init__(self):
        self.api_key = None
        self.api_secret = None
        self.bearer_token = None
        self.user_keys = {}  # ذخیره کلیدهای موقت کاربران
        
        # آمار
        self.stats = {
            'total_requests': 0,
            'rate_limit_remaining': 450,
            'rate_limit_reset': time.time() + 900,  # 15 دقیقه
            'last_request': None
        }
        
        # کش برای کاهش درخواست
        self.cache = {}
        self.cache_timeout = 300  # ۵ دقیقه
        
        logger.info("🐦 TwitterAPI initialized")
    
    def set_api_key(self, bearer_token: str, user_id: int = None):
        """تنظیم Bearer Token"""
        if user_id:
            self.user_keys[user_id] = bearer_token
            logger.info(f"✅ Twitter API key set for user {user_id}")
        else:
            self.bearer_token = bearer_token
            logger.info("✅ Twitter global API key set")
    
    def has_key(self, user_id: int = None) -> bool:
        """بررسی وجود API Key"""
        if user_id and user_id in self.user_keys:
            return True
        return self.bearer_token is not None
    
    def get_bearer_token(self, user_id: int = None) -> Optional[str]:
        """دریافت Bearer Token مناسب"""
        if user_id and user_id in self.user_keys:
            return self.user_keys[user_id]
        return self.bearer_token
    
    def get_api_request_message(self) -> str:
        """پیام درخواست API Key"""
        return (
            "🔑 **Twitter API Key Required**\n\n"
            "To analyze social sentiment, I need your Twitter Bearer Token.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://developer.twitter.com\n"
            "2. Create a developer account\n"
            "3. Create a Project and App\n"
            "4. Generate Bearer Token\n\n"
            "**Send me:** `TWITTER: YOUR_BEARER_TOKEN`\n\n"
            "Example: `TWITTER: AAAAAAAAAAAAAAAAAAAAAA`"
        )
    
    async def _make_request(self, endpoint: str, params: Dict = None,
                           user_id: int = None, version: str = 'v2') -> Optional[Dict]:
        """ساخت درخواست به Twitter API"""
        
        bearer_token = self.get_bearer_token(user_id)
        if not bearer_token:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        # Rate limiting
        now = time.time()
        if now < self.stats['rate_limit_reset']:
            if self.stats['rate_limit_remaining'] <= 0:
                wait_time = self.stats['rate_limit_reset'] - now
                logger.warning(f"Twitter rate limit reached, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
                self.stats['rate_limit_remaining'] = 450
                self.stats['rate_limit_reset'] = time.time() + 900
        else:
            self.stats['rate_limit_remaining'] = 450
            self.stats['rate_limit_reset'] = time.time() + 900
        
        base_url = self.API_V2 if version == 'v2' else self.API_V1
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }
        
        self.stats['total_requests'] += 1
        self.stats['last_request'] = datetime.now().isoformat()
        self.stats['rate_limit_remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    
                    # بررسی rate limit headers
                    if 'x-rate-limit-remaining' in response.headers:
                        self.stats['rate_limit_remaining'] = int(response.headers['x-rate-limit-remaining'])
                    
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("Twitter rate limit exceeded")
                        reset_time = int(response.headers.get('x-rate-limit-reset', time.time() + 900))
                        wait_time = reset_time - time.time()
                        if wait_time > 0:
                            await asyncio.sleep(wait_time)
                        return await self._make_request(endpoint, params, user_id, version)
                    else:
                        logger.warning(f"Twitter returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"Twitter request error: {e}")
            return None
    
    async def search_tweets(self, query: str, max_results: int = 100,
                           user_id: int = None) -> List[Dict]:
        """
        جستجوی توییت‌ها بر اساس query
        """
        cache_key = f"search_{query}_{max_results}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        params = {
            'query': query,
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,public_metrics,author_id,lang',
            'user.fields': 'name,username,verified,public_metrics',
            'expansions': 'author_id'
        }
        
        result = await self._make_request('tweets/search/recent', params, user_id)
        
        if result and 'data' in result:
            tweets = []
            users = {u['id']: u for u in result.get('includes', {}).get('users', [])}
            
            for tweet in result['data']:
                author = users.get(tweet['author_id'], {})
                
                tweets.append({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'created_at': tweet['created_at'],
                    'author': {
                        'id': author.get('id'),
                        'name': author.get('name'),
                        'username': author.get('username'),
                        'verified': author.get('verified', False),
                        'followers_count': author.get('public_metrics', {}).get('followers_count', 0)
                    },
                    'metrics': tweet.get('public_metrics', {}),
                    'url': f"https://twitter.com/{author.get('username')}/status/{tweet['id']}"
                })
            
            self.cache[cache_key] = (tweets, datetime.now())
            return tweets
        
        return []
    
    async def search_token_tweets(self, token_symbol: str, token_name: str = None,
                                  user_id: int = None) -> List[Dict]:
        """
        جستجوی توییت‌های مرتبط با یک توکن
        """
        # ساخت query هوشمند
        queries = [
            f"${token_symbol}",
            f"#{token_symbol}",
            token_symbol
        ]
        
        if token_name:
            queries.append(token_name)
        
        # اضافه کردن کلمات مرتبط با میم‌کوین
        meme_keywords = ['pump', 'moon', 'gem', '100x', 'next', 'solana', 'eth', 'bsc']
        
        all_tweets = []
        
        for query in queries[:3]:  # حداکثر ۳ query
            for keyword in meme_keywords[:3]:  # حداکثر ۳ کلمه کلیدی
                full_query = f"{query} {keyword} -is:retweet lang:en"
                tweets = await self.search_tweets(full_query, 20, user_id)
                all_tweets.extend(tweets)
                
                if len(all_tweets) >= 100:
                    break
                
                await asyncio.sleep(1)  # جلوگیری از rate limit
            
            if len(all_tweets) >= 100:
                break
        
        # حذف تکراری‌ها
        seen = set()
        unique_tweets = []
        for tweet in all_tweets:
            if tweet['id'] not in seen:
                seen.add(tweet['id'])
                unique_tweets.append(tweet)
        
        return unique_tweets[:100]
    
    async def get_tweet_sentiment(self, token_symbol: str, user_id: int = None) -> Dict:
        """
        تحلیل احساسات توییت‌های مرتبط با یک توکن
        """
        tweets = await self.search_token_tweets(token_symbol, user_id=user_id)
        
        if not tweets:
            return {
                'sentiment': 0.5,
                'volume': 0,
                'trending': False,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0
            }
        
        # تحلیل احساسات
        from textblob import TextBlob
        
        sentiments = []
        positive = 0
        negative = 0
        neutral = 0
        
        for tweet in tweets:
            blob = TextBlob(tweet['text'])
            polarity = blob.sentiment.polarity
            
            sentiments.append(polarity)
            
            if polarity > 0.1:
                positive += 1
            elif polarity < -0.1:
                negative += 1
            else:
                neutral += 1
        
        avg_sentiment = (sum(sentiments) / len(sentiments) + 1) / 2  # تبدیل به ۰-۱
        
        # تشخیص ترند
        trending = len(tweets) > 20 and avg_sentiment > 0.6
        
        return {
            'sentiment': avg_sentiment,
            'volume': len(tweets),
            'trending': trending,
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'positive_percentage': (positive / len(tweets)) * 100,
            'negative_percentage': (negative / len(tweets)) * 100,
            'neutral_percentage': (neutral / len(tweets)) * 100
        }
    
    async def get_influencer_mentions(self, token_symbol: str, min_followers: int = 10000,
                                      user_id: int = None) -> List[Dict]:
        """
        دریافت توییت‌های اینفلوئنسرها درباره یک توکن
        """
        tweets = await self.search_token_tweets(token_symbol, user_id)
        
        influencers = []
        for tweet in tweets:
            followers = tweet['author'].get('followers_count', 0)
            if followers >= min_followers:
                influencers.append({
                    'username': tweet['author']['username'],
                    'name': tweet['author']['name'],
                    'followers': followers,
                    'verified': tweet['author']['verified'],
                    'tweet': tweet['text'][:200],
                    'tweet_url': tweet['url'],
                    'created_at': tweet['created_at']
                })
        
        return sorted(influencers, key=lambda x: x['followers'], reverse=True)
    
    async def get_trending_topics(self, user_id: int = None) -> List[Dict]:
        """
        دریافت ترندهای لحظه‌ای توییتر
        """
        # این API نیاز به access level بالاتری داره
        # فعلاً از روش جایگزین استفاده می‌کنیم
        
        # جستجوی ترندهای کریپتو
        crypto_keywords = ['bitcoin', 'ethereum', 'solana', 'crypto', 'memecoin', 'pump']
        
        trends = []
        for keyword in crypto_keywords:
            tweets = await self.search_tweets(keyword, 10, user_id)
            if tweets:
                trends.append({
                    'topic': keyword,
                    'volume': len(tweets),
                    'recent_tweet': tweets[0]['text'][:100] if tweets else ''
                })
            await asyncio.sleep(1)
        
        return sorted(trends, key=lambda x: x['volume'], reverse=True)
    
    async def get_token_buzz(self, token_symbol: str, minutes: int = 60,
                             user_id: int = None) -> Dict:
        """
        میزان بحث درباره یک توکن در زمان مشخص
        """
        tweets = await self.search_token_tweets(token_symbol, user_id)
        
        # فیلتر بر اساس زمان
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent_tweets = []
        
        for tweet in tweets:
            tweet_time = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
            if tweet_time > cutoff:
                recent_tweets.append(tweet)
        
        # محاسبه نرخ
        tweets_per_minute = len(recent_tweets) / minutes if minutes > 0 else 0
        
        return {
            'total_mentions': len(recent_tweets),
            'tweets_per_minute': round(tweets_per_minute, 2),
            'unique_authors': len(set(t['author']['id'] for t in recent_tweets)),
            'avg_likes': sum(t['metrics'].get('like_count', 0) for t in recent_tweets) / len(recent_tweets) if recent_tweets else 0,
            'avg_retweets': sum(t['metrics'].get('retweet_count', 0) for t in recent_tweets) / len(recent_tweets) if recent_tweets else 0,
            'buzz_level': 'HIGH' if tweets_per_minute > 10 else 'MEDIUM' if tweets_per_minute > 5 else 'LOW'
        }
    
    async def monitor_token(self, token_symbol: str, callback: Callable = None,
                           interval: int = 60, user_id: int = None):
        """
        مانیتورینگ مداوم یک توکن
        """
        logger.info(f"👀 Starting monitor for ${token_symbol}")
        
        last_mentions = 0
        
        while True:
            try:
                buzz = await self.get_token_buzz(token_symbol, minutes=5, user_id=user_id)
                
                # اگه افزایش ناگهانی داشت
                if buzz['tweets_per_minute'] > last_mentions * 1.5 and last_mentions > 0:
                    logger.info(f"📈 Spike detected for ${token_symbol}: {buzz['tweets_per_minute']} tweets/min")
                    
                    if callback:
                        await callback({
                            'token': token_symbol,
                            'event': 'volume_spike',
                            'current': buzz['tweets_per_minute'],
                            'previous': last_mentions,
                            'increase': ((buzz['tweets_per_minute'] - last_mentions) / last_mentions) * 100,
                            'timestamp': datetime.now().isoformat()
                        })
                
                last_mentions = buzz['tweets_per_minute']
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(interval * 2)
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_keys:
            del self.user_keys[user_id]
            logger.info(f"🗑️ Cleared Twitter API key for user {user_id}")

# نمونه‌سازی سراسری
twitter_api = TwitterAPI()
