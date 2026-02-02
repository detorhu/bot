from telegram import Update
from telegram.ext import ContextTypes
from database import get_city, get_buildings
from keyboards import back_menu

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id

    city, population, happiness = get_city(uid)
    houses, school, hospital, police = get_buildings(uid)

    text = (
        "📊 *City Stats*\n\n"
        f"🏙 Name: {city}\n"
        f"👥 Population: {population}\n"
        f"😊 Happiness: {happiness}%\n\n"
        f"🏠 Houses: Lv {houses}\n"
        f"🎓 School: Lv {school}\n"
        f"🏥 Hospital: Lv {hospital}\n"
        f"🚓 Police: Lv {police}"
    )

    await query.edit_message_text(
        text,
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )
