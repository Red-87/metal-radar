import re
import feedparser


RSS_FEEDS = [
    "https://blabbermouth.net/feed",
    "https://www.loudersound.com/feeds/all",
]


BANDS = [
    "metallica",
    "iron maiden",
    "megadeth",
    "guns n' roses",
    "guns n roses",
    "judas priest",
    "pantera",
    "slayer",
    "ghost",
    "rammstein",
    "sabaton",
    "nightwish",
    "amon amarth",
    "slipknot",
    "korn",
    "disturbed",
    "avenged sevenfold",
    "dream theater",
    "opeth",
    "behemoth",
    "arch enemy",
]


# Parole/frasi che indicano un possibile evento live
LIVE_KEYWORDS = {
    "tour": 5,
    "tour dates": 6,
    "european tour": 7,
    "european dates": 6,
    "world tour": 7,
    "live dates": 6,
    "concert": 5,
    "concerts": 5,
    "live show": 5,
    "live shows": 5,
    "headline": 4,
    "headlining": 5,
    "festival": 4,
    "festival dates": 6,
    "tickets": 5,
    "ticket": 4,
    "presale": 6,
    "pre-sale": 6,
    "on sale": 5,
    "dates announced": 7,
    "announce": 2,
    "announces": 2,
    "announced": 2,
    "new dates": 6,
    "live dates": 6,
    "perform": 2,
}


# Contenuti che normalmente NON ci interessano
NEGATIVE_KEYWORDS = {
    "album": -4,
    "albums": -4,
    "new album": -5,
    "new single": -5,
    "single": -3,
    "song": -2,
    "video": -3,
    "music video": -4,
    "interview": -5,
    "interviews": -5,
    "review": -5,
    "ranked": -5,
    "ranking": -5,
    "history": -3,
    "biography": -4,
    "lineup changes": -4,
    "line-up changes": -4,
    "reissue": -4,
    "anniversary": -3,
    "merch": -3,
    "merchandise": -3,
}


def normalize(text):
    """Converte il testo in una forma più facile da analizzare."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_band(title):
    """Restituisce la band trovata nel titolo."""
    normalized_title = normalize(title)

    for band in BANDS:
        if band in normalized_title:
            return band.title()

    return None


def calculate_score(title):
    """Calcola quanto una notizia sembra riguardare un evento live."""

    text = normalize(title)
    score = 0

    for keyword, points in LIVE_KEYWORDS.items():
        if keyword in text:
            score += points

    for keyword, points in NEGATIVE_KEYWORDS.items():
        if keyword in text:
            score += points

    return score


def is_relevant(title):
    """
    Una notizia viene considerata interessante
    se raggiunge almeno 5 punti.
    """

    return calculate_score(title) >= 5


def scan():
    risultati = []

    for feed_url in RSS_FEEDS:

        try:
            feed = feedparser.parse(feed_url)

            for article in feed.entries:

                title = article.get("title", "")
                link = article.get("link", "")

                band = find_band(title)

                if not band:
                    continue

                score = calculate_score(title)

                if score < 5:
                    continue

                risultati.append(
                    {
                        "band": band,
                        "title": title,
                        "link": link,
                        "score": score,
                    }
                )

        except Exception as error:
            print(f"Errore RSS {feed_url}: {error}")

    return risultati
