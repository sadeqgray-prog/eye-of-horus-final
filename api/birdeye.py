#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API BirdEye - ردیاب هوشمند نهنگ‌ها و پرسودترین ولت‌ها
پشتیبانی از: Solana, Ethereum, BSC, Polygon, Arbitrum, Base, Sui
قابلیت‌ها:
- شناسایی خودکار ولت‌های پرسود (Smart Money)
- ردیابی لحظه‌ای خرید/فروش نهنگ‌ها
- تحلیل PnL ولت‌ها
- کشف الگوهای معاملاتی
- تشخیص زودهنگام پامپ
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import time
import json
import hashlib

logger = logging.getLogger(__name__)

class BirdEyeAPI:
    """
    API BirdEye - قدرتمندترین ابزار ردیابی نهنگ‌ها
    مستندات: https://docs.birdeye.so/reference
    """
    
    BASE_URL = "https://public-api.birdeye.so"
    
    # زنجیره‌های پشتیبانی شده
    SUPPORTED_CHAINS = {
        'solana': 'solana',
        'ethereum': 'ethereum',
        'bsc': 'bsc',
        'polygon': 'polygon',
        'arbitrum': 'arbitrum',
        'base': 'base',
        'sui': 'sui',
        'avalanche': 'avalanche',
        'fantom': 'fantom',
        'cronos': 'cronos'
    }
    
    def __init__(self):
        self.api_key = None
        self.user_api_keys = {}
        
        # حافظه نهنگ‌ها و ولت‌های پرسود
        self.profitable_wallets = {}  # آدرس ولت -> اطلاعات
        self.whale_wallets = set()     # آدرس ولت‌های نهنگ
        self.smart_money_wallets = []  # لیست ولت‌های پرسود
        
        # کش
        self.cache = {}
        self.cache_timeout = 60  # ۱ دقیقه
        
        # آمار
        self.stats = {
            'total_requests': 0,
            'wallets_tracked': 0,
            'profitable_wallets_found': 0,
            'whale_movements_detected': 0
        }
        
        logger.info("🐋 BirdEyeAPI initialized - Ready to track whales and smart money")
    
    def set_api_key(self, api_key: str, user_id: int = None):
        """تنظیم API Key"""
        if user_id:
            self.user_api_keys[user_id] = api_key
            logger.info(f"✅ BirdEye API key set for user {user_id}")
        else:
            self.api_key = api_key
            logger.info("✅ BirdEye global API key set")
    
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
            "🐋 **BirdEye API Key Required**\n\n"
            "To track whales and profitable wallets, I need your BirdEye API key.\n\n"
            "**Get it for free:**\n"
            "1. Go to https://docs.birdeye.so/reference\n"
            "2. Sign up and get your API key\n\n"
            "**Send me:** `BIRDEYE: YOUR_API_KEY`\n\n"
            "Example: `BIRDEYE: abc123xyz789`"
        )
    
    async def _make_request(self, endpoint: str, params: Dict = None,
                           chain: str = 'solana', user_id: int = None) -> Optional[Dict]:
        """ساخت درخواست به BirdEye API"""
        
        api_key = self.get_api_key(user_id)
        if not api_key:
            return {'error': 'api_key_needed', 'message': self.get_api_request_message()}
        
        headers = {
            'X-API-KEY': api_key,
            'x-chain': chain,
            'accept': 'application/json'
        }
        
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        self.stats['total_requests'] += 1
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        logger.warning("BirdEye rate limit exceeded")
                        await asyncio.sleep(60)
                        return await self._make_request(endpoint, params, chain, user_id)
                    else:
                        logger.warning(f"BirdEye returned {response.status}")
                        return None
        
        except Exception as e:
            logger.error(f"BirdEye request error: {e}")
            return None
    
    # ==================== API‌های قیمت ====================
    
    async def get_token_price(self, token_address: str, chain: str = 'solana',
                             include_liquidity: bool = True, user_id: int = None) -> Optional[Dict]:
        """
        دریافت قیمت لحظه‌ای توکن
        """
        cache_key = f"price_{chain}_{token_address}"
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < 30:  # ۳۰ ثانیه کش
                return data
        
        params = {
            'address': token_address,
            'include_liquidity': 'true' if include_liquidity else 'false'
        }
        
        result = await self._make_request('defi/price', params, chain, user_id)
        
        if result and result.get('success'):
            data = result.get('data', {})
            price_data = {
                'price': data.get('value'),
                'price_change_24h': data.get('price24hChange'),
                'liquidity': data.get('liquidity'),
                'source': 'birdeye'
            }
            self.cache[cache_key] = (price_data, datetime.now())
            return price_data
        
        return None
    
    async def get_multiple_prices(self, token_addresses: List[str], chain: str = 'solana',
                                  user_id: int = None) -> Dict[str, float]:
        """
        دریافت قیمت چند توکن به صورت همزمان
        """
        addresses = ','.join(token_addresses[:100])  # حداکثر ۱۰۰ توکن
        params = {'list_address': addresses}
        
        result = await self._make_request('defi/multi_price', params, chain, user_id)
        
        prices = {}
        if result and result.get('success'):
            data = result.get('data', {})
            for addr, price_data in data.items():
                prices[addr] = price_data.get('value', 0)
        
        return prices
    
    async def get_price_history(self, token_address: str, chain: str = 'solana',
                               time_from: int = None, time_to: int = None,
                               interval: str = '1h', user_id: int = None) -> List[Dict]:
        """
        دریافت تاریخچه قیمت
        interval: 1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 8H, 12H, 1D, 3D, 1W, 1M
        """
        if not time_to:
            time_to = int(time.time())
        if not time_from:
            time_from = time_to - 86400  # ۲۴ ساعت پیش
        
        params = {
            'address': token_address,
            'address_type': 'token',
            'type': interval,
            'time_from': time_from,
            'time_to': time_to
        }
        
        result = await self._make_request('defi/history_price', params, chain, user_id)
        
        prices = []
        if result and result.get('success'):
            data = result.get('data', {}).get('items', [])
            for item in data:
                prices.append({
                    'timestamp': item[0],
                    'price': item[1]
                })
        
        return prices
    
    # ==================== API‌های توکن ====================
    
    async def get_token_list(self, chain: str = 'solana', sort_by: str = 'v24hUSD',
                            limit: int = 50, offset: int = 0, user_id: int = None) -> List[Dict]:
        """
        دریافت لیست توکن‌ها با مرتب‌سازی
        sort_by: v24hUSD (حجم), mc (مارکت‌کپ), price (قیمت)
        """
        params = {
            'sort_by': sort_by,
            'sort_type': 'desc',
            'offset': offset,
            'limit': min(limit, 50)
        }
        
        result = await self._make_request('defi/tokenlist', params, chain, user_id)
        
        tokens = []
        if result and result.get('success'):
            data = result.get('data', [])
            for token in data:
                tokens.append({
                    'address': token.get('address'),
                    'symbol': token.get('symbol'),
                    'name': token.get('name'),
                    'price': token.get('price'),
                    'volume_24h': token.get('volume24h'),
                    'price_change_24h': token.get('priceChange24h'),
                    'market_cap': token.get('marketCap'),
                    'liquidity': token.get('liquidity'),
                    'holder': token.get('holder'),
                    'decimals': token.get('decimals'),
                    'last_trade': token.get('lastTradeAt')
                })
        
        return tokens
    
    async def get_token_overview(self, token_address: str, chain: str = 'solana',
                                user_id: int = None) -> Optional[Dict]:
        """
        دریافت نمای کلی توکن
        """
        result = await self._make_request(f'defi/token_overview', 
                                         {'address': token_address}, chain, user_id)
        
        if result and result.get('success'):
            data = result.get('data', {})
            return {
                'address': token_address,
                'symbol': data.get('symbol'),
                'name': data.get('name'),
                'decimals': data.get('decimals'),
                'price': data.get('price'),
                'price_change_24h': data.get('priceChange24h'),
                'volume_24h': data.get('volume24h'),
                'liquidity': data.get('liquidity'),
                'market_cap': data.get('marketCap'),
                'holder': data.get('holder'),
                'holder_change_24h': data.get('holderChange24h'),
                'supply': data.get('supply'),
                'unique_wallet_24h': data.get('uniqueWallet24h'),
                'creation_time': data.get('createAt'),
                'extensions': data.get('extensions', {})
            }
        
        return None
    
    # ==================== API‌های ولت ====================
    
    async def get_wallet_portfolio(self, wallet_address: str, chain: str = 'solana',
                                   user_id: int = None) -> Optional[Dict]:
        """
        دریافت پرتفوی یک ولت
        """
        result = await self._make_request(f'wallet/token_list', 
                                         {'wallet': wallet_address}, chain, user_id)
        
        if result and result.get('success'):
            data = result.get('data', [])
            
            portfolio = []
            total_value = 0
            
            for item in data:
                value = item.get('valueUsd', 0)
                total_value += value
                
                portfolio.append({
                    'address': item.get('address'),
                    'symbol': item.get('symbol'),
                    'name': item.get('name'),
                    'balance': item.get('balance'),
                    'balance_usd': value,
                    'price': item.get('priceUsd'),
                    'logo': item.get('logoURI')
                })
            
            return {
                'wallet': wallet_address,
                'total_value_usd': total_value,
                'token_count': len(portfolio),
                'tokens': sorted(portfolio, key=lambda x: x['balance_usd'], reverse=True)
            }
        
        return None
    
    async def get_wallet_transactions(self, wallet_address: str, chain: str = 'solana',
                                      limit: int = 50, user_id: int = None) -> List[Dict]:
        """
        دریافت تراکنش‌های یک ولت
        """
        params = {
            'wallet': wallet_address,
            'limit': min(limit, 100)
        }
        
        result = await self._make_request('wallet/txs', params, chain, user_id)
        
        txs = []
        if result and result.get('success'):
            data = result.get('data', {}).get('items', [])
            for tx in data:
                txs.append({
                    'hash': tx.get('txHash'),
                    'type': tx.get('type'),
                    'token': tx.get('tokenAddress'),
                    'token_symbol': tx.get('tokenSymbol'),
                    'amount': tx.get('amount'),
                    'amount_usd': tx.get('amountUsd'),
                    'price': tx.get('price'),
                    'timestamp': tx.get('unixTime'),
                    'from': tx.get('fromAddress'),
                    'to': tx.get('toAddress')
                })
        
        return txs
    
    async def analyze_wallet_profitability(self, wallet_address: str, chain: str = 'solana',
                                           days: int = 30, user_id: int = None) -> Dict:
        """
        تحلیل سودآوری یک ولت
        
        این مهم‌ترین تابع برای تشخیص ولت‌های پرسود است
        """
        cache_key = f"pnl_{chain}_{wallet_address}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # دریافت تراکنش‌ها
        txs = await self.get_wallet_transactions(wallet_address, chain, 500, user_id)
        
        if not txs:
            return {'error': 'No transactions found'}
        
        # تحلیل خرید و فروش
        buys = []
        sells = []
        current_holdings = {}
        
        cutoff = time.time() - (days * 86400)
        
        for tx in txs:
            if tx['timestamp'] < cutoff:
                continue
            
            if tx['type'] == 'buy':
                buys.append(tx)
                token = tx['token']
                if token not in current_holdings:
                    current_holdings[token] = {
                        'amount': 0,
                        'cost': 0
                    }
                current_holdings[token]['amount'] += tx['amount']
                current_holdings[token]['cost'] += tx['amount_usd']
            
            elif tx['type'] == 'sell':
                sells.append(tx)
                token = tx['token']
                if token in current_holdings:
                    current_holdings[token]['amount'] -= tx['amount']
                    if current_holdings[token]['amount'] <= 0:
                        del current_holdings[token]
        
        # محاسبه سود/زیان
        total_buy_volume = sum(tx['amount_usd'] for tx in buys)
        total_sell_volume = sum(tx['amount_usd'] for tx in sells)
        
        # ارزش فعلی دارایی‌ها
        current_value = 0
        for token, holding in current_holdings.items():
            price_data = await self.get_token_price(token, chain, user_id=user_id)
            if price_data and holding['amount'] > 0:
                current_value += holding['amount'] * price_data.get('price', 0)
        
        # محاسبه PnL
        realized_pnl = total_sell_volume - total_buy_volume
        unrealized_pnl = current_value - sum(h['cost'] for h in current_holdings.values())
        total_pnl = realized_pnl + unrealized_pnl
        roi = (total_pnl / total_buy_volume * 100) if total_buy_volume > 0 else 0
        
        result = {
            'wallet': wallet_address,
            'chain': chain,
            'period_days': days,
            'total_trades': len(buys) + len(sells),
            'buy_trades': len(buys),
            'sell_trades': len(sells),
            'total_buy_volume': total_buy_volume,
            'total_sell_volume': total_sell_volume,
            'realized_pnl': realized_pnl,
            'unrealized_pnl': unrealized_pnl,
            'total_pnl': total_pnl,
            'roi_percentage': round(roi, 2),
            'current_holdings_count': len(current_holdings),
            'current_holdings_value': current_value,
            'is_profitable': roi > 20,  # سود بیش از ۲۰٪
            'is_very_profitable': roi > 100,  # سود بیش از ۱۰۰٪
            'is_whale': total_buy_volume > 100000,  # حجم معاملات بیش از ۱۰۰k
            'analysis_time': datetime.now().isoformat()
        }
        
        # ذخیره در حافظه
        self.stats['wallets_tracked'] += 1
        if result['is_profitable']:
            self.profitable_wallets[wallet_address] = result
            self.stats['profitable_wallets_found'] += 1
        
        self.cache[cache_key] = result
        return result
    
    async def find_profitable_wallets(self, chain: str = 'solana', min_roi: float = 50,
                                      min_volume: float = 10000, user_id: int = None) -> List[Dict]:
        """
        پیدا کردن ولت‌های پرسود
        
        Args:
            min_roi: حداقل درصد سود
            min_volume: حداقل حجم معاملات
        """
        # دریافت لیست توکن‌های پرحجم
        top_tokens = await self.get_token_list(chain, 'v24hUSD', 20, user_id)
        
        profitable_wallets = []
        analyzed = set()
        
        for token in top_tokens:
            # دریافت تراکنش‌های بزرگ توکن
            txs = await self.get_token_large_transactions(token['address'], chain, user_id)
            
            for tx in txs:
                wallet = tx.get('from') if tx.get('type') == 'buy' else tx.get('to')
                
                if not wallet or wallet in analyzed:
                    continue
                
                analyzed.add(wallet)
                
                # تحلیل سودآوری ولت
                analysis = await self.analyze_wallet_profitability(wallet, chain, 30, user_id)
                
                if isinstance(analysis, dict) and not analysis.get('error'):
                    if analysis['roi_percentage'] >= min_roi and analysis['total_buy_volume'] >= min_volume:
                        profitable_wallets.append({
                            'wallet': wallet,
                            'roi': analysis['roi_percentage'],
                            'pnl': analysis['total_pnl'],
                            'volume': analysis['total_buy_volume'],
                            'trades': analysis['total_trades'],
                            'analysis': analysis
                        })
                        
                        if wallet not in self.smart_money_wallets:
                            self.smart_money_wallets.append(wallet)
            
            await asyncio.sleep(1)  # جلوگیری از rate limit
        
        # مرتب‌سازی بر اساس ROI
        profitable_wallets.sort(key=lambda x: x['roi'], reverse=True)
        
        return profitable_wallets[:20]
    
    async def get_token_large_transactions(self, token_address: str, chain: str = 'solana',
                                          min_amount: float = 10000, limit: int = 100,
                                          user_id: int = None) -> List[Dict]:
        """
        دریافت تراکنش‌های بزرگ یک توکن
        """
        params = {
            'address': token_address,
            'offset': 0,
            'limit': min(limit, 100),
            'tx_type': 'all'
        }
        
        result = await self._make_request('defi/txs', params, chain, user_id)
        
        large_txs = []
        if result and result.get('success'):
            data = result.get('data', {}).get('items', [])
            for tx in data:
                if tx.get('amountUsd', 0) >= min_amount:
                    large_txs.append({
                        'hash': tx.get('txHash'),
                        'type': tx.get('type'),
                        'from': tx.get('fromAddress'),
                        'to': tx.get('toAddress'),
                        'amount': tx.get('amount'),
                        'amount_usd': tx.get('amountUsd'),
                        'price': tx.get('price'),
                        'timestamp': tx.get('unixTime')
                    })
                    
                    # اگه تراکنش بزرگ بود، ولت رو به نهنگ‌ها اضافه کن
                    if tx.get('amountUsd', 0) > 50000:
                        if tx.get('fromAddress'):
                            self.whale_wallets.add(tx['fromAddress'])
                        if tx.get('toAddress'):
                            self.whale_wallets.add(tx['toAddress'])
                        
                        self.stats['whale_movements_detected'] += 1
        
        return large_txs
    
    async def monitor_whale_wallets(self, callback: Callable = None, interval: int = 30,
                                   user_id: int = None):
        """
        مانیتورینگ لحظه‌ای نهنگ‌ها
        """
        logger.info("🐋 Starting whale wallet monitor...")
        
        tracked_wallets = set()
        
        while True:
            try:
                # دریافت توکن‌های داغ
                top_tokens = await self.get_token_list('solana', 'v24hUSD', 10, user_id)
                
                for token in top_tokens:
                    # دریافت تراکنش‌های بزرگ
                    txs = await self.get_token_large_transactions(token['address'], 'solana', 
                                                                  50000, 20, user_id)
                    
                    for tx in txs:
                        # ایجاد signature یکتا برای تراکنش
                        sig = f"{tx['hash']}_{tx['type']}"
                        
                        if sig not in tracked_wallets:
                            tracked_wallets.add(sig)
                            
                            logger.info(f"🐋 WHALE MOVEMENT: {tx['type']} ${tx['amount_usd']:,.0f}")
                            
                            if callback:
                                tx['token'] = token['symbol']
                                await callback(tx)
                    
                    await asyncio.sleep(2)
                
                # محدودیت حافظه
                if len(tracked_wallets) > 10000:
                    tracked_wallets = set(list(tracked_wallets)[-5000:])
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Whale monitor error: {e}")
                await asyncio.sleep(interval * 2)
    
    async def get_smart_money_flow(self, token_address: str, chain: str = 'solana',
                                   user_id: int = None) -> Dict:
        """
        تحلیل جریان پول هوشمند برای یک توکن
        """
        # دریافت تراکنش‌های بزرگ
        txs = await self.get_token_large_transactions(token_address, chain, 10000, 100, user_id)
        
        smart_money_buys = 0
        smart_money_sells = 0
        smart_money_volume = 0
        
        # دریافت ولت‌های پرسود
        if not self.smart_money_wallets:
            await self.find_profitable_wallets(chain, 50, 10000, user_id)
        
        for tx in txs:
            wallet = tx.get('from') if tx.get('type') == 'sell' else tx.get('to')
            
            if wallet in self.smart_money_wallets or wallet in self.whale_wallets:
                if tx['type'] == 'buy':
                    smart_money_buys += 1
                    smart_money_volume += tx['amount_usd']
                else:
                    smart_money_sells += 1
        
        net_smart_money = smart_money_buys - smart_money_sells
        net_volume = smart_money_volume * (1 if net_smart_money > 0 else -1)
        
        return {
            'token': token_address,
            'smart_money_buys': smart_money_buys,
            'smart_money_sells': smart_money_sells,
            'net_smart_money_flow': net_smart_money,
            'smart_money_volume': smart_money_volume,
            'net_volume': net_volume,
            'sentiment': 'BULLISH' if net_smart_money > 3 else 'BEARISH' if net_smart_money < -3 else 'NEUTRAL',
            'confidence': min(100, abs(net_smart_money) * 10)
        }
    
    async def get_top_profitable_wallets(self, chain: str = 'solana', limit: int = 20,
                                         user_id: int = None) -> List[Dict]:
        """
        دریافت لیست پرسودترین ولت‌ها
        """
        if not self.smart_money_wallets:
            await self.find_profitable_wallets(chain, 50, 10000, user_id)
        
        top_wallets = []
        
        for wallet in self.smart_money_wallets[:limit]:
            analysis = await self.analyze_wallet_profitability(wallet, chain, 30, user_id)
            if isinstance(analysis, dict) and not analysis.get('error'):
                top_wallets.append({
                    'wallet': wallet,
                    'roi': analysis['roi_percentage'],
                    'pnl': analysis['total_pnl'],
                    'volume': analysis['total_buy_volume'],
                    'trades': analysis['total_trades']
                })
        
        return sorted(top_wallets, key=lambda x: x['roi'], reverse=True)
    
    async def get_token_holder_analysis(self, token_address: str, chain: str = 'solana',
                                        user_id: int = None) -> Dict:
        """
        تحلیل هولدرهای یک توکن
        """
        overview = await self.get_token_overview(token_address, chain, user_id)
        
        if not overview:
            return {'error': 'Token not found'}
        
        # دریافت تراکنش‌های بزرگ
        large_txs = await self.get_token_large_transactions(token_address, chain, 10000, 50, user_id)
        
        # شناسایی هولدرهای بزرگ
        whale_holders = set()
        smart_holders = set()
        
        for tx in large_txs:
            if tx['type'] == 'buy':
                whale_holders.add(tx['to'])
            elif tx['type'] == 'sell':
                whale_holders.add(tx['from'])
        
        return {
            'token': token_address,
            'total_holders': overview.get('holder', 0),
            'whale_holders_count': len(whale_holders),
            'whale_holders': list(whale_holders)[:10],
            'holder_concentration': (len(whale_holders) / max(overview.get('holder', 1), 1)) * 100,
            'smart_money_involved': any(w in self.smart_money_wallets for w in whale_holders)
        }
    
    def get_stats(self) -> Dict:
        """گرفتن آمار"""
        return {
            'wallets_tracked': self.stats['wallets_tracked'],
            'profitable_wallets_found': self.stats['profitable_wallets_found'],
            'whale_movements_detected': self.stats['whale_movements_detected'],
            'smart_money_wallets': len(self.smart_money_wallets),
            'whale_wallets': len(self.whale_wallets),
            'total_requests': self.stats['total_requests']
        }
    
    def clear_user_key(self, user_id: int):
        """پاک کردن کلید کاربر"""
        if user_id in self.user_api_keys:
            del self.user_api_keys[user_id]
            logger.info(f"🗑️ Cleared BirdEye API key for user {user_id}")

# نمونه‌سازی سراسری
birdeye_api = BirdEyeAPI()
