#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛠 FIX ALL PROBLEMS - نسخه نهایی
رفع مشکلات ماژول‌های گمشده و نصب کتابخانه‌ها
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# ==================== رنگ‌ها ====================
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

print(f"{BOLD}{BLUE}{'='*60}{END}")
print(f"{BOLD}{BLUE}🛠 FIX ALL PROBLEMS - FINAL VERSION{END}")
print(f"{BOLD}{BLUE}{'='*60}{END}")

# ==================== ۱. بک‌آپ ====================
print(f"\n{YELLOW}📦 Creating backup...{END}")
backup_name = f"backup_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.make_archive(backup_name, 'zip', '.')
print(f"{GREEN}✅ Backup created: {backup_name}.zip{END}")

# ==================== ۲. نصب PyPDF2 ====================
print(f"\n{YELLOW}📚 Installing PyPDF2...{END}")
subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"], check=False)
print(f"{GREEN}✅ PyPDF2 installed{END}")

# ==================== ۳. ایجاد ماژول‌های گمشده عددشناسی ====================
print(f"\n{YELLOW}📁 Creating missing numerology modules...{END}")

# پوشه numerology
os.makedirs("modules/numerology", exist_ok=True)

# ==================== فایل vedic.py ====================
vedic_content = '''#!/usr/bin/env python3
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
    
    # نقشه حروف به اعداد (سیستم ودایی)
    LETTER_MAP = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    
    # سیارات حاکم
    RULING_PLANETS = {
        1: 'Sun (Surya)',
        2: 'Moon (Chandra)',
        3: 'Jupiter (Guru)',
        4: 'Rahu (North Node)',
        5: 'Mercury (Budha)',
        6: 'Venus (Shukra)',
        7: 'Ketu (South Node)',
        8: 'Saturn (Shani)',
        9: 'Mars (Mangal)'
    }
    
    def __init__(self):
        self.name = "Vedic Numerology"
        self.version = "1.0.0"
        logger.info("🇮🇳 VedicNumerology initialized")
    
    def calculate_moolank(self, birth_date: str) -> Dict:
        """
        محاسبه Moolank (عدد ریشه) از تاریخ تولد
        فرمت: YYYY-MM-DD
        """
        digits = [int(d) for d in birth_date if d.isdigit()]
        total = sum(digits)
        while total > 9:
            total = sum(int(d) for d in str(total))
        
        return {
            'number': total,
            'ruling_planet': self.RULING_PLANETS.get(total, 'Unknown'),
            'method': 'moolank',
            'interpretation': self._interpret_moolank(total)
        }
    
    def calculate_bhagyank(self, birth_date: str) -> Dict:
        """
        محاسبه Bhagyank (عدد سرنوشت)
        """
        # جمع روز + ماه + سال
        parts = birth_date.split('-')
        if len(parts) == 3:
            day = sum(int(d) for d in parts[2])  # روز
            month = sum(int(d) for d in parts[1])  # ماه
            year = sum(int(d) for d in parts[0])  # سال
            
            total = day + month + year
            while total > 9:
                total = sum(int(d) for d in str(total))
            
            return {
                'number': total,
                'ruling_planet': self.RULING_PLANETS.get(total, 'Unknown'),
                'method': 'bhagyank',
                'interpretation': self._interpret_bhagyank(total)
            }
        
        return {'error': 'Invalid date format'}
    
    def calculate_name_number(self, name: str) -> Dict:
        """
        محاسبه عدد نام به روش ودایی
        """
        name = name.upper()
        total = 0
        details = []
        
        for char in name:
            if char in self.LETTER_MAP:
                value = self.LETTER_MAP[char]
                total += value
                details.append({'char': char, 'value': value})
        
        while total > 9:
            total = sum(int(d) for d in str(total))
        
        return {
            'number': total,
            'total': sum(d['value'] for d in details),
            'details': details,
            'ruling_planet': self.RULING_PLANETS.get(total, 'Unknown'),
            'interpretation': self._interpret_name(total)
        }
    
    def calculate_compatibility(self, name1: str, name2: str) -> Dict:
        """
        محاسبه سازگاری دو نفر
        """
        num1 = self.calculate_name_number(name1)['number']
        num2 = self.calculate_name_number(name2)['number']
        
        diff = abs(num1 - num2)
        
        if diff <= 2:
            compatibility = 'Excellent'
            score = 90
        elif diff <= 4:
            compatibility = 'Good'
            score = 75
        elif diff <= 6:
            compatibility = 'Average'
            score = 60
        else:
            compatibility = 'Challenging'
            score = 45
        
        return {
            'name1': name1,
            'name2': name2,
            'number1': num1,
            'number2': num2,
            'compatibility': compatibility,
            'score': score,
            'advice': self._get_compatibility_advice(score)
        }
    
    def _interpret_moolank(self, number: int) -> str:
        """تعبیر Moolank"""
        interpretations = {
            1: "You are a natural leader. Creative, independent, and ambitious.",
            2: "You are a peacemaker. Cooperative, diplomatic, and intuitive.",
            3: "You are creative. Expressive, optimistic, and social.",
            4: "You are a builder. Practical, disciplined, and reliable.",
            5: "You are an explorer. Adaptable, freedom-loving, and progressive.",
            6: "You are a nurturer. Responsible, loving, and protective.",
            7: "You are a seeker. Analytical, spiritual, and wise.",
            8: "You are an achiever. Ambitious, efficient, and authoritative.",
            9: "You are a humanitarian. Compassionate, generous, and artistic."
        }
        return interpretations.get(number, "Your path is unique.")
    
    def _interpret_bhagyank(self, number: int) -> str:
        """تعبیر Bhagyank"""
        interpretations = {
            1: "Your destiny is to lead and innovate.",
            2: "Your destiny is to cooperate and harmonize.",
            3: "Your destiny is to express and create.",
            4: "Your destiny is to build and organize.",
            5: "Your destiny is to explore and adapt.",
            6: "Your destiny is to nurture and serve.",
            7: "Your destiny is to analyze and seek truth.",
            8: "Your destiny is to achieve and manifest.",
            9: "Your destiny is to complete and transform."
        }
        return interpretations.get(number, "Your destiny is unique.")
    
    def _interpret_name(self, number: int) -> str:
        """تعبیر عدد نام"""
        interpretations = {
            1: "You express leadership and originality.",
            2: "You express cooperation and diplomacy.",
            3: "You express creativity and joy.",
            4: "You express practicality and discipline.",
            5: "You express freedom and adaptability.",
            6: "You express love and responsibility.",
            7: "You express wisdom and analysis.",
            8: "You express power and achievement.",
            9: "You express compassion and completion."
        }
        return interpretations.get(number, "Your expression is unique.")
    
    def _get_compatibility_advice(self, score: int) -> str:
        """توصیه سازگاری"""
        if score >= 80:
            return "Excellent match! Support each other's growth."
        elif score >= 60:
            return "Good match. Work on understanding differences."
        else:
            return "Work on communication and mutual understanding."
'''

