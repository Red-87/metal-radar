import os
from dotenv import load_dotenv
from telegram.ext import Application

from bot.commands import setup_commands


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    if not TOKEN:
        print("❌ Token Telegram mancante")
        return

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    setup_commands(application)

    print("🤘 Metal Radar avviato!")

    application.run_polling()


if __name__ == "__main__":
    main()
