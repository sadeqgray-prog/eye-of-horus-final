#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سیستم عددشناسی فیثاغورثی
بر اساس کتاب "Numbers: Their Occult Power" اثر W. Wynn Westcott
"""

import logging
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import math

logger = logging.getLogger(__name__)

class PythagoreanNumerology:
    """
    عددشناسی فیثاغورثی - دقیق‌ترین و قدیمی‌ترین سیستم
    """
    
    # نقشه حروف به اعداد (A=1, B=2, ..., I=9, J=1, ...)
    LETTER_MAP = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    
    # اعداد استاد
    MASTER_NUMBERS = [11, 22, 33, 44, 55]
    
    # اعداد کارمیک
    KARMIC_NUMBERS = [13, 14, 16, 19]
    
    # معانی اعداد
    MEANINGS = {
        1: {
            'name': 'The Leader',
            'positive': 'Independent, creative, ambitious, courageous',
            'negative': 'Arrogant, selfish, aggressive, domineering',
            'planet': 'Sun',
            'element': 'Fire',
            'color': 'Gold, Yellow',
            'crystal': 'Ruby, Diamond',
            'career': 'Entrepreneur, Manager, Innovator',
            'love': 'Passionate but needs independence',
            'advice': 'Lead with wisdom, not ego'
        },
        2: {
            'name': 'The Peacemaker',
            'positive': 'Cooperative, diplomatic, sensitive, intuitive',
            'negative': 'Timid, indecisive, overly sensitive, moody',
            'planet': 'Moon',
            'element': 'Water',
            'color': 'Silver, White',
            'crystal': 'Pearl, Moonstone',
            'career': 'Counselor, Diplomat, Partner',
            'love': 'Deeply emotional, needs harmony',
            'advice': 'Trust your intuition, find balance'
        },
        3: {
            'name': 'The Creative',
            'positive': 'Creative, expressive, optimistic, social',
            'negative': 'Scattered, superficial, exaggerating, critical',
            'planet': 'Jupiter',
            'element': 'Air',
            'color': 'Purple, Yellow',
            'crystal': 'Amethyst, Citrine',
            'career': 'Artist, Writer, Performer',
            'love': 'Romantic and expressive',
            'advice': 'Channel your creativity wisely'
        },
        4: {
            'name': 'The Builder',
            'positive': 'Practical, disciplined, reliable, honest',
            'negative': 'Rigid, stubborn, limited, controlling',
            'planet': 'Uranus',
            'element': 'Earth',
            'color': 'Blue, Green',
            'crystal': 'Sapphire, Emerald',
            'career': 'Engineer, Architect, Organizer',
            'love': 'Loyal and dependable',
            'advice': 'Embrace flexibility within structure'
        },
        5: {
            'name': 'The Explorer',
            'positive': 'Adaptable, versatile, progressive, freedom-loving',
            'negative': 'Inconsistent, restless, irresponsible, escapist',
            'planet': 'Mercury',
            'element': 'Air',
            'color': 'Light Blue, Gray',
            'crystal': 'Topaz, Aquamarine',
            'career': 'Sales, Travel, Media',
            'love': 'Needs freedom and excitement',
            'advice': 'Find stability within change'
        },
        6: {
            'name': 'The Nurturer',
            'positive': 'Responsible, compassionate, harmonious, protective',
            'negative': 'Meddlesome, worried, self-sacrificing, interfering',
            'planet': 'Venus',
            'element': 'Earth',
            'color': 'Green, Pink',
            'crystal': 'Rose Quartz, Jade',
            'career': 'Teacher, Healer, Counselor',
            'love': 'Devoted and nurturing',
            'advice': 'Nurture others, but not at your expense'
        },
        7: {
            'name': 'The Seeker',
            'positive': 'Analytical, intuitive, spiritual, wise',
            'negative': 'Cynical, isolated, secretive, aloof',
            'planet': 'Neptune',
            'element': 'Water',
            'color': 'Sea Green, Violet',
            'crystal': 'Amethyst, Lapis Lazuli',
            'career': 'Scientist, Researcher, Mystic',
            'love': 'Deep but private',
            'advice': 'Share your wisdom with the world'
        },
        8: {
            'name': 'The Achiever',
            'positive': 'Ambitious, efficient, authoritative, successful',
            'negative': 'Materialistic, greedy, workaholic, controlling',
            'planet': 'Saturn',
            'element': 'Earth',
            'color': 'Black, Dark Blue',
            'crystal': 'Onyx, Black Tourmaline',
            'career': 'Executive, Financier, Leader',
            'love': 'Powerful but can be demanding',
            'advice': 'Balance material and spiritual'
        },
        9: {
            'name': 'The Humanitarian',
            'positive': 'Compassionate, generous, artistic, idealistic',
            'negative': 'Emotional, reckless, impractical, resentful',
            'planet': 'Mars',
            'element': 'Fire',
            'color': 'Red, Crimson',
            'crystal': 'Garnet, Red Jasper',
            'career': 'Humanitarian, Artist, Healer',
            'love': 'Passionate and selfless',
            'advice': 'Transform through service'
        }
    }
    
    def __init__(self):
        self.name = "Pythagorean System"
        self.version = "1.0"
        logger.info("🔢 PythagoreanNumerology initialized")
    
    def calculate_life_path(self, birth_date: str) -> Dict[str, Any]:
        """
        محاسبه عدد مسیر زندگی از تاریخ تولد
        فرمت: YYYY-MM-DD
        """
        # استخراج اعداد
        digits = re.findall(r'\d+', birth_date)
        if not digits:
            raise ValueError("Invalid date format")
        
        date_str = ''.join(digits)
        if len(date_str) >= 8:
            year = int(date_str[0:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
        else:
            raise ValueError("Date must include year, month, day")
        
        # محاسبه به روش فیثاغورثی
        year_sum = self._reduce_to_root(sum(int(d) for d in str(year)))
        month_sum = self._reduce_to_root(month)
        day_sum = self._reduce_to_root(day)
        
        total = year_sum + month_sum + day_sum
        life_path = self._reduce_to_root(total, keep_master=True)
        
        # محاسبه اعداد ثانویه
        birthday = self._reduce_to_root(day)
        attitude = self._reduce_to_root(day + month)
        
        # تفسیر
        meaning = self.MEANINGS.get(life_path, self.MEANINGS.get(self._reduce_to_root(life_path)))
        
        result = {
            'number': life_path,
            'is_master': life_path in self.MASTER_NUMBERS,
            'is_karmic': life_path in self.KARMIC_NUMBERS,
            'reduced': self._reduce_to_root(life_path),
            'components': {
                'year': year_sum,
                'month': month_sum,
                'day': day_sum
            },
            'secondary': {
                'birthday': birthday,
                'attitude': attitude
            },
            'meaning': meaning,
            'interpretation': self._interpret_life_path(life_path),
            'method': 'pythagorean'
        }
        
        return result
    
    def calculate_expression(self, full_name: str) -> Dict[str, Any]:
        """
        محاسبه عدد بیان (سرنوشت) از نام کامل
        """
        # پاکسازی و تبدیل به uppercase
        clean_name = re.sub(r'[^A-Za-z\s]', '', full_name.upper())
        words = clean_name.split()
        
        total = 0
        details = []
        
        for word in words:
            word_sum = 0
            word_details = []
            
            for char in word:
                if char in self.LETTER_MAP:
                    value = self.LETTER_MAP[char]
                    word_sum += value
                    word_details.append({'char': char, 'value': value})
            
            word_reduced = self._reduce_to_root(word_sum)
            total += word_sum
            
            details.append({
                'word': word,
                'sum': word_sum,
                'reduced': word_reduced,
                'details': word_details
            })
        
        expression = self._reduce_to_root(total, keep_master=True)
        
        return {
            'number': expression,
            'is_master': expression in self.MASTER_NUMBERS,
            'reduced': self._reduce_to_root(expression),
            'total': total,
            'details': details,
            'meaning': self.MEANINGS.get(expression, self.MEANINGS.get(self._reduce_to_root(expression))),
            'interpretation': self._interpret_expression(expression, details)
        }
    
    def calculate_soul_urge(self, full_name: str) -> Dict[str, Any]:
        """
        محاسبه عدد تمایل روح (صداهای روح)
        فقط حروف صدادار A, E, I, O, U
        """
        clean_name = re.sub(r'[^A-Za-z\s]', '', full_name.upper())
        vowels = 'AEIOU'
        
        total = 0
        details = []
        
        for char in clean_name:
            if char in vowels and char in self.LETTER_MAP:
                value = self.LETTER_MAP[char]
                total += value
                details.append({'char': char, 'value': value})
        
        soul_urge = self._reduce_to_root(total, keep_master=True)
        
        return {
            'number': soul_urge,
            'is_master': soul_urge in self.MASTER_NUMBERS,
            'total': total,
            'details': details,
            'meaning': self.MEANINGS.get(soul_urge, self.MEANINGS.get(self._reduce_to_root(soul_urge))),
            'interpretation': self._interpret_soul_urge(soul_urge, details)
        }
    
    def calculate_personality(self, full_name: str) -> Dict[str, Any]:
        """
        محاسبه عدد شخصیت (صدای بیرونی)
        فقط حروف بی‌صدا
        """
        clean_name = re.sub(r'[^A-Za-z\s]', '', full_name.upper())
        vowels = 'AEIOU'
        
        total = 0
        details = []
        
        for char in clean_name:
            if char not in vowels and char in self.LETTER_MAP:
                value = self.LETTER_MAP[char]
                total += value
                details.append({'char': char, 'value': value})
        
        personality = self._reduce_to_root(total, keep_master=True)
        
        return {
            'number': personality,
            'is_master': personality in self.MASTER_NUMBERS,
            'total': total,
            'details': details,
            'meaning': self.MEANINGS.get(personality, self.MEANINGS.get(self._reduce_to_root(personality))),
            'interpretation': self._interpret_personality(personality, details)
        }
    
    def calculate_personal_year(self, birth_date: str, target_year: int = None) -> int:
        """محاسبه عدد سال شخصی"""
        if target_year is None:
            target_year = datetime.now().year
        
        life_path = self.calculate_life_path(birth_date)
        year_sum = self._reduce_to_root(sum(int(d) for d in str(target_year)))
        
        personal_year = life_path['number'] + year_sum
        return self._reduce_to_root(personal_year, keep_master=True)
    
    def calculate_personal_month(self, birth_date: str, target_date: str = None) -> int:
        """محاسبه عدد ماه شخصی"""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        personal_year = self.calculate_personal_year(birth_date, int(target_date[:4]))
        month = int(target_date[5:7])
        
        personal_month = personal_year + month
        return self._reduce_to_root(personal_month, keep_master=True)
    
    def calculate_personal_day(self, birth_date: str, target_date: str = None) -> int:
        """محاسبه عدد روز شخصی"""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        personal_month = self.calculate_personal_month(birth_date, target_date)
        day = int(target_date[8:10])
        
        personal_day = personal_month + day
        return self._reduce_to_root(personal_day, keep_master=True)
    
    def calculate_challenge_numbers(self, birth_date: str) -> Dict[str, int]:
        """محاسبه اعداد چالش"""
        digits = re.findall(r'\d+', birth_date)
        if len(digits) >= 3:
            month = int(digits[0][:2]) if len(digits[0]) >= 2 else int(digits[0])
            day = int(digits[1][:2]) if len(digits[1]) >= 2 else int(digits[1])
            year = int(digits[2][:4]) if len(digits[2]) >= 4 else int(digits[2])
            
            month_root = self._reduce_to_root(month)
            day_root = self._reduce_to_root(day)
            year_root = self._reduce_to_root(sum(int(d) for d in str(year)))
            
            challenges = {
                'first': abs(month_root - day_root),
                'second': abs(day_root - year_root),
                'third': abs(self._reduce_to_root(month_root + day_root) - 
                            self._reduce_to_root(day_root + year_root)),
                'fourth': abs(month_root - year_root)
            }
            
            return challenges
        
        return {'first': 0, 'second': 0, 'third': 0, 'fourth': 0}
    
    def calculate_pinnacle_numbers(self, birth_date: str) -> List[Dict[str, Any]]:
        """محاسبه اعداد قله"""
        life_path = self.calculate_life_path(birth_date)
        
        pinnacles = []
        ages = [0, 27, 54, 81]  # سنین شروع هر قله
        
        for i in range(4):
            if i == 0:
                number = self._reduce_to_root(life_path['components']['month'] + 
                                             life_path['components']['day'])
            elif i == 1:
                number = self._reduce_to_root(life_path['components']['day'] + 
                                             life_path['components']['year'])
            elif i == 2:
                pinnacle1 = self._reduce_to_root(life_path['components']['month'] + 
                                                life_path['components']['day'])
                pinnacle2 = self._reduce_to_root(life_path['components']['day'] + 
                                                life_path['components']['year'])
                number = self._reduce_to_root(pinnacle1 + pinnacle2, keep_master=True)
            else:
                number = self._reduce_to_root(life_path['components']['month'] + 
                                             life_path['components']['year'])
            
            pinnacles.append({
                'number': number,
                'start_age': ages[i],
                'end_age': ages[i+1] if i < 3 else 'death',
                'interpretation': self.MEANINGS.get(number, self.MEANINGS.get(self._reduce_to_root(number)))
            })
        
        return pinnacles
    
    def analyze_name_compatibility(self, name1: str, name2: str) -> Dict[str, Any]:
        """تحلیل سازگاری دو نام"""
        expr1 = self.calculate_expression(name1)
        expr2 = self.calculate_expression(name2)
        
        soul1 = self.calculate_soul_urge(name1)
        soul2 = self.calculate_soul_urge(name2)
        
        pers1 = self.calculate_personality(name1)
        pers2 = self.calculate_personality(name2)
        
        # محاسبه امتیاز سازگاری
        scores = []
        
        # سازگاری اعداد بیان
        expr_score = 100 - (abs(expr1['reduced'] - expr2['reduced']) * 10)
        scores.append(expr_score)
        
        # سازگاری تمایلات روح
        soul_score = 100 - (abs(soul1['reduced'] - soul2['reduced']) * 10)
        scores.append(soul_score)
        
        # سازگاری شخصیت
        pers_score = 100 - (abs(pers1['reduced'] - pers2['reduced']) * 10)
        scores.append(pers_score)
        
        total_score = sum(scores) / len(scores)
        
        # سطح سازگاری
        if total_score >= 80:
            level = "🌟 Cosmic Match"
            description = "Perfect harmony! Soulmate connection."
        elif total_score >= 60:
            level = "✨ Strong Connection"
            description = "Great potential with mutual understanding."
        elif total_score >= 40:
            level = "⭐ Good Potential"
            description = "Can work well with effort and compromise."
        elif total_score >= 20:
            level = "⚖️ Neutral"
            description = "Neither特别好 nor特别坏."
        else:
            level = "⚡ Challenging"
            description = "Requires growth and understanding."
        
        return {
            'score': round(total_score, 1),
            'level': level,
            'description': description,
            'details': {
                'expression': {'num1': expr1['number'], 'num2': expr2['number'], 'score': round(expr_score, 1)},
                'soul_urge': {'num1': soul1['number'], 'num2': soul2['number'], 'score': round(soul_score, 1)},
                'personality': {'num1': pers1['number'], 'num2': pers2['number'], 'score': round(pers_score, 1)}
            },
            'advice': self._get_compatibility_advice(total_score)
        }
    
    def _reduce_to_root(self, num: int, keep_master: bool = True) -> int:
        """کاهش عدد به ریشه (حفظ اعداد استاد)"""
        if num == 0:
            return 0
        
        if keep_master and num in self.MASTER_NUMBERS:
            return num
        
        while num > 9 and num not in self.MASTER_NUMBERS:
            num = sum(int(d) for d in str(num))
        
        return num
    
    def _interpret_life_path(self, number: int) -> str:
        """تفسیر مسیر زندگی"""
        meanings = {
            1: "You're a natural leader. Your path is to pioneer, create, and inspire others through your independence.",
            2: "You're a peacemaker. Your path is to bring harmony, cooperate with others, and trust your intuition.",
            3: "You're a creative soul. Your path is to express yourself, bring joy to others, and share your art.",
            4: "You're a builder. Your path is to create stability, work hard, and build lasting foundations.",
            5: "You're an explorer. Your path is to embrace change, seek freedom, and share your experiences.",
            6: "You're a nurturer. Your path is to love, serve, and create harmony in your community.",
            7: "You're a seeker. Your path is to analyze, seek wisdom, and share your spiritual insights.",
            8: "You're an achiever. Your path is to manifest abundance, lead with authority, and create legacy.",
            9: "You're a humanitarian. Your path is to serve humanity, complete cycles, and inspire transformation."
        }
        
        reduced = self._reduce_to_root(number)
        return meanings.get(reduced, "Your path is unique. Embrace your journey.")
    
    def _interpret_expression(self, number: int, details: List) -> str:
        """تفسیر عدد بیان"""
        meanings = {
            1: "You're here to express leadership and originality.",
            2: "You're here to express cooperation and diplomacy.",
            3: "You're here to express creativity and joy.",
            4: "You're here to express practicality and discipline.",
            5: "You're here to express freedom and adaptability.",
            6: "You're here to express love and responsibility.",
            7: "You're here to express wisdom and analysis.",
            8: "You're here to express power and achievement.",
            9: "You're here to express compassion and completion."
        }
        
        reduced = self._reduce_to_root(number)
        return meanings.get(reduced, "Your expression is uniquely yours.")
    
    def _interpret_soul_urge(self, number: int, details: List) -> str:
        """تفسیر تمایل روح"""
        meanings = {
            1: "Your soul craves independence and leadership.",
            2: "Your soul craves peace and partnership.",
            3: "Your soul craves creative expression.",
            4: "Your soul craves stability and order.",
            5: "Your soul craves freedom and adventure.",
            6: "Your soul craves love and service.",
            7: "Your soul craves wisdom and understanding.",
            8: "Your soul craves success and recognition.",
            9: "Your soul craves completion and transformation."
        }
        
        reduced = self._reduce_to_root(number)
        return meanings.get(reduced, "Your soul's desire is unique.")
    
    def _interpret_personality(self, number: int, details: List) -> str:
        """تفسیر شخصیت"""
        meanings = {
            1: "You appear confident and independent.",
            2: "You appear friendly and cooperative.",
            3: "You appear creative and expressive.",
            4: "You appear practical and reliable.",
            5: "You appear adventurous and versatile.",
            6: "You appear caring and responsible.",
            7: "You appear wise and analytical.",
            8: "You appear powerful and successful.",
            9: "You appear compassionate and artistic."
        }
        
        reduced = self._reduce_to_root(number)
        return meanings.get(reduced, "Your personality is uniquely yours.")
    
    def _get_compatibility_advice(self, score: float) -> str:
        """توصیه سازگاری"""
        if score >= 80:
            return "Celebrate this cosmic connection! Support each other's growth."
        elif score >= 60:
            return "Nurture this connection with open communication and understanding."
        elif score >= 40:
            return "Focus on your common goals and respect your differences."
        elif score >= 20:
            return "Work on understanding each other's needs and perspectives."
        else:
            return "This relationship offers great opportunity for personal growth."
    
    def get_lucky_numbers(self, base_number: int, count: int = 5) -> List[int]:
        """اعداد شانس بر اساس عدد پایه"""
        base = self._reduce_to_root(base_number)
        
        lucky = []
        for i in range(count):
            num = base + (i * 9)
            lucky.append(num)
        
        return lucky
    
    def get_unlucky_numbers(self, base_number: int, count: int = 3) -> List[int]:
        """اعداد نامبارک"""
        base = self._reduce_to_root(base_number)
        opposite = 10 - base
        
        unlucky = []
        for i in range(count):
            num = opposite + (i * 9)
            unlucky.append(num)
        
        return unlucky
    
    def get_color(self, number: int) -> str:
        """رنگ مرتبط با عدد"""
        colors = {
            1: "Gold, Yellow",
            2: "Silver, White",
            3: "Purple, Lavender",
            4: "Blue, Green",
            5: "Light Blue, Gray",
            6: "Pink, Rose",
            7: "Violet, Sea Green",
            8: "Black, Dark Blue",
            9: "Red, Crimson"
        }
        
        reduced = self._reduce_to_root(number)
        return colors.get(reduced, "Rainbow")
    
    def get_crystal(self, number: int) -> str:
        """کریستال مرتبط با عدد"""
        crystals = {
            1: "Ruby, Diamond",
            2: "Pearl, Moonstone",
            3: "Amethyst, Citrine",
            4: "Sapphire, Emerald",
            5: "Topaz, Aquamarine",
            6: "Rose Quartz, Jade",
            7: "Amethyst, Lapis Lazuli",
            8: "Onyx, Black Tourmaline",
            9: "Garnet, Red Jasper"
        }
        
        reduced = self._reduce_to_root(number)
        return crystals.get(reduced, "Clear Quartz")
    
    def get_tarot_card(self, number: int) -> str:
        """کارت تاروت مرتبط با عدد"""
        tarot = {
            1: "The Magician",
            2: "The High Priestess",
            3: "The Empress",
            4: "The Emperor",
            5: "The Hierophant",
            6: "The Lovers",
            7: "The Chariot",
            8: "Strength",
            9: "The Hermit",
            11: "Justice",
            22: "The Fool"
        }
        
        return tarot.get(number, "Unknown")
    
    def get_ruling_planet(self, number: int) -> str:
        """سیاره حاکم"""
        planets = {
            1: "Sun",
            2: "Moon",
            3: "Jupiter",
            4: "Uranus",
            5: "Mercury",
            6: "Venus",
            7: "Neptune",
            8: "Saturn",
            9: "Mars"
        }
        
        reduced = self._reduce_to_root(number)
        return planets.get(reduced, "Unknown")
    
    def get_element(self, number: int) -> str:
        """عنصر"""
        elements = {
            1: "Fire",
            2: "Water",
            3: "Air",
            4: "Earth",
            5: "Air",
            6: "Earth",
            7: "Water",
            8: "Earth",
            9: "Fire"
        }
        
        reduced = self._reduce_to_root(number)
        return elements.get(reduced, "Ether")
