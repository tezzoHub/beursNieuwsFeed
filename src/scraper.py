import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import hashlib

URL = "https://www.beurs.nl/nieuws/"

def make_id(title, link):
    raw = (title + link).encode("utf-8")
    return hashlib.md5(raw).hexdigest()

def scrape_beursnieuws():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
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
        link = title_el["href"]

        # Intro
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

    return items


if __name__ == "__main__":
    data = scrape_beursnieuws()
    with open("data/nieuws.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Scraped {len(data)} nieuwsitems.")
