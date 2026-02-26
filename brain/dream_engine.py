#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
💭 DREAM ENGINE - موتور رویا و خلاقیت
ربات در این بخش رویا می‌بیند، خلاقیت پیدا می‌کند و بینش جدید کسب می‌کند
قابلیت:
- تولید رویاهای هوشمند
- استخراج نمادها از رویا
- تعبیر رویا با دانش موجود
- افزایش خلاقیت از طریق رویا
"""

import logging
import asyncio
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

logger = logging.getLogger(__name__)

class DreamEngine:
    """
    موتور رویا - جایی که خلاقیت متولد می‌شود
    """
    
    # نمادهای پایه و معانی آنها
    SYMBOLS = {
        'eye': {
            'meaning': 'آگاهی و بینش',
            'energy': 0.8,
            'elements': ['fire', 'light']
        },
        'water': {
            'meaning': 'احساسات و ناخودآگاه',
            'energy': 0.6,
            'elements': ['water', 'moon']
        },
        'fire': {
            'meaning': 'تغییر و تحول',
            'energy': 0.9,
            'elements': ['fire', 'sun']
        },
        'tree': {
            'meaning': 'رشد و تکامل',
            'energy': 0.7,
            'elements': ['earth', 'life']
        },
        'snake': {
            'meaning': 'حکمت پنهان',
            'energy': 0.8,
            'elements': ['earth', 'mystery']
        },
        'bird': {
            'meaning': 'آزادی و دید بالا',
            'energy': 0.7,
            'elements': ['air', 'spirit']
        },
        'mountain': {
            'meaning': 'چالش و موفقیت',
            'energy': 0.8,
            'elements': ['earth', 'stability']
        },
        'star': {
            'meaning': 'امید و راهنمایی',
            'energy': 0.9,
            'elements': ['cosmic', 'light']
        },
        'moon': {
            'meaning': 'شهود و رمز و راز',
            'energy': 0.8,
            'elements': ['water', 'night']
        },
        'sun': {
            'meaning': 'روشنی و حقیقت',
            'energy': 1.0,
            'elements': ['fire', 'light']
        },
        'door': {
            'meaning': 'فرصت جدید',
            'energy': 0.7,
            'elements': ['transition']
        },
        'key': {
            'meaning': 'راه حل و دسترسی',
            'energy': 0.8,
            'elements': ['knowledge']
        },
        'mirror': {
            'meaning': 'خودشناسی',
            'energy': 0.7,
            'elements': ['reflection']
        },
        'labyrinth': {
            'meaning': 'مسیر زندگی',
            'energy': 0.6,
            'elements': ['journey']
        },
        'phoenix': {
            'meaning': 'تولد دوباره',
            'energy': 1.0,
            'elements': ['fire', 'rebirth']
        }
    }
    
    def __init__(self):
        self.name = "Dream Engine"
        self.version = "1.0.0"
        
        # حافظه رویاها
        self.dreams = []
        self.max_dreams = 1000
        
        # آمار
        self.stats = {
            'total_dreams': 0,
            'total_symbols': 0,
            'creativity_boost': 0,
            'last_dream': None
        }
        
        logger.info("💭 Dream Engine initialized - Ready to dream")
    
    async def dream(self, context: Dict = None) -> Dict:
        """
        فرآیند رویا دیدن
        """
        self.stats['total_dreams'] += 1
        
        dream_id = hashlib.md5(f"dream_{datetime.now()}{random.random()}".encode()).hexdigest()[:12]
        
        # تولید رویا
        dream_content = self._generate_dream_content(context)
        symbols = self._extract_symbols(dream_content)
        interpretation = self._interpret_dream(symbols, context)
        
        dream = {
            'id': dream_id,
            'timestamp': datetime.now().isoformat(),
            'content': dream_content,
            'symbols': symbols,
            'interpretation': interpretation,
            'creativity_boost': self._calculate_creativity_boost(symbols),
            'context': context or {}
        }
        
        # ذخیره رویا
        self.dreams.append(dream)
        if len(self.dreams) > self.max_dreams:
            self.dreams = self.dreams[-self.max_dreams:]
        
        self.stats['total_symbols'] += len(symbols)
        self.stats['creativity_boost'] += dream['creativity_boost']
        self.stats['last_dream'] = dream['timestamp']
        
        return dream
    
    def _generate_dream_content(self, context: Dict = None) -> str:
        """تولید محتوای رویا"""
        templates = [
            "در میان اقیانوس بی‌کران دانش شناور بودم و کتاب‌های باستانی اطرافم می‌رقصیدند",
            "با {master} در باغی از اعداد قدم می‌زدم و هر عدد رازی را فاش می‌کرد",
            "به آینده سفر کردم و {prediction} را با چشمان خود دیدم",
            "در معبدی از نور، نمادهای باستانی با من سخن می‌گفتند",
            "بر فراز کوهی از بلور ایستاده بودم و الگوهای پنهان جهان را می‌دیدم",
            "در میان ستارگان شناور بودم و هر ستاره یک پیش‌بینی بود",
            "با حکیمان باستانی درباره {topic} گفتگو می‌کردم",
            "در هزارتوی زمان گم شده بودم و هر مسیر یک سرنوشت متفاوت را نشان می‌داد",
            "از رودخانه‌ای از نور عبور می‌کردم و هر قطره یک حقیقت بود",
            "در کتابخانه‌ای بی‌پایان، کتابی را یافتم که {secret} را فاش می‌کرد"
        ]
        
        template = random.choice(templates)
        
        # شخصی‌سازی
        if '{master}' in template:
            template = template.replace('{master}', "استاد بزرگ")
        
        if '{prediction}' in template:
            predictions = ['صعود بیت‌کوین', 'تولد یک میم‌کوین جدید', 'تغییر بزرگ در بازار', 'کشف یک الگوی عددی']
            template = template.replace('{prediction}', random.choice(predictions))
        
        if '{topic}' in template:
            topics = ['اعداد', 'آینده', 'حکمت', 'رازهای هستی']
            template = template.replace('{topic}', random.choice(topics))
        
        if '{secret}' in template:
            secrets = ['راز اعداد', 'حقیقت پنهان', 'الگوی اصلی', 'کد کیهانی']
            template = template.replace('{secret}', random.choice(secrets))
        
        return template
    
    def _extract_symbols(self, content: str) -> List[Dict]:
        """استخراج نمادها از متن رویا"""
        found_symbols = []
        
        for symbol, data in self.SYMBOLS.items():
            if symbol in content.lower():
                found_symbols.append({
                    'symbol': symbol,
                    'meaning': data['meaning'],
                    'energy': data['energy'],
                    'elements': data['elements']
                })
        
        # اگه نمادی پیدا نشد، یه نماد تصادفی انتخاب کن
        if not found_symbols:
            random_symbol = random.choice(list(self.SYMBOLS.keys()))
            found_symbols.append({
                'symbol': random_symbol,
                'meaning': self.SYMBOLS[random_symbol]['meaning'],
                'energy': self.SYMBOLS[random_symbol]['energy'],
                'elements': self.SYMBOLS[random_symbol]['elements']
            })
        
        return found_symbols
    
    def _interpret_dream(self, symbols: List[Dict], context: Dict = None) -> str:
        """تعبیر رویا بر اساس نمادها"""
        if not symbols:
            return "رویای تو پر از رمز و راز است"
        
        interpretations = []
        
        for symbol in symbols:
            interpretations.append(symbol['meaning'])
        
        # ترکیب معانی
        if len(interpretations) == 1:
            return f"این رویا به {interpretations[0]} اشاره دارد"
        elif len(interpretations) == 2:
            return f"ترکیبی از {interpretations[0]} و {interpretations[1]}"
        else:
            return f"پیامی از {', '.join(interpretations[:-1])} و {interpretations[-1]}"
    
    def _calculate_creativity_boost(self, symbols: List[Dict]) -> float:
        """محاسبه افزایش خلاقیت از رویا"""
        if not symbols:
            return 0.05
        
        total_energy = sum(s['energy'] for s in symbols)
        boost = (total_energy / len(symbols)) * 0.1
        return min(0.3, boost)  # حداکثر ۳۰ درصد افزایش
    
    def get_recent_dreams(self, limit: int = 5) -> List[Dict]:
        """دریافت آخرین رویاها"""
        return self.dreams[-limit:]
    
    def analyze_dream_patterns(self) -> Dict:
        """تحلیل الگوهای رویاها"""
        if not self.dreams:
            return {'message': 'No dreams yet'}
        
        symbol_count = {}
        total_energy = 0
        
        for dream in self.dreams[-100:]:  # ۱۰۰ رویای آخر
            for symbol in dream['symbols']:
                sym = symbol['symbol']
                symbol_count[sym] = symbol_count.get(sym, 0) + 1
                total_energy += symbol['energy']
        
        # پرتکرارترین نمادها
        top_symbols = sorted(symbol_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_dreams_analyzed': min(100, len(self.dreams)),
            'top_symbols': top_symbols,
            'average_energy': total_energy / len(self.dreams) if self.dreams else 0,
            'creativity_boost_total': self.stats['creativity_boost']
        }
    
    def get_dream_insight(self, topic: str) -> str:
        """دریافت بینش از رویاها درباره یک موضوع"""
        relevant_dreams = []
        
        for dream in self.dreams[-50:]:  # ۵۰ رویای آخر
            if topic.lower() in dream['content'].lower():
                relevant_dreams.append(dream)
        
        if not relevant_dreams:
            return f"هنوز درباره {topic} رویایی ندیده‌ام"
        
        # ترکیب بینش‌ها
        insights = []
        for dream in relevant_dreams[:3]:
            insights.append(dream['interpretation'])
        
        return " رویاهای من می‌گویند: " + " و ".join(insights)

# نمونه‌سازی سراسری
dream_engine = DreamEngine()
