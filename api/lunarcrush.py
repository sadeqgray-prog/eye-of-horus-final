#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API LunarCrush - تحلیل اجتماعی پیشرفته
ترکیب داده‌های شبکه‌های اجتماعی و بازار
نیازمند API Key (رایگان با محدودیت)
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class LunarCrushAPI:
    """
    API LunarCrush - تحلیل اجتماعی و بازار
    رایگان: ۲۰۰ درخواست در روز
    """
    
    BASE_URL = "https://lunarcrush.com/api3"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        self.stats = {
            'total_requests': 0,
            'remaining': 200,
            'reset_time': time.time() + 86400
        }
        
        self.cache = {}
        self.cache_timeout = 300  # ۵ دقیقه
        
        logger.info("🌕 LunarCrushAPI initialized")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ LunarCrush API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ LunarCrush global API key set")
    
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
            "🔑 **LunarCrush API Key Required**\n\n"
            "For advanced social analysis, I need your LunarCrush API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://lunarcrush.com/developers\n"
            "2. Sign up and get your API key\n\n"
            "**Send me:** `LUNARCRUSH: YOUR_API_KEY`\n\n"
            "Example: `LUNARCRUSH: abc123xyz789`"
        )
    
    async def _make_request(self, endpoint: str, params: Dict = None,
                           user_id: int = None, method: str = 'GET') -> Optional[Dict]:
        """ساخت درخواست به LunarCrush"""
        
        api_key = self.get_api_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        # Rate limiting
        now = time.time()
        if now > self.stats['reset_time']:
            self.stats['remaining'] = 200
            self.stats['reset_time'] = now + 86400
        
        if self.stats['remaining'] <= 0:
            wait_time = self.stats['reset_time'] - now
            logger.warning(f"LunarCrush rate limit reached, waiting {wait_time/3600:.1f}h")
            return {'error': 'rate_limit', 'message': f'Rate limit reached. Resets in {wait_time/3600:.1f}h'}
        
        headers = {'Authorization': f'Bearer {api_key}'}
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        self.stats['total_requests'] += 1
        self.stats['remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 429:
                            logger.warning("LunarCrush rate limit exceeded")
                            return {'error': 'rate_limit', 'message': 'Rate limit exceeded'}
                        else:
                            logger.warning(f"LunarCrush returned {response.status}")
                            return None
                else:
                    async with session.post(url, json=params, headers=headers) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            return None
        
        except Exception as e:
            logger.error(f"LunarCrush request error: {e}")
            return None
    
    async def get_token_social_stats(self, token_symbol: str, user_id: int = None) -> Optional[Dict]:
        """
        دریافت آمار اجتماعی یک توکن
        """
        cache_key = f"social_{token_symbol}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        params = {'symbol': token_symbol, 'data': 'social' }
        result = await self._make_request('public/coins', params, user_id)
        
        if result and 'data' in result and len(result['data']) > 0:
            data = result['data'][0]
            
            social = {
                'symbol': data.get('s'),
                'name': data.get('n'),
                'price': data.get('p'),
                'price_change_24h': data.get('pc'),
                'market_cap': data.get('mcap'),
                'volume_24h': data.get('v'),
                
                # آمار اجتماعی
                'social_score': data.get('ac'),
                'social_volume': data.get('sv'),
                'social_contributors': data.get('sc'),
                'social_engagement': data.get('se'),
                
                # احساسات
                'sentiment': data.get('sa'),
                'bullish_sentiment': data.get('bull'),
                'bearish_sentiment': data.get('bear'),
                
                # توییتر
                'tweets_24h': data.get('tw'),
                'twitter_followers': data.get('tf'),
                'twitter_followers_growth': data.get('tfg'),
                
                # ردیت
                'reddit_subscribers': data.get('rs'),
                'reddit_active_users': data.get('ra'),
                'reddit_comments': data.get('rc'),
                
                # یوتیوب
                'youtube_subscribers': data.get('ys'),
                'youtube_views': data.get('yv'),
                
                # گالکسی
                'galaxy_score': data.get('gs'),
                'alt_rank': data.get('alt_rank'),
                'volatility': data.get('volatility'),
                
                'updated_at': data.get('updated'),
                'source': 'lunarcrush'
            }
            
            self.cache[cache_key] = (social, datetime.now())
            return social
        
        return None
    
    async def get_market_data(self, token_symbol: str, user_id: int = None) -> Optional[Dict]:
        """
        دریافت داده‌های بازار
        """
        params = {'symbol': token_symbol, 'data': 'market' }
        result = await self._make_request('public/coins', params, user_id)
        
        if result and 'data' in result and len(result['data']) > 0:
            data = result['data'][0]
            return {
                'symbol': data.get('s'),
                'price': data.get('p'),
                'price_btc': data.get('pb'),
                'price_change_24h': data.get('pc'),
                'market_cap': data.get('mcap'),
                'volume_24h': data.get('v'),
                'liquidity': data.get('liq'),
                'high_24h': data.get('high'),
                'low_24h': data.get('low'),
                'supply': data.get('sp'),
                'max_supply': data.get('ms')
            }
        
        return None
    
    async def get_trending_coins(self, user_id: int = None) -> List[Dict]:
        """
        دریافت میم‌کوین‌های داغ
        """
        params = {'sort': 'social_score', 'limit': 20}
        result = await self._make_request('public/coins/list', params, user_id)
        
        trending = []
        if result and 'data' in result:
            for coin in result['data']:
                trending.append({
                    'symbol': coin.get('s'),
                    'name': coin.get('n'),
                    'price': coin.get('p'),
                    'social_score': coin.get('ac'),
                    'social_volume': coin.get('sv'),
                    'sentiment': coin.get('sa'),
                    'alt_rank': coin.get('alt_rank'),
                    'price_change_24h': coin.get('pc')
                })
        
        return trending[:10]
    
    async def get_meme_coins_social(self, user_id: int = None) -> List[Dict]:
        """
        دریافت آمار اجتماعی میم‌کوین‌ها
        """
        meme_coins = ['DOGE', 'SHIB', 'PEPE', 'BONK', 'WIF', 'FLOKI']
        results = []
        
        for coin in meme_coins:
            data = await self.get_token_social_stats(coin, user_id)
            if data:
                results.append(data)
            await asyncio.sleep(1)  # جلوگیری از rate limit
        
        return results
    
    async def analyze_token_potential(self, token_symbol: str, user_id: int = None) -> Dict:
        """
        تحلیل پتانسیل یک توکن با ترکیب داده‌های اجتماعی و بازار
        """
        social = await self.get_token_social_stats(token_symbol, user_id)
        market = await self.get_market_data(token_symbol, user_id)
        
        if not social and not market:
            return {'error': 'Token not found'}
        
        score = 50  # پایه
        
        factors = []
        
        # 1. نمره اجتماعی
        if social and social.get('social_score'):
            social_score = social['social_score'] / 100  # نرمال‌سازی
            score += social_score * 20
            factors.append(("Social Score", social_score))
        
        # 2. احساسات
        if social and social.get('sentiment'):
            sentiment = social['sentiment'] / 100
            score += (sentiment - 0.5) * 30
            factors.append(("Sentiment", sentiment))
        
        # 3. حجم اجتماعی
        if social and social.get('social_volume'):
            volume_score = min(social['social_volume'] / 10000, 1)
            score += volume_score * 15
            factors.append(("Social Volume", volume_score))
        
        # 4. تغییر قیمت
        if market and market.get('price_change_24h'):
            price_change = market['price_change_24h'] / 100
            if price_change > 0:
                score += price_change * 20
            else:
                score += price_change * 10  # تأثیر کمتر برای منفی
            factors.append(("Price Change", price_change))
        
        # 5. رتبه
        if social and social.get('alt_rank'):
            rank_score = 1 - (social['alt_rank'] / 1000)  # رتبه بهتر = نمره بیشتر
            score += rank_score * 15
            factors.append(("Rank", rank_score))
        
        final_score = min(100, max(0, score))
        
        # سطح
        if final_score >= 80:
            level = "🚀 EXCEPTIONAL"
            recommendation = "STRONG BUY"
        elif final_score >= 70:
            level = "📈 VERY GOOD"
            recommendation = "BUY"
        elif final_score >= 60:
            level = "📊 GOOD"
            recommendation = "WATCH"
        elif final_score >= 50:
            level = "⚖️ AVERAGE"
            recommendation = "HOLD"
        else:
            level = "⚠️ WEAK"
            recommendation = "AVOID"
        
        return {
            'symbol': token_symbol,
            'final_score': final_score,
            'level': level,
            'recommendation': recommendation,
            'factors': factors,
            'social_data': social,
            'market_data': market,
            'timestamp': datetime.now().isoformat()
        }
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared LunarCrush key for user {user_id}")

# نمونه‌سازی سراسری
lunarcrush_api = LunarCrushAPI()
