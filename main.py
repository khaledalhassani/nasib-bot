import logging
import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات التوكن
TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

# إعدادات اللوق
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# العملات
currencies = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USDT", "ETH/USDT"]
selected = {}

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cur, callback_data=cur)] for cur in currencies]
    keyboard.append([InlineKeyboardButton("🚀 إرسال الإشارة", callback_data="send_signal")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر العملة ثم أرسل الإشارة 🚀", reply_markup=reply_markup)

# دالة الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "send_signal":
        await query.edit_message_text("🚀 تم إرسال الإشارة")
    else:
        selected[query.from_user.id] = query.data
        await query.edit_message_text(f"✅ تم اختيار {query.data}")

# تشغيل البوت
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

# تشغيل السيرفر لفحص الرابط الأساسي
@app.route('/')
def home():
    return "Nasib Bot is running!"

# تشغيل البوت من رابط خاص
@app.route('/start-bot')
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.start())
    loop.run_until_complete(application.updater.start_polling())
    return "Bot started!"

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)