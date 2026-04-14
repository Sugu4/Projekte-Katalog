#!/usr/bin/env python3
"""
WebM24 Projekte-Katalog Generator
Katalog exportieren: python generate_catalog.py
"""

import json
import os
import shutil
import webbrowser
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "projects.json"
TEMPLATE_FILE = BASE_DIR / "templates" / "katalog.html"
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"


def lade_daten():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def finde_logo():
    """Sucht das beste Logo in den Assets. Weisse Version bevorzugt fuer dunklen Hintergrund."""
    prioritaet = [
        "Logo WebM24 x weiß.png",
        "Logo WebM24.png",
        "Logo WebM24 x Prime.png",
        "LogoTele WebM24.png",
    ]
    for name in prioritaet:
        pfad = ASSETS_DIR / name
        if pfad.exists():
            return f"../assets/{name}"
    return None


def bild_pfad_html(relativer_pfad):
    """Konvertiert gespeicherten Pfad zu HTML-relativem Pfad."""
    if not relativer_pfad:
        return None
    return f"../{relativer_pfad}"


def kopiere_assets_nach_docs():
    """Kopiert den Assets-Ordner in docs/ damit GitHub Pages die Bilder findet."""
    ziel = DOCS_DIR / "assets"
    if ASSETS_DIR.exists():
        if ziel.exists():
            shutil.rmtree(ziel)
        shutil.copytree(ASSETS_DIR, ziel)
        print("[OK] Assets nach docs/assets/ kopiert")


def erstelle_projekt_karte(projekt):
    """Generiert HTML fuer eine einzelne Projekt-Karte."""
    bilder_html = ""
    if projekt.get("bilder"):
        bilder = projekt["bilder"]
        name = projekt["name"]
        if len(bilder) == 1:
            src = bild_pfad_html(bilder[0])
            bilder_html = f'<img src="{src}" alt="{name}" class="projekt-bild" onerror="this.style.display=\'none\'" />'
        else:
            imgs = ""
            punkte = ""
            for b in bilder:
                src = bild_pfad_html(b)
                imgs += f'\n              <img src="{src}" alt="{name}" class="projekt-bild" onerror="this.style.display=\'none\'" />'
                punkte += '<div class="slider-punkt"></div>'
            bilder_html = f"""<div class="bild-slider">
              {imgs}
              <button class="slider-pfeil slider-pfeil-links" aria-label="Vorheriges Bild">&#8249;</button>
              <button class="slider-pfeil slider-pfeil-rechts" aria-label="Naechstes Bild">&#8250;</button>
              <div class="slider-punkte">{punkte}</div>
            </div>"""

    ergebnis_html = ""
    if projekt.get("ergebnis"):
        ergebnis_html = f'<div class="projekt-ergebnis">{projekt["ergebnis"]}</div>'

    return f"""
        <div class="projekt-karte">
          {bilder_html}
          <div class="projekt-name">{projekt["name"]}</div>
          <div class="projekt-kunde">{projekt.get("kunde", "")}</div>
          <div class="projekt-beschreibung">{projekt.get("beschreibung", "")}</div>
          {ergebnis_html}
          <div class="projekt-zeitraum">{projekt.get("zeitraum", "")}</div>
        </div>"""


LEISTUNGEN = [
    {
        "icon": "🌐",
        "name": "Webseiten",
        "beschreibung": "Individuelle Webseiten von Grund auf, maßgeschneidert für Ihr Unternehmen"
    },
    {
        "icon": "🔄",
        "name": "Webseite Update",
        "beschreibung": "Pflege, Aktualisierung und Optimierung bestehender Webseiten"
    },
    {
        "icon": "✦",
        "name": "Branding",
        "beschreibung": "Logo, Corporate Design und visuelle Identitaet aus einer Hand"
    },
    {
        "icon": "⚙",
        "name": "SaaS",
        "beschreibung": "Digitale Software-Loesungen für Ihr Unternehmen"
    },
    {
        "icon": "🖼",
        "name": "Bilder bearbeiten",
        "beschreibung": "Professionelle Bildbearbeitung und Retusche für starke Wirkung"
    },
    {
        "icon": "▶",
        "name": "Videos bearbeiten",
        "beschreibung": "Videoproduktion, Schnitt und Nachbearbeitung für alle Kanaele"
    },
    {
        "icon": "📢",
        "name": "Werbung",
        "beschreibung": "Online-Werbung und Social Media Kampagnen für Unternehmen"
    },
    {
        "icon": "G",
        "name": "Google Konto",
        "beschreibung": "Google My Business Pflege, Google Ads Setup und Optimierung"
    },
    {
        "icon": "↑",
        "name": "SEO",
        "beschreibung": "Suchmaschinenoptimierung für mehr Sichtbarkeit und Reichweite"
    },
    {
        "icon": "📊",
        "name": "Monatsberichte",
        "beschreibung": "Regelmaessige Analysen und transparente Berichte für Ihre Kunden"
    },
]


