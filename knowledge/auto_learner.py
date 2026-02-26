#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧠 AUTO LEARNER - یادگیری خودکار از کتاب‌های جدید
ربات هر کتاب جدید را می‌خواند و از آن یاد می‌گیرد
"""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import random

from knowledge.downloader import downloader
from brain.master_mind import master_mind
from brain.knowledge_engine import knowledge_engine
from brain.memory_core import memory_core

class AutoLearner:
    """
    یادگیری خودکار - ربات هر روز باهوش‌تر می‌شود
    """
    
    def __init__(self):
        self.name = "Auto Learner"
        self.version = "1.0.0"
        self.is_learning = False
        self.learning_history = []
        self.learning_rate = 0.1
        
        # آمار
        self.stats = {
            'total_books_learned': 0,
            'total_knowledge_points': 0,
            'last_learning_session': None,
            'learning_speed': 1.0
        }
        
        print("🧠 Auto Learner initialized")
    
    def start_auto_learning(self):
        """
        شروع فرآیند یادگیری خودکار در پس‌زمینه
        """
        if self.is_learning:
            return
        
        self.is_learning = True
        
        def learning_worker():
            while self.is_learning:
                try:
                    # هر ساعت یک کتاب جدید یاد بگیر
                    time.sleep(3600)
                    asyncio.run(self.learn_one_book())
                except Exception as e:
                    print(f"❌ Learning error: {e}")
        
        thread = threading.Thread(target=learning_worker, daemon=True)
        thread.start()
        
        print("🔄 Auto learning started")
    
    def stop_auto_learning(self):
        """
        توقف یادگیری خودکار
        """
        self.is_learning = False
        print("🛑 Auto learning stopped")
    
    async def learn_one_book(self) -> bool:
        """
        یادگیری یک کتاب جدید
        """
        # پیدا کردن کتاب پردازش شده اما یادگیری نشده
        books = downloader.list_books()
        unlearned = [b for b in books if b.get('processed') and not b.get('learned')]
        
        if not unlearned:
            print("📚 No new books to learn")
            return False
        
        # انتخاب یک کتاب تصادفی
        book = random.choice(unlearned)
        book_id = book['id']
        
        print(f"📖 Learning: {book['title']}...")
        
        # دریافت دانش کتاب
        knowledge = downloader.get_book_knowledge(book_id)
        if not knowledge:
            print(f"❌ No knowledge for book {book_id}")
            return False
        
        # یادگیری در مغز
        await self._teach_master_mind(knowledge)
        
        # ذخیره در حافظه
        await self._store_in_memory(book_id, knowledge)
        
        # به‌روزرسانی metadata
        book['learned'] = True
        book['learned_at'] = datetime.now().isoformat()
        downloader._save_metadata()
        
        # آمار
        self.stats['total_books_learned'] += 1
        self.stats['last_learning_session'] = datetime.now().isoformat()
        self.stats['learning_speed'] = self.learning_rate
        
        print(f"✅ Learned: {book['title']}")
        print(f"   📊 Knowledge points: {len(knowledge['knowledge']['concepts'])}")
        
        # افزایش سطح هوشیاری
        master_mind.consciousness['wisdom'] += self.learning_rate
        
        return True
    
    async def _teach_master_mind(self, knowledge: Dict):
        """
        آموزش دانش به مغز متفکر
        """
        book_knowledge = knowledge['knowledge']
        
        # آموزش مفاهیم
        for concept in book_knowledge.get('concepts', []):
            await master_mind.learn_from_experience({
                'type': 'concept',
                'content': concept,
                'source': knowledge['metadata']['title'],
                'timestamp': datetime.now().isoformat()
            })
        
        # آموزش نقل قول‌ها
        for quote in book_knowledge.get('quotes', [])[:10]:
            await master_mind.learn_from_experience({
                'type': 'quote',
                'content': quote,
                'source': knowledge['metadata']['title'],
                'timestamp': datetime.now().isoformat()
            })
        
        # آموزش کلمات کلیدی
        for keyword in book_knowledge.get('keywords', [])[:50]:
            await knowledge_engine.add_keyword(keyword, knowledge['metadata']['title'])
    
    async def _store_in_memory(self, book_id: str, knowledge: Dict):
        """
        ذخیره در حافظه بلندمدت
        """
        await memory_core.store(
            key=f"book_{book_id}",
            value=knowledge,
            memory_type='long',
            importance=0.8,
            metadata={
                'title': knowledge['metadata']['title'],
                'author': knowledge['metadata']['author'],
                'learned_at': datetime.now().isoformat()
            }
        )
    
    async def learn_all_books(self):
        """
        یادگیری همه کتاب‌های پردازش شده
        """
        books = downloader.list_books()
        unlearned = [b for b in books if b.get('processed') and not b.get('learned')]
        
        print(f"📚 Found {len(unlearned)} books to learn")
        
        for i, book in enumerate(unlearned, 1):
            print(f"\n[{i}/{len(unlearned)}] ", end="")
            await self.learn_one_book()
            await asyncio.sleep(2)  # کمی صبر
    
    def get_learning_stats(self) -> Dict:
        """
        آمار یادگیری
        """
        books = downloader.list_books()
        processed = len([b for b in books if b.get('processed')])
        learned = len([b for b in books if b.get('learned')])
        
        return {
            'total_books': len(books),
            'processed_books': processed,
            'learned_books': learned,
            'learning_rate': self.learning_rate,
            'wisdom_level': master_mind.consciousness['wisdom'],
            **self.stats
        }

# نمونه‌سازی سراسری
auto_learner = AutoLearner()
