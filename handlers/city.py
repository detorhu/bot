from telegram import Update
from telegram.ext import ContextTypes
from database import create_user
from handlers.menu import show_main_menu

async def city_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_city"):
        return

    city_name = update.message.text.strip()[:20]
    uid = update.effective_user.id

    create_user(uid, city_name)
    context.user_data.clear()

    await update.message.reply_text(
        f"🏙 City *{city_name}* created successfully!",
        parse_mode="Markdown"
    )

    await show_main_menu(update, context)
