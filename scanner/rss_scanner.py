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
    "ac/dc",
    "acdc",
    "judas priest",
    "pantera",
    "slayer",
    "anthrax",
    "testament",
    "exodus",
    "overkill",
    "kreator",
    "sodom",
    "destruction",
    "rammstein",
    "ghost",
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


# Indicatori di un evento futuro o di un nuovo annuncio.
POSITIVE_KEYWORDS = {
    "tour": 5,
    "tour dates": 7,
    "european tour": 8,
    "european dates": 8,
    "europe dates": 7,
    "world tour": 8,
    "north american tour": 6,
    "uk tour": 7,
    "uk dates": 7,
    "live dates": 7,
    "new dates": 7,
    "new shows": 6,
    "new show": 6,
    "concert": 5,
    "concerts": 5,
    "headline": 5,
    "headlining": 6,
    "festival": 4,
    "festival dates": 7,
    "festival appearance": 5,
    "tickets": 5,
    "ticket": 4,
    "presale": 7,
    "pre-sale": 7,
    "pre sale": 7,
    "on sale": 6,
    "general sale": 6,
    "dates announced": 9,
    "date announced": 8,
    "announce tour": 9,
    "announces tour": 9,
    "announced tour": 9,
    "announce dates": 9,
    "announces dates": 9,
    "announced dates": 9,
    "announce european": 9,
    "announces european": 9,
    "announced european": 9,
    "add dates": 8,
    "adds dates": 8,
    "added dates": 8,
    "additional dates": 7,
    "returns to": 4,
    "will play": 4,
    "will perform": 4,
    "set to perform": 5,
}


# Indicatori di contenuti che NON sono normalmente annunci di concerti.
NEGATIVE_KEYWORDS = {
    "album": -4,
    "albums": -4,
    "new album": -5,
    "studio album": -5,
    "single": -4,
    "new single": -5,
    "song": -3,
    "new song": -4,
    "music video": -6,
    "official video": -6,
    "video": -3,
    "interview": -5,
    "interviews": -5,
    "review": -5,
    "reviews": -5,
    "ranked": -6,
    "ranking": -6,
    "history": -4,
    "biography": -5,
    "lineup changes": -5,
    "line-up changes": -5,
    "reissue": -5,
    "reissue": -5,
    "anniversary": -3,
    "merch": -4,
    "merchandise": -4,
    "recording": -4,
    "recorded": -3,
    "streaming": -3,
    "podcast": -4,
}


# Indicatori tipici di un concerto già avvenuto,
# di un video o di un report.
PAST_EVENT_KEYWORDS = {
    "see ": -8,
    "watch ": -8,
    "entire concert": -12,
    "full concert": -12,
    "full show": -12,
    "concert video": -12,
    "live video": -10,
    "pro-shot": -10,
    "pro shot": -10,
    "footage": -9,
    "highlights": -7,
    "performance": -6,
    "performed": -7,
    "performing": -5,
    "played": -7,
    "playing": -5,
    "setlist": -8,
    "live at": -6,
    "from last night's": -10,
    "from last night's show": -12,
    "last night": -8,
    "yesterday": -7,
    "review of": -8,
    "concert review": -10,
}


def normalize(text):
    """Normalizza il testo per facilitare il confronto."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_band(title):
    """
    Cerca una band nel titolo.

    La ricerca viene effettuata sul titolo,
    non sull'intero articolo, per ridurre
    falsi positivi causati da nomi citati
    incidentalmente nel testo.
    """

    normalized_title = normalize(title)

    # Ordina le band dalla più lunga alla più corta.
    # Evita problemi con nomi che possono contenere
    # altre stringhe.
    for band in sorted(BANDS, key=len, reverse=True):
        if band in normalized_title:
            return band

    return None


def calculate_score(title):
    """Calcola il punteggio di rilevanza live."""

    text = normalize(title)
    score = 0

    for keyword, points in POSITIVE_KEYWORDS.items():
        if keyword in text:
            score += points

    for keyword, points in NEGATIVE_KEYWORDS.items():
        if keyword in text:
            score += points

    for keyword, points in PAST_EVENT_KEYWORDS.items():
        if keyword in text:
            score += points

    return score


def is_relevant(title):
    """
    Determina se il titolo sembra riferirsi
    a un annuncio/evento live futuro.

    Soglia relativamente alta per privilegiare
    la precisione rispetto alla quantità.
    """

    score = calculate_score(title)

    return score >= 6


def scan():
    risultati = []

    for feed_url in RSS_FEEDS:

        try:
            feed = feedparser.parse(feed_url)

            for article in feed.entries:

                title = article.get("title", "")
                link = article.get("link", "")

                if not title or not link:
                    continue

                band = find_band(title)

                if not band:
                    continue

                score = calculate_score(title)

                if score < 6:
                    continue

                risultati.append(
                    {
                        "band": band.title(),
                        "title": title,
                        "link": link,
                        "score": score,
                    }
                )

        except Exception as error:
            print(f"Errore RSS {feed_url}: {error}")

    return risultati