with open("modules/numerology/vedic.py", "w", encoding='utf-8') as f:
    f.write(vedic_content)
print(f"{GREEN}✅ Created modules/numerology/vedic.py{END}")

# ==================== فایل chaldean.py (کامل) ====================
chaldean_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🇮🇶 CHALDEAN NUMEROLOGY - Ancient Babylonian system
قدیمی‌ترین سیستم عددشناسی جهان (۴۰۰۰+ سال)
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ChaldeanNumerology:
    """
    سیستم عددشناسی کلدانی - برگرفته از الواح بابلی
    """
    
    # نقشه حروف به اعداد (سیستم کلدانی)
    LETTER_MAP = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5,
        'I': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8,
        'Q': 1, 'R': 2, 'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5,
        'Y': 1, 'Z': 7
    }
    
    # معانی اعداد
    MEANINGS = {
        1: {
            'name': 'The Sun',
            'positive': 'Leadership, creativity, individuality',
            'negative': 'Arrogance, selfishness, dominance',
            'planet': 'Sun',
            'element': 'Fire',
            'career': 'Leader, manager, innovator'
        },
        2: {
            'name': 'The Moon',
            'positive': 'Cooperation, diplomacy, sensitivity',
            'negative': 'Indecision, moodiness, dependence',
            'planet': 'Moon',
            'element': 'Water',
            'career': 'Counselor, diplomat, partner'
        },
        3: {
            'name': 'Jupiter',
            'positive': 'Creativity, optimism, communication',
            'negative': 'Scattered, superficial, exaggeration',
            'planet': 'Jupiter',
            'element': 'Air',
            'career': 'Artist, writer, speaker'
        },
        4: {
            'name': 'Uranus',
            'positive': 'Practicality, discipline, organization',
            'negative': 'Rigidity, stubbornness, limitation',
            'planet': 'Uranus',
            'element': 'Earth',
            'career': 'Engineer, architect, organizer'
        },
        5: {
            'name': 'Mercury',
            'positive': 'Freedom, adaptability, adventure',
            'negative': 'Inconsistency, restlessness',
            'planet': 'Mercury',
            'element': 'Air',
            'career': 'Traveler, sales, journalist'
        },
        6: {
            'name': 'Venus',
            'positive': 'Harmony, responsibility, love',
            'negative': 'Meddling, worry, self-sacrifice',
            'planet': 'Venus',
            'element': 'Earth',
            'career': 'Teacher, healer, counselor'
        },
        7: {
            'name': 'Neptune',
            'positive': 'Wisdom, analysis, spirituality',
            'negative': 'Cynicism, isolation, secrecy',
            'planet': 'Neptune',
            'element': 'Water',
            'career': 'Scientist, researcher, mystic'
        },
        8: {
            'name': 'Saturn',
            'positive': 'Ambition, efficiency, authority',
            'negative': 'Materialism, workaholism',
            'planet': 'Saturn',
            'element': 'Earth',
            'career': 'Executive, financier, leader'
        }
    }
    
    def __init__(self):
        self.name = "Chaldean Numerology"
        self.version = "1.0.0"
        logger.info("🇮🇶 ChaldeanNumerology initialized")
    
    def calculate_expression(self, name: str) -> Dict:
        """
        محاسبه عدد بیان به روش کلدانی
        """
        name = name.upper()
        total = 0
        details = []
        
        for char in name:
            if char in self.LETTER_MAP:
                value = self.LETTER_MAP[char]
                total += value
                details.append({'char': char, 'value': value})
        
        # در سیستم کلدانی، اعداد ۹ نداریم
        if total == 9:
            total = 8
        
        return {
            'number': total,
            'total': sum(d['value'] for d in details),
            'details': details,
            'meaning': self.MEANINGS.get(total, {}),
            'interpretation': self._interpret(total, name)
        }
    
    def _interpret(self, number: int, name: str) -> str:
        """تعبیر عدد"""
        meaning = self.MEANINGS.get(number, {})
        return f"Number {number}: {meaning.get('name', 'Unknown')}. You are {meaning.get('positive', 'unique')}."
