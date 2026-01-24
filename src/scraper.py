import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, date
import hashlib

URL = "https://www.beurs.nl/nieuws/default.aspx"

# zet 09:31 naar ISO format
def normalize_time(tijd_str):
    if not tijd_str:
        return None
    try:
        today = date.today()
        dt = datetime.strptime(f"{today} {tijd_str}", "%Y-%m-%d %H:%M")
        return dt.isoformat()
    except:
        return None
# genereert een ID per nieuws item
def make_id(title, link):
    raw = (title + link).encode("utf-8")
    return hashlib.md5(raw).hexdigest()

# bezoekt de site en scrapet nieuws
def scrape_beursnieuws():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    seen_ids = set()

    # Zoek in elke rij in de nieuwsTabel de volgende items
    for row in soup.select("table.nieuws tr"):
        # tijd
        time_el = row.find("td", class_="tijd")
        tijd = normalize_time(time_el.get_text(strip=True)) if time_el else None

        # titel
        title_el = row.find("a")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        link = "https://www.beurs.nl" + title_el.get("href", "")

        # intro
        intro_el = row.find("p")
        intro = intro_el.get_text(strip=True) if intro_el else None

        # genereert ID
        uid = make_id(title, link)
        if uid in seen_ids:
            continue
        seen_ids.add(uid)

        items.append({
            "id": uid,
            "categorie": "Beursnieuws",
            "titel": title,
            "link": link,
            "intro": intro,
            "published_at": tijd,
            "scraped_at": datetime.utcnow().isoformat()
        })

    return items

if __name__ == "__main__":
    data = scrape_beursnieuws()
    with open("data/nieuws.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Scraped {len(data)} nieuwsitems.")
