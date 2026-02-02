from telegram import Update
from telegram.ext import ContextTypes
from services.battle import start_war

async def war_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    result = start_war(user.id)
    await update.message.reply_text(result)