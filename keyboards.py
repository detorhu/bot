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
def build_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Houses", callback_data="up_houses")],
        [InlineKeyboardButton("🎓 School", callback_data="up_school")],
        [InlineKeyboardButton("🏥 Hospital", callback_data="up_hospital")],
        [InlineKeyboardButton("🚓 Police", callback_data="up_police")],
        [InlineKeyboardButton("⬅ Back", callback_data="back")]
    ])

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
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
            InlineKeyboardButton("ℹ Help", callback_data="help")
        ]
    ])

def shop_menu():
    buttons = []
    for key, item in get_shop_items().items():
        buttons.append([
            InlineKeyboardButton(
                f"{item['label']} – {item['price']}",
                callback_data=f"buy_{key}"
            )
        ])
    buttons.append([InlineKeyboardButton("⬅ Back", callback_data="back")])
    return InlineKeyboardMarkup(buttons)
