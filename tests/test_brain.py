#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 TEST SUITE - تست جامع تمام بخش‌های ربات
"""

import unittest
import asyncio
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from brain.master_mind import master_mind, MASTER_ID
from brain.knowledge_engine import knowledge_engine
from brain.dream_engine import dream_engine
from brain.memory_core import memory_core
from brain.learning_engine import learning_engine
from brain.api_requester import api_requester

class TestMasterMind(unittest.TestCase):
    """تست مغز متفکر"""
    
    def setUp(self):
        self.master = master_mind
    
    def test_master_id(self):
        """تست تشخیص مدیر"""
        self.assertTrue(self.master.is_master(MASTER_ID))
        self.assertFalse(self.master.is_master(12345))
    
    def test_consciousness(self):
        """تست سطح هوشیاری"""
        self.assertGreaterEqual(self.master.consciousness['level'], 1.0)
        self.assertLessEqual(self.master.consciousness['level'], 10.0)
    
    def test_think(self):
        """تست تفکر"""
        async def run_test():
            result = await self.master.think("test input")
            self.assertIn('id', result)
            self.assertIn('conclusion', result)
        asyncio.run(run_test())

class TestKnowledgeEngine(unittest.TestCase):
    """تست موتور دانش"""
    
    def setUp(self):
        self.knowledge = knowledge_engine
    
    def test_books_loaded(self):
        """تست بارگذاری کتاب‌ها"""
        self.assertGreaterEqual(len(self.knowledge.books), 4)
    
    def test_search(self):
        """تست جستجو"""
        async def run_test():
            results = await self.knowledge.search("number")
            self.assertIsInstance(results, list)
        asyncio.run(run_test())

class TestDreamEngine(unittest.TestCase):
    """تست موتور رویا"""
    
    def setUp(self):
        self.dream = dream_engine
    
    def test_dream(self):
        """تست رویا دیدن"""
        async def run_test():
            dream = await self.dream.dream()
            self.assertIn('id', dream)
            self.assertIn('content', dream)
            self.assertIn('symbols', dream)
        asyncio.run(run_test())
    
    def test_symbols(self):
        """تست نمادها"""
        self.assertGreaterEqual(len(self.dream.SYMBOLS), 10)

class TestMemoryCore(unittest.TestCase):
    """تست حافظه"""
    
    def setUp(self):
        self.memory = memory_core
    
    def test_store_recall(self):
        """تست ذخیره و بازیابی"""
        async def run_test():
            key = "test_key"
            value = {"test": "data", "time": datetime.now().isoformat()}
            
            # ذخیره
            mem_id = await self.memory.store(key, value)
            self.assertIsNotNone(mem_id)
            
            # بازیابی
            results = await self.memory.recall("test")
            self.assertIsInstance(results, list)
        asyncio.run(run_test())

class TestLearningEngine(unittest.TestCase):
    """تست یادگیری"""
    
    def setUp(self):
        self.learning = learning_engine
    
    def test_learn(self):
        """تست یادگیری از تعامل"""
        async def run_test():
            interaction = {
                'type': 'test',
                'input': 'hello',
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            result = await self.learning.learn_from_interaction(interaction)
            self.assertIn('id', result)
        asyncio.run(run_test())
    
    def test_stats(self):
        """تست آمار"""
        stats = self.learning.get_learning_stats()
        self.assertIn('total_learnings', stats)

class TestAPIRequester(unittest.TestCase):
    """تست درخواست API"""
    
    def setUp(self):
        self.api_req = api_requester
    
    def test_api_info(self):
        """تست اطلاعات API"""
        info = self.api_req.get_api_info('etherscan')
        self.assertIsNotNone(info)
        self.assertIn('name', info)
    
    def test_alternatives(self):
        """تست APIهای جایگزین"""
        alts = self.api_req.suggest_alternative('etherscan')
        self.assertIsInstance(alts, list)

def run_all_tests():
    """اجرای همه تست‌ها"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMasterMind))
    suite.addTest(unittest.makeSuite(TestKnowledgeEngine))
    suite.addTest(unittest.makeSuite(TestDreamEngine))
    suite.addTest(unittest.makeSuite(TestMemoryCore))
    suite.addTest(unittest.makeSuite(TestLearningEngine))
    suite.addTest(unittest.makeSuite(TestAPIRequester))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("="*60)
    print("🧪 Running Eye of Horus Test Suite")
    print("="*60)
    success = run_all_tests()
    print("="*60)
    print(f"✅ All tests passed: {success}")
    print("="*60)
