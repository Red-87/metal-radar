import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_bands():
    path = os.path.join(BASE_DIR, "config", "bands.json")
    return load_json(path)


def load_settings():
    path = os.path.join(BASE_DIR, "config", "settings.json")
    return load_json(path)


if __name__ == "__main__":
    bands = load_bands()
    settings = load_settings()

    print("Metal Radar configurato!")
    print(f"Band monitorate: {len(bands['bands'])}")
    print(f"Lingua: {settings['language']}")
