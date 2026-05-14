#!/usr/bin/env python3
"""
WebM24 Projekte-Katalog Generator
Katalog exportieren: python generate_catalog.py
"""

import json
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
    """Sucht das beste Logo in den Assets. Weiße Version bevorzugt für dunklen Hintergrund."""
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
    """Generiert HTML für eine einzelne Projekt-Karte."""
    bilder_html = ""
    if projekt.get("video"):
        src = bild_pfad_html(projekt["video"])
        bilder_html = f'<video src="{src}" class="projekt-video" autoplay muted loop playsinline></video>'
    elif projekt.get("bilder"):
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
              <button class="slider-pfeil slider-pfeil-rechts" aria-label="Nächstes Bild">&#8250;</button>
              <div class="slider-punkte">{punkte}</div>
            </div>"""

    ergebnis_html = ""
    if projekt.get("ergebnis"):
        ergebnis_html = f'<div class="projekt-ergebnis">{projekt["ergebnis"]}</div>'

    url_html = ""
    if projekt.get("url"):
        icon_web = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/><line x1="2" y1="12" x2="22" y2="12"/></svg>'
        url_html = f'<a href="{projekt["url"]}" class="projekt-url" onclick="window.open(\'{projekt["url"]}\', \'_blank\'); return false;">{icon_web} Website besuchen</a>'

    return f"""
        <div class="projekt-karte">
          {bilder_html}
          <div class="projekt-name">{projekt["name"]}</div>
          <div class="projekt-kunde">{projekt.get("kunde", "")}</div>
          <div class="projekt-beschreibung">{projekt.get("beschreibung", "")}</div>
          {ergebnis_html}
          <div class="projekt-zeitraum">{projekt.get("zeitraum", "")}</div>
          {url_html}
        </div>"""


LEISTUNGEN = [
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/><line x1="2" y1="12" x2="22" y2="12"/></svg>',
        "name": "Webseiten",
        "beschreibung": "Individuelle Webseiten von Grund auf, maßgeschneidert für Ihr Unternehmen"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>',
        "name": "Webseite Update",
        "beschreibung": "Pflege, Aktualisierung und Optimierung bestehender Webseiten"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>',
        "name": "Branding",
        "beschreibung": "Logo, Corporate Design und visuelle Identität aus einer Hand"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>',
        "name": "SaaS",
        "beschreibung": "Digitale Software-Lösungen für Ihr Unternehmen"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
        "name": "Bilder bearbeiten",
        "beschreibung": "Professionelle Bildbearbeitung und Retusche für starke Wirkung"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m22 8-6 4 6 4V8z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/></svg>',
        "name": "Videos bearbeiten",
        "beschreibung": "Videoproduktion, Schnitt und Nachbearbeitung für alle Kanäle"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        "name": "Werbung",
        "beschreibung": "Online-Werbung und Social Media Kampagnen für Unternehmen"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>',
        "name": "Google Konto",
        "beschreibung": "Google My Business Pflege, Google Ads Setup und Optimierung"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        "name": "SEO",
        "beschreibung": "Suchmaschinenoptimierung für mehr Sichtbarkeit und Reichweite"
    },
    {
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "name": "Monatsberichte",
        "beschreibung": "Regelmäßige Auswertungen und verständliche Reports, über Website, Google & Social Media, damit Sie Reichweite, Anfragen und Sichtbarkeit klar nachvollziehen können"
    },
]


def erstelle_leistungs_seite(seiten_index, kontakt_email, kontakt_telefon):
    """Generiert die Leistungsübersicht-Seite."""
    karten_html = ""
    for leistung in LEISTUNGEN:
        karten_html += f"""
        <div class="leistungs-karte">
          <span class="leistungs-icon">{leistung['icon']}</span>
          <div class="leistungs-name">{leistung['name']}</div>
          <div class="leistungs-beschreibung">{leistung['beschreibung']}</div>
        </div>"""

    kontakt_teile = []
    if kontakt_email:
        kontakt_teile.append(f'<a href="mailto:{kontakt_email}" class="kontakt-link">{kontakt_email}</a>')
    if kontakt_telefon:
        telefon_href = kontakt_telefon.replace(' ', '').replace('-', '')
        kontakt_teile.append(f'<a href="tel:{telefon_href}" class="kontakt-link">{kontakt_telefon}</a>')
    kontakt_info = "  |  ".join(kontakt_teile)

    return f"""
    <div class="seite leistungs-seite" id="seite-{seiten_index}">
      <div class="seiten-kopf">
        <div>
          <div class="seiten-titel">Was ich für dich umsetze</div>
          <div class="seiten-nummer">10 Leistungsbereiche aus einer Hand</div>
        </div>
      </div>
      <div class="leistungs-raster">
        {karten_html}
      </div>
      <div class="leistungs-cta">
        <div class="leistungs-cta-text">Interesse geweckt? Spreche mich direkt an.</div>
        <div class="leistungs-cta-kontakt">{kontakt_info}</div>
      </div>
    </div>"""


def erstelle_kategorie_seite(kategorie, projekte, seiten_index):
    """Generiert HTML für eine Kategorie-Seite."""
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

    # Leistungsübersicht
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

    # Meta-Tags
    meta = info.get("meta", {})
    kontakt_name = info.get("kontakt", {}).get("name", "")
    html = html.replace('{{ meta_beschreibung }}', meta.get("beschreibung", info.get("untertitel", "")))
    html = html.replace('{{ meta_autor }}', kontakt_name)
    html = html.replace('{{ meta_og_bild }}', meta.get("og_bild", ""))
    html = html.replace('{{ meta_og_url }}', meta.get("og_url", ""))

    favicon_pfad = meta.get("favicon", "")
    if favicon_pfad:
        endung = Path(favicon_pfad).suffix.lower()
        mime = "image/png" if endung == ".png" else "image/svg+xml" if endung == ".svg" else "image/x-icon"
        html = html.replace('{{ meta_favicon }}', f'<link rel="icon" type="{mime}" href="{favicon_pfad}" />')
    else:
        html = html.replace('{{ meta_favicon }}', '')

    # Inhaltsverzeichnis
    html = html.replace(
        '{% for eintrag in inhaltsverzeichnis %}\n        <li class="iv-eintrag" onclick="geheZuSeite({{ eintrag.seite }})">\n          <span class="iv-name">{{ eintrag.kategorie }}</span>\n          <span class="iv-punkt"></span>\n          <span class="iv-seite">{{ eintrag.anzahl }} Projekt(e)</span>\n        </li>\n        {% endfor %}',
        iv_html
    )

    # Kategorie-Seiten
    html = html.replace('{{ kategorie_seiten }}', kategorie_seiten_html_final)

    # Leistungsübersicht
    html = html.replace('{{ leistungs_seite }}', leistungs_seite_html)

    # Kategorie Nav JS
    html = html.replace('{{ kategorie_nav_js }}', nav_js)

    # Kontakt
    kontakt_email = kontakt.get("email", "")
    kontakt_website = kontakt.get("website", "")
    kontakt_telefon = kontakt.get("telefon", "")
    kontakt_github = kontakt.get("github", "")
    kontakt_portfolio = kontakt.get("portfolio", "")

    if kontakt_email:
        html = html.replace(
            '{% if kontakt_email %}\n        <div class="kontakt-zeile"><strong>E-Mail:</strong> {{ kontakt_email }}</div>\n        {% endif %}',
            f'<div class="kontakt-zeile"><strong>E-Mail:</strong> <a href="mailto:{kontakt_email}" class="kontakt-link">{kontakt_email}</a></div>'
        )
    else:
        html = html.replace('{% if kontakt_email %}\n        <div class="kontakt-zeile"><strong>E-Mail:</strong> {{ kontakt_email }}</div>\n        {% endif %}', '')

    if kontakt_website:
        website_url = kontakt_website if kontakt_website.startswith('http') else f'https://{kontakt_website}'
        html = html.replace(
            '{% if kontakt_website %}\n        <div class="kontakt-zeile"><strong>Web:</strong> {{ kontakt_website }}</div>\n        {% endif %}',
            f'<div class="kontakt-zeile"><strong>Web:</strong> <a href="{website_url}" class="kontakt-link" target="_blank">{kontakt_website}</a></div>'
        )
    else:
        html = html.replace('{% if kontakt_website %}\n        <div class="kontakt-zeile"><strong>Web:</strong> {{ kontakt_website }}</div>\n        {% endif %}', '')

    if kontakt_telefon:
        telefon_href = kontakt_telefon.replace(' ', '').replace('-', '')
        html = html.replace(
            '{% if kontakt_telefon %}\n        <div class="kontakt-zeile"><strong>Tel:</strong> {{ kontakt_telefon }}</div>\n        {% endif %}',
            f'<div class="kontakt-zeile"><strong>Tel:</strong> <a href="tel:{telefon_href}" class="kontakt-link">{kontakt_telefon}</a></div>'
        )
    else:
        html = html.replace('{% if kontakt_telefon %}\n        <div class="kontakt-zeile"><strong>Tel:</strong> {{ kontakt_telefon }}</div>\n        {% endif %}', '')

    # SVG Icons für Links
    icon_github = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>'
    icon_portfolio = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>'
    icon_datenschutz = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'

    # Footer (unterhalb Navigation)
    footer_links = []
    if kontakt_github:
        footer_links.append(f'<a href="{kontakt_github}" class="footer-link" target="_blank">{icon_github}GitHub</a>')
    if kontakt_portfolio:
        footer_links.append(f'<a href="{kontakt_portfolio}" class="footer-link" target="_blank">{icon_portfolio}Portfolio</a>')
    footer_html = f'<div class="seiten-footer">{"".join(footer_links)}</div>' if footer_links else ''
    html = html.replace('{{ seiten_footer }}', footer_html)

    # Impressum und Datenschutz als eigene zentrierte Sektion unterhalb des Footers
    icon_impressum = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'
    rechtliches_html = (
        f'<div class="rechtliches-footer">'
        f'<a href="impressum.html" class="rechtliches-link">{icon_impressum}Impressum</a>'
        f'<a href="datenschutz.html" class="rechtliches-link">{icon_datenschutz}Datenschutz</a>'
        f'</div>'
    )
    html = html.replace('{{ rechtliches_footer }}', rechtliches_html)

    # Rückseite Links
    rueckseite_links_teile = []
    if kontakt_github:
        rueckseite_links_teile.append(f'<a href="{kontakt_github}" class="rueckseite-link" target="_blank">{icon_github}GitHub</a>')
    if kontakt_portfolio:
        rueckseite_links_teile.append(f'<a href="{kontakt_portfolio}" class="rueckseite-link" target="_blank">{icon_portfolio}Portfolio</a>')
    rueckseite_links_html = f'<div class="rueckseite-links">{"".join(rueckseite_links_teile)}</div>' if rueckseite_links_teile else ''
    html = html.replace('{{ rueckseite_links }}', rueckseite_links_html)

    # Cover Tags
    html = html.replace(
        '{% for kat in verwendete_kategorien %}\n        <div class="cover-kategorie-tag">{{ kat }}</div>\n        {% endfor %}',
        cover_tags
    )

    # Rueckseite ID fix
    html = html.replace('id="seite-rueck"', f'id="seite-{rueck_index}"')

    return html


def exportiere_projekte_json(daten):
    """Exportiert die Projektdaten als docs/projekte.json für WebMiete24."""
    ausgabe = DOCS_DIR / "projekte.json"
    with open(ausgabe, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
    print(f"[OK] Projekte-JSON:  {ausgabe}")


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

    # Assets in docs/ kopieren für GitHub Pages
    kopiere_assets_nach_docs()

    # Projektdaten für WebMiete24 exportieren
    exportiere_projekte_json(daten)

    print("\nIm Browser öffnen? (j/n): ", end="")
    antwort = input().strip().lower()
    if antwort == "j":
        webbrowser.open(str(ausgabe_lokal))

    print("\nFertig. Für GitHub Pages: 'docs/' Ordner committen und pushen.")


if __name__ == "__main__":
    generiere_katalog()
