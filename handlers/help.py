from telegram import Update
from telegram.ext import ContextTypes

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🏙️ **TOWN GAME BOT**

Commands:
/town – manage town
/ship – ships & yards
/police – cops & crime
/tax – tax system
/war – town wars
/help – help menu
""",
        parse_mode="Markdown"
    )