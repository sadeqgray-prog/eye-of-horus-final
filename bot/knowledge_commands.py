#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📚 KNOWLEDGE COMMANDS - دستورات مدیریت کتاب برای تلگرام
"""

import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from knowledge.api import knowledge_api
from knowledge.downloader import downloader
from brain.master_mind import master_mind

# وضعیت‌های مکالمه
(ADD_BOOK_URL, ADD_BOOK_MANUAL, SELECT_BOOK, 
 CONFIRM_DELETE, SHOW_KNOWLEDGE) = range(5)

class KnowledgeCommands:
    """
    دستورات مدیریت کتاب در تلگرام
    """
    
    async def knowledge_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی اصلی دانش"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("📖 لیست کتاب‌ها", callback_data="know_list")],
            [InlineKeyboardButton("➕ افزودن کتاب با URL", callback_data="know_add_url")],
            [InlineKeyboardButton("📝 افزودن دستی", callback_data="know_add_manual")],
            [InlineKeyboardButton("🔍 جستجو", callback_data="know_search")],
            [InlineKeyboardButton("📊 آمار", callback_data="know_stats")],
            [InlineKeyboardButton("🧠 یادگیری خودکار", callback_data="know_auto")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")]
        ]
        
        stats = knowledge_api.get_stats()
        
        text = f"""
📚 **مدیریت دانش**

━━━━━━━━━━━━━━━━━━━━━━
**آمار:**
📚 کل کتاب‌ها: {stats['total_books']}
📥 در انتظار دانلود: {stats['by_status']['pending']}
📊 پردازش شده: {stats['by_status']['processed']}
🧠 یاد گرفته شده: {stats['by_status']['learned']}

