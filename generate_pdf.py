#!/usr/bin/env python3
"""
WebM24 PDF Generator
PDF exportieren: python generate_pdf.py

Nutzt Chrome/Edge im Hintergrund fuer korrektes Querformat-PDF.
Kein extra Programm noetig, Chrome oder Edge muss installiert sein.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"

CHROME_PFADE = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.environ.get("USERNAME", "")),
]

EDGE_PFADE = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def finde_browser():
    for pfad in CHROME_PFADE:
        if Path(pfad).exists():
            return pfad, "Chrome"
    for pfad in EDGE_PFADE:
        if Path(pfad).exists():
            return pfad, "Edge"
    return None, None


def finde_html():
    """Sucht die aktuellste Katalog-HTML-Datei."""
    dateien = sorted(OUTPUT_DIR.glob("katalog_*.html"), reverse=True)
    if dateien:
        return dateien[0]
    return None


def generiere_pdf():
    print("\n" + "=" * 50)
    print("  WebM24 PDF Generator")
    print("=" * 50)

    browser_pfad, browser_name = finde_browser()
    if not browser_pfad:
        print("\nChrome oder Edge nicht gefunden.")
        print("Bitte manuell: Katalog im Browser oeffnen, Strg+P, Ziel: 'Als PDF speichern'")
        print("Wichtig: NICHT 'Microsoft Print to PDF' waehlen!")
        return

    html_datei = finde_html()
    if not html_datei:
        print("\nKeine Katalog-HTML gefunden. Zuerst: python generate_catalog.py")
        return

    datum = date.today().strftime("%Y-%m")
    pdf_datei = OUTPUT_DIR / f"WebM24_Katalog_{datum}.pdf"

    print(f"\nBrowser:  {browser_name}")
    print(f"Quelle:   {html_datei.name}")
    print(f"Ziel:     {pdf_datei.name}")
    print("\nPDF wird erstellt...")

    try:
        subprocess.run([
            browser_pfad,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--run-all-compositor-stages-before-draw",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_datei}",
            html_datei.as_uri()
        ], check=True, capture_output=True, timeout=30)

        if pdf_datei.exists():
            groesse = pdf_datei.stat().st_size / 1024
            print(f"\n[OK] PDF erstellt: {pdf_datei}")
            print(f"     Groesse: {groesse:.0f} KB")

            print("\nPDF oeffnen? (j/n): ", end="")
            if input().strip().lower() == "j":
                os.startfile(str(pdf_datei))
        else:
            print("\nFehler: PDF wurde nicht erstellt.")

    except subprocess.TimeoutExpired:
        print("\nTimeout: Browser hat zu lange gebraucht.")
    except subprocess.CalledProcessError as e:
        print(f"\nFehler beim PDF erstellen: {e}")
        print("Tipp: Katalog manuell im Browser oeffnen und Strg+P druecken.")
    except Exception as e:
        print(f"\nUnerwarteter Fehler: {e}")


if __name__ == "__main__":
    generiere_pdf()
