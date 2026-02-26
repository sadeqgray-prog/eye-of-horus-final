#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API BSCScan - برای تحلیل توکن‌های BSC (بایننس)
مشابه Etherscan اما برای BSC
"""

import aiohttp
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class BSCScanAPI:
    """
    API BSCScan - نیاز به API Key
    """
    
    BASE_URL = "https://api.bscscan.com/api"
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        self.stats = {
            'total_requests': 0,
            'last_request': None
        }
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ BSCScan API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ BSCScan global API key set")
    
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
            "🔑 **BSCScan API Key Required**\n\n"
            "To analyze BSC tokens, I need your BSCScan API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://bscscan.com/register\n"
            "2. Create an account\n"
            "3. Go to API Keys section\n"
            "4. Create a new API key\n\n"
            "**Send me:** `BSCSCAN: YOUR_API_KEY`\n\n"
            "Example: `BSCSCAN: ABC123XYZ456DEF789`"
        )
    
    async def _make_request(self, params: Dict, user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به BSCScan"""
        
        api_key = self.get_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        params['apikey'] = api_key
        
        self.stats['total_requests'] += 1
        self.stats['last_request'] = datetime.now().isoformat()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('status') == '1':
                            return data.get('result')
                        else:
                            error = data.get('result', 'Unknown error')
                            
                            if 'Invalid API Key' in error:
                                return {'error': 'invalid_api_key', 'message': 'Your API key is invalid'}
                            
                            return {'error': 'api_error', 'message': error}
                    else:
                        logger.warning(f"BSCScan returned {response.status}")
                        return {'error': 'http_error', 'status': response.status}
        
        except Exception as e:
            logger.error(f"BSCScan request error: {e}")
            return {'error': 'request_failed', 'message': str(e)}
    
    async def get_token_info(self, token_address: str, user_id: int = None) -> Optional[Dict]:
        """دریافت اطلاعات توکن"""
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
                'source': 'bscscan'
            }
        
        return None
    
    async def get_token_holders(self, token_address: str, user_id: int = None) -> Dict:
        """دریافت هولدرها"""
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
            return {
                'total_holders': len(result),
                'holders': result[:50],
                'source': 'bscscan'
            }
        
        return {'total_holders': 0, 'holders': []}
    
    async def get_new_tokens(self, start_block: int = None, end_block: int = None,
                              user_id: int = None) -> List[Dict]:
        """
        دریافت توکن‌های جدید BSC
        از contractcreation استفاده می‌کنه
        """
        params = {
            'module': 'contract',
            'action': 'contractcreation',
            'contractaddresses': '',
            'page': 1,
            'offset': 100
        }
        
        result = await self._make_request(params, user_id)
        
        if isinstance(result, dict) and result.get('error'):
            return []
        
        new_tokens = []
        if result:
            for contract in result:
                new_tokens.append({
                    'address': contract.get('contractAddress'),
                    'creator': contract.get('contractCreator'),
                    'tx_hash': contract.get('txHash'),
                    'block': contract.get('blockNumber'),
                    'timestamp': contract.get('timestamp'),
                    'source': 'bscscan'
                })
        
        return new_tokens
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared BSCScan API key for user {user_id}")

# نمونه‌سازی سراسری
bscscan_api = BSCScanAPI()
