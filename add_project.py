#!/usr/bin/env python3
"""
WebM24 Projekte-Katalog
Neues Projekt hinzufuegen: python add_project.py
"""

import json
import os
import shutil
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "projects.json"
BILDER_DIR = BASE_DIR / "assets" / "projekte"


def lade_daten():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def speichere_daten(daten):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)


def zeige_kategorien(kategorien):
    print("\nVerfuegbare Kategorien:")
    for i, kat in enumerate(kategorien, 1):
        print(f"  {i}. {kat}")


def waehle_kategorie(kategorien):
    zeige_kategorien(kategorien)
    while True:
        auswahl = input("\nKategorie-Nummer waehlen: ").strip()
        if auswahl.isdigit() and 1 <= int(auswahl) <= len(kategorien):
            return kategorien[int(auswahl) - 1]
        print("Ungueltige Auswahl, bitte erneut versuchen.")


def kopiere_bild(quellpfad, projekt_id):
    if not quellpfad:
        return []

    pfade = [p.strip() for p in quellpfad.split(";") if p.strip()]
    gespeicherte = []

    for pfad in pfade:
        src = Path(pfad)
        if src.exists():
            ziel = BILDER_DIR / projekt_id / src.name
            ziel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, ziel)
            gespeicherte.append(str(Path("assets") / "projekte" / projekt_id / src.name))
            print(f"  Bild kopiert: {src.name}")
        else:
            print(f"  Datei nicht gefunden: {pfad}")

    return gespeicherte


def neues_projekt():
    daten = lade_daten()
    kategorien = daten["kategorien"]

    print("\n" + "=" * 50)
    print("  WebM24 - Neues Projekt hinzufuegen")
    print("=" * 50)

    # Grunddaten
    name = input("\nProjektname (z.B. Firma Max Mustermann): ").strip()
    if not name:
        print("Projektname darf nicht leer sein.")
        return

    kategorie = waehle_kategorie(kategorien)

    kunde = input("Kundenname / Unternehmen: ").strip()
    beschreibung = input("Kurzbeschreibung (was wurde gemacht): ").strip()
    ergebnis = input("Ergebnis / Erfolg (z.B. +40% Besucher): ").strip()
    zeitraum = input(f"Zeitraum (z.B. Maerz 2026) [{date.today().strftime('%B %Y')}]: ").strip()
    if not zeitraum:
        zeitraum = date.today().strftime("%B %Y")

    # Bilder
    print("\nBilder hinzufuegen (optinal):")
    print("  Mehrere Pfade mit Semikolon trennen: C:/Bild1.png;C:/Bild2.png")
    bild_pfad = input("  Bildpfad(e) oder Enter ueberspringen: ").strip()

    # ID generieren
    projekt_id = f"{len(daten['projekte']) + 1:03d}_{name.lower().replace(' ', '_')[:20]}"

    bilder = kopiere_bild(bild_pfad, projekt_id)

    # Projekt-Objekt
    projekt = {
        "id": projekt_id,
        "name": name,
        "kategorie": kategorie,
        "kunde": kunde,
        "beschreibung": beschreibung,
        "ergebnis": ergebnis,
        "zeitraum": zeitraum,
        "bilder": bilder,
        "hinzugefuegt": str(date.today())
    }

    daten["projekte"].append(projekt)
    speichere_daten(daten)

    print(f"\nProjekt '{name}' wurde gespeichert.")
    print(f"Gesamt Projekte: {len(daten['projekte'])}")
    print("\nKatalog neu generieren: python generate_catalog.py")


def liste_projekte():
    daten = lade_daten()
    projekte = daten["projekte"]

    if not projekte:
        print("\nNoch keine Projekte vorhanden.")
        return

    print(f"\n{len(projekte)} Projekte gespeichert:\n")
    for p in projekte:
        print(f"  [{p['kategorie']}] {p['name']} - {p['kunde']} ({p['zeitraum']})")


def projekt_loeschen():
    daten = lade_daten()
    projekte = daten["projekte"]

    if not projekte:
        print("\nKeine Projekte zum Loeschen.")
        return

    liste_projekte()
    name_suche = input("\nProjektname zum Loeschen (Teilname reicht): ").strip().lower()

    treffer = [p for p in projekte if name_suche in p["name"].lower()]
    if not treffer:
        print("Kein Projekt gefunden.")
        return

    for p in treffer:
        bestaetigung = input(f"'{p['name']}' loeschen? (j/n): ").strip().lower()
        if bestaetigung == "j":
            daten["projekte"].remove(p)
            print(f"Projekt '{p['name']}' geloescht.")

    speichere_daten(daten)


def hauptmenue():
    while True:
        print("\n" + "=" * 50)
        print("  WebM24 Projekte-Katalog")
        print("=" * 50)
        print("  1. Neues Projekt hinzufuegen")
        print("  2. Alle Projekte anzeigen")
        print("  3. Projekt loeschen")
        print("  4. Katalog generieren")
        print("  0. Beenden")
        print("=" * 50)

        auswahl = input("Auswahl: ").strip()

        if auswahl == "1":
            neues_projekt()
        elif auswahl == "2":
            liste_projekte()
        elif auswahl == "3":
            projekt_loeschen()
        elif auswahl == "4":
            os.system(f'python "{BASE_DIR / "generate_catalog.py"}"')
        elif auswahl == "0":
            print("Tschuess!")
            break
        else:
            print("Ungueltige Auswahl.")


if __name__ == "__main__":
    hauptmenue()
