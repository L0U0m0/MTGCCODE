#!/usr/bin/env python3
"""Per ogni mazzo ~100c interroga Commander Spellbook (find-my-combos) e salva
in combo_cache.json: pezzi-combo presenti, n. combo, mana necessari, se la combo
e' una wincon. Cache per slug 'tag/nome'."""
import json, os, re, glob, time, urllib.request

ROOT = os.path.dirname(__file__)
DECKS = os.path.join(ROOT, "decks")
OUT = os.path.join(ROOT, "combo_cache.json")
WIN_FEATURES = ("win the game","infinite damage","lose the game","each opponent loses",
                "infinite life loss","win the","mill","poison")

def deck_files():
    for f in sorted(glob.glob(os.path.join(DECKS, "*.txt"))): yield "jimmy", f
    for f in sorted(glob.glob(os.path.join(DECKS, "*", "*.txt"))):
        yield os.path.basename(os.path.dirname(f)), f

def parse(path):
    out = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(\d+)\s+(.*)$", line.strip())
        if m: out.append((int(m.group(1)), m.group(2).strip()))
    return out

def query(cmd, main):
    body = json.dumps({"commanders":[{"card":c,"quantity":1} for c in cmd],
                       "main":[{"card":q[1],"quantity":q[0]} for q in main]}).encode()
    req = urllib.request.Request("https://backend.commanderspellbook.com/find-my-combos",
          data=body, headers={"User-Agent":"mtg-sim/1.0","Content-Type":"application/json","Accept":"application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))

def main():
    cache = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    files = list(deck_files())
    for tag, path in files:
        cards = parse(path)
        total = sum(q for q, _ in cards)
        slug = f"{tag}/{os.path.splitext(os.path.basename(path))[0]}"
        if slug in cache: continue
        if not (98 <= total <= 105):  # solo Commander ~100
            continue
        try:
            r = query([cards[0][1]], cards[1:])
        except Exception as e:
            print("ERR", slug, e); time.sleep(1); continue
        inc = r.get("results", r).get("included", [])
        pieces = set(); mvs = []; win = 0
        for cb in inc:
            for u in cb.get("uses", []):
                nm = u.get("card", {}).get("name")
                if nm: pieces.add(nm)
            mv = cb.get("manaValueNeeded")
            if isinstance(mv, (int, float)): mvs.append(mv)
            feats = " ".join((p.get("feature", {}) or {}).get("name","").lower()
                             for p in cb.get("produces", []))
            if any(w in feats for w in WIN_FEATURES): win += 1
        cache[slug] = {"n_combos": len(inc), "pieces": len(pieces),
                       "mvs": mvs, "wincons": win}
        print(f"{slug:34} combos={len(inc):3} pieces={len(pieces):3} wincons={win}")
        time.sleep(0.15)
    json.dump(cache, open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=0)
    print("cache combo:", len(cache))

if __name__ == "__main__":
    main()
