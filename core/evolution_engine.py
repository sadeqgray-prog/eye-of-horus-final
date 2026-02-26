#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
موتور تکامل هوشمند - قلب تپنده پیشرفت ربات
قابلیت‌ها:
- یادگیری از تجربیات
- بهینه‌سازی خودکار
- کشف الگوهای جدید
- ارتقاء نسخه
- پیش‌بینی آینده
"""

import os
import sys
import json
import time
import logging
import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pickle
import random
import threading

logger = logging.getLogger(__name__)

class EvolutionEngine:
    """
    موتور تکامل - مثل یه مغز زنده که هر روز باهوش‌تر میشه
    """
    
    def __init__(self):
        self.version = "5.0.0"
        self.evolution_stage = 1
        self.experience_pool = []
        self.successful_patterns = []
        self.failed_patterns = []
        self.genetic_code = {}
        self.learning_rate = 0.01
        
        # آمار
        self.stats = {
            'total_evolutions': 0,
            'successful_mutations': 0,
            'patterns_discovered': 0,
            'accuracy_improvement': 0,
            'current_accuracy': 0.75
        }
        
        # حافظه ژنتیکی
        self.dna = {
            'intelligence': 50,
            'creativity': 50,
            'memory': 50,
            'speed': 50,
            'accuracy': 50
        }
        
        # بارگذاری حافظه قبلی
        self.load_genetic_memory()
        
        # شروع تکامل خودکار
        self.start_evolution_loop()
        
        logger.info(f"🧬 EvolutionEngine v{self.version} initialized at stage {self.evolution_stage}")
    
    def evolve(self, force: bool = False) -> Dict:
        """
        اجرای یک مرحله تکامل
        """
        # بررسی نیاز به تکامل
        if not force and not self._should_evolve():
            return {'status': 'skipped', 'reason': 'not_ready'}
        
        logger.info("🔄 Starting evolution process...")
        
        # 1. تحلیل تجربیات
        lessons = self._analyze_experiences()
        
        # 2. کشف الگوهای جدید
        new_patterns = self._discover_patterns()
        
        # 3. جهش ژنتیکی
        mutations = self._genetic_mutation()
        
        # 4. به‌روزرسانی DNA
        self._update_dna(mutations)
        
        # 5. ارتقاء نسخه
        self.evolution_stage += 1
        self.stats['total_evolutions'] += 1
        
        # 6. ذخیره حافظه
        self.save_genetic_memory()
        
        result = {
            'new_stage': self.evolution_stage,
            'lessons_learned': len(lessons),
            'new_patterns': len(new_patterns),
            'mutations': mutations,
            'dna': self.dna.copy(),
            'accuracy': self.stats['current_accuracy'],
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Evolution complete: Stage {self.evolution_stage}")
        
        return result
    
    def _should_evolve(self) -> bool:
        """بررسی نیاز به تکامل"""
        
        # معیارهای تکامل:
        # 1. تعداد تجربیات کافی
        if len(self.experience_pool) < 100:
            return False
        
        # 2. زمان از آخرین تکامل
        if hasattr(self, 'last_evolution'):
            if datetime.now() - self.last_evolution < timedelta(hours=24):
                return False
        
        # 3. دقت پایین
        if self.stats['current_accuracy'] < 0.6:
            return True
        
        # 4. کشف الگوهای جدید
        if len(self._detect_anomalies()) > 10:
            return True
        
        return random.random() < 0.1  # 10% شانس تکامل خودکار
    
    def _analyze_experiences(self) -> List[Dict]:
        """تحلیل تجربیات گذشته"""
        lessons = []
        
        if len(self.experience_pool) < 10:
            return lessons
        
        # دسته‌بندی تجربیات
        successful = [exp for exp in self.experience_pool if exp.get('success', False)]
        failed = [exp for exp in self.experience_pool if not exp.get('success', False)]
        
        # محاسبه دقت
        total = len(successful) + len(failed)
        if total > 0:
            self.stats['current_accuracy'] = len(successful) / total
            self.stats['accuracy_improvement'] = self.stats['current_accuracy'] - 0.75
        
        # استخراج درس‌ها
        for exp in successful[-50:]:  # ۵۰ موفقیت آخر
            lesson = {
                'pattern': exp.get('pattern'),
                'context': exp.get('context'),
                'action': exp.get('action'),
                'result': 'success',
                'confidence': exp.get('confidence', 0.8)
            }
            lessons.append(lesson)
            self.successful_patterns.append(lesson)
        
        for exp in failed[-20:]:  # ۲۰ شکست آخر
            lesson = {
                'pattern': exp.get('pattern'),
                'context': exp.get('context'),
                'action': exp.get('action'),
                'result': 'failure',
                'reason': exp.get('error', 'unknown')
            }
            lessons.append(lesson)
            self.failed_patterns.append(lesson)
        
        # محدودیت حجم
        self.successful_patterns = self.successful_patterns[-1000:]
        self.failed_patterns = self.failed_patterns[-500:]
        
        return lessons
    
    def _discover_patterns(self) -> List[Dict]:
        """کشف الگوهای جدید با هوش مصنوعی"""
        new_patterns = []
        
        if len(self.experience_pool) < 50:
            return new_patterns
        
        # تبدیل به بردار
        vectors = []
        for exp in self.experience_pool[-500:]:
            vec = self._experience_to_vector(exp)
            vectors.append(vec)
        
        if len(vectors) < 10:
            return new_patterns
        
        try:
            # خوشه‌بندی با sklearn (اگه باشه)
            from sklearn.cluster import DBSCAN
            import numpy as np
            
            X = np.array(vectors)
            clustering = DBSCAN(eps=0.5, min_samples=3).fit(X)
            
            # پیدا کردن خوشه‌های معنی‌دار
            labels = clustering.labels_
            unique_labels = set(labels)
            
            for label in unique_labels:
                if label == -1:  # نویز
                    continue
                
                cluster_indices = [i for i, l in enumerate(labels) if l == label]
                if len(cluster_indices) >= 3:
                    cluster_exps = [self.experience_pool[-500:][i] for i in cluster_indices]
                    
                    # محاسبه نرخ موفقیت خوشه
                    success_rate = sum(1 for e in cluster_exps if e.get('success', False)) / len(cluster_exps)
                    
                    if success_rate > 0.7:  # الگوی قابل اعتماد
                        pattern = {
                            'id': hashlib.md5(str(cluster_indices).encode()).hexdigest()[:10],
                            'type': 'success_pattern',
                            'size': len(cluster_exps),
                            'success_rate': success_rate,
                            'features': self._extract_common_features(cluster_exps),
                            'discovered_at': datetime.now().isoformat()
                        }
                        new_patterns.append(pattern)
                        self.stats['patterns_discovered'] += 1
                        
        except Exception as e:
            logger.error(f"Pattern discovery error: {e}")
        
        return new_patterns
    
    def _experience_to_vector(self, experience: Dict) -> List[float]:
        """تبدیل تجربه به بردار عددی"""
        vector = []
        
        # ویژگی‌های عددی
        vector.append(experience.get('confidence', 0.5))
        vector.append(1.0 if experience.get('success', False) else 0.0)
        vector.append(experience.get('complexity', 0.5))
        
        # زمان
        if 'timestamp' in experience:
            dt = datetime.fromisoformat(experience['timestamp'])
            hour = dt.hour / 24
            day = dt.weekday() / 7
            vector.extend([hour, day])
        
        # پر کردن به طول ثابت
        while len(vector) < 10:
            vector.append(0)
        
        return vector[:10]
    
    def _extract_common_features(self, experiences: List[Dict]) -> Dict:
        """استخراج ویژگی‌های مشترک"""
        common = {}
        
        # جمع‌آوری همه کلیدها
        all_keys = set()
        for exp in experiences:
            all_keys.update(exp.keys())
        
        for key in all_keys:
            values = [exp.get(key) for exp in experiences if key in exp]
            if values:
                # اگه همه یکسان بودن
                if all(v == values[0] for v in values):
                    common[key] = values[0]
        
        return common
    
    def _genetic_mutation(self) -> Dict:
        """جهش ژنتیکی برای بهبود"""
        mutations = {}
        
        for trait in self.dna:
            # احتمال جهش
            if random.random() < 0.3:
                # مقدار جهش
                mutation = random.uniform(-5, 5)
                old_value = self.dna[trait]
                new_value = max(0, min(100, old_value + mutation))
                
                if abs(new_value - old_value) > 1:
                    mutations[trait] = {
                        'from': old_value,
                        'to': new_value,
                        'delta': mutation
                    }
        
        if mutations:
            self.stats['successful_mutations'] += 1
        
        return mutations
    
    def _update_dna(self, mutations: Dict):
        """به‌روزرسانی DNA با جهش‌ها"""
        for trait, change in mutations.items():
            self.dna[trait] = change['to']
    
    def learn_from_experience(self, experience: Dict):
        """
        یادگیری از یک تجربه جدید
        """
        # افزودن به pool
        self.experience_pool.append({
            **experience,
            'timestamp': datetime.now().isoformat(),
            'id': hashlib.md5(str(time.time()).encode()).hexdigest()[:10]
        })
        
        # محدودیت حجم
        if len(self.experience_pool) > 10000:
            self.experience_pool = self.experience_pool[-10000:]
        
        # بررسی نیاز به تکامل
        if len(self.experience_pool) % 100 == 0:
            self.evolve()
    
    def get_recommendation(self, context: Dict) -> Dict:
        """
        دریافت توصیه بر اساس تجربیات گذشته
        """
        # پیدا کردن تجربیات مشابه
        similar = self._find_similar_experiences(context)
        
        if not similar:
            return {'action': 'unknown', 'confidence': 0.3}
        
        # محاسبه بهترین اقدام
        actions = {}
        for exp in similar:
            action = exp.get('action')
            if action:
                if action not in actions:
                    actions[action] = {'count': 0, 'success': 0}
                actions[action]['count'] += 1
                if exp.get('success', False):
                    actions[action]['success'] += 1
        
        if not actions:
            return {'action': 'unknown', 'confidence': 0.3}
        
        # انتخاب بهترین
        best_action = max(actions.items(), 
                         key=lambda x: x[1]['success'] / max(x[1]['count'], 1))
        
        confidence = best_action[1]['success'] / max(best_action[1]['count'], 1)
        
        return {
            'action': best_action[0],
            'confidence': confidence,
            'similar_count': len(similar),
            'based_on': best_action[1]['count']
        }
    
    def _find_similar_experiences(self, context: Dict, limit: int = 10) -> List[Dict]:
        """پیدا کردن تجربیات مشابه"""
        similar = []
        
        for exp in self.experience_pool[-1000:]:  # ۱۰۰۰ تای آخر
            similarity = self._calculate_similarity(context, exp)
            if similarity > 0.7:
                similar.append((similarity, exp))
        
        # مرتب‌سازی بر اساس شباهت
        similar.sort(key=lambda x: x[0], reverse=True)
        
        return [exp for _, exp in similar[:limit]]
    
    def _calculate_similarity(self, context: Dict, experience: Dict) -> float:
        """محاسبه شباهت بین دو دیکشنری"""
        common_keys = set(context.keys()) & set(experience.keys())
        
        if not common_keys:
            return 0
        
        similarities = []
        for key in common_keys:
            val1 = context[key]
            val2 = experience[key]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # شباهت عددی
                max_val = max(abs(val1), abs(val2))
                if max_val > 0:
                    sim = 1 - abs(val1 - val2) / max_val
                else:
                    sim = 1
                similarities.append(sim)
            else:
                # شباهت رشته‌ای
                sim = 1 if str(val1) == str(val2) else 0
                similarities.append(sim)
        
        return sum(similarities) / len(similarities) if similarities else 0
    
    def _detect_anomalies(self) -> List[Dict]:
        """تشخیص ناهنجاری‌ها برای تکامل"""
        anomalies = []
        
        if len(self.experience_pool) < 50:
            return anomalies
        
        # محاسبه میانگین و انحراف معیار
        values = []
        for exp in self.experience_pool[-100:]:
            if 'confidence' in exp:
                values.append(exp['confidence'])
        
        if len(values) < 10:
            return anomalies
        
        mean = sum(values) / len(values)
        std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        
        # پیدا کردن نقاط دورافتاده
        for i, exp in enumerate(self.experience_pool[-100:]):
            if 'confidence' in exp:
                z_score = abs(exp['confidence'] - mean) / max(std, 0.001)
                if z_score > 3:
                    anomalies.append({
                        'index': i,
                        'value': exp['confidence'],
                        'z_score': z_score,
                        'experience': exp
                    })
        
        return anomalies
    
    def start_evolution_loop(self):
        """شروع حلقه تکامل خودکار در پس‌زمینه"""
        
        def evolution_worker():
            while True:
                try:
                    time.sleep(3600)  # چک هر ساعت
                    self.evolve()
                except:
                    pass
        
        thread = threading.Thread(target=evolution_worker, daemon=True)
        thread.start()
        logger.info("🔄 Evolution loop started")
    
    def save_genetic_memory(self):
        """ذخیره حافظه ژنتیکی"""
        try:
            memory_file = 'memory/evolution_memory.pkl'
            os.makedirs('memory', exist_ok=True)
            
            memory = {
                'version': self.version,
                'stage': self.evolution_stage,
                'dna': self.dna,
                'stats': self.stats,
                'successful_patterns': self.successful_patterns[-500:],
                'failed_patterns': self.failed_patterns[-500:],
                'timestamp': datetime.now().isoformat()
            }
            
            with open(memory_file, 'wb') as f:
                pickle.dump(memory, f)
                
        except Exception as e:
            logger.error(f"Failed to save genetic memory: {e}")
    
    def load_genetic_memory(self):
        """بارگذاری حافظه ژنتیکی"""
        try:
            memory_file = 'memory/evolution_memory.pkl'
            if os.path.exists(memory_file):
                with open(memory_file, 'rb') as f:
                    memory = pickle.load(f)
                    self.version = memory.get('version', self.version)
                    self.evolution_stage = memory.get('stage', self.evolution_stage)
                    self.dna = memory.get('dna', self.dna)
                    self.stats = memory.get('stats', self.stats)
                    self.successful_patterns = memory.get('successful_patterns', [])
                    self.failed_patterns = memory.get('failed_patterns', [])
                    logger.info(f"🧬 Loaded genetic memory: stage {self.evolution_stage}")
        except:
            pass
    
    def get_dna_report(self) -> Dict:
        """گزارش کامل DNA"""
        return {
            'version': self.version,
            'stage': self.evolution_stage,
            'dna': self.dna,
            'stats': self.stats,
            'experience_count': len(self.experience_pool),
            'patterns': {
                'successful': len(self.successful_patterns),
                'failed': len(self.failed_patterns),
                'discovered': self.stats['patterns_discovered']
            },
            'learning_rate': self.learning_rate,
            'next_evolution': self._estimate_next_evolution()
        }
    
    def _estimate_next_evolution(self) -> str:
        """تخمین زمان تکامل بعدی"""
        if hasattr(self, 'last_evolution'):
            next_time = self.last_evolution + timedelta(hours=24)
            return next_time.isoformat()
        return datetime.now().isoformat()

# نمونه‌سازی سراسری
evolution_engine = EvolutionEngine()
