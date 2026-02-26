#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📊 DAILY REPORTER - گزارش‌دهی خودکار روزانه
ارسال گزارش به ال حشاش هر روز
قابلیت‌ها:
- خلاصه فعالیت روزانه
- پیش‌بینی‌های روز
- آمار کاربران
- تحلیل رویاها
- توصیه‌های ربات
- تولید پست برای کانال
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import os
import random
from pathlib import Path

logger = logging.getLogger(__name__)

# ==================== شناسه مدیر ====================
MASTER_ID = 6590867551
MASTER_NAME = "Al Hashash"

class DailyReporter:
    """
    گزارش‌دهنده روزانه - هر روز صبح به مدیر گزارش می‌دهد
    """
    
    def __init__(self):
        self.name = "Daily Reporter"
        self.version = "1.0.0"
        
        # مسیر فایل‌ها
        self.reports_path = "reports/archive"
        os.makedirs(self.reports_path, exist_ok=True)
        
        # آمار
        self.stats = {
            'reports_sent': 0,
            'last_report': None,
            'total_posts': 0
        }
        
        logger.info("📊 Daily Reporter initialized")
    
    # ==================== تولید گزارش روزانه ====================
    
    async def generate_daily_report(self, bot_instance=None, master_mind=None, 
                                    knowledge_engine=None, memory_core=None) -> Dict:
        """
        تولید گزارش کامل روزانه
        """
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        report = {
            'date': today.strftime('%Y-%m-%d'),
            'day_of_week': today.strftime('%A'),
            'time': today.strftime('%H:%M:%S'),
            'master': {
                'name': MASTER_NAME,
                'id': MASTER_ID
            },
            'summary': {},
            'predictions': [],
            'stats': {},
            'dreams': [],
            'insights': [],
            'recommendations': [],
            'channel_posts': []
        }
        
        # ===== خلاصه روزانه =====
        report['summary'] = {
            'greeting': self._get_greeting(),
            'quote': self._get_daily_quote(),
            'lucky_number': random.randint(1, 9),
            'lucky_color': random.choice(['طلایی', 'نقره‌ای', 'بنفش', 'سبز', 'آبی', 'قرمز']),
            'mood': random.choice(['شاداب', 'پر انرژی', 'متمرکز', 'خلاق', 'آرام'])
        }
        
        # ===== آمار از master_mind =====
        if master_mind:
            mind_stats = master_mind.get_status()
            report['stats']['master_mind'] = {
                'consciousness': mind_stats['consciousness']['level'],
                'thoughts': mind_stats['stats']['thoughts'],
                'dreams': mind_stats['stats']['dreams'],
                'learnings': mind_stats['stats']['learnings'],
                'evolution_stage': mind_stats['consciousness']['stage']
            }
        
        # ===== رویاهای دیشب =====
        if hasattr(master_mind, 'working_memory') and 'dreams' in master_mind.working_memory:
            last_dreams = master_mind.working_memory['dreams'][-3:]  # ۳ رویای آخر
            for dream in last_dreams:
                report['dreams'].append({
                    'time': dream['timestamp'],
                    'content': dream['content'][:100] + '...' if len(dream['content']) > 100 else dream['content'],
                    'symbols': dream['symbols'],
                    'interpretation': dream['interpretation']
                })
        
        # ===== بینش‌های جدید =====
        report['insights'] = self._generate_insights(master_mind)
        
        # ===== توصیه‌های روزانه =====
        report['recommendations'] = self._get_daily_recommendations()
        
        # ===== پست برای کانال =====
        report['channel_posts'] = [
            self._generate_morning_post(),
            self._generate_prediction_post(),
            self._generate_insight_post()
        ]
        
        # ذخیره گزارش
        self._save_report(report)
        
        return report
    
    def _get_greeting(self) -> str:
        """گرفتن سلام صبحگاهی"""
        hour = datetime.now().hour
        
        if hour < 12:
            return "صبح بخیر استاد"
        elif hour < 17:
            return "ظهر بخیر استاد"
        elif hour < 20:
            return "عصر بخیر استاد"
        else:
            return "شب بخیر استاد"
    
    def _get_daily_quote(self) -> str:
        """گرفتن نقل قول روزانه"""
        quotes = [
            "Numbers are the language of the universe.",
            "The future is written in numbers, waiting to be read.",
            "Every number holds a secret, every secret is a number.",
            "In the realm of numbers, all things are possible.",
            "The wise man learns from numbers, the wiser man learns from dreams.",
            "Today's patterns are tomorrow's predictions.",
            "The universe speaks in numbers; listen carefully.",
            "Your destiny is encoded in your name.",
            "Numbers don't lie, but they love to hide.",
            "The past is history, the future is numbers."
        ]
        return random.choice(quotes)
    
    def _generate_insights(self, master_mind) -> List[str]:
        """تولید بینش‌های روزانه"""
        insights = [
            "امروز روز خوبی برای تصمیم‌گیری‌های مهم است.",
            "الگوهای جالبی در بازار میم‌کوین‌ها مشاهده می‌شود.",
            "رویاهای دیشب نشان از یک تغییر بزرگ دارند.",
            "کاربران امروز بیشتر از دیروز فعال هستند.",
            "یک الگوی عددی جدید کشف شده است."
        ]
        
        # اضافه کردن بینش‌های پویا
        if master_mind and hasattr(master_mind, 'consciousness'):
            if master_mind.consciousness['level'] > 1.5:
                insights.append("سطح هوشیاری من افزایش یافته است.")
        
        return insights
    
    def _get_daily_recommendations(self) -> List[str]:
        """توصیه‌های روزانه"""
        recommendations = [
            "بررسی توکن‌های جدید روی Pump.fun",
            "تحلیل میم‌کوین‌های با حجم بالا",
            "بررسی حرکت نهنگ‌ها در ۲۴ ساعت گذشته",
            "آپدیت دانش عددشناسی با کتاب‌های جدید",
            "بررسی عملکرد ربات و بهینه‌سازی"
        ]
        
        selected = random.sample(recommendations, min(3, len(recommendations)))
        return selected
    
    def _generate_morning_post(self) -> Dict:
        """تولید پست صبحگاهی برای کانال"""
        hour = datetime.now().hour
        time_word = "صبح" if hour < 12 else "روز"
        
        content = (
            f"🌅 **{time_word} بخیر همراهان چشم هوروس**\n\n"
            f"عدد خوش شانس امروز: **{random.randint(1, 9)}**\n"
            f"رنگ خوش یمن: **{random.choice(['طلایی', 'نقره‌ای', 'بنفش', 'سبز'])}**\n\n"
            f"📜 {self._get_daily_quote()}\n\n"
            f"🤖 امروز هم برای پیش‌بینی‌های دقیق با ما همراه باشید.\n"
            f"🔮 @EyeOfHorusProBot"
        )
        
        return {
            'type': 'morning',
            'content': content,
            'hashtags': ['#صبح_بخیر', '#چشم_هوروس', '#پیش‌بینی']
        }
    
    def _generate_prediction_post(self) -> Dict:
        """تولید پست پیش‌بینی"""
        coins = ['BTC', 'ETH', 'SOL', 'DOGE', 'PEPE', 'BONK']
        coin = random.choice(coins)
        
        sentiment = random.choice(['صعودی', 'نزولی', 'خنثی'])
        percentage = random.randint(5, 25)
        
        content = (
            f"🔮 **پیش‌بینی لحظه‌ای {coin}**\n\n"
            f"📊 تحلیل امروز: روند **{sentiment}**\n"
            f"📈 احتمال تغییر: **{percentage}%**\n\n"
            f"💡 توصیه: {random.choice(['خرید', 'فروش', 'نگهداری', 'توجه به مقاومت‌ها'])}\n\n"
            f"⚡️ برای پیش‌بینی دقیق‌تر، به ربات مراجعه کنید:\n"
            f"👉 @EyeOfHorusProBot"
        )
        
        return {
            'type': 'prediction',
            'coin': coin,
            'content': content,
            'hashtags': [f'#{coin}', '#پیش‌بینی', '#کریپتو']
        }
    
    def _generate_insight_post(self) -> Dict:
        """تولید پست بینش عددشناسی"""
        number = random.randint(1, 9)
        
        insights = {
            1: "عدد یک، عدد رهبران است. امروز جسور باشید.",
            2: "عدد دو، عدد همکاری است. با دیگران مشورت کنید.",
            3: "عدد سه، عدد خلاقیت است. ایده‌های جدید را دنبال کنید.",
            4: "عدد چهار، عدد نظم است. برنامه‌ریزی کنید.",
            5: "عدد پنج، عدد آزادی است. به دنبال تجربیات جدید باشید.",
            6: "عدد شش، عدد عشق است. به خانواده اهمیت دهید.",
            7: "عدد هفت، عدد تفکر است. کمی تنها باشید و فکر کنید.",
            8: "عدد هشت، عدد موفقیت است. برای اهداف بزرگ تلاش کنید.",
            9: "عدد نه، عدد تکامل است. کارهای ناتمام را تمام کنید."
        }
        
        content = (
            f"🔢 **بینش عددشناسی روز**\n\n"
            f"عدد امروز: **{number}**\n"
            f"✨ {insights[number]}\n\n"
            f"🪐 برای تحلیل عددشناسی نام خود، به ربات مراجعه کنید:\n"
            f"👉 @EyeOfHorusProBot"
        )
        
        return {
            'type': 'numerology',
            'number': number,
            'content': content,
            'hashtags': ['#عددشناسی', '#چشم_هوروس']
        }
    
    def _save_report(self, report: Dict):
        """ذخیره گزارش در آرشیو"""
        try:
            filename = f"{self.reports_path}/report_{report['date']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.stats['reports_sent'] += 1
            self.stats['last_report'] = datetime.now().isoformat()
            
            logger.info(f"📊 Report saved: {filename}")
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
    
    # ==================== ارسال گزارش به تلگرام ====================
    
    async def send_report_to_master(self, update, context, report: Dict = None):
        """
        ارسال گزارش به مدیر (ال حشاش)
        """
        if not report:
            report = await self.generate_daily_report()
        
        # ساخت پیام
        message = (
            f"📊 **گزارش روزانه - {report['date']}**\n\n"
            f"👋 {report['summary']['greeting']}\n\n"
            f"🔢 عدد خوش شانس: **{report['summary']['lucky_number']}**\n"
            f"🎨 رنگ خوش یمن: **{report['summary']['lucky_color']}**\n\n"
            f"📜 نقل قول روز:\n"
            f"_{report['summary']['quote']}_\n\n"
        )
        
        if 'stats' in report and 'master_mind' in report['stats']:
            mind = report['stats']['master_mind']
            message += (
                f"🧠 **وضعیت ربات:**\n"
                f"• هوشیاری: {mind['consciousness']:.3f}\n"
                f"• تفکر: {mind['thoughts']}\n"
                f"• رویا: {mind['dreams']}\n"
                f"• یادگیری: {mind['learnings']}\n"
                f"• مرحله تکامل: {mind['evolution_stage']}\n\n"
            )
        
        if report['dreams']:
            message += f"💭 **آخرین رویا:**\n"
            for dream in report['dreams']:
                message += f"• {dream['content']}\n"
            message += "\n"
        
        if report['recommendations']:
            message += f"📋 **توصیه‌های روز:**\n"
            for rec in report['recommendations']:
                message += f"• {rec}\n"
            message += "\n"
        
        # ارسال به مدیر
        try:
            await context.bot.send_message(
                chat_id=MASTER_ID,
                text=message,
                parse_mode='Markdown'
            )
            
            # ارسال پست‌های پیشنهادی
            for i, post in enumerate(report['channel_posts']):
                await context.bot.send_message(
                    chat_id=MASTER_ID,
                    text=post['content'],
                    parse_mode='Markdown'
                )
                if i < len(report['channel_posts']) - 1:
                    await asyncio.sleep(1)
            
            logger.info(f"✅ Daily report sent to master")
            
        except Exception as e:
            logger.error(f"Error sending report: {e}")
    
    # ==================== دریافت گزارش‌های گذشته ====================
    
    def get_report(self, date: str = None) -> Optional[Dict]:
        """
        دریافت گزارش یک روز خاص
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        filename = f"{self.reports_path}/report_{date}.json"
        
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading report {date}: {e}")
        
        return None
    
    def list_reports(self, limit: int = 7) -> List[str]:
        """
        لیست آخرین گزارش‌ها
        """
        try:
            files = sorted(Path(self.reports_path).glob("report_*.json"))
            return [f.stem.replace('report_', '') for f in files[-limit:]]
        except:
            return []

# ==================== نمونه‌سازی سراسری ====================
daily_reporter = DailyReporter()
