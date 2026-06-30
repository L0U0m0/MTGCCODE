#!/usr/bin/env python3
"""Raccoglie i nomi carta unici da tutti i decks/**/*.txt e scarica i dati
Scryfall (tipo, costo, testo, keyword) in cache JSON. Standard library only."""
import json, os, re, time, urllib.request, glob

CACHE = os.path.join(os.path.dirname(__file__), "scryfall_cache.json")
DECKS = os.path.join(os.path.dirname(__file__), "decks")

def deck_files():
    yield from glob.glob(os.path.join(DECKS, "*.txt"))
    yield from glob.glob(os.path.join(DECKS, "*", "*.txt"))

def parse(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line: continue
        m = re.match(r"^(\d+)\s+(.*)$", line)
        if m: out.append((int(m.group(1)), m.group(2).strip()))
    return out

def main():
    names = set()
    for f in deck_files():
        for _, nm in parse(f):
            names.add(nm)
    print("nomi unici:", len(names))

    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))
    todo = [n for n in names if n.lower() not in cache]
    print("da scaricare:", len(todo))

    def post(idents):
        body = json.dumps({"identifiers": idents}).encode()
        req = urllib.request.Request("https://api.scryfall.com/cards/collection", data=body,
              headers={"User-Agent":"mtg-pod-sim/1.0","Accept":"application/json","Content-Type":"application/json"})
        return json.load(urllib.request.urlopen(req, timeout=40))

    def store(card):
        faces = card.get("card_faces") or []
        otext = card.get("oracle_text") or " ".join(f.get("oracle_text","") for f in faces)
        tline = card.get("type_line") or " // ".join(f.get("type_line","") for f in faces)
        rec = {"name": card["name"], "cmc": card.get("cmc",0.0), "type_line": tline,
               "oracle": otext, "keywords": card.get("keywords",[]),
               "ci": card.get("color_identity",[])}
        cache[card["name"].lower()] = rec
        # indicizza anche per faccia anteriore
        if " // " in card["name"]:
            cache.setdefault(card["name"].split(" // ")[0].lower(), rec)

    miss = []
    for i in range(0, len(todo), 75):
        chunk = todo[i:i+75]
        idents = [{"name": n} for n in chunk]
        try:
            r = post(idents)
        except Exception as e:
            print("batch err", e); time.sleep(1); continue
        for c in r.get("data", []): store(c)
        for nf in r.get("not_found", []):
            miss.append(nf.get("name",""))
        time.sleep(0.12)
        print(f"  {min(i+75,len(todo))}/{len(todo)}")

    # retry dei non trovati con la sola faccia anteriore
    retry = [{"name": m.split(" // ")[0]} for m in miss if " // " in m]
    if retry:
        for i in range(0, len(retry), 75):
            try:
                r = post(retry[i:i+75])
                for c in r.get("data", []): store(c)
            except Exception as e:
                print("retry err", e)
            time.sleep(0.12)

    json.dump(cache, open(CACHE,"w",encoding="utf-8"), ensure_ascii=False)
    still = [n for n in names if n.lower() not in cache]
    print("cache totale:", len(cache), "| ancora mancanti:", len(still))
    for n in still[:40]: print("  MISS:", n)

if __name__ == "__main__":
    main()
