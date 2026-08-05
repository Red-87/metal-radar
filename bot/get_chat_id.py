import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def get_updates():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    response = requests.get(url)

    data = response.json()

    print(data)


if __name__ == "__main__":
    get_updates()