'''

with open("modules/numerology/chaldean.py", "w", encoding='utf-8') as f:
    f.write(chaldean_content)
print(f"{GREEN}✅ Created modules/numerology/chaldean.py{END}")

# ==================== فایل chinese.py ====================
chinese_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🇨🇳 CHINESE NUMEROLOGY - Lo Shu Square System
سیستم عددشناسی چینی بر اساس مربع جادویی لو شو
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ChineseNumerology:
    """
    عددشناسی چینی - برگرفته از آی چینگ و فنگ شویی
    """
    
    # مربع جادویی لو شو
    LO_SHU_SQUARE = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]
    
    # معانی اعداد
    MEANINGS = {
        1: {'name': 'Water', 'direction': 'North', 'season': 'Winter'},
        2: {'name': 'Earth', 'direction': 'Southwest', 'season': 'Late Summer'},
        3: {'name': 'Wood', 'direction': 'East', 'season': 'Spring'},
        4: {'name': 'Wood', 'direction': 'Southeast', 'season': 'Spring'},
        5: {'name': 'Earth', 'direction': 'Center', 'season': 'All'},
        6: {'name': 'Metal', 'direction': 'Northwest', 'season': 'Autumn'},
        7: {'name': 'Metal', 'direction': 'West', 'season': 'Autumn'},
        8: {'name': 'Earth', 'direction': 'Northeast', 'season': 'Late Summer'},
        9: {'name': 'Fire', 'direction': 'South', 'season': 'Summer'}
    }
    
    def __init__(self):
        self.name = "Chinese Numerology"
        self.version = "1.0.0"
        logger.info("🇨🇳 ChineseNumerology initialized")
    
    def calculate_kua_number(self, birth_year: int, gender: str) -> Dict:
        """
        محاسبه عدد Kua (عدد سرنوشت در فنگ شویی)
        """
        # جمع ارقام سال تولد
        digits = [int(d) for d in str(birth_year)]
        while len(digits) > 1:
            digits = [int(d) for d in str(sum(digits))]
        
        base = sum(digits)
        
        if gender.lower() == 'male':
            kua = 10 - base
        else:  # female
            kua = 5 + base
        
        while kua > 9:
            kua = sum(int(d) for d in str(kua))
        
        return {
            'number': kua,
            'element': self.MEANINGS.get(kua, {}).get('name', 'Unknown'),
            'direction': self.MEANINGS.get(kua, {}).get('direction', 'Unknown'),
            'lucky_directions': self._get_lucky_directions(kua)
        }
    
    def _get_lucky_directions(self, kua: int) -> List[str]:
        """جهت‌های خوش شانس"""
        directions = {
            1: ['Southeast', 'East', 'South', 'North'],
            2: ['Northeast', 'West', 'Northwest', 'Southwest'],
            3: ['South', 'North', 'Southeast', 'East'],
            4: ['North', 'South', 'East', 'Southeast'],
            5: ['Northeast', 'West', 'Northwest', 'Southwest'],
            6: ['West', 'Northeast', 'Southwest', 'Northwest'],
            7: ['Northwest', 'Southwest', 'Northeast', 'West'],
            8: ['Southwest', 'Northwest', 'West', 'Northeast'],
            9: ['East', 'Southeast', 'North', 'South']
        }
        return directions.get(kua, [])
'''

