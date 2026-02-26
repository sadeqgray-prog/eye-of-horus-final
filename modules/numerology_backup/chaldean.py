#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
عددشناسی کلدانی - قدیمی‌ترین سیستم عددشناسی جهان
منبع: بر اساس الواح بابلی و متون کلدانی
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ChaldeanNumerology:
    """
    سیستم عددشناسی کلدانی - دقیق‌ترین و قدیمی‌ترین روش
    اعداد: ۱ تا ۸ (۹ عدد روحانی و مقدس است)
    """
    
    # نقشه حروف به اعداد (سیستم کلدانی)
    LETTER_MAP = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'C': 2, 'K': 2, 'R': 2,
        'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    
    # معانی اعداد
    MEANINGS = {
        1: {
            'name': 'The Creator',
            'element': 'Fire',
            'planet': 'Sun',
            'positive': 'Leadership, innovation, willpower',
            'negative': 'Arrogance, selfishness',
            'career': 'Leader, inventor, pioneer'
        },
        2: {
            'name': 'The Mediator',
            'element': 'Water',
            'planet': 'Moon',
            'positive': 'Diplomacy, intuition, cooperation',
            'negative': 'Indecision, sensitivity',
            'career': 'Counselor, diplomat, partner'
        },
        3: {
            'name': 'The Artist',
            'element': 'Air',
            'planet': 'Jupiter',
            'positive': 'Creativity, expression, optimism',
            'negative': 'Scattered, exaggeration',
            'career': 'Artist, writer, performer'
        },
        4: {
            'name': 'The Builder',
            'element': 'Earth',
            'planet': 'Uranus',
            'positive': 'Practical, disciplined, reliable',
            'negative': 'Rigid, stubborn',
            'career': 'Architect, engineer, organizer'
        },
        5: {
            'name': 'The Explorer',
            'element': 'Air',
            'planet': 'Mercury',
            'positive': 'Adaptable, freedom-loving, progressive',
            'negative': 'Restless, inconsistent',
            'career': 'Traveler, sales, communicator'
        },
        6: {
            'name': 'The Nurturer',
            'element': 'Earth',
            'planet': 'Venus',
            'positive': 'Responsible, loving, harmonious',
            'negative': 'Meddlesome, worried',
            'career': 'Teacher, healer, parent'
        },
        7: {
            'name': 'The Seeker',
            'element': 'Water',
            'planet': 'Neptune',
            'positive': 'Wise, analytical, spiritual',
            'negative': 'Isolated, cynical',
            'career': 'Scientist, mystic, researcher'
        },
        8: {
            'name': 'The Achiever',
            'element': 'Earth',
            'planet': 'Saturn',
            'positive': 'Ambitious, efficient, authoritative',
            'negative': 'Materialistic, workaholic',
            'career': 'Executive, financier, leader'
        }
    }
    
    def calculate_name_number(self, name: str) -> Dict[str, Any]:
        """محاسبه عدد نام به روش کلدانی"""
        clean_name = ''.join(c for c in name.upper() if c.isalpha())
        
        total = 0
        details = []
        
        for char in clean_name:
            if char in self.LETTER_MAP:
                value = self.LETTER_MAP[char]
                total += value
                details.append({'char': char, 'value': value})
        
        root = self._reduce_to_root(total)
        meaning = self.MEANINGS.get(root, self.MEANINGS.get(self._reduce_to_root(root)))
        
        return {
            'name': name,
            'chaldean_number': total,
            'root_number': root,
            'details': details,
            'meaning': meaning,
            'interpretation': self._interpret_number(root, name)
        }
    
    def _reduce_to_root(self, num: int) -> int:
        """کاهش به عدد ریشه"""
        while num > 8:
            num = sum(int(d) for d in str(num))
        return num
    
    def _interpret_number(self, number: int, name: str) -> str:
        """تفسیر عدد"""
        interpretations = {
            1: f"You are a natural leader, {name}.",
            2: f"You are a peacemaker, {name}.",
            3: f"You are creative, {name}.",
            4: f"You are a builder, {name}.",
            5: f"You are an explorer, {name}.",
            6: f"You are a nurturer, {name}.",
            7: f"You are a seeker, {name}.",
            8: f"You are an achiever, {name}."
        }
        return interpretations.get(number, f"Your number {number} has special meaning.")
