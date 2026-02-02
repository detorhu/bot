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

from services.buildings import upgrade_building, upgrade_cost
from services.shop import get_shop_items
from database import has_item, add_item, init_inventory

# ---------------- INIT ----------------
init_db()
init_inventory()

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

# ---------------- TEXT HANDLER ----------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_city"):
        return

    uid = update.effective_user.id
    name = update.message.text.strip()[:20]

    create_user(uid, name)
    context.user_data.clear()

    await update.message.reply_text(
        f"🏙 City *{name}* created!",
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
            return await q.answer("⏳ Nothing to collect yet", show_alert=True)

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
            parse_mode="Markdown",
        )

    # ---- BUILD UPGRADE ----
    elif q.data.startswith("up_"):
        building = q.data.replace("up_", "")
        cash, _ = get_user(uid)

        h, s, ho, p = get_buildings(uid)
        levels = {"houses": h, "school": s, "hospital": ho, "police": p}
        level = levels.get(building, 0)
        cost = upgrade_cost(level)

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

    # ---- SHOP MENU ----
    elif q.data == "shop":
        await q.edit_message_text(
            "🛒 *Shop*\n\nBuy items using cash:",
            reply_markup=shop_menu(),
            parse_mode="Markdown",
        )

    # ---- BUY ITEM ----
    elif q.data.startswith("buy_"):
        item_key = q.data.replace("buy_", "")
        shop = get_shop_items()

        if item_key not in shop:
            return await q.answer("Invalid item", show_alert=True)

        if has_item(uid, item_key):
            return await q.answer("❌ You already own this item", show_alert=True)

        price = shop[item_key]["price"]
        cash, _ = get_user(uid)

        if cash < price:
            return await q.answer("❌ Not enough cash", show_alert=True)

        update_cash(uid, cash - price)
        add_item(uid, item_key)

        await q.answer("✅ Item purchased!")
        await show_main(update, context)

    # ---- BACK ----
    elif q.data == "back":
        await show_main(update, context)

    else:
        await q.answer("🚧 Coming soon", show_alert=True)

# ---------------- RUN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 🔥 CALLBACK HANDLERS (CORRECT ORDER)
    app.add_handler(CallbackQueryHandler(callbacks, pattern="^(collect|stats|back)$"))
    app.add_handler(CallbackQueryHandler(callbacks, pattern="^build$"))
    app.add_handler(CallbackQueryHandler(callbacks, pattern="^up_"))
    app.add_handler(CallbackQueryHandler(callbacks, pattern="^shop$"))
    app.add_handler(CallbackQueryHandler(callbacks, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(callbacks))  # fallback LAST

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )

    print("✅ Idle City Bot started (BUILD + SHOP WORKING)")
    app.run_polling()

if __name__ == "__main__":
    main()
