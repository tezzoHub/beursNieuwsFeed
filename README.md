# beursNieuwsFeed
Scrapes the newsitems from beurs.nl

# beursNieuwsFeed
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
