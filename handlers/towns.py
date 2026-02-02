from telegram import Update
from telegram.ext import ContextTypes
from services.town_logic import get_or_create_town

async def town_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    town = get_or_create_town(user.id, user.first_name)

    await update.message.reply_text(
        f"🏙️ **Your Town**\n"
        f"Name: {town['name']}\n"
        f"Level: {town['level']}\n"
        f"Citizens: {town['citizens']}\n"
        f"Coins: {town['coins']}",
        parse_mode="Markdown"
    )