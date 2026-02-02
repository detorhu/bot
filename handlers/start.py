from telegram import Update
from telegram.ext import ContextTypes
from database import user_exists, create_user
from handlers.menu import show_main_menu

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not user_exists(uid):
        context.user_data["awaiting_city"] = True
        await update.message.reply_text(
            "🏙 Welcome!\n\nPlease send your *city name*:",
            parse_mode="Markdown"
        )
    else:
        await show_main_menu(update, context)
