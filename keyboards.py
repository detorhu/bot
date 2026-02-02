from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏗 Build", callback_data="build"),
            InlineKeyboardButton("💰 Collect", callback_data="collect")
        ],
        [
            InlineKeyboardButton("⚔ Duel", callback_data="duel"),
            InlineKeyboardButton("🛒 Shop", callback_data="shop")
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats")
        ]
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅ Back", callback_data="back")]
    ])