**دسته‌بندی‌ها:**
"""
        
        for cat, count in stats['by_category'].items():
            text += f"• {cat}: {count} کتاب\n"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return ConversationHandler.END
    
    async def list_books(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """لیست کتاب‌ها"""
        query = update.callback_query
        await query.answer()
        
        books = knowledge_api.list_books()
        
        if not books:
            await query.edit_message_text("📭 هیچ کتابی یافت نشد")
            return ConversationHandler.END
        
        keyboard = []
        for book in books[:10]:  # ۱۰ کتاب اول
            status_emoji = {
                'pending': '⏳',
                'downloaded': '📥',
                'processed': '📊',
                'processing_failed': '❌'
            }.get(book.get('status'), '📄')
            
            learned = '🧠' if book.get('learned') else ''
            
            keyboard.append([
                InlineKeyboardButton(
                    f"{status_emoji} {book['title'][:30]} {learned}",
                    callback_data=f"know_view_{book['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="know_menu")])
        
        await query.edit_message_text(
            "📚 **لیست کتاب‌ها:**\n\nبرای مشاهده جزئیات روی هر کتاب کلیک کنید.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return SELECT_BOOK
    
    async def view_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مشاهده جزئیات کتاب"""
        query = update.callback_query
        await query.answer()
        
        book_id = query.data.replace('know_view_', '')
        book = knowledge_api.get_book_status(book_id)
        
        if 'error' in book:
            await query.edit_message_text("❌ کتاب یافت نشد")
            return ConversationHandler.END
        
        status_text = {
            'pending': '⏳ در انتظار دانلود',
            'downloading': '📥 در حال دانلود',
            'downloaded': '📥 دانلود شده',
            'processed': '📊 پردازش شده',
            'processing_failed': '❌ خطا در پردازش',
            'failed': '❌ خطا'
        }.get(book.get('status'), 'نامشخص')
        
        learned_text = "✅ بله" if book.get('learned') else "❌ خیر"
        
        text = f"""
📖 **{book['title']}**

━━━━━━━━━━━━━━━━━━━━━━
✍️ نویسنده: {book.get('author', 'نامشخص')}
📂 دسته: {book.get('category', 'نامشخص')}
📊 وضعیت: {status_text}
🧠 یادگیری: {learned_text}
📅 افزوده شده: {book.get('added_at', 'نامشخص')[:10]}

"""
        
        if book.get('stats'):
            text += f"📄 صفحات: {book['stats'].get('total_pages', 0)}\n"
            text += f"📝 کلمات: {book['stats'].get('total_words', 0)}\n"
        
        keyboard = []
        
        if book.get('status') == 'pending' and book.get('url'):
            keyboard.append([InlineKeyboardButton("📥 دانلود", callback_data=f"know_download_{book_id}")])
        
        if book.get('status') == 'downloaded' and not book.get('processed'):
            keyboard.append([InlineKeyboardButton("📊 پردازش", callback_data=f"know_process_{book_id}")])
        
        if book.get('processed') and not book.get('learned'):
            keyboard.append([InlineKeyboardButton("🧠 یادگیری", callback_data=f"know_learn_{book_id}")])
        
        if book.get('learned'):
            keyboard.append([InlineKeyboardButton("🔍 مشاهده دانش", callback_data=f"know_show_{book_id}")])
        
        keyboard.append([InlineKeyboardButton("❌ حذف", callback_data=f"know_delete_{book_id}")])
        keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="know_list")])
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return SELECT_BOOK
    
    async def add_book_url_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """شروع افزودن کتاب با URL"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "🔗 **لینک کتاب PDF را ارسال کنید:**\n\n"
            "مثال: `https://example.com/book.pdf`\n\n"
            "یا برای انصراف /cancel را بزنید.",
            parse_mode='Markdown'
        )
        
        return ADD_BOOK_URL
    
    async def add_book_url_receive(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دریافت URL و افزودن کتاب"""
        url = update.message.text.strip()
        
        await update.message.reply_text(f"📥 در حال افزودن کتاب از {url}...")
        
        result = knowledge_api.add_book_by_url(url)
        
        if result['success']:
            await update.message.reply_text(
                f"✅ کتاب با موفقیت اضافه شد!\n"
                f"🆔 آیدی کتاب: `{result['book_id']}`\n\n"
                f"دانلود به زودی شروع می‌شود."
            )
        else:
            await update.message.reply_text(f"❌ خطا: {result['message']}")
        
        return ConversationHandler.END
    
    async def download_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دانلود کتاب"""
        query = update.callback_query
        await query.answer()
        
        book_id = query.data.replace('know_download_', '')
        
        await query.edit_message_text("📥 در حال دانلود...")
        
        success = downloader.download_book(book_id)
        
        if success:
            await query.edit_message_text("✅ دانلود با موفقیت انجام شد.")
        else:
            await query.edit_message_text("❌ خطا در دانلود.")
        
        # بازگشت به جزئیات کتاب
        return await self.view_book(update, context)
    
    async def process_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش کتاب"""
        query = update.callback_query
        await query.answer()
        
        book_id = query.data.replace('know_process_', '')
        
        await query.edit_message_text("📊 در حال پردازش کتاب...")
        
        result = knowledge_api.process_book(book_id)
        
        await query.edit_message_text(
            "✅ پردازش با موفقیت انجام شد." if result['success'] else f"❌ خطا: {result['message']}"
        )
        
        return await self.view_book(update, context)
    
    async def learn_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """یادگیری کتاب توسط مغز"""
        query = update.callback_query
        await query.answer()
        
        book_id = query.data.replace('know_learn_', '')
        
        await query.edit_message_text("🧠 در حال یادگیری...")
        
        result = await knowledge_api.learn_book(book_id)
        
        if result['success']:
            await query.edit_message_text("✅ کتاب با موفقیت یاد گرفته شد!")
        else:
            await query.edit_message_text(f"❌ خطا: {result['message']}")
        
        return await self.view_book(update, context)
    
    async def delete_book_confirm(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تأیید حذف کتاب"""
        query = update.callback_query
        await query.answer()
        
        book_id = query.data.replace('know_delete_', '')
        context.user_data['delete_book_id'] = book_id
        
        keyboard = [
            [
                InlineKeyboardButton("✅ بله، حذف شود", callback_data="know_delete_yes"),
                InlineKeyboardButton("❌ خیر", callback_data="know_delete_no")
            ]
        ]
        
        await query.edit_message_text(
            "⚠️ **آیا از حذف این کتاب اطمینان دارید؟**\nاین عمل غیرقابل بازگشت است.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return CONFIRM_DELETE
    
    async def delete_book_execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """اجرای حذف کتاب"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "know_delete_yes":
            book_id = context.user_data.get('delete_book_id')
            result = knowledge_api.delete_book(book_id)
            
            await query.edit_message_text(
                f"✅ {result['message']}"
            )
        else:
            await query.edit_message_text("❌ عملیات لغو شد.")
        
        return await self.list_books(update, context)
    
    async def show_knowledge(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش دانش کتاب"""
        query = update.callback_query
        await query.answer()
        
        book_id = query.data.replace('know_show_', '')
        knowledge = downloader.get_book_knowledge(book_id)
        
        if not knowledge:
            await query.edit_message_text("❌ دانشی یافت نشد")
            return ConversationHandler.END
        
        book = knowledge['metadata']
        know = knowledge['knowledge']
        
        text = f"""
📖 **دانش کتاب: {book['title']}**

━━━━━━━━━━━━━━━━━━━━━━
📝 **خلاصه:**
{know.get('summary', 'ندارد')}

📚 **فصل‌ها:**
"""
        
        for chapter in know.get('chapters', [])[:5]:
            text += f"• {chapter}\n"
        
        if know.get('quotes'):
            text += f"\n💬 **نقل قول نمونه:**\n{know['quotes'][0][:200]}...\n"
        
        text += f"\n🔑 **کلمات کلیدی:**\n"
        text += ', '.join(know.get('keywords', [])[:10])
        
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data=f"know_view_{book_id}")]]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return SELECT_BOOK
    
    async def search_books(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """جستجوی کتاب"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "🔍 **عبارت جستجو را ارسال کنید:**\n\n"
            "می‌توانید در عنوان کتاب یا نویسنده جستجو کنید.",
            parse_mode='Markdown'
        )
        
        return SHOW_KNOWLEDGE
    
    async def search_receive(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دریافت و نمایش نتایج جستجو"""
        query_text = update.message.text
        
        results = knowledge_api.search_books(query_text)
        
        if not results:
            await update.message.reply_text("❌ هیچ کتابی با این عبارت یافت نشد.")
            return ConversationHandler.END
        
        text = f"🔍 **نتایج جستجو برای «{query_text}»:**\n\n"
        
        for book in results[:10]:
            text += f"• {book['title']} - {book.get('author', 'نامشخص')}\n"
        
        await update.message.reply_text(text, parse_mode='Markdown')
        
        return ConversationHandler.END
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """نمایش آمار"""
        query = update.callback_query
        await query.answer()
        
        stats = knowledge_api.get_stats()
        
        text = f"""
📊 **آمار دانش**

━━━━━━━━━━━━━━━━━━━━━━
📚 **کتاب‌ها:**
• کل: {stats['total_books']}
• در انتظار: {stats['by_status']['pending']}
• دانلود شده: {stats['by_status']['downloaded']}
• پردازش شده: {stats['by_status']['processed']}
• یاد گرفته شده: {stats['by_status']['learned']}

📂 **دسته‌بندی:**
"""
        
        for cat, count in stats['by_category'].items():
            text += f"• {cat}: {count}\n"
        
        text += f"""
🧠 **یادگیری:**
• کتاب‌های یاد گرفته شده: {stats['learning_stats']['learned_books']}
• نرخ یادگیری: {stats['learning_stats']['learning_rate']}
• آخرین یادگیری: {stats['learning_stats']['last_learning_session'] or 'هنوز'}
        """
        
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="know_menu")]]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return ConversationHandler.END
    
    async def auto_learn_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """منوی یادگیری خودکار"""
        query = update.callback_query
        await query.answer()
        
        from knowledge.auto_learner import auto_learner
        
        keyboard = [
            [InlineKeyboardButton("▶️ شروع یادگیری خودکار", callback_data="know_auto_start")],
            [InlineKeyboardButton("⏸️ توقف", callback_data="know_auto_stop")],
            [InlineKeyboardButton("⚡ یادگیری همه", callback_data="know_learn_all")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="know_menu")]
        ]
        
        status = "✅ فعال" if auto_learner.is_learning else "❌ غیرفعال"
        
        text = f"""
🧠 **یادگیری خودکار**

وضعیت: {status}

ربات هر ساعت یک کتاب جدید را می‌خواند و از آن یاد می‌گیرد.
        """
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return ConversationHandler.END
    
    async def auto_learn_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """شروع یادگیری خودکار"""
        query = update.callback_query
        await query.answer()
        
        from knowledge.auto_learner import auto_learner
        auto_learner.start_auto_learning()
        
        await query.edit_message_text("✅ یادگیری خودکار فعال شد.")
        
        return await self.auto_learn_menu(update, context)
    
    async def auto_learn_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """توقف یادگیری خودکار"""
        query = update.callback_query
        await query.answer()
        
        from knowledge.auto_learner import auto_learner
        auto_learner.stop_auto_learning()
        
        await query.edit_message_text("⏸️ یادگیری خودکار متوقف شد.")
        
        return await self.auto_learn_menu(update, context)
    
    async def learn_all_books(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """یادگیری همه کتاب‌ها"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text("🧠 در حال یادگیری همه کتاب‌ها...")
        
        from knowledge.auto_learner import auto_learner
        await auto_learner.learn_all_books()
        
        await query.edit_message_text("✅ همه کتاب‌ها یاد گرفته شدند!")
        
        return await self.auto_learn_menu(update, context)

# نمونه‌سازی
knowledge_commands = KnowledgeCommands()