def erstelle_leistungs_seite(seiten_index, kontakt_email, kontakt_telefon):
    """Generiert die Leistungsuebersicht-Seite."""
    karten_html = ""
    for leistung in LEISTUNGEN:
        karten_html += f"""
        <div class="leistungs-karte">
          <span class="leistungs-icon">{leistung['icon']}</span>
          <div class="leistungs-name">{leistung['name']}</div>
          <div class="leistungs-beschreibung">{leistung['beschreibung']}</div>
        </div>"""

    kontakt_info = ""
    if kontakt_email:
        kontakt_info = kontakt_email
    if kontakt_telefon:
        trennzeichen = "  |  " if kontakt_info else ""
        kontakt_info += f"{trennzeichen}{kontakt_telefon}"

    return f"""
    <div class="seite leistungs-seite" id="seite-{seiten_index}">
      <div class="seiten-kopf">
        <div>
          <div class="seiten-titel">Was ich für Sie mache</div>
          <div class="seiten-nummer">10 Leistungsbereiche aus einer Hand</div>
        </div>
      </div>
      <div class="leistungs-raster">
        {karten_html}
      </div>
      <div class="leistungs-cta">
        <div class="leistungs-cta-text">Interesse geweckt? Sprechen Sie mich direkt an.</div>
        <div class="leistungs-cta-kontakt">{kontakt_info}</div>
      </div>
    </div>"""


def erstelle_kategorie_seite(kategorie, projekte, seiten_index):
    """Generiert HTML fuer eine Kategorie-Seite."""
    karten_html = ""
    for p in projekte:
        karten_html += erstelle_projekt_karte(p)

    anzahl_text = f"{len(projekte)} Projekt{'e' if len(projekte) != 1 else ''}"

    return f"""
    <div class="seite kategorie-seite" id="seite-{seiten_index}">
      <div class="kategorie-header">
        <div class="kategorie-nummer">{seiten_index:02d}</div>
        <div class="kategorie-info">
          <div class="kategorie-titel">{kategorie}</div>
          <div class="kategorie-anzahl">{anzahl_text}</div>
        </div>
      </div>
      <div class="projekte-raster">
        {karten_html}
      </div>
    </div>"""


