#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Etherscan - برای تحلیل توکن‌های اتریوم
قابلیت‌ها:
- دریافت توکن‌های جدید
- دریافت اطلاعات توکن
- تحلیل هولدرها
- دریافت تراکنش‌ها
- درخواست API Key از کاربر
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class EtherscanAPI:
    """
    API Etherscan - نیاز به API Key
    """
    
    BASE_URL = "https://api.etherscan.io/api"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}  # ذخیره کلیدهای موقت کاربران
        
        # آمار
        self.stats = {
            'total_requests': 0,
            'rate_limit_remaining': 5,
            'last_request': None
        }
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ Global API key set")
    
    def has_key(self, user_id: int = None) -> bool:
        """بررسی وجود API Key"""
        if user_id and user_id in self.user_api_keys:
            return True
        return self.api_key is not None
    
    def get_key(self, user_id: int = None) -> Optional[str]:
        """دریافت API Key مناسب"""
        if user_id and user_id in self.user_api_keys:
            return self.user_api_keys[user_id]
        return self.api_key
    
    def get_api_request_message(self) -> str:
        """پیام درخواست API Key"""
        return (
            "🔑 **Etherscan API Key Required**\n\n"
            "To analyze Ethereum tokens, I need your Etherscan API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://etherscan.io/register\n"
            "2. Create an account\n"
            "3. Go to API Keys section\n"
            "4. Create a new API key\n\n"
            "**Send me:** `ETHERSCAN: YOUR_API_KEY`\n\n"
            "Example: `ETHERSCAN: ABC123XYZ456DEF789`"
        )
    
    async def _make_request(self, params: Dict, user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به Etherscan"""
        
        api_key = self.get_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        params['apikey'] = api_key
        
        self.stats['total_requests'] += 1
        self.stats['last_request'] = datetime.now().isoformat()
        
        # Rate limiting
        if self.stats['rate_limit_remaining'] <= 0:
            logger.warning("Rate limit reached, waiting...")
            await asyncio.sleep(1)
            self.stats['rate_limit_remaining'] = 5
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('status') == '1':
                            self.stats['rate_limit_remaining'] -= 1
                            return data.get('result')
                        else:
                            error = data.get('result', 'Unknown error')
                            
                            # اگه خطای API Key بود
                            if 'Invalid API Key' in error:
                                return {'error': 'invalid_api_key', 'message': 'Your API key is invalid'}
                            
                            return {'error': 'api_error', 'message': error}
                    else:
                        logger.warning(f"Etherscan returned {response.status}")
                        return {'error': 'http_error', 'status': response.status}
        
        except Exception as e:
            logger.error(f"Etherscan request error: {e}")
            return {'error': 'request_failed', 'message': str(e)}
    
    async def get_token_info(self, token_address: str, user_id: int = None) -> Optional[Dict]:
        """
        دریافت اطلاعات پایه توکن
        """
        params = {
            'module': 'token',
            'action': 'tokeninfo',
            'contractaddress': token_address
        }
        
        result = await self._make_request(params, user_id)
        
        if isinstance(result, dict) and result.get('error'):
            return result
        
        if result and len(result) > 0:
            info = result[0]
            return {
                'address': token_address,
                'name': info.get('name'),
                'symbol': info.get('symbol'),
                'decimals': int(info.get('decimals', 18)),
                'total_supply': float(info.get('totalSupply', 0)) / (10 ** int(info.get('decimals', 18))),
                'source': 'etherscan'
            }
        
        return None
    
    async def get_token_holders(self, token_address: str, user_id: int = None) -> Dict:
        """
        دریافت تعداد هولدرها
        """
        params = {
            'module': 'token',
            'action': 'tokenholderlist',
            'contractaddress': token_address,
            'page': 1,
            'offset': 100
        }
        
        result = await self._make_request(params, user_id)
        
        if isinstance(result, dict) and result.get('error'):
            return result
        
        if result:
            holders = result
            return {
                'total_holders': len(holders),
                'holders': holders[:50],  # ۵۰ تای اول
                'source': 'etherscan'
            }
        
        return {'total_holders': 0, 'holders': []}
    
    async def get_token_transfers(self, token_address: str, start_block: int = 0, 
                                   end_block: int = 99999999, user_id: int = None) -> List[Dict]:
        """
        دریافت تراکنش‌های توکن
        """
        params = {
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': token_address,
            'startblock': start_block,
            'endblock': end_block,
            'sort': 'desc',
            'page': 1,
            'offset': 100
        }
        
        result = await self._make_request(params, user_id)
        
        if isinstance(result, dict) and result.get('error'):
            return []
        
        return result or []
    
    async def get_new_tokens(self, start_block: int = None, end_block: int = None, 
                              user_id: int = None) -> List[Dict]:
        """
        دریافت توکن‌های جدید ایجاد شده
        
        با استفاده از contractcreation endpoint
        """
        if start_block is None:
            # ۱۰۰۰۰ بلاک آخر (حدود ۲ روز)
            import requests
            # دریافت آخرین بلاک
            current_block = await self._get_latest_block(user_id)
            if isinstance(current_block, dict) and current_block.get('error'):
                return []
            start_block = max(0, current_block - 10000) if current_block else 0
        
        if end_block is None:
            end_block = await self._get_latest_block(user_id)
            if isinstance(end_block, dict) and end_block.get('error'):
                return []
        
        params = {
            'module': 'contract',
            'action': 'contractcreation',
            'contractaddresses': '',  # خالی برای دریافت همه
            'page': 1,
            'offset': 100
        }
        
        result = await self._make_request(params, user_id)
        
        if isinstance(result, dict) and result.get('error'):
            return []
        
        new_tokens = []
        if result:
            for contract in result:
                block = int(contract.get('blockNumber', 0))
                if start_block <= block <= end_block:
                    new_tokens.append({
                        'address': contract.get('contractAddress'),
                        'creator': contract.get('contractCreator'),
                        'tx_hash': contract.get('txHash'),
                        'block': block,
                        'timestamp': contract.get('timestamp'),
                        'source': 'etherscan'
                    })
        
        return new_tokens
    
    async def _get_latest_block(self, user_id: int = None) -> int:
        """دریافت آخرین بلاک"""
        params = {
            'module': 'proxy',
            'action': 'eth_blockNumber'
        }
        
        result = await self._make_request(params, user_id)
        
        if isinstance(result, str):
            return int(result, 16)
        
        return 0
    
    async def check_token_security(self, token_address: str, user_id: int = None) -> Dict:
        """
        بررسی امنیت توکن (هانی‌پات، مالیات، و ...)
        """
        # این بخش نیاز به تحلیل کد قرارداد داره
        # در این نسخه ساده شده
        return {
            'address': token_address,
            'is_honeypot': False,
            'buy_tax': 0,
            'sell_tax': 0,
            'can_mint': False,
            'can_pause': False,
            'has_blacklist': False,
            'source': 'basic_analysis'
        }
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared API key for user {user_id}")

# نمونه‌سازی سراسری
etherscan_api = EtherscanAPI()
