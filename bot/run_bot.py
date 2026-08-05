import os
from dotenv import load_dotenv

from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤘 Metal Radar online!\n\n"
        "Bot collegato correttamente.\n\n"
        "Comandi disponibili presto:\n"
        "/stato - stato del radar"
    )


async def stato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛰️ Metal Radar operativo!"
    )


def main():
    if not TOKEN:
        print("Token mancante")
        return

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("stato", stato)
    )

    print("🤘 Bot Telegram avviato")

    app.run_polling()


if __name__ == "__main__":
    main()
