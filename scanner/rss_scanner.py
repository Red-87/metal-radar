import feedparser

RSS_FEEDS = [
    "https://blabbermouth.net/feed",
    "https://www.loudersound.com/feeds/all",
]

KEYWORDS = [
    "metallica",
    "megadeth",
    "iron maiden",
    "guns n' roses",
    "guns n roses",
    "slayer",
    "pantera",
    "ghost",
    "rammstein",
    "judas priest",
    "dream theater",
    "amon amarth",
    "sabaton",
    "nightwish",
    "slipknot",
]


def scan():
    risultati = []

    for feed in RSS_FEEDS:
        try:
            news = feedparser.parse(feed)

            for articolo in news.entries:
                titolo = articolo.title.lower()

                for band in KEYWORDS:
                    if band in titolo:
                        risultati.append({
                            "band": band.title(),
                            "title": articolo.title,
                            "link": articolo.link
                        })

        except Exception as e:
            print(e)

    return risultati
