from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"👋 Welcome {user.first_name}\n🏙️ Town Game Bot Online"

    if user.id in ADMIN_IDS:
        text += "\n👑 Admin Access"

    await update.message.reply_text(text)