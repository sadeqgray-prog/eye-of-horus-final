#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ردیاب هوشمند پول - ترکیب BirdEye با سایر APIها
قابلیت‌ها:
- شناسایی خودکار پرسودترین معامله‌گران
- ردیابی لحظه‌ای خرید/فروش نهنگ‌ها
- تحلیل الگوهای معاملاتی
- پیش‌بینی پامپ بر اساس حرکت‌های نهنگ
- هشدار زودهنگام
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import json

from api.birdeye import birdeye_api
from api.dexscreener import dexscreener_api
from api.pump_fun import pump_fun_api
from core.cosmic_intelligence import cosmic_ai
from core.quantum_memory import quantum_memory
from core.safe_imports import importer

logger = logging.getLogger(__name__)

class SmartMoneyTracker:
    """
    ردیاب پول هوشمند - مغز متفکر برای دنبال کردن نهنگ‌ها
    """
    
    def __init__(self):
        self.tracked_wallets = set()
        self.profitable_wallets = []
        self.whale_alerts = []
        self.prediction_history = []
        
        # آستانه‌ها
        self.WHALE_THRESHOLD = 50000  # ۵۰k دلار
        self.SUPER_WHALE_THRESHOLD = 500000  # ۵۰۰k دلار
        self.PROFITABLE_THRESHOLD = 50  # ۵۰٪ سود
        
        self.callbacks = []
        
        logger.info("💰 SmartMoneyTracker initialized - Ready to follow smart money")
    
    async def find_smart_money_wallets(self, chain: str = 'solana', limit: int = 50) -> List[Dict]:
        """
        پیدا کردن ولت‌های پول هوشمند
        """
        logger.info(f"🔍 Finding smart money wallets on {chain}...")
        
        # روش ۱: از BirdEye
        birdeye_wallets = await birdeye_api.find_profitable_wallets(chain, self.PROFITABLE_THRESHOLD, 
                                                                   10000, user_id=None)
        
        # روش ۲: از تراکنش‌های بزرگ
        whale_wallets = []
        try:
            top_tokens = await birdeye_api.get_token_list(chain, 'v24hUSD', 20)
            for token in top_tokens[:5]:
                txs = await birdeye_api.get_token_large_transactions(token['address'], chain, 
                                                                     self.WHALE_THRESHOLD, 50)
                for tx in txs:
                    if tx['amount_usd'] > self.WHALE_THRESHOLD:
                        wallet = tx['to'] if tx['type'] == 'buy' else tx['from']
                        whale_wallets.append({
                            'wallet': wallet,
                            'type': 'whale',
                            'last_trade': tx
                        })
                await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error finding whale wallets: {e}")
        
        # ترکیب نتایج
        all_wallets = []
        seen = set()
        
        for w in birdeye_wallets:
            if w['wallet'] not in seen:
                seen.add(w['wallet'])
                all_wallets.append({
                    'wallet': w['wallet'],
                    'type': 'smart_money',
                    'roi': w['roi'],
                    'pnl': w['pnl'],
                    'volume': w['volume'],
                    'trades': w['trades'],
                    'discovered_at': datetime.now().isoformat()
                })
                self.tracked_wallets.add(w['wallet'])
        
        for w in whale_wallets:
            if w['wallet'] not in seen:
                seen.add(w['wallet'])
                all_wallets.append({
                    'wallet': w['wallet'],
                    'type': 'whale',
                    'last_trade': w['last_trade'],
                    'discovered_at': datetime.now().isoformat()
                })
                self.tracked_wallets.add(w['wallet'])
        
        # ذخیره در حافظه
        self.profitable_wallets = all_wallets
        await self._save_wallets()
        
        return all_wallets[:limit]
    
    async def monitor_wallet(self, wallet_address: str, callback: Callable = None,
                             interval: int = 60, chain: str = 'solana'):
        """
        مانیتورینگ یک ولت خاص
        """
        logger.info(f"👀 Monitoring wallet: {wallet_address[:10]}...")
        
        last_tx_time = 0
        
        while True:
            try:
                # دریافت تراکنش‌های جدید
                txs = await birdeye_api.get_wallet_transactions(wallet_address, chain, 20)
                
                for tx in txs:
                    if tx['timestamp'] > last_tx_time:
                        last_tx_time = tx['timestamp']
                        
                        # تحلیل تراکنش
                        analysis = await self._analyze_transaction(tx, wallet_address, chain)
                        
                        if analysis['is_significant']:
                            logger.info(f"💰 SIGNIFICANT MOVE: {analysis['action']} ${tx['amount_usd']:,.0f}")
                            
                            self.whale_alerts.append(analysis)
                            
                            if callback:
                                await callback(analysis)
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(interval * 2)
    
    async def _analyze_transaction(self, tx: Dict, wallet: str, chain: str) -> Dict:
        """تحلیل یک تراکنش"""
        
        is_significant = False
        action = "UNKNOWN"
        
        # بررسی اهمیت
        if tx['amount_usd'] > self.SUPER_WHALE_THRESHOLD:
            is_significant = True
            action = "🐋 SUPER WHALE"
        elif tx['amount_usd'] > self.WHALE_THRESHOLD:
            is_significant = True
            action = "🐋 WHALE"
        
        # تشخیص خرید یا فروش
        if tx['type'] == 'buy':
            action += " BUY"
        elif tx['type'] == 'sell':
            action += " SELL"
        
        # دریافت اطلاعات توکن
        token_info = await dexscreener_api.get_token_info(tx['token'], chain)
        
        return {
            'type': 'wallet_move',
            'action': action,
            'wallet': wallet,
            'transaction': tx,
            'token_info': token_info,
            'is_significant': is_significant,
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_smart_money_signals(self, chain: str = 'solana') -> List[Dict]:
        """
        دریافت سیگنال‌های پول هوشمند
        """
        signals = []
        
        # دریافت توکن‌های داغ
        hot_tokens = await birdeye_api.get_token_list(chain, 'v24hUSD', 20)
        
        for token in hot_tokens:
            # تحلیل جریان پول هوشمند
            flow = await birdeye_api.get_smart_money_flow(token['address'], chain)
            
            if flow['confidence'] > 50:
                signals.append({
                    'token': token['symbol'],
                    'address': token['address'],
                    'sentiment': flow['sentiment'],
                    'confidence': flow['confidence'],
                    'smart_money_buys': flow['smart_money_buys'],
                    'smart_money_sells': flow['smart_money_sells'],
                    'price': token['price'],
                    'price_change': token['price_change_24h'],
                    'time': datetime.now().isoformat()
                })
        
        return sorted(signals, key=lambda x: x['confidence'], reverse=True)
    
    async def predict_pump_from_whales(self, token_address: str, chain: str = 'solana') -> Dict:
        """
        پیش‌بینی پامپ بر اساس حرکت نهنگ‌ها
        """
        # دریافت تراکنش‌های نهنگ برای این توکن
        whale_txs = await birdeye_api.get_token_large_transactions(token_address, chain, 
                                                                   self.WHALE_THRESHOLD, 50)
        
        if not whale_txs:
            return {'probability': 0, 'reason': 'No whale activity'}
        
        # تحلیل الگو
        recent_buys = 0
        recent_sells = 0
        whale_accumulation = 0
        
        cutoff = time.time() - 86400  # ۲۴ ساعت
        
        for tx in whale_txs:
            if tx['timestamp'] > cutoff:
                if tx['type'] == 'buy':
                    recent_buys += 1
                    whale_accumulation += tx['amount_usd']
                else:
                    recent_sells += 1
        
        net_whale_flow = recent_buys - recent_sells
        accumulation_score = min(100, (whale_accumulation / 1000000) * 10)  # ۱M = 10%
        
        # محاسبه احتمال
        probability = 50 + (net_whale_flow * 5) + accumulation_score
        probability = max(0, min(100, probability))
        
        return {
            'token': token_address,
            'probability': probability,
            'whale_buys_24h': recent_buys,
            'whale_sells_24h': recent_sells,
            'net_whale_flow': net_whale_flow,
            'accumulation_usd': whale_accumulation,
            'accumulation_score': accumulation_score,
            'pump_chance': 'HIGH' if probability > 70 else 'MEDIUM' if probability > 50 else 'LOW',
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_top_wallets_to_follow(self, limit: int = 10) -> List[Dict]:
        """
        دریافت بهترین ولت‌ها برای دنبال کردن
        """
        if not self.profitable_wallets:
            await self.find_smart_money_wallets('solana', 50)
        
        # مرتب‌سازی بر اساس سودآوری
        top_by_roi = sorted([w for w in self.profitable_wallets if 'roi' in w], 
                           key=lambda x: x.get('roi', 0), reverse=True)
        
        # مرتب‌سازی بر اساس حجم
        top_by_volume = sorted([w for w in self.profitable_wallets if 'volume' in w],
                               key=lambda x: x.get('volume', 0), reverse=True)
        
        # ترکیب
        combined = []
        seen = set()
        
        for w in top_by_roi[:limit]:
            if w['wallet'] not in seen:
                seen.add(w['wallet'])
                combined.append(w)
        
        for w in top_by_volume[:limit]:
            if w['wallet'] not in seen and len(combined) < limit:
                seen.add(w['wallet'])
                combined.append(w)
        
        return combined[:limit]
    
    async def _save_wallets(self):
        """ذخیره ولت‌ها در حافظه"""
        await quantum_memory.store('smart_money_wallets', self.profitable_wallets)
    
    async def load_wallets(self):
        """بارگذاری ولت‌ها از حافظه"""
        wallets = await quantum_memory.retrieve('smart_money_wallets')
        if wallets:
            self.profitable_wallets = wallets
            self.tracked_wallets = {w['wallet'] for w in wallets}
            logger.info(f"📚 Loaded {len(wallets)} smart money wallets")
    
    def get_stats(self) -> Dict:
        """گرفتن آمار"""
        return {
            'tracked_wallets': len(self.tracked_wallets),
            'profitable_wallets': len(self.profitable_wallets),
            'whale_alerts': len(self.whale_alerts),
            'predictions': len(self.prediction_history)
        }

# نمونه‌سازی سراسری
smart_money_tracker = SmartMoneyTracker()
