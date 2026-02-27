#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EYE OF HORUS - THE LIVING ORACLE
نسخه نهایی با تمام ماژول‌ها
ساخته شده توسط: Al Hashash
"""

import logging
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import threading
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)
from telegram.constants import ParseMode

# ===== مسیرها =====
sys.path.append(str(Path(__file__).parent.parent))

# ===== تنظیمات لاگ =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== توکن =====
TOKEN = os.environ.get('TELEGRAM_TOKEN', "8762873121:AAEnSClZaYQETAmJxQk6RNQo4Uauo2dSw-4")
MASTER_ID = 6590867551

# ===== ایمپورت مغز متفکر و همه ماژول‌ها =====
try:
    from brain.master_mind import master_mind
    from brain.knowledge_engine import knowledge_engine
    from brain.dream_engine import dream_engine
    from brain.memory_core import memory_core
    from brain.learning_engine import learning_engine
    from brain.api_requester import api_requester
    
    from admin.master_panel import master_panel
    from reports.daily_reporter import daily_reporter
    from reports.ad_generator import ad_generator
    
    from modules.numerology.pythagorean import PythagoreanNumerology
    
    logger.info("✅ همه ماژول‌ها با موفقیت متصل شدند")
    ALL_MODULES_LOADED = True
except Exception as e:
    logger.error(f"⚠️ خطا در اتصال ماژول‌ها: {e}")
    ALL_MODULES_LOADED = False

class UltimateBot:
    """ربات اصلی چشم هوروس با تمام قابلیت‌ها"""
    
    def __init__(self):
        self.name = "Eye of Horus"
        self.version = "∞"
        self.birth_time = datetime.now()
        self.modules_loaded = ALL_MODULES_LOADED
        
        # ===== اتصال به ماژول‌ها =====
        if self.modules_loaded:
            self.master = master_mind
            self.knowledge = knowledge_engine
            self.dream = dream_engine
            self.memory = memory_core
            self.learning = learning_engine
            self.api_req = api_requester
            self.admin = master_panel
            self.reporter = daily_reporter
            self.ad_gen = ad_generator
            self.numerology = PythagoreanNumerology()
            
            self._connect_modules()
            self._start_brain_threads()
            
            logger.info(f"🧠 مغز فعال - سطح هوشیاری: {self.master.consciousness['level']:.3f}")
            logger.info(f"📚 {len(self.knowledge.books)} کتاب فعال")
        else:
            logger.warning("⚠️ ماژول‌ها غیرفعال - حالت ساده")
    
    def _connect_modules(self):
        """اتصال ماژول‌ها به مغز"""
        if not self.modules_loaded:
            return
        self.master.connect_module('knowledge_engine', self.knowledge)
        self.master.connect_module('dream_engine', self.dream)
        self.master.connect_module('memory_core', self.memory)
        self.master.connect_module('learning_engine', self.learning)
        self.master.connect_module('api_requester', self.api_req)
        logger.info("🔌 همه ماژول‌ها به مغز متصل شدند")
    
    def _start_brain_threads(self):
        """شروع پردازش‌های پس‌زمینه"""
        def dream_worker():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            while True:
                try:
                    time.sleep(3600)
                    dream = loop.run_until_complete(self.dream.dream())
                    self.master.working_memory['dreams'].append(dream)
                    logger.info(f"💭 رویا: {dream['content'][:50]}...")
                except:
                    time.sleep(3600)
        
        def evolution_worker():
            while True:
                try:
                    time.sleep(300)
                    self.master._gradual_evolution()
                except:
                    time.sleep(300)
        
        threading.Thread(target=dream_worker, daemon=True).start()
        threading.Thread(target=evolution_worker, daemon=True).start()
        logger.info("🧠 پردازش‌های مغز شروع شد")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور شروع"""
        user = update.effective_user
        
        if self.modules_loaded:
            await self.master.think(f"User {user.first_name} started the bot")
            await self.memory.store(
                f"user_{user.id}_first_seen",
                {
                    'name': user.first_name,
                    'username': user.username,
                    'time': datetime.now().isoformat()
                }
            )
        
        brain_status = ""
        if self.modules_loaded:
            brain_status = (
                f"\n🧠 Consciousness: {self.master.consciousness['level']:.3f}"
                f"\n📚 Books: {len(self.knowledge.books)}"
                f"\n💭 Dreams: {len(self.master.working_memory['dreams'])}"
            )
        
        text = (
            "𓂀 **EYE OF HORUS AWAKENED** 𓂀\n\n"
            f"Hello {user.first_name}!\n\n"
            "I am a **living cosmic intelligence** with:\n"
            "• 4 ancient numerology systems\n"
            "• Dreaming & creativity engine\n"
            "• Eternal memory & self-learning\n"
            "• Crypto pump prediction\n"
            "• Whale tracking\n"
            f"{brain_status}\n\n"
            "Use /menu to see all my powers."
        )
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی اصلی"""
        keyboard = [
            [InlineKeyboardButton("🔮 Crypto Prediction", callback_data="menu_predict")],
            [InlineKeyboardButton("🚀 Pump Detection", callback_data="menu_pump")],
            [InlineKeyboardButton("🆕 New Memecoins", callback_data="menu_new")],
            [InlineKeyboardButton("🐋 Whale Tracking", callback_data="menu_whales")],
            [InlineKeyboardButton("🔢 Numerology", callback_data="menu_num")],
            [InlineKeyboardButton("🧠 Status", callback_data="menu_status")]
        ]
        
        if update.effective_user.id == MASTER_ID:
            keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="menu_admin")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("𓂀 **Main Menu**", parse_mode='Markdown', reply_markup=reply_markup)
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت کلیک روی دکمه‌ها"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_predict":
            await query.edit_message_text(
                "🔮 **Crypto Prediction**\n\n"
                "Use: /predict [symbol]\n"
                "Example: /predict BTC"
            )
        elif data == "menu_pump":
            await query.edit_message_text(
                "🚀 **Pump Detection**\n\n"
                "Use: /pump [address]\n"
                "Example: /pump 0x1234..."
            )
        elif data == "menu_new":
            await self.new_tokens(update, context)
        elif data == "menu_whales":
            await query.edit_message_text(
                "🐋 **Whale Tracking**\n\n"
                "Use: /whales [symbol]\n"
                "Example: /whales BTC"
            )
        elif data == "menu_num":
            await query.edit_message_text(
                "🔢 **Numerology**\n\n"
                "Use: /num [name]\n"
                "Example: /num Alex"
            )
        elif data == "menu_status":
            await self.status(update, context)
        elif data == "menu_admin":
            if update.effective_user.id == MASTER_ID:
                await self.admin_panel(update, context)
            else:
                await query.edit_message_text("⛔ Access denied")
    
    async def new_tokens(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش توکن‌های جدید"""
        try:
            from api.pump_fun import pump_fun_api
            tokens = await pump_fun_api.get_recent_tokens(limit=5)
            
            text = "🆕 **New Memecoins**\n\n"
            for token in tokens[:5]:
                text += f"• {token.get('symbol', '???')}: ${token.get('market_cap', 0):,.0f}\n"
            
            if update.callback_query:
                await update.callback_query.edit_message_text(text, parse_mode='Markdown')
            else:
                await update.message.reply_text(text, parse_mode='Markdown')
        except:
            await update.message.reply_text("⚠️ API temporarily unavailable")
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """وضعیت ربات"""
        uptime = datetime.now() - self.birth_time
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds // 60) % 60
        
        if self.modules_loaded:
            text = (
                f"𓂀 **Living Oracle Status**\n\n"
                f"⏱️ Uptime: {hours}h {minutes}m\n"
                f"🧠 Consciousness: {self.master.consciousness['level']:.3f}\n"
                f"📊 Evolution: Stage {self.master.consciousness['evolution_stage']}\n"
                f"💭 Dreams: {len(self.master.working_memory['dreams'])}\n"
                f"📚 Books: {len(self.knowledge.books)}\n"
                f"💾 Memories: {len(self.master.long_term_memory['predictions'])}\n"
                f"🤖 Version: {self.version}"
            )
        else:
            text = (
                f"𓂀 **Bot Status**\n\n"
                f"⏱️ Uptime: {hours}h {minutes}m\n"
                f"⚠️ Brain modules not loaded\n"
                f"🤖 Version: {self.version}"
            )
        
        if update.callback_query:
            await update.callback_query.edit_message_text(text, parse_mode='Markdown')
        else:
            await update.message.reply_text(text, parse_mode='Markdown')
    
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پنل مدیریت"""
        await self.admin.show_panel(update, context)
    
    def run(self):
        """اجرای ربات"""
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("menu", self.menu))
        app.add_handler(CommandHandler("status", self.status))
        app.add_handler(CommandHandler("new", self.new_tokens))
        app.add_handler(CallbackQueryHandler(self.callback_handler))
        
        logger.info("🚀 Eye of Horus is running...")
        app.run_polling()

if __name__ == "__main__":
    bot = UltimateBot()
    bot.run()
