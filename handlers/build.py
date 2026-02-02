from telegram import Update
from telegram.ext import ContextTypes
from database import get_user, update_cash
from services.buildings import apply_upgrade, upgrade_cost
from keyboards import build_menu, back_menu

async def build_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.edit_message_text(
        "🏗 *Upgrade Buildings*",
        reply_markup=build_menu(),
        parse_mode="Markdown"
    )

async def upgrade_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    building = q.data.replace("up_", "")

    cash, _ = get_user(uid)
    cost = upgrade_cost(0)  # calculated inside service based on level

    if cash < cost:
        return await q.answer("❌ Not enough cash", show_alert=True)

    ok, result = apply_upgrade(uid, building)
    if not ok:
        return await q.answer(result, show_alert=True)

    update_cash(uid, cash - cost)
    await q.answer(f"✅ {building.title()} upgraded!")
