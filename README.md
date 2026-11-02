# Prep Box

Meal-Prep-App für eine 4-Wochen-Rotation im Muskelaufbau (2.400–2.500 kcal): Mittags-Box (kalt) und schnelles Abendessen, Einkauf am Samstag, Prep am Sonntag, Mo–Fr. Wochenplan, Einkaufsliste zum Abhaken, Prep-Schritte, Rezepte mit Makros.

Läuft als PWA über GitHub Pages: Settings → Pages → Branch `main` / root. Code und Design aus [meal-prep-app](https://github.com/haakonbessert-boop/meal-prep-app).

- `data/rezepte.json`, `data/zutaten.json`: Rezepte und Nährwerte (`python3 data/make.py` rechnet die Makros neu)
- `src/`: Vorlage, Service Worker, Icons
- `python3 build.py` baut `index.html`, `manifest.webmanifest`, `sw.js` und `icons/` ins Root