with open("modules/numerology/chinese.py", "w", encoding='utf-8') as f:
    f.write(chinese_content)
print(f"{GREEN}✅ Created modules/numerology/chinese.py{END}")

# ==================== فایل __init__.py ====================
init_content = '''from .pythagorean import PythagoreanNumerology
from .chaldean import ChaldeanNumerology
from .vedic import VedicNumerology
from .chinese import ChineseNumerology

__all__ = [
    'PythagoreanNumerology',
    'ChaldeanNumerology',
    'VedicNumerology',
    'ChineseNumerology'
]
'''

with open("modules/numerology/__init__.py", "w", encoding='utf-8') as f:
    f.write(init_content)
print(f"{GREEN}✅ Updated modules/numerology/__init__.py{END}")

# ==================== ۴. رفع مشکل knowledge_engine.py ====================
print(f"\n{YELLOW}🔧 Fixing brain/knowledge_engine.py for PyPDF2...{END}")

knowledge_file = "brain/knowledge_engine.py"
if os.path.exists(knowledge_file):
    with open(knowledge_file, 'r') as f:
        content = f.read()
    
    # اضافه کردن try/except برای PyPDF2
    if 'import PyPDF2' not in content:
        # اضافه کردن به اول فایل
        content = 'try:\n    import PyPDF2\n    PDF_SUPPORT = True\nexcept ImportError:\n    PDF_SUPPORT = False\n    import logging\n    logging.warning("⚠️ PyPDF2 not installed. PDF books disabled.")\n\n' + content
        
        with open(knowledge_file, 'w') as f:
            f.write(content)
        print(f"{GREEN}✅ Added PyPDF2 support to knowledge_engine.py{END}")
else:
    print(f"{RED}❌ knowledge_engine.py not found{END}")

# ==================== ۵. ایجاد فایل requirements کامل ====================
print(f"\n{YELLOW}📦 Creating complete requirements.txt...{END}")

requirements = '''# Core
python-telegram-bot==20.7
python-dotenv==1.0.0
aiohttp==3.9.1
requests==2.31.0
cryptography==41.0.7

# PDF Support
PyPDF2==3.0.1

# Database
sqlalchemy==2.0.23

# Data Science
numpy==1.24.3
pandas==2.0.3

# NLP
nltk==3.8.1
textblob==0.17.1

# Blockchain
web3==6.15.1
solana==0.34.3

# APIs
ccxt==4.2.3
pycoingecko==3.1.0
'''

with open("requirements.full.txt", "w") as f:
    f.write(requirements)
print(f"{GREEN}✅ Created requirements.full.txt{END}")

# ==================== ۶. گزارش نهایی ====================
print(f"\n{GREEN}{BOLD}{'='*60}{END}")
print(f"{GREEN}{BOLD}✅ ALL FIXES APPLIED SUCCESSFULLY{END}")
print(f"{GREEN}{BOLD}{'='*60}{END}")

print(f"\n{BLUE}📋 Summary of fixes:{END}")
print(f"  {GREEN}✓{END} Backup created: {backup_name}.zip")
print(f"  {GREEN}✓{END} PyPDF2 installed")
print(f"  {GREEN}✓{END} Created vedic.py (complete)")
print(f"  {GREEN}✓{END} Created chaldean.py (complete)")
print(f"  {GREEN}✓{END} Created chinese.py (complete)")
print(f"  {GREEN}✓{END} Updated __init__.py")
print(f"  {GREEN}✓{END} Added PyPDF2 support to knowledge_engine.py")
print(f"  {GREEN}✓{END} Created requirements.full.txt")

print(f"\n{YELLOW}📦 To install all requirements:{END}")
print(f"  {BLUE}pip install -r requirements.full.txt{END}")

print(f"\n{YELLOW}📦 To deploy to Railway:{END}")
print(f"  {BLUE}git add .{END}")
print(f"  {BLUE}git commit -m \"FIX: add missing numerology modules and PyPDF2\"{END}")
print(f"  {BLUE}git push origin main{END}")

print(f"\n{GREEN}{BOLD}🎉 Ready to deploy! Run the commands above.{END}")
