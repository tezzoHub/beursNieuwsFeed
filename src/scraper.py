import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import hashlib
import logging
from urllib.parse import urljoin

URL = "https://www.beurs.nl/nieuws"

# Logging instellen voor GitHub Actions
logging.basicConfig(level=logging.INFO, format="%(message)s")

def make_id(title, link):
    raw = (title + link).encode("utf-8")
    return hashlib.md5(raw).hexdigest()

def scrape_beursnieuws():
    logging.info("Scraper gestart...")

    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    except Exception as e:
        logging.error(f"FOUT: Kon de pagina niet ophalen: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    seen_ids = set()

    # Elk nieuwsitem staat in een <li class="timelist__item">
    for li in soup.select("li.timelist__item"):
        
        # Categorie
        cat_el = li.select_one(".tag")
        categorie = cat_el.get_text(strip=True) if cat_el else None

        # Tijd
        time_el = li.select_one("time")
        published_at = time_el["datetime"] if time_el and time_el.has_attr("datetime") else None

        # Titel
        title_el = li.select_one("h3.timelist__title a")
        if not title_el:
            continue
        titel = title_el.get_text(strip=True)
        link = urljoin(URL, title_el.get("href", ""))

        # Intro (verbeterde extractie)
        intro_el = li.select_one("p.timelist__intro")
        if intro_el:
            # Soms zit de tekst in een <a> binnen de <p>
            intro = intro_el.get_text(strip=True)
        else:
            intro = None

        # ID
        uid = make_id(titel, link)
        if uid in seen_ids:
            continue
        seen_ids.add(uid)

        items.append({
            "id": uid,
            "categorie": categorie,
            "titel": titel,
            "link": link,
            "intro": intro,
            "published_at": published_at,
            "scraped_at": datetime.utcnow().isoformat()
        })

    logging.info(f"Gevonden items: {len(items)}")
    return items


if __name__ == "__main__":
    data = scrape_beursnieuws()

    # 3 — Nooit een lege JSON wegschrijven
    if not data:
    logging.error("WAARSCHUWING: Geen items gevonden — foutmelding JSON wordt geschreven.")

    error_json = {
        "error": "beursNieuwsFeed is niet gegenereerd, kijk naar je GitHub Scraper & Actions logs",
        "scraped_at": datetime.utcnow().isoformat()
    }

    with open("data/nieuws.json", "w", encoding="utf-8") as f:
        json.dump(error_json, f, ensure_ascii=False, indent=2)

    exit(0)

    logging.info(f"Scraped {len(data)} nieuwsitems.")
