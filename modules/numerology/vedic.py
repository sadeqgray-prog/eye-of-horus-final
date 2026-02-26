#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🇮🇳 VEDIC NUMEROLOGY - Jyotish Shastra
سیستم عددشناسی ودایی بر اساس ستاره‌شناسی هندی
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class VedicNumerology:
    """
    عددشناسی ودایی - برگرفته از جیوتیش شاسترا
    """
    
    def __init__(self):
        self.name = "Vedic Numerology"
        self.version = "1.0.0"
        logger.info("🇮🇳 VedicNumerology initialized")
    
    def calculate_moolank(self, birth_date: str) -> Dict:
        """محاسبه Moolank (عدد ریشه) از تاریخ تولد"""
        digits = [int(d) for d in birth_date if d.isdigit()]
        total = sum(digits)
        while total > 9:
            total = sum(int(d) for d in str(total))
        
        return {
            'number': total,
            'method': 'moolank',
            'interpretation': self._interpret_moolank(total)
        }
    
    def calculate_bhagyank(self, birth_date: str) -> Dict:
        """محاسبه Bhagyank (عدد سرنوشت)"""
        parts = birth_date.split('-')
        if len(parts) == 3:
            day = sum(int(d) for d in parts[2])
            month = sum(int(d) for d in parts[1])
            year = sum(int(d) for d in parts[0])
            
            total = day + month + year
            while total > 9:
                total = sum(int(d) for d in str(total))
            
            return {
                'number': total,
                'method': 'bhagyank',
                'interpretation': self._interpret_bhagyank(total)
            }
        return {'error': 'Invalid date format'}
    
    def calculate_name_number(self, name: str) -> Dict:
        """محاسبه عدد نام"""
        total = sum(ord(c) for c in name.upper() if c.isalpha())
        while total > 9:
            total = sum(int(d) for d in str(total))
        
        return {
            'number': total,
            'interpretation': self._interpret_name(total)
        }
    
    def _interpret_moolank(self, number: int) -> str:
        interpretations = {
            1: "You are a natural leader.",
            2: "You are a peacemaker.",
            3: "You are creative.",
            4: "You are a builder.",
            5: "You are an explorer.",
            6: "You are a nurturer.",
            7: "You are a seeker.",
            8: "You are an achiever.",
            9: "You are a humanitarian."
        }
        return interpretations.get(number, "Your path is unique.")
    
    def _interpret_bhagyank(self, number: int) -> str:
        interpretations = {
            1: "Your destiny is to lead.",
            2: "Your destiny is to cooperate.",
            3: "Your destiny is to create.",
            4: "Your destiny is to build.",
            5: "Your destiny is to explore.",
            6: "Your destiny is to nurture.",
            7: "Your destiny is to seek.",
            8: "Your destiny is to achieve.",
            9: "Your destiny is to serve."
        }
        return interpretations.get(number, "Your destiny is unique.")
    
    def _interpret_name(self, number: int) -> str:
        interpretations = {
            1: "You express leadership.",
            2: "You express cooperation.",
            3: "You express creativity.",
            4: "You express practicality.",
            5: "You express freedom.",
            6: "You express love.",
            7: "You express wisdom.",
            8: "You express power.",
            9: "You express compassion."
        }
        return interpretations.get(number, "Your expression is unique.")
