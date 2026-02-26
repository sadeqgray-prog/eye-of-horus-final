import json
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📖 THE CHALDEAN ORACLES & BABYLONIAN TEXTS
متون مقدس کلدانی و بابلی - قدیمی‌ترین منبع عددشناسی جهان
بر اساس الواح گلی بین‌النهرین و متون کلدانی
"""

BOOK_DATA = {
    'title': 'The Chaldean Oracles and Babylonian Sacred Texts',
    'author': 'Ancient Chaldean Priests & Babylonian Sages',
    'year': 'حدود 3000 سال قبل از میلاد',
    'subjects': ['Chaldean', 'Babylonian', 'Numerology', 'Astrology', 'Mysticism'],
    'language': 'Sumerian, Akkadian (ترجمه شده)',
    'summary': '''
    قدیمی‌ترین منبع عددشناسی جهان. کلدانیان باستان معتقد بودند که
    اعداد روح جهان هستند و هر عدد یک خدای خاص را نمایندگی می‌کند.
    این متون شامل الواح بابلی، زیگورات‌ها، و اوراکل‌های کلدانی است.
    ''',
    'keywords': [
        'chaldean', 'babylonian', 'sumerian', 'ziggurat', 'marduk',
        'ishtar', 'enki', 'anu', 'enlil', 'nergal', 'shamash',
        'sin', 'nabu', 'tiamat', 'apsu'
    ]
}

# ==================== خدایان و اعداد کلدانی ====================
CHALDEAN_DEITIES = {
    1: {
        'name': 'Anu',
        'domain': 'آسمان، پدر خدایان',
        'planet': 'Uranus',
        'number': 60,
        'symbol': 'ستاره هشت‌پر',
        'temple': 'زیگورات اوروک',
        'meaning': 'وحدت، منبع همه چیز'
    },
    2: {
        'name': 'Enlil',
        'domain': 'باد، طوفان، فرمانروایی',
        'planet': 'Jupiter',
        'number': 50,
        'symbol': 'باد',
        'temple': 'زیگورات نیپور',
        'meaning': 'دوگانگی، قدرت'
    },
    3: {
        'name': 'Enki',
        'domain': 'آب، خرد، جادو',
        'planet': 'Mercury',
        'number': 40,
        'symbol': 'بز-ماهی',
        'temple': 'زیگورات اریدو',
        'meaning': 'سه‌گانگی، آفرینش'
    },
    4: {
        'name': 'Ninhursag',
        'domain': 'زمین، مادر خدایان',
        'planet': 'Earth',
        'number': 55,
        'symbol': 'کوه',
        'temple': 'زیگورات کیش',
        'meaning': 'چهار عنصر'
    },
    5: {
        'name': 'Nanna (Sin)',
        'domain': 'ماه، تقویم، زمان',
        'planet': 'Moon',
        'number': 30,
        'symbol': 'هلال ماه',
        'temple': 'زیگورات اور',
        'meaning': 'پنج حس'
    },
    6: {
        'name': 'Utu (Shamash)',
        'domain': 'خورشید، عدالت، پیش‌گویی',
        'planet': 'Sun',
        'number': 20,
        'symbol': 'خورشید',
        'temple': 'زیگورات لارسا',
        'meaning': 'شش جهت'
    },
    7: {
        'name': 'Inanna (Ishtar)',
        'domain': 'عشق، جنگ، سیاره ناهید',
        'planet': 'Venus',
        'number': 15,
        'symbol': 'ستاره هشت‌پر',
        'temple': 'زیگورات اوروک',
        'meaning': 'هفت آسمان'
    },
    8: {
        'name': 'Nabu',
        'domain': 'نوشتن، حکمت، کاتبان',
        'planet': 'Mercury',
        'number': 12,
        'symbol': 'قلم نی',
        'temple': 'زیگورات بُرسپا',
        'meaning': 'هشت جهت'
    },
    9: {
        'name': 'Nergal',
        'domain': 'دنیای زیرین، جنگ، طاعون',
        'planet': 'Mars',
        'number': 14,
        'symbol': 'شیر-سر',
        'temple': 'زیگورات کوتا',
        'meaning': 'نه جهان زیرین'
    }
}

# ==================== اعداد مقدس بابلی ====================
SACRED_NUMBERS = {
    7: {
        'name': 'Sebettu',
        'meaning': 'هفت خدای سرنوشت',
        'planets': ['خورشید', 'ماه', 'مریخ', 'عطارد', 'مشتری', 'زهره', 'زحل'],
        'gates': 'هفت دروازه جهان زیرین',
        'ziggurat': 'هفت طبقه زیگورات'
    },
    12: {
        'name': 'Dodecad',
        'meaning': 'دوازده ماه سال، دوازده برج فلکی',
        'gods': ['Anu', 'Enlil', 'Enki', 'Ninhursag', 'Nanna', 'Utu', 
                 'Inanna', 'Nabu', 'Nergal', 'Marduk', 'Ninurta', 'Gula'],
        'signs': 'دوازده برج فلکی'
    },
    60: {
        'name': 'Geshtu',
        'meaning': 'عدد پایه بابلی (پایه ۶۰)',
        'system': 'سیستم عددی بابلی',
        'gods': 'آنو (خدای آسمان)'
    }
}

# ==================== زیگورات‌ها و اعداد ====================
ZIGGURATS = {
    'ur': {
        'name': 'زیگورات اور (Great Ziggurat of Ur)',
        'god': 'Nanna (Sin)',
        'levels': 7,
        'height': 'حدود ۳۰ متر',
        'meaning': 'پل ارتباط زمین و آسمان',
        'numbers': [7, 30, 60]
    },
    'babylon': {
        'name': 'Etemenanki (زیگورات بابل)',
        'god': 'Marduk',
        'levels': 7,
        'height': 'حدود ۹۱ متر',
        'meaning': 'خانه شالوده آسمان و زمین',
        'numbers': [7, 50]
    },
    'chogha_zanbil': {
        'name': 'زیگورات چغازنبیل',
        'god': 'Inshushinak',
        'levels': 5,
        'height': 'حدود ۲۵ متر',
        'meaning': 'معبد عیلامی',
        'numbers': [5, 7]
    }
}

# ==================== سیستم عددی بابلی ====================
BABYLONIAN_NUMERALS = {
    'base': 60,
    'symbols': {
        '1': '𐎫',
        '10': '𐎬',
        '60': '𐎭'
    },
    'planets': {
        'Jupiter': 11,
        'Venus': 15,
        'Saturn': 10,
        'Mercury': 28,
        'Mars': 35,
        'Sun': 20,
        'Moon': 30
    }
}

# ==================== اوراکل‌های کلدانی ====================
CHALDEAN_ORACLES = [
    {
        'number': 1,
        'text': '''
        در آغاز، وحدت بود. از وحدت، دوگانگی زاده شد.
        از دوگانگی، سه‌گانگی، و از سه‌گانگی، همه اعداد.
        ''',
        'meaning': 'اصل آفرینش از طریق اعداد'
    },
    {
        'number': 7,
        'text': '''
        هفت دروازه را باید گذشت تا به نور رسید.
        هفت طبقه زیگورات، هفت آسمان، هفت خدای سرنوشت.
        ''',
        'meaning': 'سیر صعودی روح'
    },
    {
        'number': 12,
        'text': '''
        دوازده ماه، دوازده برج، دوازده نام خدا.
        در دوازده، کمال زمان نهفته است.
        ''',
        'meaning': 'چرخه کامل زمان'
    },
    {
        'number': 60,
        'text': '''
        شصت، عدد خدایان است. شصت ثانیه، شصت دقیقه،
        شصت سال - همه از یک منبع می‌آیند.
        ''',
        'meaning': 'کمال عددی'
    }
]

# ==================== نجوم کلدانی ====================
CHALDEAN_ASTRONOMY = {
    'planets': {
        'Shamash': {'name': 'خورشید', 'number': 20},
        'Sin': {'name': 'ماه', 'number': 30},
        'Nergal': {'name': 'مریخ', 'number': 14},
        'Nabu': {'name': 'عطارد', 'number': 12},
        'Marduk': {'name': 'مشتری', 'number': 11},
        'Ishtar': {'name': 'زهره', 'number': 15},
        'Ninurta': {'name': 'زحل', 'number': 10}
    },
    'constellations': [
        'The Bull', 'The Lion', 'The Scorpion', 'The Fish',
        'The Ram', 'The Twins', 'The Crab', 'The Virgin',
        'The Balance', 'The Archer', 'The Goat', 'The Water Pourer'
    ],
    'eclipses': 'پیش‌بینی خورشیدگرفتگی با اعداد'
}

# ==================== روش عددشناسی کلدانی ====================
CHALDEAN_METHOD = '''
روش کلدانی (قدیمی‌ترین روش):

۱. هر حرف یک عدد دارد (سیستم کلدانی)
۲. اعداد ۱ تا ۸ استفاده می‌شوند (۹ مقدس است)
۳. نام کامل محاسبه می‌شود
۴. عدد ریشه به دست می‌آید

نکته مهم: در سیستم کلدانی، عدد ۹ هرگز استفاده نمی‌شود 
زیرا مقدس است و به خدایان تعلق دارد.
'''

# ==================== طلسم‌های عددی کلدانی ====================
NUMERICAL_AMULETS = {
    1: 'طلسم آنو - برای محافظت و قدرت',
    2: 'طلسم انلیل - برای فرمانروایی',
    3: 'طلسم انکی - برای خرد',
    4: 'طلسم نینهورساگ - برای باروری',
    5: 'طلسم سین - برای زمان و پیش‌گویی',
    6: 'طلسم شمش - برای عدالت',
    7: 'طلسم ایشتار - برای عشق',
    8: 'طلسم نابو - برای دانش',
    9: 'طلسم نرگال - برای محافظت در سفر'
}

# ==================== نقل قول‌های کلدانی ====================
QUOTES = [
    "Numbers are the thoughts of the gods.",
    "The universe was created by number and measure.",
    "In the beginning was the One, and the One became many.",
    "Seven is the number of completion.",
    "Sixty is the number of the divine.",
    "The stars write our destiny in numbers.",
    "Know the numbers, and you will know the gods."
]

# ==================== کتابشناسی کلدانی ====================
BIBLIOGRAPHY = [
    "The Chaldean Oracles - Translated by William Wynn Westcott",
    "Babylonian Magic and Sorcery - Leonard W. King",
    "The Religion of Babylonia and Assyria - Morris Jastrow",
    "Cuneiform Texts from Babylonian Tablets - British Museum",
    "The Epic of Gilgamesh (Tablets)",
    "Enuma Elish (Babylonian Creation Myth)"
]

BOOK_DATA['content'] = f"""
{BOOK_DATA['summary']}

