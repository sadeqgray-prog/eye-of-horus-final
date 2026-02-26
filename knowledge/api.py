#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔌 KNOWLEDGE API - API برای افزودن کتاب توسط کاربر
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from knowledge.downloader import downloader
from knowledge.auto_learner import auto_learner

class KnowledgeAPI:
    """
    API برای مدیریت دانش توسط کاربر و ربات
    """
    
    def __init__(self):
        self.name = "Knowledge API"
        self.version = "1.0.0"
    
    # ==================== افزودن کتاب ====================
    
    def add_book_by_url(self, url: str, category: str = 'general', 
                        title: str = None, author: str = None) -> Dict:
        """
        افزودن کتاب با URL
        """
        book = downloader.add_book_by_url(url, category)
        
        if title:
            book['title'] = title
        if author:
            book['author'] = author
        
        downloader._save_metadata()
        
        # شروع دانلود
        downloader.download_book(book['id'])
        
        return {
            'success': True,
            'book_id': book['id'],
            'message': f"Book added and downloading started: {book['title']}"
        }
    
    def add_book_by_file(self, file_path: str, category: str = 'general',
                        title: str = None, author: str = None) -> Dict:
        """
        افزودن کتاب با آپلود فایل
        """
        path = Path(file_path)
        if not path.exists():
            return {'success': False, 'message': 'File not found'}
        
        if not title:
            title = path.stem.replace('_', ' ').title()
        
        if not author:
            author = 'Unknown'
        
        # کپی فایل به پوشه raw
        book_id = hashlib.md5(f"{title}_{author}_{datetime.now()}".encode()).hexdigest()[:16]
        dest_path = downloader.raw_dir / f"{book_id}{path.suffix}"
        
        import shutil
        shutil.copy2(path, dest_path)
        
        book = downloader.add_book_manually(
            title=title,
            author=author,
            category=category,
            file_path=str(dest_path)
        )
        
        book['id'] = book_id
        book['status'] = 'downloaded'
        downloader._save_metadata()
        
        return {
            'success': True,
            'book_id': book_id,
            'message': f"Book added from file: {title}"
        }
    
    def add_book_manually(self, title: str, author: str, category: str,
                         content: str = None) -> Dict:
        """
        افزودن کتاب به صورت دستی (با متن)
        """
        book = downloader.add_book_manually(title, author, category)
        
        if content:
            # ذخیره متن به عنوان فایل
            text_file = downloader.raw_dir / f"{book['id']}.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            book['file_path'] = str(text_file)
            book['status'] = 'downloaded'
            downloader._save_metadata()
        
        return {
            'success': True,
            'book_id': book['id'],
            'message': f"Book added manually: {title}"
        }
    
    # ==================== مدیریت کتاب‌ها ====================
    
    def list_books(self, category: str = None, status: str = None) -> List[Dict]:
        """
        لیست کتاب‌ها با فیلتر
        """
        books = downloader.list_books(category)
        
        if status:
            books = [b for b in books if b.get('status') == status]
        
        return books
    
    def get_book_status(self, book_id: str) -> Dict:
        """
        وضعیت یک کتاب
        """
        book = downloader.books_metadata['books'].get(book_id)
        if not book:
            return {'error': 'Book not found'}
        
        return book
    
    def delete_book(self, book_id: str) -> Dict:
        """
        حذف کتاب
        """
        book = downloader.books_metadata['books'].get(book_id)
        if not book:
            return {'success': False, 'message': 'Book not found'}
        
        # حذف فایل‌ها
        if book.get('file_path'):
            Path(book['file_path']).unlink(missing_ok=True)
        
        if book.get('knowledge_file'):
            Path(book['knowledge_file']).unlink(missing_ok=True)
        
        # حذف از metadata
        del downloader.books_metadata['books'][book_id]
        
        category = book.get('category')
        if category and category in downloader.books_metadata['categories']:
            if book_id in downloader.books_metadata['categories'][category]:
                downloader.books_metadata['categories'][category].remove(book_id)
        
        downloader.books_metadata['total_books'] -= 1
        downloader._save_metadata()
        
        return {
            'success': True,
            'message': f"Book deleted: {book['title']}"
        }
    
    # ==================== پردازش و یادگیری ====================
    
    def process_book(self, book_id: str) -> Dict:
        """
        پردازش یک کتاب
        """
        success = downloader.process_book(book_id)
        
        if success:
            return {
                'success': True,
                'message': f"Book processed successfully"
            }
        else:
            return {
                'success': False,
                'message': "Processing failed"
            }
    
    async def learn_book(self, book_id: str) -> Dict:
        """
        یادگیری یک کتاب توسط مغز
        """
        book = downloader.books_metadata['books'].get(book_id)
        if not book:
            return {'success': False, 'message': 'Book not found'}
        
        if not book.get('processed'):
            return {'success': False, 'message': 'Book not processed yet'}
        
        knowledge = downloader.get_book_knowledge(book_id)
        if not knowledge:
            return {'success': False, 'message': 'Knowledge not found'}
        
        from knowledge.auto_learner import auto_learner
        await auto_learner._teach_master_mind(knowledge)
        await auto_learner._store_in_memory(book_id, knowledge)
        
        book['learned'] = True
        book['learned_at'] = datetime.now().isoformat()
        downloader._save_metadata()
        
        return {
            'success': True,
            'message': f"Book learned: {book['title']}"
        }
    
    async def learn_all_pending(self) -> Dict:
        """
        یادگیری همه کتاب‌های پردازش شده
        """
        books = downloader.list_books()
        pending = [b for b in books if b.get('processed') and not b.get('learned')]
        
        results = []
        for book in pending:
            result = await self.learn_book(book['id'])
            results.append(result)
        
        return {
            'success': True,
            'total': len(pending),
            'learned': len([r for r in results if r['success']]),
            'results': results
        }
    
    def process_all_pending(self) -> Dict:
        """
        پردازش همه کتاب‌های دانلود شده
        """
        books = downloader.list_books()
        pending = [b for b in books if b.get('status') == 'downloaded' and not b.get('processed')]
        
        results = []
        for book in pending:
            result = self.process_book(book['id'])
            results.append(result)
        
        return {
            'success': True,
            'total': len(pending),
            'processed': len([r for r in results if r['success']]),
            'results': results
        }
    
    def download_all_pending(self) -> Dict:
        """
        دانلود همه کتاب‌های در انتظار
        """
        books = downloader.list_books()
        pending = [b for b in books if b.get('status') == 'pending' and b.get('url')]
        
        results = []
        for book in pending:
            success = downloader.download_book(book['id'])
            results.append({'book_id': book['id'], 'success': success})
        
        return {
            'success': True,
            'total': len(pending),
            'downloaded': len([r for r in results if r['success']]),
            'results': results
        }
    
    # ==================== جستجو ====================
    
    def search_books(self, query: str) -> List[Dict]:
        """
        جستجو در کتاب‌ها
        """
        return downloader.search_books(query)
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """
        جستجو در دانش کتاب‌ها
        """
        results = []
        query = query.lower()
        
        for book_id, book in downloader.books_metadata['books'].items():
            if not book.get('processed'):
                continue
            
            knowledge = downloader.get_book_knowledge(book_id)
            if not knowledge:
                continue
            
            # جستجو در مفاهیم
            for concept in knowledge['knowledge'].get('concepts', []):
                if query in concept.lower():
                    results.append({
                        'book': book['title'],
                        'type': 'concept',
                        'content': concept
                    })
            
            # جستجو در نقل قول‌ها
            for quote in knowledge['knowledge'].get('quotes', []):
                if query in quote.lower():
                    results.append({
                        'book': book['title'],
                        'type': 'quote',
                        'content': quote
                    })
        
        return results[:20]
    
    # ==================== آمار ====================
    
    def get_stats(self) -> Dict:
        """
        آمار کامل
        """
        books = downloader.list_books()
        
        return {
            'total_books': len(books),
            'by_category': {
                cat: len([b for b in books if b.get('category') == cat])
                for cat in downloader.books_metadata['categories']
            },
            'by_status': {
                'pending': len([b for b in books if b.get('status') == 'pending']),
                'downloaded': len([b for b in books if b.get('status') == 'downloaded']),
                'processed': len([b for b in books if b.get('processed')]),
                'learned': len([b for b in books if b.get('learned')])
            },
            'learning_stats': auto_learner.get_learning_stats()
        }

# نمونه‌سازی سراسری
knowledge_api = KnowledgeAPI()
