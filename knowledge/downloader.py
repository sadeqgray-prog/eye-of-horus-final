#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📥 KNOWLEDGE DOWNLOADER - دانلود خودکار کتاب‌های PDF
قابلیت افزودن کتاب جدید توسط کاربر یا ربات
"""

import os
import requests
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.parse
import PyPDF2
import time

class KnowledgeDownloader:
    """
    دانلود و پردازش خودکار کتاب‌ها
    """
    
    def __init__(self):
        self.base_dir = Path('knowledge')
        self.raw_dir = self.base_dir / 'raw'
        self.processed_dir = self.base_dir / 'processed'
        self.metadata_file = self.base_dir / 'books_metadata.json'
        
        # ایجاد پوشه‌ها
        for d in [self.raw_dir, self.processed_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # بارگذاری metadata
        self.books_metadata = self._load_metadata()
        
        print("📥 Knowledge Downloader initialized")
    
    def _load_metadata(self) -> Dict:
        """بارگذاری metadata کتاب‌ها"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'books': {},
            'categories': {},
            'total_books': 0,
            'last_update': None
        }
    
    def _save_metadata(self):
        """ذخیره metadata"""
        self.books_metadata['last_update'] = datetime.now().isoformat()
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.books_metadata, f, indent=2, ensure_ascii=False)
    
    # ==================== اضافه کردن کتاب جدید ====================
    
    def add_book_manually(self, title: str, author: str, category: str, 
                         file_path: str = None, url: str = None) -> Dict:
        """
        اضافه کردن کتاب به صورت دستی
        """
        book_id = hashlib.md5(f"{title}_{author}_{datetime.now()}".encode()).hexdigest()[:16]
        
        book_info = {
            'id': book_id,
            'title': title,
            'author': author,
            'category': category,
            'added_at': datetime.now().isoformat(),
            'added_by': 'user',
            'file_path': str(file_path) if file_path else None,
            'url': url,
            'processed': False,
            'status': 'pending'
        }
        
        self.books_metadata['books'][book_id] = book_info
        
        if category not in self.books_metadata['categories']:
            self.books_metadata['categories'][category] = []
        self.books_metadata['categories'][category].append(book_id)
        
        self.books_metadata['total_books'] += 1
        self._save_metadata()
        
        print(f"📚 Book added manually: {title}")
        return book_info
    
    def add_book_by_url(self, url: str, category: str = 'general') -> Dict:
        """
        اضافه کردن کتاب با URL
        """
        # استخراج نام فایل از URL
        parsed = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename:
            filename = f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        title = filename.replace('_', ' ').replace('.pdf', '').title()
        
        book_info = self.add_book_manually(
            title=title,
            author='Unknown',
            category=category,
            url=url
        )
        
        # شروع دانلود در پس‌زمینه
        book_info['status'] = 'downloading'
        self._save_metadata()
        
        return book_info
    
    def download_book(self, book_id: str) -> bool:
        """
        دانلود کتاب با ID
        """
        if book_id not in self.books_metadata['books']:
            print(f"❌ Book {book_id} not found")
            return False
        
        book = self.books_metadata['books'][book_id]
        
        if not book.get('url'):
            print(f"❌ No URL for book {book_id}")
            return False
        
        print(f"📥 Downloading: {book['title']}...")
        
        try:
            # دانلود فایل
            response = requests.get(book['url'], stream=True, timeout=30)
            response.raise_for_status()
            
            # ذخیره فایل
            file_path = self.raw_dir / f"{book_id}.pdf"
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            book['file_path'] = str(file_path)
            book['status'] = 'downloaded'
            book['downloaded_at'] = datetime.now().isoformat()
            book['file_size'] = file_path.stat().st_size
            
            self._save_metadata()
            
            print(f"✅ Downloaded: {book['title']} ({book['file_size']} bytes)")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            book['status'] = 'failed'
            book['error'] = str(e)
            self._save_metadata()
            return False
    
    # ==================== پردازش کتاب ====================
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """استخراج متن از PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n\n--- Page {page_num + 1} ---\n\n"
                            text += page_text
                    except Exception as e:
                        print(f"⚠️ Error on page {page_num}: {e}")
                        continue
        except Exception as e:
            print(f"❌ PDF extraction error: {e}")
        
        return text
    
    def extract_knowledge(self, text: str, book_type: str = 'general') -> Dict:
        """
        استخراج دانش از متن با هوش مصنوعی ساده
        """
        knowledge = {
            'summary': '',
            'chapters': [],
            'concepts': [],
            'quotes': [],
            'teachings': [],
            'keywords': [],
            'entities': [],
            'statistics': {}
        }
        
        # خلاصه (اولین پاراگراف)
        paragraphs = text.split('\n\n')
        if paragraphs:
            knowledge['summary'] = paragraphs[0][:500] + '...'
        
        # استخراج فصل‌ها
        chapter_patterns = [
            r'Chapter\s+(\d+)[.\s]+([^\n]+)',
            r'CHAPTER\s+(\d+)[.\s]+([^\n]+)',
            r'فصل\s+(\d+)[.\s]+([^\n]+)',
            r'\d+\.\s+([^\n]+)'  # 1. Title
        ]
        
        for pattern in chapter_patterns:
            chapters = re.findall(pattern, text)
            for ch in chapters:
                if isinstance(ch, tuple):
                    knowledge['chapters'].append(f"Chapter {ch[0]}: {ch[1]}")
                else:
                    knowledge['chapters'].append(ch)
        
        # استخراج نقل قول‌ها
        quote_patterns = [
            r'"([^"]+)"',
            r'«([^»]+)»',
            r'“([^”]+)”'
        ]
        
        for pattern in quote_patterns:
            quotes = re.findall(pattern, text)
            knowledge['quotes'].extend(quotes[:20])  # ۲۰ نقل قول اول
        
        # استخراج کلمات کلیدی (کلمات پرتکرار)
        words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
        from collections import Counter
        word_counts = Counter(words)
        knowledge['keywords'] = [word for word, count in word_counts.most_common(50)]
        
        # آمار
        knowledge['statistics'] = {
            'total_chars': len(text),
            'total_words': len(text.split()),
            'total_sentences': len(re.findall(r'[.!?]+', text)),
            'total_pages': len(re.findall(r'--- Page \d+ ---', text))
        }
        
        return knowledge
    
    def process_book(self, book_id: str) -> bool:
        """
        پردازش کامل یک کتاب
        """
        if book_id not in self.books_metadata['books']:
            print(f"❌ Book {book_id} not found")
            return False
        
        book = self.books_metadata['books'][book_id]
        
        if book.get('status') != 'downloaded' and not book.get('file_path'):
            print(f"❌ Book {book_id} not downloaded")
            return False
        
        print(f"🔄 Processing: {book['title']}...")
        
        try:
            # استخراج متن
            file_path = Path(book['file_path'])
            text = self.extract_text_from_pdf(file_path)
            
            # استخراج دانش
            knowledge = self.extract_knowledge(text, book.get('category', 'general'))
            
            # ذخیره دانش پردازش شده
            processed_file = self.processed_dir / f"{book_id}.json"
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': book,
                    'knowledge': knowledge
                }, f, indent=2, ensure_ascii=False)
            
            # به‌روزرسانی metadata
            book['processed'] = True
            book['processed_at'] = datetime.now().isoformat()
            book['knowledge_file'] = str(processed_file)
            book['status'] = 'processed'
            book['stats'] = knowledge['statistics']
            
            self._save_metadata()
            
            print(f"✅ Processed: {book['title']}")
            print(f"   📊 Pages: {knowledge['statistics']['total_pages']}")
            print(f"   📝 Words: {knowledge['statistics']['total_words']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            book['status'] = 'processing_failed'
            book['error'] = str(e)
            self._save_metadata()
            return False
    
    # ==================== کتابخانه ====================
    
    def list_books(self, category: str = None) -> List[Dict]:
        """
        لیست همه کتاب‌ها
        """
        books = []
        for book_id, book in self.books_metadata['books'].items():
            if not category or book.get('category') == category:
                books.append(book)
        
        return sorted(books, key=lambda x: x['added_at'], reverse=True)
    
    def search_books(self, query: str) -> List[Dict]:
        """
        جستجو در کتاب‌ها
        """
        results = []
        query = query.lower()
        
        for book_id, book in self.books_metadata['books'].items():
            if query in book['title'].lower() or query in book.get('author', '').lower():
                results.append(book)
        
        return results
    
    def get_book_knowledge(self, book_id: str) -> Optional[Dict]:
        """
        دریافت دانش پردازش شده یک کتاب
        """
        book = self.books_metadata['books'].get(book_id)
        if not book or not book.get('knowledge_file'):
            return None
        
        knowledge_file = Path(book['knowledge_file'])
        if not knowledge_file.exists():
            return None
        
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # ==================== پیشنهاد کتاب ====================
    
    def suggest_books(self, topic: str) -> List[Dict]:
        """
        پیشنهاد کتاب بر اساس موضوع
        """
        suggestions = []
        
        for book_id, book in self.books_metadata['books'].items():
            if not book.get('processed'):
                continue
            
            knowledge = self.get_book_knowledge(book_id)
            if not knowledge:
                continue
            
            # جستجو در keywords
            if topic.lower() in ' '.join(knowledge['knowledge']['keywords']):
                suggestions.append(book)
        
        return suggestions[:5]
    
    # ==================== پردازش خودکار ====================
    
    def process_all_pending(self):
        """
        پردازش همه کتاب‌های در انتظار
        """
        for book_id, book in self.books_metadata['books'].items():
            if book.get('status') == 'downloaded' and not book.get('processed'):
                self.process_book(book_id)
                time.sleep(1)  # کمی صبر بین پردازش‌ها
    
    def download_all_pending(self):
        """
        دانلود همه کتاب‌های در انتظار
        """
        for book_id, book in self.books_metadata['books'].items():
            if book.get('status') == 'pending' and book.get('url'):
                self.download_book(book_id)
                time.sleep(2)  # کمی صبر بین دانلودها

# نمونه‌سازی سراسری
downloader = KnowledgeDownloader()
