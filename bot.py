from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN

from handlers.help import help_cmd
from handlers.admin import start_cmd
from handlers.town import town_cmd
from handlers.tax import tax_cmd
from handlers.ship import ship_cmd
from handlers.police import police_cmd
from handlers.war import war_cmd

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("town", town_cmd))
    app.add_handler(CommandHandler("tax", tax_cmd))
    app.add_handler(CommandHandler("ship", ship_cmd))
    app.add_handler(CommandHandler("police", police_cmd))
    app.add_handler(CommandHandler("war", war_cmd))

    print("🚀 Town Game Bot running")
    app.run_polling()

if __name__ == "__main__":
    main()
