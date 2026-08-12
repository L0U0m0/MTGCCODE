#!/usr/bin/env python3
"""Importa un export della collezione di pol (tool 'Mythic') e la normalizza in
{nome_canonico_scryfall: quantita_totale}.

Formato 2026-08-12+: colonne Card Name / English Name / Set Code / Collector Number /
Scryfall ID / Container Type / Container Name. A differenza del formato precedente
(2026-07-01..2026-07-31, colonne Count/Name/Edition, nessun nome inglese ne' ID), qui
il nome inglese e' gia' in colonna: NON serve piu' risolvere via Scryfall set+collector
number per le carte non in inglese. Somma le quantita' su TUTTI i Container Type
(box/deck/maybeboard) — sono comunque copie fisicamente possedute, il container e'
solo l'organizzazione interna dell'app.
"""
import csv
import json
import os
import sys
from collections import Counter


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src:
        print("uso: python3 import_collection_deckbox.py <export.csv> [YYYY-MM-DD]")
        sys.exit(1)
    date = sys.argv[2] if len(sys.argv) > 2 else None
    if not date:
        base = os.path.basename(src)
        # atteso: collection_YYYY-MM-DD.csv
        date = base.replace("collection_", "").replace(".csv", "")

    here = os.path.dirname(__file__)
    with open(src, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    print("righe export:", len(rows))

    owned = Counter()
    per_container = Counter()
    missing_name = 0
    for row in rows:
        name = (row.get("English Name") or "").strip()
        if not name:
            missing_name += 1
            name = (row.get("Card Name") or "").strip()
        qty = int(row.get("Quantity") or 0)
        owned[name] += qty
        per_container[row.get("Container Type", "?")] += qty

    if missing_name:
        print(f"ATTENZIONE: {missing_name} righe senza English Name, uso Card Name (potrebbero essere non-inglesi non risolte)")

    print("nomi unici:", len(owned))
    print("totale copie:", sum(owned.values()))
    print("per container:", dict(per_container))

    out_norm = os.path.join(here, "decks", "pol", f"collection_normalized_{date}.json")
    json.dump(dict(sorted(owned.items())), open(out_norm, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("scritto:", out_norm)


if __name__ == "__main__":
    main()
