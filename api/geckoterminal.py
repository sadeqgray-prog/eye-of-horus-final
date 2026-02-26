#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API GeckoTerminal - داده‌های لحظه‌ای DEX
پشتیبانی از: Ethereum, BSC, Polygon, Solana و...
"""

import aiohttp
import asyncio
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class GeckoTerminalAPI:
    """
    API GeckoTerminal - داده‌های لحظه‌ای از DEXها
    """
    
    BASE_URL = "https://api.geckoterminal.com/api/v2"
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 60
    
    async def get_token_info(self, token_address: str, chain: str = "ethereum") -> Optional[Dict]:
        """دریافت اطلاعات توکن"""
        cache_key = f"token_{chain}_{token_address}"
        
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return data
        
        url = f"{self.BASE_URL}/networks/{chain}/tokens/{token_address}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        token_data = data.get('data', {}).get('attributes', {})
                        
                        result = {
                            'address': token_address,
                            'name': token_data.get('name'),
                            'symbol': token_data.get('symbol'),
                            'price': float(token_data.get('price_usd', 0)),
                            'volume_24h': float(token_data.get('volume_usd', {}).get('h24', 0)),
                            'liquidity': float(token_data.get('reserve_in_usd', 0)),
                            'price_change_24h': float(token_data.get('price_change_percentage', {}).get('h24', 0)),
                            'source': 'geckoterminal'
                        }
                        
                        self.cache[cache_key] = (result, datetime.now())
                        return result
        
        except Exception as e:
            logger.error(f"GeckoTerminal error: {e}")
        
        return None

# نمونه‌سازی سراسری
geckoterminal_api = GeckoTerminalAPI()
