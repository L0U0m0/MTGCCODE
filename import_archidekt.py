#!/usr/bin/env python3
"""Importa mazzi Commander pubblici da Archidekt per giocatori diversi da pol.

Fonte: archidekt.com/api (pubblica, nessuna autenticazione richiesta — lo stesso
endpoint usato da bolasscryer-pricebot/deck_import.py per /importa). Cammina
l'albero cartelle di un profilo, prende solo i mazzi deckFormat==3 (Commander),
e scrive decks/<player>/<slug>.txt nel formato standard della repo (comandante
in prima riga, resto in ordine alfabetico, terre base incluse).
"""
import json
import os
import re
import sys
import time

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36")
H = {"User-Agent": UA}
ROOT = os.path.dirname(__file__)
DECKS = os.path.join(ROOT, "decks")

# player -> (username archidekt, sottocartelle Archidekt da ESCLUDERE — es. napkin mai montati)
PLAYERS = {
    "rocchi": ("ODN_RooK", {"Brew Only"}),
    "saverio": ("CancaroMan", set()),
    "sbernuz": ("Sbernuz", set()),
    "sbaragli": ("Sbara", set()),
}


def root_folder(username):
    r = requests.get(f"https://archidekt.com/u/{username}", headers=H, timeout=20)
    r.raise_for_status()
    m = re.search(r'"rootFolderId":(\d+)', r.text)
    if not m:
        raise RuntimeError(f"rootFolderId non trovato per {username}")
    return int(m.group(1))


def walk_folders(folder_id, path):
    r = requests.get(f"https://archidekt.com/api/decks/folders/{folder_id}/", headers=H, timeout=20)
    r.raise_for_status()
    d = r.json()
    here = path + [d["name"]]
    for dk in d.get("decks", []):
        yield here, dk
    for sf in d.get("subfolders", []):
        yield from walk_folders(sf["id"], here)


def fetch_deck(deck_id):
    r = requests.get(f"https://archidekt.com/api/decks/{deck_id}/", headers=H, timeout=20)
    r.raise_for_status()
    return r.json()


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def parse_deck(dati):
    """Ritorna (commander_names, righe [(qty, nome)], gc_count, edh_bracket)."""
    escluse = {c.get("name") for c in dati.get("categories", [])
               if c.get("includedInDeck") is False}
    commanders, righe, gc = [], [], 0
    for c in dati.get("cards", []):
        oc = (c.get("card") or {}).get("oracleCard") or {}
        nome = oc.get("name")
        if not nome:
            continue
        categorie = c.get("categories") or []
        if categorie and categorie[0] in escluse:
            continue
        qty = c.get("quantity", 1)
        righe.append((qty, nome))
        if "Commander" in categorie:
            commanders.append(nome)
        if oc.get("gameChanger"):
            gc += qty
    return commanders, righe, gc, dati.get("edhBracket")


def write_deck_file(player, slug, commanders, righe):
    path = os.path.join(DECKS, player, f"{slug}.txt")
    cmdr_set = set(commanders)
    resto = sorted([(q, n) for q, n in righe if n not in cmdr_set], key=lambda x: x[1])
    with open(path, "w", encoding="utf-8") as f:
        for nome in commanders:
            f.write(f"1 {nome}\n")
        for q, n in resto:
            f.write(f"{q} {n}\n")
    return path


def main():
    os.makedirs(os.path.join(DECKS, "sbaragli"), exist_ok=True)
    report = []
    for player, (uname, escludi_cartelle) in PLAYERS.items():
        print(f"=== {player} ({uname}) ===")
        rid = root_folder(uname)
        seen_slugs = {}
        for path, dk in walk_folders(rid, []):
            if dk["deckFormat"] != 3:
                continue
            if escludi_cartelle & set(path):
                continue
            time.sleep(0.15)
            try:
                dati = fetch_deck(dk["id"])
            except Exception as e:
                print(f"  ERRORE deck {dk['id']} ({dk['name']}): {e}")
                continue
            commanders, righe, gc, bracket = parse_deck(dati)
            if not commanders:
                print(f"  SALTATO (nessun comandante rilevato): {dk['name']}")
                continue
            slug = slugify(commanders[0])
            if slug in seen_slugs:
                seen_slugs[slug] += 1
                slug = f"{slug}_{seen_slugs[slug]}"
            else:
                seen_slugs[slug] = 1
            out_path = write_deck_file(player, slug, commanders, righe)
            folder_path = "/".join(path)
            print(f"  {slug}: {dk['name']} — {len(righe)} carte, GC={gc}, bracket={bracket}, cartella={folder_path}")
            report.append({
                "player": player, "slug": slug, "archidekt_name": dk["name"],
                "archidekt_id": dk["id"], "url": f"https://archidekt.com/decks/{dk['id']}",
                "n_cards": len(righe), "gc_count": gc, "edh_bracket": bracket,
                "folder_path": folder_path,
            })
    with open(os.path.join(DECKS, "archidekt_import_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(f"\nTotale mazzi importati: {len(report)}")
    print("Report: decks/archidekt_import_report.json")


if __name__ == "__main__":
    main()
