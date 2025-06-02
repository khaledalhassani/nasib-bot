
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace this with your actual token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the currencies you want to show as buttons
currencies = ["EUR/USD", "USD/JPY", "GBP/USD", "BTC/USDT", "ETH/USDT", "XAU/USD"]
selected = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cur, callback_data=cur)] for cur in currencies]
    keyboard.append([InlineKeyboardButton("🚀 إرسال الإشارة", callback_data="SEND_SIGNAL")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر العملة ثم اضغط إرسال الإشارة", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "SEND_SIGNAL":
        if user_id in selected:
            await context.bot.send_message(chat_id=user_id, text=f"🔔 الإشارة: {selected[user_id]}")
        else:
            await context.bot.send_message(chat_id=user_id, text="⚠️ لم تقم باختيار عملة")
    else:
        selected[user_id] = query.data
        await query.edit_message_text(text=f"✅ تم اختيار: {query.data}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