def generiere_html(daten):
    """Erstellt das vollstaendige HTML des Katalogs."""
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    info = daten["katalog_info"]
    alle_projekte = daten["projekte"]
    alle_kategorien = daten["kategorien"]

    # Nur Kategorien mit Projekten
    kategorien_mit_projekten = {}
    for kat in alle_kategorien:
        projekte_in_kat = [p for p in alle_projekte if p["kategorie"] == kat]
        if projekte_in_kat:
            kategorien_mit_projekten[kat] = projekte_in_kat

    verwendete_kategorien = list(kategorien_mit_projekten.keys())

    # Seiten aufbauen (0=Cover, 1=Inhalt, 2..n=Kategorien, n+1=Rueckseite)
    seiten_index = 2
    kategorie_seiten_html = ""
    inhaltsverzeichnis = []
    kategorie_nav_eintraege = []

    for kat, projekte in kategorien_mit_projekten.items():
        kategorie_seiten_html += erstelle_kategorie_seite(kat, projekte, seiten_index)
        inhaltsverzeichnis.append({
            "kategorie": kat,
            "anzahl": len(projekte),
            "seite": seiten_index
        })
        kategorie_nav_eintraege.append({"name": kat, "seite": seiten_index})
        seiten_index += 1

    # Leistungsuebersicht
    kontakt = info.get("kontakt", {})
    leistungs_seite_html = erstelle_leistungs_seite(
        seiten_index,
        kontakt.get("email", ""),
        kontakt.get("telefon", "")
    )
    seiten_index += 1

    # Rueckseite Index
    rueck_index = seiten_index

    # Inhaltsverzeichnis HTML
    iv_html = ""
    for eintrag in inhaltsverzeichnis:
        iv_html += f"""
        <li class="iv-eintrag" onclick="geheZuSeite({eintrag['seite']})">
          <span class="iv-name">{eintrag['kategorie']}</span>
          <span class="iv-punkt"></span>
          <span class="iv-seite">{eintrag['anzahl']} Projekt(e)</span>
        </li>"""

    # Kategorie-Nav JS
    nav_js = ""
    for eintrag in kategorie_nav_eintraege:
        sicherer_name = eintrag["name"].replace("'", "\\'")
        nav_js += f"""
    const btn_{eintrag['seite']} = document.createElement('button');
    btn_{eintrag['seite']}.className = 'kat-nav-btn';
    btn_{eintrag['seite']}.textContent = '{sicherer_name}';
    btn_{eintrag['seite']}.onclick = () => geheZuSeite({eintrag['seite']});
    kategorieNav.appendChild(btn_{eintrag['seite']});"""

    logo = finde_logo()

    # Cover Kategorien Tags
    cover_tags = ""
    for kat in verwendete_kategorien:
        cover_tags += f'<div class="cover-kategorie-tag">{kat}</div>\n'

    # Rueckseite ID fix: muss als letztes nummerisch sein
    # Wir ersetzen id="seite-rueck" mit korrektem Index
    kategorie_seiten_html_final = kategorie_seiten_html

    # Template befuellen
    html = template

    # Logo
    if logo:
        html = html.replace(
            '{% if logo %}\n      <img src="{{ logo }}" alt="Logo" class="cover-logo" />\n      {% endif %}',
            f'<img src="{logo}" alt="Logo" class="cover-logo" />'
        )
        html = html.replace(
            '{% if logo_klein %}\n        <img src="{{ logo_klein }}" alt="Logo" style="max-height:40px; opacity:0.5;" />\n        {% endif %}',
            f'<img src="{logo}" alt="Logo" style="max-height:40px; opacity:0.5;" />'
        )
        html = html.replace(
            '{% if logo %}\n      <img src="{{ logo }}" alt="Logo" class="rueckseite-logo" />\n      {% endif %}',
            f'<img src="{logo}" alt="Logo" class="rueckseite-logo" />'
        )
    else:
        for block in [
            '{% if logo %}\n      <img src="{{ logo }}" alt="Logo" class="cover-logo" />\n      {% endif %}',
            '{% if logo_klein %}\n        <img src="{{ logo_klein }}" alt="Logo" style="max-height:40px; opacity:0.5;" />\n        {% endif %}',
            '{% if logo %}\n      <img src="{{ logo }}" alt="Logo" class="rueckseite-logo" />\n      {% endif %}'
        ]:
            html = html.replace(block, '')

    # Basis-Variablen
    html = html.replace('{{ katalog_titel }}', info.get("titel", "Projekte-Katalog"))
    html = html.replace('{{ katalog_untertitel }}', info.get("untertitel", ""))
    html = html.replace('{{ gesamte_projekte }}', str(len(alle_projekte)))
    html = html.replace('{{ anzahl_kategorien }}', str(len(verwendete_kategorien)))

    # Inhaltsverzeichnis
    html = html.replace(
        '{% for eintrag in inhaltsverzeichnis %}\n        <li class="iv-eintrag" onclick="geheZuSeite({{ eintrag.seite }})">\n          <span class="iv-name">{{ eintrag.kategorie }}</span>\n          <span class="iv-punkt"></span>\n          <span class="iv-seite">{{ eintrag.anzahl }} Projekt(e)</span>\n        </li>\n        {% endfor %}',
        iv_html
    )

    # Kategorie-Seiten
    html = html.replace('{{ kategorie_seiten }}', kategorie_seiten_html_final)

    # Leistungsuebersicht
    html = html.replace('{{ leistungs_seite }}', leistungs_seite_html)

    # Kategorie Nav JS
    html = html.replace('{{ kategorie_nav_js }}', nav_js)

    # Kontakt
    kontakt_email = kontakt.get("email", "")
    kontakt_website = kontakt.get("website", "")
    kontakt_telefon = kontakt.get("telefon", "")

    if kontakt_email:
        html = html.replace(
            '{% if kontakt_email %}\n        <div class="kontakt-zeile"><strong>E-Mail:</strong> {{ kontakt_email }}</div>\n        {% endif %}',
            f'<div class="kontakt-zeile"><strong>E-Mail:</strong> {kontakt_email}</div>'
        )
    else:
        html = html.replace('{% if kontakt_email %}\n        <div class="kontakt-zeile"><strong>E-Mail:</strong> {{ kontakt_email }}</div>\n        {% endif %}', '')

    if kontakt_website:
        html = html.replace(
            '{% if kontakt_website %}\n        <div class="kontakt-zeile"><strong>Web:</strong> {{ kontakt_website }}</div>\n        {% endif %}',
            f'<div class="kontakt-zeile"><strong>Web:</strong> {kontakt_website}</div>'
        )
    else:
        html = html.replace('{% if kontakt_website %}\n        <div class="kontakt-zeile"><strong>Web:</strong> {{ kontakt_website }}</div>\n        {% endif %}', '')

    if kontakt_telefon:
        html = html.replace(
            '{% if kontakt_telefon %}\n        <div class="kontakt-zeile"><strong>Tel:</strong> {{ kontakt_telefon }}</div>\n        {% endif %}',
            f'<div class="kontakt-zeile"><strong>Tel:</strong> {kontakt_telefon}</div>'
        )
    else:
        html = html.replace('{% if kontakt_telefon %}\n        <div class="kontakt-zeile"><strong>Tel:</strong> {{ kontakt_telefon }}</div>\n        {% endif %}', '')

    # Cover Tags
    html = html.replace(
        '{% for kat in verwendete_kategorien %}\n        <div class="cover-kategorie-tag">{{ kat }}</div>\n        {% endfor %}',
        cover_tags
    )

    # Rueckseite ID fix
    html = html.replace('id="seite-rueck"', f'id="seite-{rueck_index}"')

    return html


