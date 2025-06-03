import logging
import os
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد التوكن
TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

# إعداد اللوق
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# العملات
currencies = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USDT"]
selected = {}

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cur, callback_data=cur)] for cur in currencies]
    keyboard.append([InlineKeyboardButton("🚀 إرسال الإشارة", callback_data="send_signal")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر عملة ثم اضغط إرسال الإشارة:", reply_markup=reply_markup)

# دالة الضغط على الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "send_signal":
        await query.edit_message_text("📡 تم إرسال الإشارة!")
    else:
        selected[query.from_user.id] = query.data
        await query.edit_message_text(f"✅ تم اختيار: {query.data}")

# البوت ككائن
bot_app = Application.builder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button))

# Flask route فقط للفحص
@app.route('/')
def home():
    return "Nasib Bot is running!"

# تشغيل البوت داخل Render (بدون /start-bot)
@app.before_first_request
def start_bot():
    import asyncio
    asyncio.create_task(bot_app.initialize())
    asyncio.create_task(bot_app.start())
    asyncio.create_task(bot_app.updater.start_polling())