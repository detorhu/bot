from telegram import Update
from telegram.ext import ContextTypes
from services.town_logic import add_ship

async def ship_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ship = add_ship(user.id)
    await update.message.reply_text(f"🚢 New ship built: {ship}")