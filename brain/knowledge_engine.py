#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📚 KNOWLEDGE ENGINE - موتور دانش بی‌نهایت
نسخه سالم و بدون خطا
"""

import logging
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class KnowledgeEngine:
    """
    موتور دانش - کتابخانه نامحدود ربات
    """
    
    def __init__(self):
        self.name = "Knowledge Engine"
        self.version = "1.0.0"
        
        # مسیر کتاب‌ها
        self.books_path = Path("knowledge/books")
        self.patterns_path = Path("knowledge/patterns")
        self.wisdom_path = Path("knowledge/wisdom")
        
        # ایجاد پوشه‌ها
        for path in [self.books_path, self.patterns_path, self.wisdom_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # بارگذاری دانش موجود
        self.books = {}
        self.patterns = []
        self.wisdom = {}
        
        # بارگذاری کتاب‌ها
        self._load_books_safely()
        
        # ایندکس جستجو
        self.search_index = self._build_search_index()
        
        logger.info(f"📚 Knowledge Engine initialized with {len(self.books)} books")
    
    def _load_books_safely(self):
        """بارگذاری کتاب‌ها بدون circular import"""
        books_dir = Path("knowledge/books")
        
        if not books_dir.exists():
            logger.warning("⚠️ Books directory not found")
            return
        
        for book_file in books_dir.glob("*.py"):
            if book_file.name == "__init__.py":
                continue
                
            try:
                book_name = book_file.stem
                # import دینامیک بدون وابستگی
                spec = importlib.util.spec_from_file_location(book_name, book_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'BOOK_DATA'):
                        self.books[book_name] = module.BOOK_DATA
                        logger.info(f"✅ Loaded book: {book_name}")
                    else:
                        logger.warning(f"⚠️ Book {book_name} has no BOOK_DATA")
                        
            except Exception as e:
                logger.warning(f"⚠️ Could not load book {book_file.stem}: {e}")
    
    def _build_search_index(self) -> Dict:
        """ساخت ایندکس برای جستجوی سریع"""
        index = {
            'keywords': {},
            'topics': {},
            'numbers': {},
            'patterns': {}
        }
        
        # ایندکس کردن کتاب‌ها
        for book_name, book_data in self.books.items():
            if 'content' in book_data:
                self._index_book_content(book_name, book_data['content'], index)
            
            if 'keywords' in book_data:
                for keyword in book_data['keywords']:
                    if keyword not in index['keywords']:
                        index['keywords'][keyword] = []
                    index['keywords'][keyword].append(book_name)
        
        return index
    
    def _index_book_content(self, book_name: str, content: str, index: Dict):
        """ایندکس کردن محتوای کتاب"""
        words = content.lower().split()
        for word in words:
            if len(word) > 3:
                if word not in index['keywords']:
                    index['keywords'][word] = []
                if book_name not in index['keywords'][word]:
                    index['keywords'][word].append(book_name)
    
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        جستجوی هوشمند در تمام منابع دانش
        """
        query = query.lower()
        results = []
        
        # جستجو در کتاب‌ها
        for book_name, book_data in self.books.items():
            relevance = self._calculate_relevance(query, book_data)
            if relevance > 0:
                results.append({
                    'type': 'book',
                    'source': book_name,
                    'title': book_data.get('title', book_name),
                    'author': book_data.get('author', 'Unknown'),
                    'relevance': relevance,
                    'content': self._extract_relevant_content(query, book_data)
                })
        
        # جستجو در الگوها
        for pattern in self.patterns:
            if query in pattern.get('description', '').lower():
                results.append({
                    'type': 'pattern',
                    'pattern': pattern,
                    'relevance': 0.8
                })
        
        # مرتب‌سازی بر اساس ارتباط
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return results[:limit]
    
    def _calculate_relevance(self, query: str, book_data: Dict) -> float:
        """محاسبه میزان ارتباط کتاب با جستجو"""
        relevance = 0
        query_words = query.split()
        
        # جستجو در کلمات کلیدی
        keywords = book_data.get('keywords', [])
        for word in query_words:
            if word in keywords:
                relevance += 0.3
        
        # جستجو در عنوان
        title = book_data.get('title', '').lower()
        for word in query_words:
            if word in title:
                relevance += 0.2
        
        # جستجو در محتوا
        content = book_data.get('content', '').lower()
        for word in query_words:
            if word in content:
                relevance += 0.1
        
        return min(1.0, relevance)
    
    def _extract_relevant_content(self, query: str, book_data: Dict) -> str:
        """استخراج بخش مرتبط از کتاب"""
        content = book_data.get('content', '')
        if not content:
            return ""
        
        # پیدا کردن جمله‌های مرتبط
        sentences = content.split('.')
        relevant_sentences = []
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in query.split()):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            return '. '.join(relevant_sentences[:3]) + '.'
        
        return book_data.get('summary', '')
    
    def get_knowledge_by_topic(self, topic: str) -> List[Dict]:
        """دریافت دانش مرتبط با یک موضوع"""
        results = []
        
        for book_name, book_data in self.books.items():
            if topic.lower() in book_data.get('title', '').lower():
                results.append({
                    'book': book_name,
                    'title': book_data.get('title'),
                    'summary': book_data.get('summary')
                })
        
        return results
    
    def get_stats(self) -> Dict:
        """گرفتن آمار دانش"""
        return {
            'total_books': len(self.books),
            'total_patterns': len(self.patterns),
            'total_wisdom': len(self.wisdom),
            'book_names': list(self.books.keys())
        }

# نمونه‌سازی سراسری
knowledge_engine = KnowledgeEngine()
