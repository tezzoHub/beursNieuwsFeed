import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import hashlib
import logging
from urllib.parse import urljoin

# -------------------------
# Configuratie
# -------------------------

URL = "https://www.beurs.nl/nieuws"

# Logging voor o.a. GitHub Actions
logging.basicConfig(level=logging.INFO, format="%(message)s")


#----------------------------
# Helper functions
#----------------------------

# Creates an ID for each item;
def make_id(title, link):
    raw = (title + link).encode("utf-8")
    return hashlib.md5(raw).hexdigest()

# Sorting the items;
def sort_items(items):
    return sorted(
        items,
        key=lambda x: x.get("published_at") or "",
        reverse=True
    )

# Normalize the items
def normalize_item(item):
    return {
        "id": item.get("id"),
        "categorie": item.get("categorie"),
        "titel": item.get("titel"),
        "link": item.get("link"),
        "intro": item.get("intro"),
        "published_at": item.get("published_at"),
        "scraped_at": item.get("scraped_at")
    }

#----------------------------
# Main function - Scraper
#----------------------------

# Scrapet de items van de site
def scrape_beursnieuws():
    logging.info("Scraper gestart...")

    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        logging.error(f"FOUT: Kon de pagina niet ophalen: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    seen_ids = set()

    # Voor elk nieuwsitem uit <li class="timelist__item">
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

        # Intro (verbeterd)
        intro_el = li.select_one("p.timelist__intro")
        intro = intro_el.get_text(strip=True) if intro_el else None

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

#----------------------------
# Main console execute
#----------------------------

if __name__ == "__main__":
    scraped_at = datetime.utcnow().isoformat()
    data = scrape_beursnieuws()
    data = sort_items(data)
    data = [normalize_item(i) | {"scraped_at": scraped_at} for i in data] 
    
    if not data:
        logging.error("WAARSCHUWING: Geen items gevonden — foutmelding JSON wordt geschreven.")
        error_json = {
            "error": "beursNieuwsFeed is niet gegenereerd, kijk naar je GitHub Actions logs",
            "scraped_at": datetime.utcnow().isoformat()
        }
        with open("data/nieuws.json", "w", encoding="utf-8") as f:
            json.dump(error_json, f, ensure_ascii=False, indent=2)
        exit(0)

    with open("data/nieuws.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"Scraped {len(data)} nieuwsitems.")
