import logging
import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://nasib-bot.onrender.com/webhook"

app = Flask(__name__)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

currencies = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USD"]
selected = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cur, callback_data=cur)] for cur in currencies]
    keyboard.append([InlineKeyboardButton("🚀 إرسال الإشارة", callback_data="send_signal")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر العملة ثم أرسل الإشارة:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "send_signal":
        await query.edit_message_text("📡 تم إرسال الإشارة!")
    else:
        selected[query.from_user.id] = query.data
        await query.edit_message_text(f"✅ تم اختيار: {query.data}")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

@app.route('/')
def index():
    return "Nasib Bot is running!"

@app.route('/webhook', methods=['POST'])
async def webhook():
    await application.initialize()
    await application.process_update(Update.de_json(request.get_json(force=True), application.bot))
    return 'ok'

if __name__ == '__main__':
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )