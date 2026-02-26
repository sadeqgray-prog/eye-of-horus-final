import json

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📖 THREE BOOKS OF OCCULT PHILOSOPHY
نوشته: Heinrich Cornelius Agrippa
کامل‌ترین منبع فلسفه غربی، جادوی اعداد، و کابالای مسیحی
نسخه کامل با تمام دانش
"""

BOOK_DATA = {
    'title': 'Three Books of Occult Philosophy',
    'author': 'Heinrich Cornelius Agrippa von Nettesheim',
    'year': 1531,
    'subjects': ['Occult', 'Magic', 'Kabbalah', 'Numerology', 'Astrology', 'Alchemy'],
    'language': 'Latin (ترجمه شده)',
    'summary': '''
    Agrippa's magnum opus, synthesizing all of Western occult tradition.
    It covers the three worlds: elemental, celestial, and intellectual.
    The book is the foundation of Western ceremonial magic and contains
    extensive material on the magical properties of numbers, the Kabbalah,
    and the relationship between the microcosm and macrocosm.
    ''',
    'keywords': [
        'occult philosophy', 'magic', 'kabbalah', 'four elements', 'celestial spheres',
        'divine names', 'angelic magic', 'planetary hours', 'numerical squares',
        'talismans', 'sigils', 'theurgy', 'goetia', 'alchemy', 'astrology'
    ]
}

# ==================== سه جهان (The Three Worlds) ====================
THREE_WORLDS = {
    'elemental': {
        'name': 'The Elemental World',
        'description': 'The physical world of the four elements',
        'elements': ['Earth', 'Water', 'Air', 'Fire'],
        'governing': 'The physical body and material existence',
        'magic': 'Natural magic - herbs, stones, animals',
        'numbers': [1, 2, 3, 4],
        'sephirah': 'Malkuth'
    },
    'celestial': {
        'name': 'The Celestial World',
        'description': 'The astral world of the planets and stars',
        'planets': ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'],
        'governing': 'The soul and astral body',
        'magic': 'Celestial magic - planetary influences, talismans',
        'numbers': [5, 6, 7, 8],
        'sephirah': 'Yesod, Hod, Netzach, Tiphareth'
    },
    'intellectual': {
        'name': 'The Intellectual World',
        'description': 'The divine world of the Sephiroth and angels',
        'sephiroth': ['Kether', 'Chokmah', 'Binah', 'Chesed', 'Geburah', 'Tiphareth', 
                     'Netzach', 'Hod', 'Yesod', 'Malkuth'],
        'governing': 'The spirit and divine intellect',
        'magic': 'Ceremonial magic - angelic invocation, divine names',
        'numbers': [9, 10, 11, 22],
        'sephirah': 'All'
    }
}

# ==================== اعداد در فلسفه آگریپا ====================
AGRIPPA_NUMBERS = {
    1: {
        'name': 'The Monad',
        'divine_name': 'אֶהְיֶה (Eheieh)',
        'angel': 'Metatron',
        'sephirah': 'Kether',
        'planet': 'Primum Mobile',
        'meaning': '''
        The One, the source of all numbers. In the intellectual world, it represents
        the Divine Will. In the celestial world, the Primum Mobile. In the elemental
        world, the point from which all extension proceeds.
        ''',
        'magical_square': [
            [1]
        ],
        'sum': 1,
        'talisman': 'For unity, focus, divine connection'
    },
    2: {
        'name': 'The Duad',
        'divine_name': 'יָה (Yah)',
        'angel': 'Ratziel',
        'sephirah': 'Chokmah',
        'planet': 'The Zodiac',
        'meaning': '''
        The number of wisdom and the beginning of manifestation. It represents the
        first reflection of the One, the principle of duality that underlies creation.
        In Kabbalah, it is the first flash of wisdom.
        ''',
        'magical_square': [
            [4, 1],
            [2, 3]
        ],
        'sum': 5,
        'talisman': 'For wisdom, knowledge, understanding'
    },
    3: {
        'name': 'The Triad',
        'divine_name': 'יְהוָה אֱלֹהִים (YHVH Elohim)',
        'angel': 'Tzaphkiel',
        'sephirah': 'Binah',
        'planet': 'Saturn',
        'meaning': '''
        The number of understanding and form. It represents the first complete number,
        having beginning, middle, and end. In Kabbalah, it is the receptive womb of
        Binah, giving form to the wisdom of Chokmah.
        ''',
        'magical_square': [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ],
        'sum': 15,
        'talisman': 'For understanding, completion, manifestation'
    },
    4: {
        'name': 'The Tetrad',
        'divine_name': 'אֵל (El)',
        'angel': 'Tzadkiel',
        'sephirah': 'Chesed',
        'planet': 'Jupiter',
        'meaning': '''
        The number of mercy and expansion. It represents the four elements, the four
        directions, the four letters of the Tetragrammaton. In Kabbalah, it is the
        expansive force of Chesed.
        ''',
        'magical_square': [
            [4, 14, 15, 1],
            [9, 7, 6, 12],
            [5, 11, 10, 8],
            [16, 2, 3, 13]
        ],
        'sum': 34,
        'talisman': 'For expansion, mercy, abundance'
    },
    5: {
        'name': 'The Pentad',
        'divine_name': 'אֱלֹהִים גִּבּוֹר (Elohim Gibor)',
        'angel': 'Khamael',
        'sephirah': 'Geburah',
        'planet': 'Mars',
        'meaning': '''
        The number of severity and strength. It represents the five senses, the five
        wounds of Christ, the five books of the Torah. In Kabbalah, it is the
        restrictive force of Geburah.
        ''',
        'magical_square': [
            [11, 24, 7, 20, 3],
            [4, 12, 25, 8, 16],
            [17, 5, 13, 21, 9],
            [10, 18, 1, 14, 22],
            [23, 6, 19, 2, 15]
        ],
        'sum': 65,
        'talisman': 'For strength, courage, protection'
    },
    6: {
        'name': 'The Hexad',
        'divine_name': 'יְהוָה אֱלֹהַ וָדַעַת (YHVH Eloah va-Da\'at)',
        'angel': 'Raphael',
        'sephirah': 'Tiphareth',
        'planet': 'Sun',
        'meaning': '''
        The number of beauty and harmony. It represents the six days of creation,
        the six directions of space. In Kabbalah, it is the central point of
        Tiphareth, the beauty that harmonizes all forces.
        ''',
        'magical_square': [
            [6, 32, 3, 34, 35, 1],
            [7, 11, 27, 28, 8, 30],
            [19, 14, 16, 15, 23, 24],
            [18, 20, 22, 21, 17, 13],
            [25, 29, 10, 9, 26, 12],
            [36, 5, 33, 4, 2, 31]
        ],
        'sum': 111,
        'talisman': 'For harmony, beauty, healing'
    },
    7: {
        'name': 'The Heptad',
        'divine_name': 'יְהוָה צְבָאוֹת (YHVH Tzabaoth)',
        'angel': 'Haniel',
        'sephirah': 'Netzach',
        'planet': 'Venus',
        'meaning': '''
        The number of victory and eternity. It represents the seven classical planets,
        the seven days of the week, the seven metals of alchemy. In Kabbalah, it is
        the eternal victory of Netzach.
        ''',
        'magical_square': [
            [22, 47, 16, 41, 10, 35, 4],
            [5, 23, 48, 17, 42, 11, 29],
            [30, 6, 24, 49, 18, 36, 12],
            [13, 31, 7, 25, 43, 19, 37],
            [38, 14, 32, 1, 26, 44, 20],
            [21, 39, 8, 33, 2, 27, 45],
            [46, 15, 40, 9, 34, 3, 28]
        ],
        'sum': 175,
        'talisman': 'For victory, love, eternity'
    },
    8: {
        'name': 'The Ogdoad',
        'divine_name': 'אֱלֹהִים צְבָאוֹת (Elohim Tzabaoth)',
        'angel': 'Michael',
        'sephirah': 'Hod',
        'planet': 'Mercury',
        'meaning': '''
        The number of splendor and intellect. It represents the eight Beatitudes,
        the eight directions of the compass. In Kabbalah, it is the intellectual
        splendor of Hod.
        ''',
        'magical_square': [
            [8, 58, 59, 5, 4, 62, 63, 1],
            [49, 15, 14, 52, 53, 11, 10, 56],
            [41, 23, 22, 44, 45, 19, 18, 48],
            [32, 34, 35, 29, 28, 38, 39, 25],
            [40, 26, 27, 37, 36, 30, 31, 33],
            [17, 47, 46, 20, 21, 43, 42, 24],
            [9, 55, 54, 12, 13, 51, 50, 16],
            [64, 2, 3, 61, 60, 6, 7, 57]
        ],
        'sum': 260,
        'talisman': 'For intellect, communication, writing'
    },
    9: {
        'name': 'The Ennead',
        'divine_name': 'שַׁדַּי אֵל חַי (Shaddai El Chai)',
        'angel': 'Gabriel',
        'sephirah': 'Yesod',
        'planet': 'Moon',
        'meaning': '''
        The number of foundation and the subconscious. It represents the nine orders
        of angels, the nine months of gestation. In Kabbalah, it is the foundation
        of Yesod, the lunar sphere that connects the physical and spiritual.
        ''',
        'magical_square': [
            [37, 78, 29, 70, 21, 62, 13, 54, 5],
            [6, 38, 79, 30, 71, 22, 63, 14, 46],
            [47, 7, 39, 80, 31, 72, 23, 55, 15],
            [16, 48, 8, 40, 81, 32, 64, 24, 56],
            [57, 17, 49, 9, 41, 73, 33, 65, 25],
            [26, 58, 18, 50, 1, 42, 74, 34, 66],
            [67, 27, 59, 10, 51, 2, 43, 75, 35],
            [36, 68, 19, 60, 11, 52, 3, 44, 76],
            [77, 28, 69, 20, 61, 12, 53, 4, 45]
        ],
        'sum': 369,
        'talisman': 'For foundation, intuition, dreams'
    },
    10: {
        'name': 'The Decad',
        'divine_name': 'אֲדֹנָי הָאָרֶץ (Adonai ha-Aretz)',
        'angel': 'Sandalphon',
        'sephirah': 'Malkuth',
        'planet': 'Earth',
        'meaning': '''
        The number of completion and manifestation. It represents the ten Sephiroth,
        the Ten Commandments. In Kabbalah, it is the Kingdom of Malkuth, the final
        manifestation of all divine forces in the physical world.
        ''',
        'magical_square': [
            [92, 99, 1, 8, 15, 67, 74, 51, 58, 40],
            [98, 80, 7, 14, 16, 73, 55, 57, 64, 41],
            [4, 6, 88, 95, 22, 54, 56, 63, 70, 47],
            [85, 87, 19, 21, 3, 60, 62, 69, 71, 28],
            [86, 93, 25, 2, 9, 61, 68, 75, 52, 34],
            [17, 24, 76, 83, 90, 42, 49, 26, 33, 65],
            [23, 5, 82, 89, 91, 48, 30, 32, 39, 66],
            [79, 81, 13, 20, 97, 29, 31, 38, 45, 72],
            [10, 12, 94, 96, 78, 35, 37, 44, 46, 53],
            [11, 18, 100, 77, 84, 36, 43, 50, 27, 59]
        ],
        'sum': 505,
        'talisman': 'For manifestation, completion, grounding'
    }
}

# ==================== مربع‌های جادویی (Magical Squares) ====================
MAGICAL_SQUARES = {
    'saturn': AGRIPPA_NUMBERS[3]['magical_square'],
    'jupiter': AGRIPPA_NUMBERS[4]['magical_square'],
    'mars': AGRIPPA_NUMBERS[5]['magical_square'],
    'sun': AGRIPPA_NUMBERS[6]['magical_square'],
    'venus': AGRIPPA_NUMBERS[7]['magical_square'],
    'mercury': AGRIPPA_NUMBERS[8]['magical_square'],
    'moon': AGRIPPA_NUMBERS[9]['magical_square'],
    'earth': AGRIPPA_NUMBERS[10]['magical_square']
}

# ==================== ساعات سیاره‌ای (Planetary Hours) ====================
PLANETARY_HOURS = {
    'sunday': ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars'],
    'monday': ['Moon', 'Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury'],
    'tuesday': ['Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter'],
    'wednesday': ['Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus'],
    'thursday': ['Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'Saturn'],
    'friday': ['Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars', 'Sun'],
    'saturday': ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
}

# ==================== طلسم‌ها و تعویذها (Talismans) ====================
TALISMANS = {
    'sun': {
        'metal': 'Gold',
        'day': 'Sunday',
        'angel': 'Michael',
        'purpose': 'Glory, wealth, favor, advancement',
        'square': AGRIPPA_NUMBERS[6]['magical_square'],
        'sigil': '☉',
        'colors': ['Gold', 'Yellow', 'Orange']
    },
    'moon': {
        'metal': 'Silver',
        'day': 'Monday',
        'angel': 'Gabriel',
        'purpose': 'Travel, dreams, intuition, messages',
        'square': AGRIPPA_NUMBERS[9]['magical_square'],
        'sigil': '☽',
        'colors': ['Silver', 'White', 'Pale Blue']
    },
    'mercury': {
        'metal': 'Mercury',
        'day': 'Wednesday',
        'angel': 'Raphael',
        'purpose': 'Intellect, communication, writing, commerce',
        'square': AGRIPPA_NUMBERS[8]['magical_square'],
        'sigil': '☿',
        'colors': ['Yellow', 'Purple', 'Mixed']
    },
    'venus': {
        'metal': 'Copper',
        'day': 'Friday',
        'angel': 'Haniel',
        'purpose': 'Love, friendship, beauty, art',
        'square': AGRIPPA_NUMBERS[7]['magical_square'],
        'sigil': '♀',
        'colors': ['Green', 'Pink', 'White']
    },
    'mars': {
        'metal': 'Iron',
        'day': 'Tuesday',
        'angel': 'Khamael',
        'purpose': 'Courage, victory, protection, war',
        'square': AGRIPPA_NUMBERS[5]['magical_square'],
        'sigil': '♂',
        'colors': ['Red', 'Orange', 'Black']
    },
    'jupiter': {
        'metal': 'Tin',
        'day': 'Thursday',
        'angel': 'Tzadkiel',
        'purpose': 'Expansion, abundance, honor, wealth',
        'square': AGRIPPA_NUMBERS[4]['magical_square'],
        'sigil': '♃',
        'colors': ['Blue', 'Purple', 'White']
    },
    'saturn': {
        'metal': 'Lead',
        'day': 'Saturday',
        'angel': 'Tzaphkiel',
        'purpose': 'Protection, binding, discipline, time',
        'square': AGRIPPA_NUMBERS[3]['magical_square'],
        'sigil': '♄',
        'colors': ['Black', 'Indigo', 'Dark Blue']
    }
}

# ==================== اسامی الهی (Divine Names) ====================
DIVINE_NAMES = {
    'hebrew': {
        'Eheieh': {'meaning': 'I Am', 'number': 21, 'sephirah': 'Kether'},
        'Yah': {'meaning': 'He Who Is', 'number': 15, 'sephirah': 'Chokmah'},
        'YHVH Elohim': {'meaning': 'Lord God', 'number': 26, 'sephirah': 'Binah'},
        'El': {'meaning': 'God', 'number': 31, 'sephirah': 'Chesed'},
        'Elohim Gibor': {'meaning': 'Mighty God', 'number': 216, 'sephirah': 'Geburah'},
        'YHVH Eloah va-Daat': {'meaning': 'Lord God of Knowledge', 'number': 71, 'sephirah': 'Tiphareth'},
        'YHVH Tzabaoth': {'meaning': 'Lord of Hosts', 'number': 26, 'sephirah': 'Netzach'},
        'Elohim Tzabaoth': {'meaning': 'God of Hosts', 'number': 156, 'sephirah': 'Hod'},
        'Shaddai El Chai': {'meaning': 'Almighty Living God', 'number': 363, 'sephirah': 'Yesod'},
        'Adonai ha-Aretz': {'meaning': 'Lord of the Earth', 'number': 671, 'sephirah': 'Malkuth'}
    },
    'greek': {
        'Theos': {'meaning': 'God', 'number': 284},
        'Kosmos': {'meaning': 'World', 'number': 600},
        'Sophia': {'meaning': 'Wisdom', 'number': 781},
        'Phos': {'meaning': 'Light', 'number': 1500},
        'Zoe': {'meaning': 'Life', 'number': 815}
    },
    'latin': {
        'Deus': {'meaning': 'God', 'number': 306},
        'Mundus': {'meaning': 'World', 'number': 714},
        'Sapientia': {'meaning': 'Wisdom', 'number': 583},
        'Lux': {'meaning': 'Light', 'number': 63},
        'Vita': {'meaning': 'Life', 'number': 312}
    }
}

# ==================== تناسبات هارمونیک (Harmonic Proportions) ====================
HARMONIC_PROPORTIONS = {
    'unison': {'ratio': '1:1', 'planet': 'Sun', 'number': 1},
    'octave': {'ratio': '2:1', 'planet': 'Moon', 'number': 2},
    'fifth': {'ratio': '3:2', 'planet': 'Mercury', 'number': 3},
    'fourth': {'ratio': '4:3', 'planet': 'Venus', 'number': 4},
    'third': {'ratio': '5:4', 'planet': 'Mars', 'number': 5},
    'sixth': {'ratio': '5:3', 'planet': 'Jupiter', 'number': 6},
    'seventh': {'ratio': '15:8', 'planet': 'Saturn', 'number': 7},
    'whole_tone': {'ratio': '9:8', 'element': 'Air', 'number': 8},
    'half_tone': {'ratio': '16:15', 'element': 'Water', 'number': 9}
}

# ==================== عناصر چهارگانه (Four Elements) ====================
FOUR_ELEMENTS = {
    'fire': {
        'direction': 'South',
        'quality': 'Hot & Dry',
        'active': True,
        'season': 'Summer',
        'time': 'Noon',
        'color': 'Red',
        'angel': 'Michael',
        'animal': 'Lion',
        'elemental': 'Salamander',
        'number': 1,
        'body': 'Vitality, metabolism',
        'soul': 'Will, passion',
        'spirit': 'Inspiration'
    },
    'earth': {
        'direction': 'North',
        'quality': 'Cold & Dry',
        'active': False,
        'season': 'Winter',
        'time': 'Midnight',
        'color': 'Green/Brown',
        'angel': 'Uriel',
        'animal': 'Bull',
        'elemental': 'Gnome',
        'number': 2,
        'body': 'Structure, bones',
        'soul': 'Stability, patience',
        'spirit': 'Manifestation'
    },
    'air': {
        'direction': 'East',
        'quality': 'Hot & Wet',
        'active': True,
        'season': 'Spring',
        'time': 'Dawn',
        'color': 'Yellow',
        'angel': 'Raphael',
        'animal': 'Eagle',
        'elemental': 'Sylph',
        'number': 3,
        'body': 'Breath, nervous system',
        'soul': 'Intellect, thought',
        'spirit': 'Communication'
    },
    'water': {
        'direction': 'West',
        'quality': 'Cold & Wet',
        'active': False,
        'season': 'Autumn',
        'time': 'Dusk',
        'color': 'Blue',
        'angel': 'Gabriel',
        'animal': 'Fish',
        'elemental': 'Undine',
        'number': 4,
        'body': 'Fluids, emotions',
        'soul': 'Feelings, intuition',
        'spirit': 'Compassion'
    }
}

# ==================== روش محاسبه عددی آگریپا ====================
AGRIPPA_METHOD = '''
روش آگریپا برای محاسبه اعداد:

1. Pythagorean reduction (کاهش فیثاغورثی)
2. Kabbalistic gematria (جماتریا)
3. Planetary attribution (تخصیص سیاره‌ای)
4. Elemental balance (تعادل عنصری)

سه سطح تحلیل:
- Elemental World: اعداد ۱-۴ (عناصر)
- Celestial World: اعداد ۵-۸ (سیارات)
- Intellectual World: اعداد ۹-۱۰ (سفیروت)

هر عدد یک مربع جادویی دارد که جمع هر سطر آن برابر است با:
Sum = n × (n² + 1) / 2
'''

# ==================== نقل قول‌های آگریپا ====================
QUOTES = [
    "The numbers have a power that cannot be resisted by either gods or men.",
    "As above, so below; as within, so without.",
    "The soul of the world is the universal spirit that contains all things.",
    "There is no number without its own particular virtue and power.",
    "The world is threefold: elemental, celestial, and intellectual.",
    "Every number is a key to the divine.",
    "The magician must know the correspondences between all things."
]

BOOK_DATA['content'] = f"""
{BOOK_DATA['summary']}

# THE THREE WORLDS
{json.dumps(THREE_WORLDS, indent=2, ensure_ascii=False)}

# NUMBERS AND THEIR MAGICAL SQUARES
{json.dumps(AGRIPPA_NUMBERS, indent=2, ensure_ascii=False)}

# PLANETARY HOURS
{json.dumps(PLANETARY_HOURS, indent=2, ensure_ascii=False)}

# TALISMANS AND THEIR CORRESPONDENCES
{json.dumps(TALISMANS, indent=2, ensure_ascii=False)}

# DIVINE NAMES
{json.dumps(DIVINE_NAMES, indent=2, ensure_ascii=False)}

# HARMONIC PROPORTIONS
{json.dumps(HARMONIC_PROPORTIONS, indent=2, ensure_ascii=False)}

# FOUR ELEMENTS
{json.dumps(FOUR_ELEMENTS, indent=2, ensure_ascii=False)}

{AGRIPPA_METHOD}

# QUOTES
{json.dumps(QUOTES, indent=2, ensure_ascii=False)}
"""
