from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# إعدادات Flask
app = Flask(__name__)

# جلب التوكن من المتغيرات البيئية
BOT_TOKEN = os.environ.get("BOT_TOKEN")
application = Application.builder().token(BOT_TOKEN).build()

# دالة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم تفعيل البوت ✅")

# دالة الأمر /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب /signal لطلب إشارة 🔔")

# دالة الأمر /signal
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 تم تسجيل طلبك لإشارة")

# إضافة الأوامر
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("signal", signal))

# ربط Webhook مع Flask
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# صفحة اختبار
@app.route("/")
def index():
    return "بوت النسيب شغال 🔥"

# تشغيل التطبيق
if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=f"https://nasib-bot.onrender.com/{BOT_TOKEN}"
    )