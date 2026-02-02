from telegram import Update
from telegram.ext import ContextTypes
import time

from database import get_user, get_city, get_buildings, update_cash, update_last_collect
from services.economy import calculate_income

async def collect_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id

    cash, last_collect = get_user(uid)
    now = int(time.time())

    hours = (now - last_collect) // 3600
    if hours <= 0:
        await query.answer("⏳ No income yet", show_alert=True)
        return

    _, population, _ = get_city(uid)
    _, school, _, _ = get_buildings(uid)

    income = calculate_income(population, school) * hours
    update_cash(uid, cash + income)
    update_last_collect(uid, now)

    await query.answer(f"+${income} collected!")
