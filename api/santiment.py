#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Santiment - داده‌های On-Chain و تحلیل پیشرفته
نیازمند API Key (رایگان با محدودیت)
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class SantimentAPI:
    """
    API Santiment - تحلیل On-Chain
    رایگان: ۱۰۰۰ درخواست در روز
    """
    
    BASE_URL = "https://api.santiment.net/graphql"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        self.stats = {
            'total_requests': 0,
            'remaining': 1000,
            'reset_time': time.time() + 86400
        }
        
        self.cache = {}
        self.cache_timeout = 600  # ۱۰ دقیقه
        
        logger.info("📊 SantimentAPI initialized")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ Santiment API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ Santiment global API key set")
    
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
            "🔑 **Santiment API Key Required**\n\n"
            "For on-chain data analysis, I need your Santiment API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://app.santiment.net/account\n"
            "2. Generate API key\n\n"
            "**Send me:** `SANTIMENT: YOUR_API_KEY`\n\n"
            "Example: `SANTIMENT: abc123xyz789`"
        )
    
    async def _make_graphql_request(self, query: str, user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست GraphQL"""
        
        api_key = self.get_api_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        # Rate limiting
        now = time.time()
        if now > self.stats['reset_time']:
            self.stats['remaining'] = 1000
            self.stats['reset_time'] = now + 86400
        
        if self.stats['remaining'] <= 0:
            wait_time = self.stats['reset_time'] - now
            logger.warning(f"Santiment rate limit reached, waiting {wait_time/3600:.1f}h")
            return {'error': 'rate_limit', 'message': f'Rate limit reached. Resets in {wait_time/3600:.1f}h'}
        
        headers = {'Authorization': f'Bearer {api_key}'}
        payload = {'query': query}
        
        self.stats['total_requests'] += 1
        self.stats['remaining'] -= 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.BASE_URL, json=payload, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("Santiment rate limit exceeded")
                        return {'error': 'rate_limit', 'message': 'Rate limit exceeded'}
                    else:
                        logger.warning(f"Santiment returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"Santiment request error: {e}")
            return None
    
    async def get_dev_activity(self, token_slug: str, days: int = 30,
                               user_id: int = None) -> Optional[Dict]:
        """
        دریافت فعالیت توسعه‌دهندگان
        """
        query = f"""
        {{
          developerActivity(slug: "{token_slug}", from: "utc_now-{days}d", interval: "1d") {{
            datetime
            activity
          }}
        }}
        """
        
        result = await self._make_graphql_request(query, user_id)
        
        if result and 'data' in result:
            return {
                'activity': result['data']['developerActivity'],
                'total': sum(d['activity'] for d in result['data']['developerActivity']),
                'average': sum(d['activity'] for d in result['data']['developerActivity']) / days
            }
        
        return None
    
    async def get_social_volume(self, token_slug: str, days: int = 7,
                                user_id: int = None) -> Optional[Dict]:
        """
        دریافت حجم مباحث اجتماعی
        """
        query = f"""
        {{
          socialVolume(slug: "{token_slug}", from: "utc_now-{days}d", interval: "1d") {{
            datetime
            mentionsCount
          }}
        }}
        """
        
        result = await self._make_graphql_request(query, user_id)
        
        if result and 'data' in result:
            mentions = [m['mentionsCount'] for m in result['data']['socialVolume']]
            return {
                'mentions': result['data']['socialVolume'],
                'total_mentions': sum(mentions),
                'avg_mentions': sum(mentions) / len(mentions) if mentions else 0
            }
        
        return None
    
    async def get_exchange_flow(self, token_slug: str, days: int = 7,
                                user_id: int = None) -> Optional[Dict]:
        """
        دریافت جریان ورود/خروج از صرافی‌ها
        """
        query = f"""
        {{
          exchangeFundFlow(slug: "{token_slug}", from: "utc_now-{days}d", interval: "1d") {{
            datetime
            inOutDiff
            inOutDiffPercent
          }}
        }}
        """
        
        result = await self._make_graphql_request(query, user_id)
        
        if result and 'data' in result:
            flows = result['data']['exchangeFundFlow']
            net_flow = sum(f['inOutDiff'] for f in flows)
            
            return {
                'flows': flows,
                'net_flow': net_flow,
                'is_accumulation': net_flow < 0  # منفی = خارج شدن = نگهداری
            }
        
        return None
    
    async def get_whale_transactions(self, token_slug: str, days: int = 1,
                                      user_id: int = None) -> Optional[Dict]:
        """
        دریافت تراکنش‌های بزرگ
        """
        query = f"""
        {{
          whaleTransactions(slug: "{token_slug}", from: "utc_now-{days}d") {{
            datetime
            fromAddress
            toAddress
            transactionCount
            volume
          }}
        }}
        """
        
        result = await self._make_graphql_request(query, user_id)
        
        if result and 'data' in result:
            txs = result['data']['whaleTransactions']
            return {
                'count': len(txs),
                'total_volume': sum(t['volume'] for t in txs),
                'transactions': txs
            }
        
        return None
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared Santiment key for user {user_id}")

# نمونه‌سازی سراسری
santiment_api = SantimentAPI()