# CHALDEAN DEITIES (خدایان کلدانی)
{json.dumps(CHALDEAN_DEITIES, indent=2, ensure_ascii=False)}

# SACRED NUMBERS (اعداد مقدس)
{json.dumps(SACRED_NUMBERS, indent=2, ensure_ascii=False)}

# ZIGGURATS (زیگورات‌ها)
{json.dumps(ZIGGURATS, indent=2, ensure_ascii=False)}

# BABYLONIAN NUMERALS (اعداد بابلی)
{json.dumps(BABYLONIAN_NUMERALS, indent=2, ensure_ascii=False)}

# CHALDEAN ORACLES (اوراکل‌های کلدانی)
{json.dumps(CHALDEAN_ORACLES, indent=2, ensure_ascii=False)}

# CHALDEAN ASTRONOMY (نجوم کلدانی)
{json.dumps(CHALDEAN_ASTRONOMY, indent=2, ensure_ascii=False)}

# NUMERICAL AMULETS (طلسم‌های عددی)
{json.dumps(NUMERICAL_AMULETS, indent=2, ensure_ascii=False)}

{CHALDEAN_METHOD}

# QUOTES
{json.dumps(QUOTES, indent=2, ensure_ascii=False)}

# BIBLIOGRAPHY
{json.dumps(BIBLIOGRAPHY, indent=2, ensure_ascii=False)}
"""
