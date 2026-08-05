import os
from dotenv import load_dotenv
from telegram import Bot


load_dotenv()


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_message(message):
    if not TOKEN:
        print("Token Telegram non configurato")
        return

    bot = Bot(token=TOKEN)

    bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=message
    )


if __name__ == "__main__":
    send_message(
        "🤘 Metal Radar avviato!\n"
        "Sistema di monitoraggio concerti operativo."
    )
