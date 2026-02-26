import json
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📖 THE KABBALAH OF NUMBERS
نوشته: Sepharial (Walter Gorn Old)
منبع اصلی عددشناسی کابالیستی و طالع‌بینی اعداد
"""

BOOK_DATA = {
    'title': 'The Kabbalah of Numbers',
    'author': 'Sepharial (Walter Gorn Old)',
    'year': 1913,
    'subjects': ['Kabbalah', 'Numerology', 'Astrology', 'Mysticism'],
    'language': 'English',
    'summary': '''
    A comprehensive work on the mystical significance of numbers,
    combining Kabbalistic wisdom with practical numerology. Sepharial
    explores the relationship between numbers, human character, and destiny.
    ''',
    'keywords': [
        'kabbalah', 'numbers', 'destiny', 'character', 'vibration',
        'sephiroth', 'tree of life', 'gematria', 'notarikon', 'temurah'
    ]
}

# ==================== اصول کابالیستی ====================
KABBALISTIC_PRINCIPLES = {
    'gematria': '''
    The science of numerical values of Hebrew letters. Each letter has a
    numerical value, and words with equal values are considered to have
    a mystical connection.
    ''',
    'notarikon': '''
    The art of forming words from the initial or final letters of other
    words. Used to find hidden meanings in sacred texts.
    ''',
    'temurah': '''
    The science of permutation of letters. Based on the idea that letters
    can be rearranged to reveal hidden meanings and correspondences.
    '''
}

# ==================== Sephiroth (ده سفیروت) ====================
SEPHIROTH = {
    1: {
        'name': 'Kether',
        'meaning': 'The Crown',
        'description': 'The first emanation, pure consciousness, the point of creation',
        'number': 1,
        'divine_name': 'Eheieh',
        'archangel': 'Metatron',
        'color': 'White',
        'planet': 'Neptune',
        'experience': 'Union with God'
    },
    2: {
        'name': 'Chokmah',
        'meaning': 'Wisdom',
        'description': 'The first outpouring of creative energy, the Father',
        'number': 2,
        'divine_name': 'Yah',
        'archangel': 'Raziel',
        'color': 'Gray',
        'planet': 'Uranus',
        'experience': 'Vision of God'
    },
    3: {
        'name': 'Binah',
        'meaning': 'Understanding',
        'description': 'The receptive womb, the Mother, form-giving',
        'number': 3,
        'divine_name': 'YHVH Elohim',
        'archangel': 'Tzaphkiel',
        'color': 'Black',
        'planet': 'Saturn',
        'experience': 'Sorrow of God'
    },
    4: {
        'name': 'Chesed',
        'meaning': 'Mercy',
        'description': 'Love, compassion, expansive force',
        'number': 4,
        'divine_name': 'El',
        'archangel': 'Tzadkiel',
        'color': 'Blue',
        'planet': 'Jupiter',
        'experience': 'Vision of Love'
    },
    5: {
        'name': 'Geburah',
        'meaning': 'Severity',
        'description': 'Strength, judgment, restrictive force',
        'number': 5,
        'divine_name': 'Elohim Gibor',
        'archangel': 'Khamael',
        'color': 'Red',
        'planet': 'Mars',
        'experience': 'Vision of Power'
    },
    6: {
        'name': 'Tiphareth',
        'meaning': 'Beauty',
        'description': 'Harmony, balance, the center',
        'number': 6,
        'divine_name': 'YHVH Eloah va-Da\'at',
        'archangel': 'Raphael',
        'color': 'Yellow',
        'planet': 'Sun',
        'experience': 'Vision of Harmony'
    },
    7: {
        'name': 'Netzach',
        'meaning': 'Victory',
        'description': 'Eternity, victory, feeling',
        'number': 7,
        'divine_name': 'YHVH Tzabaoth',
        'archangel': 'Haniel',
        'color': 'Green',
        'planet': 'Venus',
        'experience': 'Vision of Beauty'
    },
    8: {
        'name': 'Hod',
        'meaning': 'Splendor',
        'description': 'Glory, splendor, intellect',
        'number': 8,
        'divine_name': 'Elohim Tzabaoth',
        'archangel': 'Michael',
        'color': 'Orange',
        'planet': 'Mercury',
        'experience': 'Vision of Splendor'
    },
    9: {
        'name': 'Yesod',
        'meaning': 'Foundation',
        'description': 'Foundation, subconscious, lunar realm',
        'number': 9,
        'divine_name': 'Shaddai El Chai',
        'archangel': 'Gabriel',
        'color': 'Purple',
        'planet': 'Moon',
        'experience': 'Vision of the Machinery'
    },
    10: {
        'name': 'Malkuth',
        'meaning': 'Kingdom',
        'description': 'The physical world, manifestation',
        'number': 10,
        'divine_name': 'Adonai ha-Aretz',
        'archangel': 'Sandalphon',
        'color': 'Citrine, Olive, Russet, Black',
        'planet': 'Earth',
        'experience': 'Vision of the Holy Guardian Angel'
    }
}

# ==================== اعداد و شخصیت ====================
PERSONALITY_NUMBERS = {
    1: {
        'name': 'The Individualist',
        'positive': 'Independent, creative, pioneering, determined',
        'negative': 'Selfish, arrogant, domineering, lonely',
        'kabbalistic': 'Kether - the point of individuality'
    },
    2: {
        'name': 'The Diplomat',
        'positive': 'Cooperative, sensitive, intuitive, tactful',
        'negative': 'Indecisive, moody, dependent, self-deprecating',
        'kabbalistic': 'Chokmah and Binah - duality and polarity'
    },
    3: {
        'name': 'The Communicator',
        'positive': 'Expressive, optimistic, creative, social',
        'negative': 'Scattered, superficial, exaggerating, gossip',
        'kabbalistic': 'Binah - the threefold nature of understanding'
    },
    4: {
        'name': 'The Builder',
        'positive': 'Practical, disciplined, reliable, organized',
        'negative': 'Rigid, stubborn, limited, controlling',
        'kabbalistic': 'Chesed - the fourfold mercy'
    },
    5: {
        'name': 'The Adventurer',
        'positive': 'Adaptable, freedom-loving, progressive, curious',
        'negative': 'Restless, inconsistent, escapist, irresponsible',
        'kabbalistic': 'Geburah - the five severities'
    },
    6: {
        'name': 'The Nurturer',
        'positive': 'Responsible, loving, compassionate, harmonious',
        'negative': 'Meddlesome, worried, self-sacrificing, interfering',
        'kabbalistic': 'Tiphareth - the sixfold beauty'
    },
    7: {
        'name': 'The Seeker',
        'positive': 'Analytical, intuitive, spiritual, wise',
        'negative': 'Cynical, isolated, secretive, aloof',
        'kabbalistic': 'Netzach - the sevenfold victory'
    },
    8: {
        'name': 'The Achiever',
        'positive': 'Ambitious, efficient, authoritative, successful',
        'negative': 'Materialistic, greedy, workaholic, controlling',
        'kabbalistic': 'Hod - the eightfold splendor'
    },
    9: {
        'name': 'The Humanitarian',
        'positive': 'Compassionate, generous, artistic, idealistic',
        'negative': 'Emotional, reckless, impractical, resentful',
        'kabbalistic': 'Yesod - the ninefold foundation'
    }
}

# ==================== اعداد سرنوشت ====================
DESTINY_NUMBERS = {
    1: 'To lead, innovate, and pioneer new paths',
    2: 'To cooperate, mediate, and bring harmony',
    3: 'To express, create, and inspire joy',
    4: 'To build, organize, and create stability',
    5: 'To explore, adapt, and embrace change',
    6: 'To nurture, love, and serve others',
    7: 'To analyze, seek truth, and share wisdom',
    8: 'To achieve, manifest, and lead with power',
    9: 'To complete, heal, and serve humanity'
}

# ==================== چرخه‌های زندگی ====================
LIFE_CYCLES = {
    'youth': {
        'years': '0-27',
        'influence': 'Moon and Venus',
        'focus': 'Emotional development, relationships'
    },
    'middle': {
        'years': '28-55',
        'influence': 'Sun and Mars',
        'focus': 'Career, achievement, self-expression'
    },
    'mature': {
        'years': '56+',
        'influence': 'Jupiter and Saturn',
        'focus': 'Wisdom, legacy, spiritual growth'
    }
}

# ==================== روزهای خوش شانس ====================
LUCKY_DAYS = {
    1: ['Sunday'],
    2: ['Monday'],
    3: ['Thursday'],
    4: ['Saturday'],
    5: ['Wednesday'],
    6: ['Friday'],
    7: ['Monday'],
    8: ['Saturday'],
    9: ['Tuesday']
}

# ==================== رنگ‌ها و جواهرات ====================
COLORS_GEMS = {
    1: {'colors': ['Gold', 'Yellow', 'Orange'], 'gems': ['Ruby', 'Garnet']},
    2: {'colors': ['White', 'Silver', 'Pale Blue'], 'gems': ['Pearl', 'Moonstone']},
    3: {'colors': ['Purple', 'Lavender', 'Blue'], 'gems': ['Amethyst', 'Sapphire']},
    4: {'colors': ['Blue', 'Green', 'Brown'], 'gems': ['Sapphire', 'Emerald']},
    5: {'colors': ['Light Blue', 'Gray', 'Yellow'], 'gems': ['Topaz', 'Citrine']},
    6: {'colors': ['Pink', 'Green', 'Rose'], 'gems': ['Rose Quartz', 'Jade']},
    7: {'colors': ['Violet', 'Sea Green', 'Indigo'], 'gems': ['Amethyst', 'Lapis Lazuli']},
    8: {'colors': ['Black', 'Dark Blue', 'Brown'], 'gems': ['Onyx', 'Black Tourmaline']},
    9: {'colors': ['Red', 'Crimson', 'Pink'], 'gems': ['Garnet', 'Red Jasper']}
}

# ==================== روش محاسبه کابالیستی ====================
KABBALISTIC_METHOD = '''
برای محاسبه عدد کابالیستی یک نام:

1. حروف عبری نام را پیدا کنید (ترجمه کنید)
2. هر حرف ارزش عددی خود را دارد
3. اعداد را جمع کنید
4. به رقم ریشه کاهش دهید

ارزش حروف عبری:
א (Aleph) = 1
ב (Beth) = 2
ג (Gimel) = 3
ד (Daleth) = 4
ה (He) = 5
ו (Vav) = 6
ז (Zayin) = 7
ח (Cheth) = 8
ט (Teth) = 9
י (Yod) = 10
כ (Kaph) = 20
ל (Lamed) = 30
מ (Mem) = 40
נ (Nun) = 50
ס (Samekh) = 60
ע (Ayin) = 70
פ (Pe) = 80
צ (Tzaddi) = 90
ק (Qoph) = 100
ר (Resh) = 200
ש (Shin) = 300
ת (Tav) = 400
'''

# ==================== نقل قول‌های سفیاریال ====================
QUOTES = [
    "Numbers are the keys to the universe.",
    "The Kabbalah teaches that all things are numbers.",
    "Your name is your destiny.",
    "The vibration of numbers affects all of life.",
    "In the Tree of Life, all paths lead to understanding.",
    "The number reveals the nature of the thing.",
    "As above, so below; as within, so without."
]

BOOK_DATA['content'] = f"""
{BOOK_DATA['summary']}

# KABBALISTIC PRINCIPLES
{json.dumps(KABBALISTIC_PRINCIPLES, indent=2, ensure_ascii=False)}

# SEPHIROTH (THE TEN EMANATIONS)
{json.dumps(SEPHIROTH, indent=2, ensure_ascii=False)}

# PERSONALITY NUMBERS
{json.dumps(PERSONALITY_NUMBERS, indent=2, ensure_ascii=False)}

# DESTINY NUMBERS
{json.dumps(DESTINY_NUMBERS, indent=2, ensure_ascii=False)}

# LIFE CYCLES
{json.dumps(LIFE_CYCLES, indent=2, ensure_ascii=False)}

# LUCKY DAYS
{json.dumps(LUCKY_DAYS, indent=2, ensure_ascii=False)}

# COLORS AND GEMS
{json.dumps(COLORS_GEMS, indent=2, ensure_ascii=False)}

# KABBALISTIC METHOD
{KABBALISTIC_METHOD}

# QUOTES
{json.dumps(QUOTES, indent=2, ensure_ascii=False)}
"""
