import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"  # استبدله بتوكن البوت

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

currencies = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USD"]
selected = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cur, callback_data=cur)] for cur in currencies]
    keyboard.append([InlineKeyboardButton("🚀 إرسال الإشارة", callback_data="send_signal")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر العملة أو اضغط 🚀 لإرسال الإشارة", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "send_signal":
        await query.edit_message_text(text="📡 تم إرسال الإشارة!")
    else:
        selected[query.from_user.id] = query.data
        await query.edit_message_text(text=f"✅ تم اختيار العملة: {query.data}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()