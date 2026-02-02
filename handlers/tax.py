from telegram import Update
from telegram.ext import ContextTypes
from services.economy import collect_tax

async def tax_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tax = collect_tax(user.id)
    await update.message.reply_text(f"💰 Collected tax: {tax} coins")