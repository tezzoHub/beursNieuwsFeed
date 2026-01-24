import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.beurs.nl/nieuws/default.aspx"

def scrape_beursnieuws():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    items = []

    # Zoek alle regels die beginnen met "Beursnieuws" + tijd + titel
    for block in soup.find_all(text=lambda t: "Beursnieuws" in t):
        parent = block.parent

        # Tijdstip staat meestal direct erachter
        time_el = parent.find_next(text=lambda t: ":" in t and len(t.strip()) <= 5)
        title_el = parent.find_next("a")

        if not title_el:
            continue

        intro_el = title_el.find_next("p")

        items.append({
            "categorie": "Beursnieuws",
            "tijd": time_el.strip() if time_el else None,
            "titel": title_el.get_text(strip=True),
            "link": "https://www.beurs.nl" + title_el["href"],
            "intro": intro_el.get_text(strip=True) if intro_el else None,
            "scraped_at": datetime.utcnow().isoformat()
        })

    return items


if __name__ == "__main__":
    data = scrape_beursnieuws()
    with open("data/nieuws.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Scraped {len(data)} nieuwsitems.")
