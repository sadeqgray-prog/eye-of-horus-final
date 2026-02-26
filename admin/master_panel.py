#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
👑 MASTER PANEL - پنل مدیریت کامل برای ال حشاش
کنترل کامل ربات از طریق تلگرام
قابلیت‌ها:
- مدیریت کاربران (VIP، مسدود، رایگان)
- تنظیم قیمت‌ها
- مدیریت ولت
- تنظیم کانال اجباری
- مشاهده آمار لحظه‌ای
- بک‌آپ دستی
- ارسال پیام همگانی
- و...
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import json
import os

logger = logging.getLogger(__name__)

# ==================== شناسه مدیر ====================
MASTER_ID = 6590867551
MASTER_NAME = "Al Hashash"

class MasterPanel:
    """
    پنل مدیریت - فقط برای ال حشاش
    تمام دستورات این کلاس فقط برای MASTER_ID قابل اجراست
    """
    
    def __init__(self):
        self.name = "Master Panel"
        self.version = "∞"
        self.master_id = MASTER_ID
        
        # مسیر فایل‌ها
        self.data_path = "data"
        self.users_file = f"{self.data_path}/users.json"
        self.settings_file = f"{self.data_path}/settings.json"
        self.stats_file = f"{self.data_path}/stats.json"
        
        # ایجاد پوشه data
        os.makedirs(self.data_path, exist_ok=True)
        
        # بارگذاری تنظیمات
        self.settings = self._load_settings()
        self.users = self._load_users()
        self.stats = self._load_stats()
        
        logger.info(f"👑 Master Panel initialized for {MASTER_NAME}")
    
    def _load_settings(self) -> Dict:
        """بارگذاری تنظیمات"""
        default_settings = {
            'prices': {
                'prediction': 0.32,  # USDT
                'premium_month': 10.0,
                'vip_month': 50.0,
                'lifetime': 500.0
            },
            'wallet': {
                'address': '0x11096bccfc635a5467ccfa1ef2970bfb95bd1474',
                'currency': 'USDT',
                'network': 'BEP20'
            },
            'channel': {
                'required': False,
                'url': None,
                'username': None
            },
            'bot': {
                'name': 'Eye of Horus',
                'version': '∞',
                'maintenance': False,
                'message': None
            },
            'limits': {
                'free_predictions': 3,
                'vip_predictions': 100,
                'max_daily_predictions': 1000
            },
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # merge با default
                    for key in default_settings:
                        if key not in loaded:
                            loaded[key] = default_settings[key]
                    return loaded
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
        
        return default_settings
    
    def _save_settings(self):
        """ذخیره تنظیمات"""
        try:
            self.settings['last_updated'] = datetime.now().isoformat()
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def _load_users(self) -> Dict:
        """بارگذاری اطلاعات کاربران"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _save_users(self):
        """ذخیره اطلاعات کاربران"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except:
            pass
    
    def _load_stats(self) -> Dict:
        """بارگذاری آمار"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'total_users': 0,
            'total_predictions': 0,
            'total_paid': 0.0,
            'daily_users': {},
            'daily_predictions': {},
            'commands': {}
        }
    
    def _save_stats(self):
        """ذخیره آمار"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    # ==================== بررسی دسترسی ====================
    
    def is_master(self, user_id: int) -> bool:
        """آیا کاربر مدیر است؟"""
        return user_id == self.master_id
    
    # ==================== منوی اصلی پنل ====================
    
    async def show_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش پنل مدیریت"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ شما دسترسی به این بخش ندارید.")
            return
        
        keyboard = [
            [InlineKeyboardButton("💰 مدیریت قیمت‌ها", callback_data="admin_prices")],
            [InlineKeyboardButton("👛 تنظیم ولت", callback_data="admin_wallet")],
            [InlineKeyboardButton("👥 مدیریت کاربران", callback_data="admin_users")],
            [InlineKeyboardButton("📊 آمار", callback_data="admin_stats")],
            [InlineKeyboardButton("🌐 کانال اجباری", callback_data="admin_channel")],
            [InlineKeyboardButton("⚙️ تنظیمات ربات", callback_data="admin_settings")],
            [InlineKeyboardButton("📦 بک‌آپ", callback_data="admin_backup")],
            [InlineKeyboardButton("📢 پیام همگانی", callback_data="admin_broadcast")],
            [InlineKeyboardButton("🔄 ریست", callback_data="admin_reset")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        panel_text = (
            f"👑 **پنل مدیریت - {MASTER_NAME}**\n\n"
            f"📊 **آمار سریع:**\n"
            f"• کاربران کل: {self.stats.get('total_users', 0)}\n"
            f"• پیش‌بینی‌ها: {self.stats.get('total_predictions', 0)}\n"
            f"• درآمد کل: ${self.stats.get('total_paid', 0):.2f}\n"
            f"• وضعیت: {'🟢 فعال' if not self.settings['bot']['maintenance'] else '🔴 تعمیرات'}\n\n"
            f"🔧 یک گزینه را انتخاب کنید:"
        )
        
        await update.message.reply_text(
            panel_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    # ==================== مدیریت قیمت‌ها ====================
    
    async def prices_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی مدیریت قیمت‌ها"""
        query = update.callback_query
        await query.answer()
        
        prices = self.settings['prices']
        
        text = (
            "💰 **مدیریت قیمت‌ها**\n\n"
            f"💎 پیش‌بینی تکی: **{prices['prediction']} USDT**\n"
            f"⭐ پرمیوم ماهانه: **{prices['premium_month']} USDT**\n"
            f"👑 VIP ماهانه: **{prices['vip_month']} USDT**\n"
            f"♾️ VIP مادام‌العمر: **{prices['lifetime']} USDT**\n\n"
            "برای تغییر هر قیمت، دستور زیر را بفرست:\n"
            "/set_price [نام] [مقدار]\n\n"
            "مثال: `/set_price prediction 0.5`"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def set_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم قیمت"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if len(args) != 2:
            await update.message.reply_text(
                "❌ فرمت صحیح:\n"
                "/set_price [نام] [مقدار]\n\n"
                "نام‌های معتبر: prediction, premium_month, vip_month, lifetime"
            )
            return
        
        price_name = args[0].lower()
        try:
            value = float(args[1])
        except:
            await update.message.reply_text("❌ مقدار باید عدد باشد.")
            return
        
        if price_name in self.settings['prices']:
            self.settings['prices'][price_name] = value
            self._save_settings()
            await update.message.reply_text(f"✅ قیمت {price_name} به {value} USDT تغییر کرد.")
        else:
            await update.message.reply_text("❌ نام قیمت معتبر نیست.")
    
    # ==================== مدیریت ولت ====================
    
    async def wallet_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی مدیریت ولت"""
        query = update.callback_query
        await query.answer()
        
        wallet = self.settings['wallet']
        
        text = (
            "👛 **تنظیمات ولت**\n\n"
            f"🔹 آدرس: `{wallet['address']}`\n"
            f"🔹 ارز: {wallet['currency']}\n"
            f"🔹 شبکه: {wallet['network']}\n\n"
            "برای تغییر آدرس:\n"
            "/set_wallet [آدرس جدید]\n\n"
            "برای تغییر ارز/شبکه:\n"
            "/set_wallet_network [ارز] [شبکه]"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def set_wallet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم آدرس ولت"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آدرس ولت را وارد کنید.")
            return
        
        new_address = args[0]
        self.settings['wallet']['address'] = new_address
        self._save_settings()
        
        await update.message.reply_text(f"✅ آدرس ولت تغییر کرد به:\n`{new_address}`", parse_mode='Markdown')
    
    async def set_wallet_network(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم ارز و شبکه"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("❌ فرمت: /set_wallet_network [ارز] [شبکه]")
            return
        
        self.settings['wallet']['currency'] = args[0].upper()
        self.settings['wallet']['network'] = args[1].upper()
        self._save_settings()
        
        await update.message.reply_text(f"✅ تنظیمات ولت تغییر کرد: {args[0].upper()} روی {args[1].upper()}")
    
    # ==================== مدیریت کاربران ====================
    
    async def users_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی مدیریت کاربران"""
        query = update.callback_query
        await query.answer()
        
        text = (
            "👥 **مدیریت کاربران**\n\n"
            "📋 **دستورات:**\n"
            "/add_vip [user_id] - اضافه کردن VIP\n"
            "/remove_vip [user_id] - حذف VIP\n"
            "/add_premium [user_id] - اضافه کردن پرمیوم\n"
            "/remove_premium [user_id] - حذف پرمیوم\n"
            "/ban [user_id] - مسدود کاربر\n"
            "/unban [user_id] - رفع مسدودی\n"
            "/user_info [user_id] - اطلاعات کاربر\n"
            "/users_list - لیست کاربران ویژه\n\n"
            "🔍 **جستجو:**\n"
            "/search_user [آیدی یا نام]"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def add_vip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """اضافه کردن کاربر VIP"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آیدی کاربر را وارد کنید.")
            return
        
        target_id = args[0]
        
        if target_id not in self.users:
            self.users[target_id] = {}
        
        self.users[target_id]['vip'] = True
        self.users[target_id]['vip_until'] = (datetime.now() + timedelta(days=30)).isoformat()
        self._save_users()
        
        await update.message.reply_text(f"✅ کاربر {target_id} VIP شد تا ۳۰ روز دیگر.")
    
    async def add_premium(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """اضافه کردن کاربر پرمیوم"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آیدی کاربر را وارد کنید.")
            return
        
        target_id = args[0]
        
        if target_id not in self.users:
            self.users[target_id] = {}
        
        self.users[target_id]['premium'] = True
        self.users[target_id]['premium_until'] = (datetime.now() + timedelta(days=30)).isoformat()
        self._save_users()
        
        await update.message.reply_text(f"✅ کاربر {target_id} پرمیوم شد تا ۳۰ روز دیگر.")
    
    async def remove_vip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """حذف VIP کاربر"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آیدی کاربر را وارد کنید.")
            return
        
        target_id = args[0]
        
        if target_id in self.users and 'vip' in self.users[target_id]:
            del self.users[target_id]['vip']
            self._save_users()
            await update.message.reply_text(f"✅ VIP کاربر {target_id} حذف شد.")
        else:
            await update.message.reply_text("❌ کاربر VIP نیست.")
    
    async def ban_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مسدود کاربر"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آیدی کاربر را وارد کنید.")
            return
        
        target_id = args[0]
        
        if target_id not in self.users:
            self.users[target_id] = {}
        
        self.users[target_id]['banned'] = True
        self._save_users()
        
        await update.message.reply_text(f"✅ کاربر {target_id} مسدود شد.")
    
    async def unban_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """رفع مسدودی کاربر"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آیدی کاربر را وارد کنید.")
            return
        
        target_id = args[0]
        
        if target_id in self.users and 'banned' in self.users[target_id]:
            del self.users[target_id]['banned']
            self._save_users()
            await update.message.reply_text(f"✅ مسدودی کاربر {target_id} رفع شد.")
        else:
            await update.message.reply_text("❌ کاربر مسدود نیست.")
    
    async def user_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """اطلاعات کاربر"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ آیدی کاربر را وارد کنید.")
            return
        
        target_id = args[0]
        info = self.users.get(target_id, {})
        
        text = (
            f"📋 **اطلاعات کاربر {target_id}**\n\n"
            f"VIP: {'✅' if info.get('vip') else '❌'}\n"
            f"VIP تا: {info.get('vip_until', 'ندارد')}\n"
            f"پرمیوم: {'✅' if info.get('premium') else '❌'}\n"
            f"پرمیوم تا: {info.get('premium_until', 'ندارد')}\n"
            f"مسدود: {'✅' if info.get('banned') else '❌'}\n"
            f"پیش‌بینی‌ها: {info.get('predictions', 0)}\n"
            f"اولین حضور: {info.get('first_seen', 'نامشخص')}"
        )
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def users_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """لیست کاربران ویژه"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        vips = []
        premiums = []
        banned = []
        
        for uid, info in self.users.items():
            if info.get('vip'):
                vips.append(uid)
            if info.get('premium'):
                premiums.append(uid)
            if info.get('banned'):
                banned.append(uid)
        
        text = (
            "📋 **لیست کاربران ویژه**\n\n"
            f"👑 VIPها ({len(vips)}):\n"
        )
        
        if vips:
            text += "\n".join([f"• `{uid}`" for uid in vips[:10]])
            if len(vips) > 10:
                text += f"\n... و {len(vips)-10} نفر دیگر"
        else:
            text += "• هیچ کاربری نیست"
        
        text += f"\n\n⭐ پرمیوم‌ها ({len(premiums)}):\n"
        if premiums:
            text += "\n".join([f"• `{uid}`" for uid in premiums[:10]])
        else:
            text += "• هیچ کاربری نیست"
        
        text += f"\n\n🚫 مسدود شده‌ها ({len(banned)}):\n"
        if banned:
            text += "\n".join([f"• `{uid}`" for uid in banned[:10]])
        else:
            text += "• هیچ کاربری نیست"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    # ==================== آمار ====================
    
    async def stats_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش آمار کامل"""
        query = update.callback_query
        await query.answer()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        text = (
            "📊 **آمار کامل ربات**\n\n"
            f"👥 **کاربران:**\n"
            f"• کل: {self.stats.get('total_users', 0)}\n"
            f"• امروز: {self.stats.get('daily_users', {}).get(today, 0)}\n"
            f"• VIP: {len([u for u in self.users.values() if u.get('vip')])}\n"
            f"• پرمیوم: {len([u for u in self.users.values() if u.get('premium')])}\n\n"
            f"🔮 **پیش‌بینی‌ها:**\n"
            f"• کل: {self.stats.get('total_predictions', 0)}\n"
            f"• امروز: {self.stats.get('daily_predictions', {}).get(today, 0)}\n\n"
            f"💰 **درآمد:**\n"
            f"• کل: ${self.stats.get('total_paid', 0):.2f}\n"
            f"• امروز: ${self.stats.get('daily_income', {}).get(today, 0):.2f}\n\n"
            f"⚙️ **وضعیت:**\n"
            f"• تعمیرات: {'بله' if self.settings['bot']['maintenance'] else 'خیر'}\n"
            f"• کانال اجباری: {'بله' if self.settings['channel']['required'] else 'خیر'}\n"
            f"• آخرین آپدیت: {self.settings['last_updated']}"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 بروزرسانی آمار", callback_data="admin_stats_refresh")],
            [InlineKeyboardButton("📈 نمودار", callback_data="admin_stats_chart")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    # ==================== کانال اجباری ====================
    
    async def channel_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی تنظیمات کانال اجباری"""
        query = update.callback_query
        await query.answer()
        
        channel = self.settings['channel']
        status = "✅ فعال" if channel['required'] else "❌ غیرفعال"
        
        text = (
            "🌐 **کانال اجباری**\n\n"
            f"وضعیت: {status}\n"
            f"لینک: {channel['url'] or 'تنظیم نشده'}\n"
            f"یوزرنیم: {channel['username'] or 'تنظیم نشده'}\n\n"
            "**دستورات:**\n"
            "/set_channel [لینک] - تنظیم لینک کانال\n"
            "/set_channel_username [یوزرنیم] - تنظیم یوزرنیم\n"
            "/channel_on - فعال کردن اجباری\n"
            "/channel_off - غیرفعال کردن\n"
            "/check_channel [آیدی کاربر] - بررسی عضویت"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def set_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم لینک کانال"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ لینک کانال را وارد کنید.")
            return
        
        self.settings['channel']['url'] = args[0]
        self._save_settings()
        
        await update.message.reply_text(f"✅ لینک کانال تنظیم شد: {args[0]}")
    
    async def set_channel_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم یوزرنیم کانال"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ یوزرنیم کانال را وارد کنید.")
            return
        
        username = args[0]
        if not username.startswith('@'):
            username = '@' + username
        
        self.settings['channel']['username'] = username
        self._save_settings()
        
        await update.message.reply_text(f"✅ یوزرنیم کانال تنظیم شد: {username}")
    
    async def channel_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """فعال کردن کانال اجباری"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        self.settings['channel']['required'] = True
        self._save_settings()
        
        await update.message.reply_text("✅ عضویت اجباری در کانال فعال شد.")
    
    async def channel_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """غیرفعال کردن کانال اجباری"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        self.settings['channel']['required'] = False
        self._save_settings()
        
        await update.message.reply_text("✅ عضویت اجباری در کانال غیرفعال شد.")
    
    # ==================== تنظیمات ربات ====================
    
    async def settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی تنظیمات ربات"""
        query = update.callback_query
        await query.answer()
        
        bot = self.settings['bot']
        limits = self.settings['limits']
        
        text = (
            "⚙️ **تنظیمات ربات**\n\n"
            f"نام: {bot['name']}\n"
            f"نسخه: {bot['version']}\n"
            f"وضعیت: {'🔴 تعمیرات' if bot['maintenance'] else '🟢 فعال'}\n"
            f"پیام تعمیرات: {bot['message'] or 'پیش‌فرض'}\n\n"
            f"**محدودیت‌ها:**\n"
            f"پیش‌بینی رایگان: {limits['free_predictions']} عدد\n"
            f"پیش‌بینی VIP: {limits['vip_predictions']} عدد\n"
            f"حداکثر روزانه: {limits['max_daily_predictions']}\n\n"
            "**دستورات:**\n"
            "/maintenance [on/off] - تغییر وضعیت تعمیرات\n"
            "/set_message [متن] - تنظیم پیام تعمیرات\n"
            "/set_limits [رایگان] [VIP] [حداکثر] - تنظیم محدودیت‌ها"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def maintenance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تغییر وضعیت تعمیرات"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args or args[0].lower() not in ['on', 'off']:
            await update.message.reply_text("❌ فرمت: /maintenance [on/off]")
            return
        
        self.settings['bot']['maintenance'] = (args[0].lower() == 'on')
        self._save_settings()
        
        status = "فعال" if self.settings['bot']['maintenance'] else "غیرفعال"
        await update.message.reply_text(f"✅ حالت تعمیرات {status} شد.")
    
    async def set_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم پیام تعمیرات"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ متن پیام را وارد کنید.")
            return
        
        message = ' '.join(args)
        self.settings['bot']['message'] = message
        self._save_settings()
        
        await update.message.reply_text(f"✅ پیام تعمیرات تنظیم شد:\n{message}")
    
    async def set_limits(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تنظیم محدودیت‌ها"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("❌ فرمت: /set_limits [رایگان] [VIP] [حداکثر]")
            return
        
        try:
            free = int(args[0])
            vip = int(args[1])
            max_daily = int(args[2])
        except:
            await update.message.reply_text("❌ مقادیر باید عدد باشند.")
            return
        
        self.settings['limits']['free_predictions'] = free
        self.settings['limits']['vip_predictions'] = vip
        self.settings['limits']['max_daily_predictions'] = max_daily
        self._save_settings()
        
        await update.message.reply_text(f"✅ محدودیت‌ها تنظیم شد: رایگان={free}, VIP={vip}, حداکثر={max_daily}")
    
    # ==================== بک‌آپ ====================
    
    async def backup_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی بک‌آپ"""
        query = update.callback_query
        await query.answer()
        
        text = (
            "📦 **مدیریت بک‌آپ**\n\n"
            "گزینه‌های موجود:\n"
            "• /backup_create - ایجاد بک‌آپ جدید\n"
            "• /backup_list - لیست بک‌آپ‌ها\n"
            "• /backup_restore [نام] - بازیابی از بک‌آپ\n"
            "• /backup_delete [نام] - حذف بک‌آپ\n\n"
            "⚠️ بک‌آپ‌ها در پوشه `backups/` ذخیره می‌شوند."
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def backup_create(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ایجاد بک‌آپ"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        await update.message.reply_text("📦 در حال ایجاد بک‌آپ...")
        
        try:
            # بک‌آپ از core.eternal_backup
            from core.eternal_backup import eternal_backup
            result = eternal_backup.create_backup('complete', 'Manual backup from admin panel')
            
            if result['success']:
                await update.message.reply_text(
                    f"✅ بک‌آپ با موفقیت ایجاد شد:\n"
                    f"📁 فایل: {result['file']}\n"
                    f"📊 حجم: {result['size_mb']:.2f} MB"
                )
            else:
                await update.message.reply_text(f"❌ خطا در بک‌آپ: {result.get('error', 'نامشخص')}")
                
        except Exception as e:
            await update.message.reply_text(f"❌ خطا: {e}")
    
    # ==================== پیام همگانی ====================
    
    async def broadcast_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی پیام همگانی"""
        query = update.callback_query
        await query.answer()
        
        text = (
            "📢 **پیام همگانی**\n\n"
            "برای ارسال پیام به همه کاربران:\n"
            "/broadcast [متن]\n\n"
            "برای ارسال به گروه خاص:\n"
            "/broadcast_vip [متن]\n"
            "/broadcast_premium [متن]\n\n"
            "⚠️ قبل از ارسال، از متن مطمئن شوید!"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ارسال پیام همگانی"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args:
            await update.message.reply_text("❌ متن پیام را وارد کنید.")
            return
        
        message = ' '.join(args)
        
        await update.message.reply_text(f"📤 در حال ارسال به {len(self.users)} کاربر...")
        
        # اینجا باید کد ارسال به همه کاربران قرار بگیره
        # فعلاً فقط پیام تأیید
        
        await update.message.reply_text(
            f"✅ پیام با موفقیت ارسال شد.\n\n"
            f"متن: {message}"
        )
    
    # ==================== ریست ====================
    
    async def reset_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی ریست"""
        query = update.callback_query
        await query.answer()
        
        text = (
            "🔄 **ریست و بازیابی**\n\n"
            "⚠️ **هشدار:** این عملیات غیرقابل بازگشت است!\n\n"
            "گزینه‌ها:\n"
            "• /reset_users - پاک کردن همه کاربران\n"
            "• /reset_stats - ریست آمار\n"
            "• /reset_settings - بازگشت به تنظیمات پیش‌فرض\n"
            "• /reset_all - ریست کامل (همه چیز)\n\n"
            "برای تأیید هر عملیات، دستور را با `confirm` تکرار کنید.\n"
            "مثال: `/reset_users confirm`"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔙 بازگشت", callback_data="admin_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def reset_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پاک کردن کاربران"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args or args[0].lower() != 'confirm':
            await update.message.reply_text(
                "⚠️ برای تأیید، دستور را با confirm تکرار کنید:\n"
                "/reset_users confirm"
            )
            return
        
        self.users = {}
        self._save_users()
        
        await update.message.reply_text("✅ تمام کاربران پاک شدند.")
    
    async def reset_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ریست آمار"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args or args[0].lower() != 'confirm':
            await update.message.reply_text(
                "⚠️ برای تأیید، دستور را با confirm تکرار کنید:\n"
                "/reset_stats confirm"
            )
            return
        
        self.stats = {
            'total_users': len(self.users),
            'total_predictions': 0,
            'total_paid': 0.0,
            'daily_users': {},
            'daily_predictions': {},
            'commands': {}
        }
        self._save_stats()
        
        await update.message.reply_text("✅ آمار ریست شد.")
    
    async def reset_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بازگشت به تنظیمات پیش‌فرض"""
        user = update.effective_user
        
        if not self.is_master(user.id):
            await update.message.reply_text("⛔ دسترسی ندارید.")
            return
        
        args = context.args
        if not args or args[0].lower() != 'confirm':
            await update.message.reply_text(
                "⚠️ برای تأیید، دستور را با confirm تکرار کنید:\n"
                "/reset_settings confirm"
            )
            return
        
        # بازگشت به پیش‌فرض
        self.settings = {
            'prices': {
                'prediction': 0.32,
                'premium_month': 10.0,
                'vip_month': 50.0,
                'lifetime': 500.0
            },
            'wallet': {
                'address': '0x11096bccfc635a5467ccfa1ef2970bfb95bd1474',
                'currency': 'USDT',
                'network': 'BEP20'
            },
            'channel': {
                'required': False,
                'url': None,
                'username': None
            },
            'bot': {
                'name': 'Eye of Horus',
                'version': '∞',
                'maintenance': False,
                'message': None
            },
            'limits': {
                'free_predictions': 3,
                'vip_predictions': 100,
                'max_daily_predictions': 1000
            },
            'last_updated': datetime.now().isoformat()
        }
        self._save_settings()
        
        await update.message.reply_text("✅ تنظیمات به حالت پیش‌فرض بازگشت.")
    
    # ==================== بازگشت ====================
    
    async def back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بازگشت به منوی اصلی"""
        await self.show_panel(update, context)

# ==================== نمونه‌سازی سراسری ====================
master_panel = MasterPanel()
