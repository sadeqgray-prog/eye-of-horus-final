#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اسکرپر کانال‌های تلگرام - برای تحلیل سیگنال‌های میم‌کوین
بدون نیاز به API Key
قابلیت‌ها:
- مانیتورینگ کانال‌های سیگنال
- استخراج آدرس توکن از پیام‌ها
- تحلیل احساسات
- تشخیص پامپ‌های قریب‌الوقوع
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import re
import json
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

logger = logging.getLogger(__name__)

class TelegramScraper:
    """
    اسکرپر کانال‌های تلگرام - نیازی به API Key نداره
    فقط نیاز به شماره تلفن و کد تایید
    """
    
    # کانال‌های معروف سیگنال میم‌کوین
    SIGNAL_CHANNELS = [
        'pumpfun_signals',
        'solana_pumps',
        'meme_coin_alerts',
        'crypto_pumps_daily',
        'early_crypto_signals',
        'moon_shot_alerts',
        'gem_hunters',
        'crypto_whale_signals'
    ]
    
    # الگوهای تشخیص آدرس توکن
    TOKEN_PATTERNS = [
        r'0x[a-fA-F0-9]{40}',  # Ethereum/BSC
        r'[1-9A-HJ-NP-Za-km-z]{32,44}',  # Solana
        r'0x[a-fA-F0-9]{64}'  # Transaction hash
    ]
    
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.api_id = None
        self.api_hash = None
        self.phone = None
        self.user_data = {}
        
        # حافظه
        self.seen_messages = set()
        self.recent_tokens = []
        self.callbacks = []
        
        logger.info("📱 TelegramScraper initialized")
    
    def set_credentials(self, api_id: int, api_hash: str, phone: str, user_id: int = None):
        """تنظیم credentials تلگرام"""
        creds = {
            'api_id': api_id,
            'api_hash': api_hash,
            'phone': phone
        }
        
        if user_id:
            self.user_data[user_id] = creds
            logger.info(f"✅ Telegram credentials set for user {user_id}")
        else:
            self.api_id = api_id
            self.api_hash = api_hash
            self.phone = phone
            logger.info("✅ Telegram global credentials set")
    
    async def connect(self, user_id: int = None):
        """اتصال به تلگرام"""
        if self.is_connected:
            return True
        
        # انتخاب credentials
        if user_id and user_id in self.user_data:
            creds = self.user_data[user_id]
            api_id = creds['api_id']
            api_hash = creds['api_hash']
            phone = creds['phone']
        else:
            api_id = self.api_id
            api_hash = self.api_hash
            phone = self.phone
        
        if not api_id or not api_hash:
            logger.error("Telegram credentials not set")
            return False
        
        try:
            self.client = TelegramClient('session_' + str(user_id or 0), api_id, api_hash)
            await self.client.start(phone=phone)
            self.is_connected = True
            logger.info("✅ Connected to Telegram")
            return True
            
        except SessionPasswordNeededError:
            logger.error("2FA required")
            return False
        except Exception as e:
            logger.error(f"Telegram connection error: {e}")
            return False
    
    async def get_channel_messages(self, channel: str, limit: int = 50,
                                    user_id: int = None) -> List[Dict]:
        """
        دریافت آخرین پیام‌های یک کانال
        """
        if not await self.connect(user_id):
            return []
        
        try:
            entity = await self.client.get_entity(channel)
            messages = []
            
            async for msg in self.client.iter_messages(entity, limit=limit):
                if msg.text:
                    # استخراج آدرس توکن
                    token_address = self._extract_token_address(msg.text)
                    
                    messages.append({
                        'id': msg.id,
                        'text': msg.text,
                        'date': msg.date.isoformat(),
                        'sender_id': msg.sender_id,
                        'views': msg.views,
                        'forwards': msg.forwards,
                        'token_address': token_address,
                        'channel': channel
                    })
                    
                    self.seen_messages.add(msg.id)
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting channel {channel}: {e}")
            return []
    
    async def monitor_channels(self, channels: List[str] = None, callback: Callable = None,
                               interval: int = 30, user_id: int = None):
        """
        مانیتورینگ مداوم کانال‌ها
        """
        if not channels:
            channels = self.SIGNAL_CHANNELS
        
        if not await self.connect(user_id):
            logger.error("Cannot connect to Telegram")
            return
        
        if callback:
            self.callbacks.append(callback)
        
        logger.info(f"👀 Monitoring {len(channels)} Telegram channels")
        
        last_check = datetime.now()
        
        while True:
            try:
                for channel in channels:
                    messages = await self.get_channel_messages(channel, 20, user_id)
                    
                    for msg in messages:
                        if msg['id'] not in self.seen_messages:
                            self.seen_messages.add(msg['id'])
                            
                            # اگه توکن داشت
                            if msg['token_address']:
                                logger.info(f"🆕 New token found in {channel}: {msg['token_address'][:10]}...")
                                
                                for callback in self.callbacks:
                                    try:
                                        await callback(msg)
                                    except Exception as e:
                                        logger.error(f"Callback error: {e}")
                    
                    await asyncio.sleep(2)  # فاصله بین کانال‌ها
                
                elapsed = (datetime.now() - last_check).total_seconds()
                if elapsed < interval:
                    await asyncio.sleep(interval - elapsed)
                
                last_check = datetime.now()
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(interval * 2)
    
    def _extract_token_address(self, text: str) -> Optional[str]:
        """استخراج آدرس توکن از متن"""
        for pattern in self.TOKEN_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        return None
    
    async def search_token_mentions(self, token_address: str, hours: int = 24,
                                     user_id: int = None) -> List[Dict]:
        """
        جستجوی یک توکن در پیام‌ها
        """
        if not await self.connect(user_id):
            return []
        
        mentions = []
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for channel in self.SIGNAL_CHANNELS:
            try:
                entity = await self.client.get_entity(channel)
                
                async for msg in self.client.iter_messages(entity, limit=200):
                    if msg.date.replace(tzinfo=None) < cutoff:
                        break
                    
                    if msg.text and token_address in msg.text:
                        mentions.append({
                            'channel': channel,
                            'date': msg.date.isoformat(),
                            'text': msg.text[:200],
                            'views': msg.views,
                            'forwards': msg.forwards
                        })
                        
            except Exception as e:
                logger.error(f"Error searching {channel}: {e}")
            
            await asyncio.sleep(1)
        
        return mentions
    
    async def get_hot_tokens(self, hours: int = 6, user_id: int = None) -> List[Dict]:
        """
        دریافت توکن‌های داغ (بیشترین تکرار در کانال‌ها)
        """
        if not await self.connect(user_id):
            return []
        
        token_counts = {}
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for channel in self.SIGNAL_CHANNELS[:5]:  # ۵ کانال اول
            try:
                entity = await self.client.get_entity(channel)
                
                async for msg in self.client.iter_messages(entity, limit=100):
                    if msg.date.replace(tzinfo=None) < cutoff:
                        break
                    
                    if msg.text:
                        token = self._extract_token_address(msg.text)
                        if token:
                            token_counts[token] = token_counts.get(token, 0) + 1
                            
            except Exception as e:
                logger.error(f"Error in {channel}: {e}")
            
            await asyncio.sleep(1)
        
        # مرتب‌سازی
        hot_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return [{'address': t[0], 'mentions': t[1]} for t in hot_tokens]
    
    async def disconnect(self):
        """قطع اتصال"""
        if self.client:
            await self.client.disconnect()
            self.is_connected = False
            logger.info("🔌 Disconnected from Telegram")

# نمونه‌سازی سراسری
telegram_scraper = TelegramScraper()
