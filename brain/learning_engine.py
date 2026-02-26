#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📚 LEARNING ENGINE - موتور یادگیری خودکار
ربات از هر تعاملی یاد می‌گیرد و تکامل می‌یابد
قابلیت:
- یادگیری از مکالمات
- تشخیص الگوهای جدید
- بهینه‌سازی الگوریتم‌ها
- تطبیق با رفتار کاربران
- کشف دانش جدید
"""

import logging
import asyncio
import json
import hashlib
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import random

logger = logging.getLogger(__name__)

class LearningEngine:
    """
    موتور یادگیری - ربات هر روز باهوش‌تر می‌شود
    """
    
    def __init__(self):
        self.name = "Learning Engine"
        self.version = "1.0.0"
        
        # حافظه یادگیری
        self.learned_patterns = []
        self.successful_predictions = []
        self.failed_predictions = []
        self.user_preferences = defaultdict(dict)
        
        # آمار
        self.stats = {
            'total_learnings': 0,
            'patterns_discovered': 0,
            'accuracy_improvement': 0,
            'current_accuracy': 0.75,
            'last_learning': None
        }
        
        # مدل‌های یادگیری
        self.models = {}
        
        logger.info("📚 Learning Engine initialized")
    
    async def learn_from_interaction(self, interaction: Dict) -> Dict:
        """
        یادگیری از یک تعامل جدید
        """
        self.stats['total_learnings'] += 1
        self.stats['last_learning'] = datetime.now().isoformat()
        
        learning_id = hashlib.md5(f"{datetime.now()}{random.random()}".encode()).hexdigest()[:10]
        
        # استخراج ویژگی‌ها
        features = self._extract_features(interaction)
        
        # تشخیص الگو
        pattern = self._detect_pattern(features)
        
        # به‌روزرسانی مدل
        self._update_model(interaction, pattern)
        
        # ذخیره یادگیری
        learning = {
            'id': learning_id,
            'timestamp': datetime.now().isoformat(),
            'interaction': interaction,
            'features': features,
            'pattern': pattern,
            'applied': False
        }
        
        if pattern:
            self.learned_patterns.append(learning)
            self.stats['patterns_discovered'] += 1
        
        return learning
    
    def _extract_features(self, interaction: Dict) -> Dict:
        """استخراج ویژگی‌ها از تعامل"""
        features = {
            'type': interaction.get('type', 'unknown'),
            'user_id': interaction.get('user_id'),
            'time': interaction.get('timestamp', ''),
            'length': len(str(interaction.get('input', ''))),
            'sentiment': self._analyze_sentiment(interaction.get('input', '')),
            'success': interaction.get('success', False)
        }
        
        return features
    
    def _analyze_sentiment(self, text: str) -> float:
        """تحلیل احساسات متن"""
        # اینجا می‌تونیم از الگوریتم‌های پیچیده‌تر استفاده کنیم
        positive_words = ['good', 'great', 'excellent', 'خوب', 'عالی', 'perfect']
        negative_words = ['bad', 'worst', 'terrible', 'بد', 'افتضاح']
        
        score = 0.5
        text = text.lower()
        
        for word in positive_words:
            if word in text:
                score += 0.1
        
        for word in negative_words:
            if word in text:
                score -= 0.1
        
        return max(0, min(1, score))
    
    def _detect_pattern(self, features: Dict) -> Optional[Dict]:
        """تشخیص الگو در ویژگی‌ها"""
        # الگوهای ساده
        patterns = []
        
        # الگوی زمانی
        hour = datetime.fromisoformat(features['time']).hour if features['time'] else 0
        if hour in [9, 10, 14, 15, 20]:  # ساعات پرترافیک
            patterns.append('peak_hour')
        
        # الگوی طول پیام
        if features['length'] > 500:
            patterns.append('long_message')
        elif features['length'] < 10:
            patterns.append('short_message')
        
        # الگوی احساسات
        if features['sentiment'] > 0.8:
            patterns.append('very_positive')
        elif features['sentiment'] < 0.2:
            patterns.append('very_negative')
        
        if patterns:
            return {
                'type': 'interaction_pattern',
                'patterns': patterns,
                'confidence': len(patterns) * 0.2
            }
        
        return None
    
    def _update_model(self, interaction: Dict, pattern: Optional[Dict]):
        """به‌روزرسانی مدل یادگیری"""
        # ثبت نتیجه
        if interaction.get('success'):
            self.successful_predictions.append(interaction)
            
            # به‌روزرسانی دقت
            total = len(self.successful_predictions) + len(self.failed_predictions)
            if total > 0:
                self.stats['current_accuracy'] = len(self.successful_predictions) / total
            
            # اگر الگویی کشف شد
            if pattern:
                self.stats['accuracy_improvement'] += 0.01
        else:
            self.failed_predictions.append(interaction)
    
    def get_recommendation(self, user_id: int, context: Dict) -> Dict:
        """
        دریافت توصیه بر اساس یادگیری‌های قبلی
        """
        user_history = self.user_preferences.get(user_id, {})
        
        recommendation = {
            'confidence': 0.5,
            'action': 'unknown',
            'based_on': []
        }
        
        # تحلیل تاریخچه کاربر
        if user_history:
            # محبوب‌ترین دستورات کاربر
            commands = user_history.get('commands', [])
            if commands:
                most_used = max(set(commands), key=commands.count)
                recommendation['action'] = most_used
                recommendation['confidence'] = 0.6
                recommendation['based_on'].append('user_history')
        
        # تحلیل الگوهای کلی
        if self.learned_patterns:
            recent_patterns = self.learned_patterns[-10:]
            pattern_types = [p['pattern']['type'] for p in recent_patterns if p['pattern']]
            if pattern_types:
                common_pattern = max(set(pattern_types), key=pattern_types.count)
                recommendation['based_on'].append(common_pattern)
                recommendation['confidence'] += 0.1
        
        return recommendation
    
    def learn_user_preference(self, user_id: int, command: str, success: bool):
        """یادگیری ترجیحات کاربر"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'commands': [],
                'successful_commands': [],
                'failed_commands': [],
                'first_seen': datetime.now().isoformat()
            }
        
        prefs = self.user_preferences[user_id]
        prefs['commands'].append(command)
        prefs['last_seen'] = datetime.now().isoformat()
        
        if success:
            prefs['successful_commands'].append(command)
        else:
            prefs['failed_commands'].append(command)
    
    def get_learning_stats(self) -> Dict:
        """گرفتن آمار یادگیری"""
        return {
            'total_learnings': self.stats['total_learnings'],
            'patterns_discovered': self.stats['patterns_discovered'],
            'accuracy': f"{self.stats['current_accuracy']*100:.1f}%",
            'successful_predictions': len(self.successful_predictions),
            'failed_predictions': len(self.failed_predictions),
            'active_patterns': len(self.learned_patterns),
            'users_learned': len(self.user_preferences)
        }
    
    async def optimize_algorithms(self) -> Dict:
        """
        بهینه‌سازی خودکار الگوریتم‌ها
        """
        optimizations = []
        
        # تحلیل دقت
        if len(self.successful_predictions) > 100:
            accuracy = len(self.successful_predictions) / (
                len(self.successful_predictions) + len(self.failed_predictions)
            )
            
            if accuracy < 0.6:
                optimizations.append('need_improvement')
                # اینجا می‌تونیم الگوریتم‌ها رو بهینه کنیم
        
        # تحلیل الگوها
        if len(self.learned_patterns) > 50:
            pattern_types = {}
            for p in self.learned_patterns[-50:]:
                if p['pattern']:
                    for pat in p['pattern'].get('patterns', []):
                        pattern_types[pat] = pattern_types.get(pat, 0) + 1
            
            optimizations.append({
                'top_patterns': sorted(pattern_types.items(), key=lambda x: x[1], reverse=True)[:5]
            })
        
        return {
            'optimizations_applied': len(optimizations),
            'details': optimizations,
            'timestamp': datetime.now().isoformat()
        }

# نمونه‌سازی سراسری
learning_engine = LearningEngine()
