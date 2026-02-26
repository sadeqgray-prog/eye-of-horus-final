"""
📚 KNOWLEDGE PACKAGE - مدیریت دانش بی‌نهایت
"""

from .downloader import KnowledgeDownloader, downloader
from .auto_learner import AutoLearner, auto_learner
from .api import KnowledgeAPI, knowledge_api

__all__ = [
    'downloader',
    'auto_learner',
    'knowledge_api'
]
