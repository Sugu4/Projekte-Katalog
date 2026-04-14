# WebM24 Projekte-Katalog

Digitaler Katalog zum Präsentieren deiner Projekte. Zeigt Webseiten, Branding, SEO und alle anderen Leistungen in einem professionellen Design.

---

[![Katalog](https://img.shields.io/badge/Katalog-ansehen-green?style=for-the-badge)](https://sugu4.github.io/Projekte-Katalog/)


## Voraussetzungen

- Python 3.. installiert
- Google Chrome installiert (für PDF-Export)

---

## Ordnerstruktur

```
Projekte-Katalog/
├── data/
│   └── projects.json        ← Datenbank aller Projekte
├── assets/
│   ├── Logo WebM24.png
│   └── projekte/            ← Bilder der Projekte
│       ├── 001_projektname/
│       └── 002_projektname/
├── templates/
│   └── katalog.html         ← Design-Template (hier Design anpassen)
├── output/                  ← generierte HTML-Dateien (lokal)
├── docs/
│   └── index.html           ← GitHub Pages Version (automatisch)
├── add_project.py           ← Projekt hinzufügen
├── generate_catalog.py      ← Katalog als HTML exportieren
├── generate_pdf.py          ← Katalog als PDF exportieren
└── README.md                ← diese Datei
```

---

## Schritt 1: Projekt hinzufügen

```bash
python add_project.py
```

Du wirst durch folgende Eingaben geführt:

| Feld | Beispiel |
|---|---|
| Projektname | SanTech Devey UG |
| Kategorie | Webseiten |
| Kundenname | SanTech Devey UG |
| Beschreibung | Webseite von Grund auf erstellt |
| Ergebnis | Innerhalb 2 Wochen live geschaltet |
| Zeitraum | Dezember 2025 |
| Bildpfad(e) | C:/Bilder/santech1.png;C:/Bilder/santech2.png |

Mehrere Bilder mit Semikolon trennen: `Bild1.png;Bild2.png`

---

## Schritt 2: Katalog generieren

```bash
python generate_catalog.py
```

Erstellt automatisch:
- `output/katalog_JAHR-MONAT.html` — lokale Version mit Datum
- `docs/index.html` — GitHub Pages Version

---

## Schritt 3: PDF exportieren

```bash
python generate_pdf.py
```

Erstellt:
- `output/WebM24_Katalog_JAHR-MONAT.pdf` — Querformat, alle Seiten

Nutzt Chrome im Hintergrund. Kein extra Programm nötig.

---

## Schritt 4: Katalog ansehen

HTML lokal öffnen:
```bash
start output/katalog_2026-04.html
```

Navigation im Katalog:
- Pfeiltasten Links/Rechts zum Blättern
- Kategorie-Buttons oben für Schnellnavigation
- "Cover" und "Inhalt" Buttons oben links

---

## Projekt bearbeiten oder löschen

```bash
python add_project.py
```

Im Menü:
- `2` — Alle Projekte anzeigen
- `3` — Projekt löschen

Direkt in der Datei bearbeiten:
```
data/projects.json
```

---

## Kategorien

| Kategorie | Beschreibung |
|---|---|
| Webseiten | Neue Webseiten von Grund auf |
| Webseite Update | Pflege bestehender Seiten |
| Branding | Logo, Design, Corporate Identity |
| SaaS | Software-Lösungen |
| Bilder bearbeiten | Bildbearbeitung und Retusche |
| Videos bearbeiten | Videoproduktion und Schnitt |
| Werbung | Online-Werbung und Kampagnen |
| Google Konto | Google My Business und Ads |
| SEO | Suchmaschinenoptimierung |
| Monatsberichte | Analysen und Berichte |

---

## Projekt-Bilder hinzufügen

Bilder gehören in den passenden Ordner:

```
assets/projekte/001_santechdevey/   ← Bilder für SanTech
assets/projekte/002_byglanz/        ← Bilder für By Glanz
```

Danach Katalog neu generieren:
```bash
python generate_catalog.py
```

---

## Design anpassen

Design-Datei: `templates/katalog.html`

Farben oben in der Datei unter `:root`:

```css
--farbe-akzent: #2e7dd1;    /* Blau  */
--farbe-gruen:  #3db54a;    /* Grün  */
--farbe-seite:  #0f1e30;    /* Hintergrund */
```

Nach Änderungen immer neu generieren:
```bash
python generate_catalog.py
```

---

## Änderungen

| Was | Date |
|---|---|
| Design, Farben, Layout | templates/katalog.html |
| Slider-Geschwindigkeit | templates/katalog.html |
| Projektdaten, Bilder | data/projects.json |
| Neue Projekte hinzufügen | python add_project.py |
| Ausgabe neu bauen | python generate_catalog.py |


## Kontaktdaten aktualisieren

In `data/projects.json` unter `katalog_info > kontakt`:

```json
"kontakt": {
  "name": "Süleyman Gümüs",
  "email": "sueleyman.guemues46@gmail.com",
  "website": "",
  "telefon": "+49 176 41966733"
}
```

---

## Häufige Fragen

**Neue Version im Mai: kommt ein neues HTML?**
Ja. `generate_catalog.py` erstellt `katalog_2026-05.html` automatisch. Die alten Dateien bleiben erhalten.

**Zeigt index.html immer alle Projekte?**
Ja. `docs/index.html` zeigt immer alle Projekte aus `projects.json`, egal wann sie hinzugefügt wurden.

**Manuelle Änderungen in index.html oder katalog_*.html?**
Nicht empfohlen. Diese Dateien werden bei jedem `generate_catalog.py` überschrieben. Änderungen immer in `templates/katalog.html` oder `data/projects.json` vornehmen.

**PDF ist im Hochformat?**
`python generate_pdf.py` verwenden, nicht den Windows-Drucker. Der Generator nutzt Chrome direkt und erstellt das PDF immer im Querformat.
