import os
from dotenv import load_dotenv
from telegram import Bot


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def main():
    if not TOKEN or not CHAT_ID:
        print("❌ Configurazione Telegram mancante")
        return

    bot = Bot(token=TOKEN)

    bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "🤘 Metal Radar avviato!\n\n"
            "Sistema di monitoraggio concerti operativo."
        )
    )

    print("✅ Messaggio Telegram inviato")


if __name__ == "__main__":
    main()
