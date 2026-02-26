import json
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📖 NUMBERS: THEIR OCCULT POWER AND MYSTIC VIRTUE
نوشته: W. Wynn Westcott
منبع اصلی عددشناسی فیثاغورثی و کابالیستی
این کتاب شامل دانش عمیق درباره اعداد و معانی آنهاست
"""

# ==================== اطلاعات کتاب ====================
BOOK_DATA = {
    'title': 'Numbers: Their Occult Power and Mystic Virtue',
    'author': 'William Wynn Westcott',
    'year': 1890,
    'subjects': ['Numerology', 'Pythagorean', 'Kabbalah', 'Mysticism'],
    'language': 'English',
    'source': 'Sacred Texts',
    'summary': '''
    This book is a comprehensive study of the occult meanings of numbers,
    drawing from Pythagorean, Kabbalistic, and other esoteric traditions.
    Westcott explores the mystical properties of numbers from 1 to 10,
    as well as compound numbers and their significance in various traditions.
    ''',
    'keywords': [
        'pythagoras', 'kabbalah', 'mystic numbers', 'sacred geometry',
        'tetractys', 'monad', 'duad', 'triad', 'tetrad', 'decad',
        'apocalyptic numbers', 'gematria', 'theosophic addition'
    ]
}

# ==================== دانش عدد ۱ ====================
NUMBER_1 = {
    'name': 'The Monad',
    'symbol': '•',
    'deity': 'Apollo, Brahma, Odin',
    'element': 'Fire',
    'quality': 'Active',
    'gender': 'Masculine',
    'planet': 'Sun',
    'metal': 'Gold',
    'color': 'Yellow, Gold',
    'gem': 'Ruby, Diamond',
    'meaning': '''
    The Monad represents the Absolute, the Source of all things. It is
    Unity, the One without division. In Pythagorean philosophy, the Monad
    returns to itself and generates all other numbers. It symbolizes:
    - Divine origin
    - Creative power
    - Individuality
    - Leadership
    - Beginning of all things
    ''',
    'pythagorean': '''
    Pythagoras taught that the Monad is the essence of all numbers,
    containing both the seed and the potential of everything that exists.
    The Monad is both odd and even, male and female, containing all
    opposites in perfect balance.
    ''',
    'kabbalistic': '''
    In Kabbalah, the Monad corresponds to Kether, the Crown, the first
    Sephirah. It represents the Divine Will, the initial emanation from
    the Infinite (Ein Sof). It is the point from which all creation
    begins.
    ''',
    'apocalyptic': '''
    In Revelation, the number 1 appears as the One God, the Alpha and
    Omega, the Beginning and the End. It represents the unity of the
    Divine nature.
    ''',
    'personality': '''
    People influenced by number 1 are natural leaders. They are:
    - Independent and self-reliant
    - Creative and innovative
    - Ambitious and determined
    - Original thinkers
    - Often pioneers in their field
    ''',
    'career': ['Leader', 'Entrepreneur', 'Inventor', 'Pioneer', 'Director'],
    'compatible': [1, 3, 5, 7],
    'incompatible': [2, 4, 6, 8]
}

# ==================== دانش عدد ۲ ====================
NUMBER_2 = {
    'name': 'The Duad',
    'symbol': '••',
    'deity': 'Luna, Isis, Mary',
    'element': 'Water',
    'quality': 'Passive',
    'gender': 'Feminine',
    'planet': 'Moon',
    'metal': 'Silver',
    'color': 'White, Silver',
    'gem': 'Pearl, Moonstone',
    'meaning': '''
    The Duad represents duality, reflection, and polarity. It is the
    first division of the One into two. It symbolizes:
    - Balance and harmony
    - Partnership and union
    - Reflection and intuition
    - Reception and sensitivity
    - The mother principle
    ''',
    'pythagorean': '''
    The Duad is the first feminine number, representing diversity within
    unity. Pythagoras taught that it is the number of opinion and
    reflection, as opposed to the absolute truth of the Monad.
    ''',
    'kabbalistic': '''
    Corresponds to Chokmah (Wisdom) and Binah (Understanding), the second
    and third Sephiroth. It represents the primal duality of wisdom and
    understanding, father and mother.
    ''',
    'apocalyptic': '''
    The number 2 appears in the two witnesses, the two olive trees, and
    the two candlesticks. It represents testimony and witness.
    ''',
    'personality': '''
    People influenced by number 2 are natural diplomats. They are:
    - Cooperative and peace-loving
    - Intuitive and sensitive
    - Good mediators
    - Patient and detail-oriented
    - Supportive partners
    ''',
    'career': ['Diplomat', 'Counselor', 'Mediator', 'Partner', 'Analyst'],
    'compatible': [2, 4, 6, 8],
    'incompatible': [1, 3, 5, 7, 9]
}

# ==================== دانش عدد ۳ ====================
NUMBER_3 = {
    'name': 'The Triad',
    'symbol': '•••',
    'deity': 'Zeus, Jupiter, Odin',
    'element': 'Air',
    'quality': 'Creative',
    'gender': 'Masculine',
    'planet': 'Jupiter',
    'metal': 'Tin',
    'color': 'Purple, Blue',
    'gem': 'Amethyst, Sapphire',
    'meaning': '''
    The Triad represents creation, manifestation, and synthesis. It is the
    first true number, combining the Monad and Duad. It symbolizes:
    - Creation and expression
    - Growth and expansion
    - Social interaction
    - Optimism and joy
    - The trinity in all traditions
    ''',
    'pythagorean': '''
    Pythagoras considered 3 the first true number, as it has a beginning,
    middle, and end. It represents the three worlds: celestial, terrestrial,
    and infernal. The triangle is the first geometric figure.
    ''',
    'kabbalistic': '''
    Corresponds to Binah (Understanding) and the three pillars of the Tree
    of Life. It represents the three mother letters in Hebrew: Aleph, Mem,
    Shin.
    ''',
    'apocalyptic': '''
    The number 3 appears throughout Revelation: three woes, three unclean
    spirits, the Trinity. It represents divine completeness.
    ''',
    'personality': '''
    People influenced by number 3 are naturally creative. They are:
    - Artistic and expressive
    - Social and charismatic
    - Optimistic and enthusiastic
    - Inspiring to others
    - Lovers of beauty
    ''',
    'career': ['Artist', 'Writer', 'Performer', 'Designer', 'Speaker'],
    'compatible': [3, 6, 9],
    'incompatible': [1, 2, 4, 5, 7, 8]
}

# ==================== دانش عدد ۴ ====================
NUMBER_4 = {
    'name': 'The Tetrad',
    'symbol': '••••',
    'deity': 'Uranus, Prometheus',
    'element': 'Earth',
    'quality': 'Stable',
    'gender': 'Feminine',
    'planet': 'Uranus',
    'metal': 'Uranium',
    'color': 'Green, Brown',
    'gem': 'Emerald, Jade',
    'meaning': '''
    The Tetrad represents foundation, stability, and manifestation. It is
    the number of the four elements, four directions, four seasons.
    It symbolizes:
    - Structure and order
    - Practicality and work
    - Discipline and patience
    - Material manifestation
    - The square and cube
    ''',
    'pythagorean': '''
    The Tetrad was sacred to Pythagoras as the number of justice and
    completeness. The Tetractys, the triangular figure of ten points
    arranged in four rows, was their most sacred symbol.
    ''',
    'kabbalistic': '''
    Corresponds to Chesed (Mercy) and the four worlds of Kabbalah:
    Atziluth, Briah, Yetzirah, Assiah. Also the four letters of the
    Tetragrammaton YHVH.
    ''',
    'apocalyptic': '''
    The number 4 appears as the four living creatures, four horsemen,
    four corners of the earth. It represents earthly completeness.
    ''',
    'personality': '''
    People influenced by number 4 are natural builders. They are:
    - Practical and organized
    - Hardworking and reliable
    - Patient and persistent
    - Detail-oriented
    - Loyal and trustworthy
    ''',
    'career': ['Architect', 'Engineer', 'Manager', 'Organizer', 'Builder'],
    'compatible': [4, 8],
    'incompatible': [1, 2, 3, 5, 6, 7, 9]
}

# ==================== دانش عدد ۵ ====================
NUMBER_5 = {
    'name': 'The Pentad',
    'symbol': '•••••',
    'deity': 'Mercury, Hermes, Thoth',
    'element': 'Air',
    'quality': 'Adaptable',
    'gender': 'Masculine',
    'planet': 'Mercury',
    'metal': 'Mercury',
    'color': 'Light Blue, Yellow',
    'gem': 'Topaz, Citrine',
    'meaning': '''
    The Pentad represents freedom, change, and adventure. It is the number
    of the five senses, five fingers, five points of the pentagram.
    It symbolizes:
    - Freedom and adventure
    - Change and versatility
    - Communication and travel
    - Curiosity and learning
    - The pentagram (human form)
    ''',
    'pythagorean': '''
    Pythagoras called 5 the number of marriage, being the union of the
    first feminine (2) and first masculine (3). It represents the
    five regular solids and the five elements.
    ''',
    'kabbalistic': '''
    Corresponds to Geburah (Severity) and the five severities. The
    pentagram is a powerful protective symbol in Kabbalistic magic.
    ''',
    'apocalyptic': '''
    The number 5 appears as the five wounds of Christ, five wise and five
    foolish virgins. It represents grace and mercy.
    ''',
    'personality': '''
    People influenced by number 5 are natural explorers. They are:
    - Adventurous and freedom-loving
    - Versatile and adaptable
    - Curious and quick-witted
    - Social and communicative
    - Change agents
    ''',
    'career': ['Traveler', 'Sales', 'Journalist', 'Teacher', 'Adventurer'],
    'compatible': [1, 3, 5, 7],
    'incompatible': [2, 4, 6, 8, 9]
}

# ==================== دانش عدد ۶ ====================
NUMBER_6 = {
    'name': 'The Hexad',
    'symbol': '••••••',
    'deity': 'Venus, Aphrodite, Lakshmi',
    'element': 'Earth',
    'quality': 'Nurturing',
    'gender': 'Feminine',
    'planet': 'Venus',
    'metal': 'Copper',
    'color': 'Pink, Green',
    'gem': 'Rose Quartz, Emerald',
    'meaning': '''
    The Hexad represents love, harmony, and responsibility. It is the
    number of the six directions, six days of creation. It symbolizes:
    - Love and compassion
    - Harmony and balance
    - Family and community
    - Responsibility and service
    - Beauty and art
    ''',
    'pythagorean': '''
    Pythagoras considered 6 the number of creation, as it is the product
    of the first feminine and masculine (2 × 3). It represents the six
    directions in space.
    ''',
    'kabbalistic': '''
    Corresponds to Tiphareth (Beauty), the central Sephirah on the Tree
    of Life. It represents harmony, balance, and the heart.
    ''',
    'apocalyptic': '''
    The number 6 appears as the six days of creation, the six wings of
    the seraphim, and the number of man (666). It represents imperfection
    before completion.
    ''',
    'personality': '''
    People influenced by number 6 are natural nurturers. They are:
    - Loving and compassionate
    - Responsible and caring
    - Family-oriented
    - Artistic and harmonious
    - Service-oriented
    ''',
    'career': ['Teacher', 'Healer', 'Counselor', 'Artist', 'Parent'],
    'compatible': [2, 3, 6, 9],
    'incompatible': [1, 4, 5, 7, 8]
}

# ==================== دانش عدد ۷ ====================
NUMBER_7 = {
    'name': 'The Heptad',
    'symbol': '•••••••',
    'deity': 'Neptune, Poseidon, Varuna',
    'element': 'Water',
    'quality': 'Mystical',
    'gender': 'Feminine',
    'planet': 'Neptune',
    'metal': 'Platinum',
    'color': 'Violet, Sea Green',
    'gem': 'Amethyst, Lapis Lazuli',
    'meaning': '''
    The Heptad represents wisdom, spirituality, and mystery. It is the
    number of the seven planets, seven chakras, seven notes. It symbolizes:
    - Wisdom and knowledge
    - Spirituality and mysticism
    - Analysis and research
    - Inner truth
    - Perfection and completion
    ''',
    'pythagorean': '''
    Pythagoras called 7 the number of wisdom, as it is the sum of 3 and 4,
    spirit and matter. It was sacred to Athena, goddess of wisdom. The
    seven vowels of the Greek alphabet were considered magical.
    ''',
    'kabbalistic': '''
    Corresponds to Netzach (Victory) and the seven lower Sephiroth. The
    seven palaces, seven heavens, and seven earths in Kabbalistic cosmology.
    ''',
    'apocalyptic': '''
    The number 7 appears more than any other in Revelation: seven churches,
    seven seals, seven trumpets, seven bowls, seven spirits of God.
    It represents divine perfection.
    ''',
    'personality': '''
    People influenced by number 7 are natural seekers. They are:
    - Analytical and thoughtful
    - Spiritual and intuitive
    - Mysterious and private
    - Wise beyond their years
    - Seekers of truth
    ''',
    'career': ['Scientist', 'Researcher', 'Philosopher', 'Mystic', 'Analyst'],
    'compatible': [1, 4, 7],
    'incompatible': [2, 3, 5, 6, 8, 9]
}

# ==================== دانش عدد ۸ ====================
NUMBER_8 = {
    'name': 'The Ogdoad',
    'symbol': '••••••••',
    'deity': 'Saturn, Chronos, Yama',
    'element': 'Earth',
    'quality': 'Powerful',
    'gender': 'Masculine',
    'planet': 'Saturn',
    'metal': 'Lead',
    'color': 'Black, Dark Blue',
    'gem': 'Onyx, Black Tourmaline',
    'meaning': '''
    The Ogdoad represents power, success, and material mastery. It is the
    number of infinity (∞) turned sideways. It symbolizes:
    - Power and authority
    - Material success
    - Business and finance
    - Karma and justice
    - Rebirth and renewal
    ''',
    'pythagorean': '''
    Pythagoras considered 8 the number of justice and balance, as it is
    the first cube (2×2×2). It represents the eight directions in space
    and the eight spheres of the cosmos.
    ''',
    'kabbalistic': '''
    Corresponds to Hod (Splendor) and the eight kings of Edom. The eight
    gates of the Tree of Life, the eight paths of wisdom.
    ''',
    'apocalyptic': '''
    The number 8 represents new beginnings, as it follows the perfection
    of 7. It is the number of resurrection and eternal life. The eighth
    day is the day of circumcision and new covenant.
    ''',
    'personality': '''
    People influenced by number 8 are natural achievers. They are:
    - Ambitious and powerful
    - Business-minded
    - Efficient and organized
    - Authoritative
    - Success-oriented
    ''',
    'career': ['Executive', 'Financier', 'Manager', 'Leader', 'Investor'],
    'compatible': [4, 8],
    'incompatible': [1, 2, 3, 5, 6, 7, 9]
}

# ==================== دانش عدد ۹ ====================
NUMBER_9 = {
    'name': 'The Ennead',
    'symbol': '•••••••••',
    'deity': 'Mars, Ares, Kartikeya',
    'element': 'Fire',
    'quality': 'Universal',
    'gender': 'Masculine',
    'planet': 'Mars',
    'metal': 'Iron',
    'color': 'Red, Crimson',
    'gem': 'Garnet, Red Jasper',
    'meaning': '''
    The Ennead represents completion, wisdom, and universal love. It is
    the last single digit, containing all others within it. It symbolizes:
    - Completion and endings
    - Universal love
    - Wisdom and enlightenment
    - Humanitarian service
    - Spiritual mastery
    ''',
    'pythagorean': '''
    Pythagoras called 9 the number of man, as it is the number of months
    of human gestation. It represents the nine Muses, the nine spheres,
    and the completion of the decade.
    ''',
    'kabbalistic': '''
    Corresponds to Yesod (Foundation) and the ninth Sephirah. The nine
    orders of angels, the nine chambers of the Tree of Life.
    ''',
    'apocalyptic': '''
    The number 9 represents finality and judgment. The nine fruits of the
    Spirit, the nine gifts of the Spirit. It is the number of completion
    before the decade.
    ''',
    'personality': '''
    People influenced by number 9 are natural humanitarians. They are:
    - Compassionate and giving
    - Wise and enlightened
    - Artistic and creative
    - Universal in outlook
    - Completion-oriented
    ''',
    'career': ['Humanitarian', 'Artist', 'Philosopher', 'Healer', 'Teacher'],
    'compatible': [3, 6, 9],
    'incompatible': [1, 2, 4, 5, 7, 8]
}

# ==================== دانش اعداد مرکب ====================
COMPOUND_NUMBERS = {
    11: {
        'name': 'Master Number 11',
        'meaning': '''
        The number of spiritual illumination and intuition. It is the
        master number of revelation and inspiration. Those with this
        number are highly intuitive and may have psychic abilities.
        ''',
        'challenge': 'Nervous tension, over-sensitivity',
        'positive': 'Inspiration, intuition, spiritual insight',
        'negative': 'Fanaticism, deception, fraud'
    },
    22: {
        'name': 'Master Number 22',
        'meaning': '''
        The Master Builder number. It combines the intuition of 11 with
        the practicality of 4 (2+2). Those with this number can manifest
        grand visions into reality.
        ''',
        'challenge': 'Overwhelming responsibility',
        'positive': 'Master builder, visionary, practical idealist',
        'negative': 'Obsession, megalomania'
    },
    33: {
        'name': 'Master Number 33',
        'meaning': '''
        The Master Teacher number. It combines the wisdom of all numbers.
        Those with this number are here to teach and heal humanity.
        ''',
        'challenge': 'Self-sacrifice, burden of knowledge',
        'positive': 'Master teacher, healer, spiritual guide',
        'negative': 'Martyr complex, overwhelming others'
    },
    44: {
        'name': 'Master Number 44',
        'meaning': '''
        The number of material mastery combined with spiritual wisdom.
        Represents the ability to build lasting spiritual and material
        foundations.
        ''',
        'challenge': 'Extreme responsibility',
        'positive': 'Master healer, spiritual architect',
        'negative': 'Workaholic, spiritual pride'
    }
}

# ==================== اعداد آخرالزمانی ====================
APOCALYPTIC_NUMBERS = {
    7: {
        'meaning': 'Divine perfection',
        'references': [
            '7 Churches of Asia',
            '7 Candlesticks',
            '7 Stars',
            '7 Spirits of God',
            '7 Seals',
            '7 Trumpets',
            '7 Thunders',
            '7 Plagues',
            '7 Bowls'
        ],
        'source': 'Revelation'
    },
    10: {
        'meaning': 'Worldly completeness',
        'references': [
            '10 Days of Tribulation',
            '10 Horns of the Beast',
            '10 Crowns'
        ],
        'source': 'Revelation'
    },
    12: {
        'meaning': 'Governmental perfection',
        'references': [
            '12 Tribes of Israel',
            '12 Apostles',
            '12 Gates',
            '12 Foundations',
            '12 Pearls',
            '12 Angels',
            '144,000 (12×12)'
        ],
        'source': 'Revelation'
    },
    24: {
        'meaning': 'Heavenly government',
        'references': [
            '24 Elders',
            '24 Thrones'
        ],
        'source': 'Revelation'
    },
    144: {
        'meaning': 'Spiritual perfection',
        'references': [
            '144 Cubits (city wall)',
            '144,000 sealed'
        ],
        'source': 'Revelation'
    },
    666: {
        'meaning': 'Number of the Beast',
        'references': [
            'Revelation 13:18',
            'Number of man',
            'Imperfection (falls short of 777)'
        ],
        'source': 'Revelation'
    },
    888: {
        'meaning': 'Number of Jesus (in Greek gematria)',
        'references': [
            'Iesous = 888',
            'Resurrection number'
        ],
        'source': 'Early Christian'
    }
}

# ==================== روش‌های عددشناسی ====================
METHODS = {
    'pythagorean_reduction': '''
    Add all digits until you reach a single number (1-9), preserving
    master numbers 11, 22, 33.
    ''',
    'theosophic_addition': '''
    Add the value of all letters in a name, reducing to root number.
    ''',
    'theosophic_reduction': '''
    Reduce compound numbers by adding their digits.
    ''',
    'gematria': '''
    Hebrew system where each letter has a numerical value.
    ''',
    'isopsephy': '''
    Greek system of letter-number correspondence.
    '''
}

# ==================== نقل قول‌های مهم ====================
QUOTES = [
    "The world is built upon the power of numbers.",
    "Number is the within of all things.",
    "God geometrizes.",
    "All things are numbers.",
    "Number rules the universe.",
    "The knowledge of numbers is the knowledge of the gods.",
    "In numbers we find the keys to the universe."
]

# ==================== کتابشناسی ====================
BIBLIOGRAPHY = [
    "Pythagoras - The Golden Verses",
    "Plato - Timaeus",
    "Iamblichus - Life of Pythagoras",
    "Porphyry - Life of Pythagoras",
    "Reuchlin - De Arte Cabbalistica",
    "Agrippa - Three Books of Occult Philosophy",
    "The Kabbalah Unveiled - S.L. MacGregor Mathers",
    "The Secret Doctrine - H.P. Blavatsky"
]

# ==================== خلاصه نهایی ====================
BOOK_DATA['content'] = f"""
{BOOK_DATA['summary']}

# NUMBER 1
{json.dumps(NUMBER_1, indent=2)}

# NUMBER 2
{json.dumps(NUMBER_2, indent=2)}

# NUMBER 3
{json.dumps(NUMBER_3, indent=2)}

# NUMBER 4
{json.dumps(NUMBER_4, indent=2)}

# NUMBER 5
{json.dumps(NUMBER_5, indent=2)}

# NUMBER 6
{json.dumps(NUMBER_6, indent=2)}

# NUMBER 7
{json.dumps(NUMBER_7, indent=2)}

# NUMBER 8
{json.dumps(NUMBER_8, indent=2)}

# NUMBER 9
{json.dumps(NUMBER_9, indent=2)}

# COMPOUND NUMBERS
{json.dumps(COMPOUND_NUMBERS, indent=2)}

# APOCALYPTIC NUMBERS
{json.dumps(APOCALYPTIC_NUMBERS, indent=2)}

# METHODS
{json.dumps(METHODS, indent=2)}

# QUOTES
{json.dumps(QUOTES, indent=2)}

# BIBLIOGRAPHY
{json.dumps(BIBLIOGRAPHY, indent=2)}
"""
