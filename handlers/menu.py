from telegram import Update
from telegram.ext import ContextTypes
from database import get_user, get_city, get_buildings
from services.economy import calculate_income
from keyboards import main_menu

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    cash, _ = get_user(uid)
    city, population, happiness = get_city(uid)
    houses, school, hospital, police = get_buildings(uid)

    income = calculate_income(population, school)

    text = (
        f"🏙 *{city}*\n"
        f"👥 Population: {population}\n"
        f"😊 Happiness: {happiness}%\n\n"
        f"💰 Cash: ${cash}\n"
        f"⏳ Income / hr: ${income}"
    )

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
