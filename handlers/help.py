from telegram import Update
from telegram.ext import ContextTypes
from keyboards import back_menu

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Shows help / how to play screen
    """
    q = update.callback_query
    await q.answer()

    text = (
        "ℹ️ *Idle City – Help*\n\n"
        "🏙 *Goal*\n"
        "Build and grow your city using idle income.\n\n"
        "💰 *Income*\n"
        "• Earn cash every hour automatically\n"
        "• Tap *Collect* to claim income\n\n"
        "🏗 *Buildings*\n"
        "• Houses → Increase population\n"
        "• School → Increase income\n"
        "• Hospital → Increase happiness\n"
        "• Police → Increase happiness\n\n"
        "📊 *Stats*\n"
        "View your city details anytime\n\n"
        "_More features coming soon_ 🚀"
    )

    await q.edit_message_text(
        text,
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )
