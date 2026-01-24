# beursNieuwsFeed

Automatische scraper voor het ophalen van nieuwsitems van  
https://www.beurs.nl/nieuws.
De scraper draait via GitHub Actions en publiceert de output als JSON via GitHub Pages.

---

## 📡 Live JSON Feed

De actuele nieuwsfeed is publiek beschikbaar via GitHub Pages:
**https://tezzohub.github.io/beursNieuwsFeed/data/nieuws.json**
Deze URL kan worden gebruikt in WordPress of andere systemen om de nieuwsitems automatisch in te laden.

---

## 📁 Repository structuur

beursNieuwsFeed/
│
├── src/
│   └── scraper.py
│
├── data/
│   └── nieuws.json        (wordt automatisch gevuld)
│
├── .github/
│   └── workflows/
│       └── scrapeBeursNieuwsWorkflow.yml
│
├── README.md
└── requirements.txt

---


---

## 🚀 Automatisering (GitHub Actions)

De scraper wordt automatisch uitgevoerd via een workflow (`scrapeBeursNieuwsWorkflow.yml`) die:

- de website bezoekt  
- nieuwsitems verzamelt  
- `data/nieuws.json` bijwerkt  
- wijzigingen commit naar de repository  
- de JSON-feed publiceert via GitHub Pages  

---

## 🔄 GitHub Actions workflow

De scraper draait automatisch:

- elke 30 minuten via cron  
- handmatig via “Run workflow”

De workflow:

1. installeert Python  
2. installeert dependencies  
3. draait `scraper.py`  
4. commit & pusht wijzigingen naar `main`  
5. publiceert de JSON via GitHub Pages  

---

## 📦 JSON Schema

Elk nieuwsitem in `nieuws.json` heeft de volgende structuur:

{
  "id": "string",               // Unieke hash van titel + link
  "categorie": "string",        // Categorie van het nieuwsitem
  "titel": "string",            // Titel van het artikel
  "link": "string",             // Absolute URL naar het artikel
  "intro": "string",            // Korte intro van het artikel
  "published_at": "string",     // Datum + tijd van publicatie (ISO)
  "scraped_at": "string"        // Centrale timestamp van de scraper-run (ISO)
}


## 🌐 JSON-feed gebruiken in WordPress

De JSON-feed kan worden ingeladen in WordPress via een shortcode of custom plugin.  
Voorbeeld shortcode (nog te implementeren): [beursnieuws limit="10"]



## 📝 Toekomstige uitbreidingen

- Validatie van dubbele items  
- RSS‑achtige output  
- WordPress shortcode integratie  
- Caching en diff‑detectie
- Source toevoegen aan item (to be discussed)
