import os
import requests
from dotenv import load_dotenv

from scanner.rss_scanner import scan

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False
        },
        timeout=20
    )


def main():

    risultati = scan()

    if not risultati:
        send_message("🤘 Metal Radar\n\nNessuna nuova notizia trovata.")
        return

    for news in risultati:

        messaggio = (
            f"🤘 Metal Radar\n\n"
            f"🎸 {news['band']}\n\n"
            f"📰 {news['title']}\n\n"
            f"{news['link']}"
        )

        send_message(messaggio)


if __name__ == "__main__":
    main()
