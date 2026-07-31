#!/usr/bin/env python3
"""Importa un export Deckbox-format (tool 'Mythic') della collezione di pol e la
normalizza in {nome_canonico_scryfall: quantita_totale}.

A differenza del vecchio export Moxfield, questo formato NON ha Scryfall ID ne'
Container Type/Name: niente piu' distinzione box vs mazzo, e la risoluzione dei
nomi non-inglesi va fatta via (set code, collector number) invece che via ID
diretto. Standard library only, stesso stile di fetch_scryfall.py."""
import json, os, sys, csv, time, urllib.request

HERE = os.path.dirname(__file__)
RESOLVE_CACHE = os.path.join(HERE, "decks", "pol", "collection_resolve_cache.json")

def load_rows(path):
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        return list(r)

def post_collection(idents):
    body = json.dumps({"identifiers": idents}).encode()
    req = urllib.request.Request(
        "https://api.scryfall.com/cards/collection", data=body,
        headers={"User-Agent": "mtg-pod-sim/1.0", "Accept": "application/json",
                 "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=40))

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "decks", "pol", "collection_2026-07-31.csv")
    rows = load_rows(src)
    print("righe export:", len(rows))

    cache = {}
    if os.path.exists(RESOLVE_CACHE):
        cache = json.load(open(RESOLVE_CACHE, encoding="utf-8"))

    # chiave di risoluzione: set#collector_number (case-insensitive sul set)
    def key(row):
        return f"{row['Edition'].strip().lower()}#{row['Collector Number'].strip()}"

    todo_keys = {}
    for row in rows:
        k = key(row)
        if k not in cache:
            todo_keys[k] = row

    print("da risolvere via Scryfall:", len(todo_keys))
    items = list(todo_keys.items())
    not_found = []
    for i in range(0, len(items), 75):
        chunk = items[i:i+75]
        idents = [{"set": row["Edition"].strip().lower(),
                    "collector_number": row["Collector Number"].strip()} for _, row in chunk]
        try:
            r = post_collection(idents)
        except Exception as e:
            print("batch err:", e)
            time.sleep(1)
            continue
        got_keys = set()
        for c in r.get("data", []):
            ck = f"{c.get('set','').lower()}#{c.get('collector_number','')}"
            cache[ck] = c["name"]
            got_keys.add(ck)
        for k, row in chunk:
            if k not in got_keys:
                not_found.append(row)
        time.sleep(0.12)
        print(f"  {min(i+75,len(items))}/{len(items)}")

    # retry not_found matchando solo per nome (fallback, meno preciso ma meglio di niente)
    still_missing = []
    if not_found:
        retry_items = [(row, {"name": row["Name"]}) for row in not_found]
        for i in range(0, len(retry_items), 75):
            chunk = retry_items[i:i+75]
            idents = [id_ for _, id_ in chunk]
            try:
                r = post_collection(idents)
                data = r.get("data", [])
                # allinea per ordine: la collection endpoint preserva l'ordine solo se tutto trovato,
                # quindi ri-matchiamo per nome case-insensitive
                by_name = {c["name"].lower(): c["name"] for c in data}
                for row, _ in chunk:
                    nm = row["Name"].strip().lower()
                    k = key(row)
                    if nm in by_name:
                        cache[k] = by_name[nm]
                    else:
                        still_missing.append(row)
            except Exception as e:
                print("retry err:", e)
                still_missing.extend(r for r, _ in chunk)
            time.sleep(0.12)

    json.dump(cache, open(RESOLVE_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    # aggrega quantita' per nome canonico
    totals = {}
    unresolved_qty = 0
    for row in rows:
        k = key(row)
        qty = int(row["Count"] or 0)
        name = cache.get(k)
        if name is None:
            unresolved_qty += qty
            continue
        totals[name] = totals.get(name, 0) + qty

    out_path = os.path.join(HERE, "decks", "pol", "collection_normalized_2026-07-31.json")
    json.dump(totals, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)

    print("carte canoniche distinte:", len(totals))
    print("copie totali:", sum(totals.values()))
    print("copie non risolte (ancora mancanti):", unresolved_qty, f"({len(still_missing)} righe)")
    for row in still_missing[:20]:
        print("  MISS:", row["Name"], row["Edition"], row["Collector Number"], row["Language"])
    print("output:", out_path)

if __name__ == "__main__":
    main()
