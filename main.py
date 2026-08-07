import json
import os

import requests
from dotenv import load_dotenv

from scanner.rss_scanner import scan


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HISTORY_FILE = "storage/history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data.get("articles", []))

    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_history(history):
    data = {
        "articles": list(history)
    }

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )

    response.raise_for_status()


def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Configurazione Telegram mancante")
        return

    history = load_history()
    risultati = scan()

    nuovi = []

    for news in risultati:
        link = news["link"]

        if link in history:
            continue

        messaggio = (
            "🤘 Metal Radar\n\n"
            f"🎸 {news['band']}\n"
            f"📰 {news['title']}\n\n"
            f"{news['link']}"
        )

        try:
            send_message(messaggio)

            history.add(link)
            nuovi.append(news)

            print(f"✅ Notificato: {news['title']}")

        except requests.RequestException as error:
            print(f"❌ Errore Telegram: {error}")

    save_history(history)

    print(
        f"Scansione completata: "
        f"{len(risultati)} risultati rilevanti, "
        f"{len(nuovi)} nuovi."
    )


if __name__ == "__main__":
    main()
