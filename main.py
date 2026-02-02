from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import time

from config import BOT_TOKEN, CURRENCY, BASE_INCOME_PER_POP
from database import *
from keyboards import *

# V2 services
from services.buildings import upgrade_building, upgrade_cost

# ---------------- INIT ----------------
init_db()

# ---------------- HELPERS ----------------
def calc_income(population: int, school_lvl: int) -> int:
    bonus = 1 + (school_lvl * 0.05)
    return int(population * BASE_INCOME_PER_POP * bonus)

# ---------------- COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not user_exists(uid):
        context.user_data["awaiting_city"] = True
        await update.message.reply_text(
            "🏙 Welcome to *Idle City*\n\nSend your *city name*:",
            parse_mode="Markdown",
        )
    else:
        await show_main(update, context)

# ---------------- TEXT (CITY NAME) ----------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_city"):
        return

    name = update.message.text.strip()[:20]
    uid = update.effective_user.id

    create_user(uid, name)
    context.user_data.clear()

    await update.message.reply_text(
        f"🏙 City *{name}* created successfully!",
        parse_mode="Markdown",
    )
    await show_main(update, context)

# ---------------- MAIN MENU ----------------
async def show_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    cash, _ = get_user(uid)
    cname, pop, happy = get_city(uid)
    houses, school, _, _ = get_buildings(uid)

    income = calc_income(pop, school)

    text = (
        f"🏙 *{cname}*\n"
        f"👥 Population: {pop}\n"
        f"😊 Happiness: {happy}%\n\n"
        f"💰 Cash: {CURRENCY}{cash}\n"
        f"⏳ Income / hr: {CURRENCY}{income}"
    )

    if update.message:
        await update.message.reply_text(
            text, reply_markup=main_menu(), parse_mode="Markdown"
        )
    else:
        await update.callback_query.edit_message_text(
            text, reply_markup=main_menu(), parse_mode="Markdown"
        )

# ---------------- CALLBACKS ----------------
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    # ---- COLLECT ----
    if q.data == "collect":
        cash, last = get_user(uid)
        now = int(time.time())
        hours = (now - last) // 3600

        if hours <= 0:
            await q.answer("⏳ Nothing to collect yet", show_alert=True)
            return

        _, pop, _ = get_city(uid)
        _, school, _, _ = get_buildings(uid)

        income = calc_income(pop, school) * hours

        update_cash(uid, cash + income)
        update_last_collect(uid, now)

        await q.answer(f"+{CURRENCY}{income} collected!")
        await show_main(update, context)

    # ---- BUILD MENU ----
    elif q.data == "build":
        await q.edit_message_text(
            "🏗 *Upgrade Buildings*",
            reply_markup=build_menu(),
            parse_mode="Markdown"
        )

    # ---- BUILD UPGRADE ----
    elif q.data.startswith("up_"):
        building = q.data.replace("up_", "")
        cash, _ = get_user(uid)

        h, s, ho, p = get_buildings(uid)
        levels = {
            "houses": h,
            "school": s,
            "hospital": ho,
            "police": p,
        }

        lvl = levels[building]
        cost = upgrade_cost(lvl)

        if cash < cost:
            return await q.answer("❌ Not enough cash", show_alert=True)

        ok, msg = upgrade_building(uid, building)
        if not ok:
            return await q.answer(msg, show_alert=True)

        update_cash(uid, cash - cost)
        await q.answer(f"✅ {building.title()} upgraded!")
        await show_main(update, context)

    # ---- STATS ----
    elif q.data == "stats":
        cname, pop, happy = get_city(uid)
        h, s, ho, p = get_buildings(uid)

        text = (
            "📊 *City Stats*\n\n"
            f"🏙 Name: {cname}\n"
            f"👥 Population: {pop}\n"
            f"😊 Happiness: {happy}%\n\n"
            f"🏠 Houses: Lv {h}\n"
            f"🎓 School: Lv {s}\n"
            f"🏥 Hospital: Lv {ho}\n"
            f"🚓 Police: Lv {p}"
        )

        await q.edit_message_text(
            text, reply_markup=back_menu(), parse_mode="Markdown"
        )

    # ---- BACK ----
    elif q.data == "back":
        await show_main(update, context)

    # ---- PLACEHOLDER ----
    else:
        await q.answer("🚧 Coming soon", show_alert=True)

# ---------------- RUN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )

    print("✅ Idle City Bot started (V2 Build Enabled)")
    app.run_polling()

if __name__ == "__main__":
    main()
