import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

import os
TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# إعدادات اللوق
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# العملات
currencies = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USD"]
selected = {}

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cur, callback_data=cur)] for cur in currencies]
    keyboard.append([InlineKeyboardButton("🚀 إرسال الإشارة", callback_data="send_signal")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر عملة أو أرسل إشارة 🚀", reply_markup=reply_markup)

# دالة الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "send_signal":
        await query.edit_message_text("📡 تم إرسال الإشارة!")
    else:
        selected[query.from_user.id] = query.data
        await query.edit_message_text(f"✅ تم اختيار: {query.data}")

# تشغيل البوت
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

# تشغيل فلَسك للسيرفر
@app.route('/')
def home():
    return "Nasib Bot is running!"



    async def main():
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        app.run(host='0.0.0.0', port=10000)

    asyncio.run(main())