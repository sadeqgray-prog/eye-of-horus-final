"""
ماژول عددشناسی - علوم اعداد با ۵ سیستم مختلف
منبع: کتاب‌های Westcott, Sepharial, Agrippa
"""

from .pythagorean import PythagoreanNumerology
from .chaldean import ChaldeanNumerology

# ماژول‌های دیگر در آینده اضافه می‌شن
# from .vedic import VedicNumerology
# from .chinese import ChineseNumerology

__all__ = [
    'PythagoreanNumerology',
    'ChaldeanNumerology'
]