def generiere_katalog():
    print("\n" + "=" * 50)
    print("  WebM24 Katalog-Generator")
    print("=" * 50)

    daten = lade_daten()
    projekte = daten["projekte"]

    if not projekte:
        print("\nKeine Projekte vorhanden. Zuerst Projekte hinzufuegen:")
        print("  python add_project.py")
        return

    print(f"\n{len(projekte)} Projekte werden verarbeitet...")

    html = generiere_html(daten)

    # Lokale Version (mit Datum)
    OUTPUT_DIR.mkdir(exist_ok=True)
    ausgabe_lokal = OUTPUT_DIR / f"katalog_{date.today().strftime('%Y-%m')}.html"
    with open(ausgabe_lokal, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n[OK] Lokal:       {ausgabe_lokal}")

    # GitHub Pages Version (docs/index.html)
    # Pfade von ../assets/ auf assets/ anpassen
    html_docs = html.replace("../assets/", "assets/")
    DOCS_DIR.mkdir(exist_ok=True)
    ausgabe_docs = DOCS_DIR / "index.html"
    with open(ausgabe_docs, "w", encoding="utf-8") as f:
        f.write(html_docs)
    print(f"[OK] GitHub Pages: {ausgabe_docs}")

    # Assets in docs/ kopieren fuer GitHub Pages
    kopiere_assets_nach_docs()

    print("\nIm Browser oeffnen? (j/n): ", end="")
    antwort = input().strip().lower()
    if antwort == "j":
        webbrowser.open(str(ausgabe_lokal))

    print("\nFertig. Fuer GitHub Pages: 'docs/' Ordner committen und pushen.")


if __name__ == "__main__":
    generiere_katalog()
