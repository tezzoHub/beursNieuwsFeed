# beursNieuwsFeed
Scrapes the newsitems from beurs.nl

Automatische scraper voor het ophalen van nieuwsitems van https://www.beurs.nl/nieuws/default.aspx.  
De scraper draait via GitHub Actions en publiceert de output als JSON via GitHub Pages.

## 📡 Live JSON Feed
De actuele nieuwsfeed is publiek beschikbaar via GitHub Pages:

**https://tezzohub.github.io/beursNieuwsFeed/data/nieuws.json**

Deze URL kan worden gebruikt in WordPress of andere systemen om de nieuwsitems automatisch in te laden.

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
│       └── scrape.yml     (komt in stap 4)
│
├── README.md
└── requirements.txt


## 🚀 Automatisering (GitHub Actions)

De scraper wordt automatisch uitgevoerd via een workflow (scrape.yml) die:
- de website bezoekt
- nieuwsitems verzamelt
- `data/nieuws.json` bijwerkt
- wijzigingen commit naar de repository
- de JSON-feed publiceert via GitHub Pages

(Workflow wordt toegevoegd in stap 4.)

## 📝 Toekomstige uitbreidingen

- Validatie van dubbele items  
- RSS‑achtige output  
- WordPress shortcode integratie  
- Caching en diff‑detectie
