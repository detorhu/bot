from telegram import Update
from telegram.ext import ContextTypes
from services.town_logic import patrol

async def police_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    result = patrol(user.id)
    await update.message.reply_text(result)