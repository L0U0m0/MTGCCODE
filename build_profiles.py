#!/usr/bin/env python3
"""build_profiles.py — STRADA 1: deduce un profilo di simulazione da ogni
lista decks/**/*.txt usando i dati carta Scryfall (scryfall_cache.json).

I parametri prodotti sono gli stessi di edh_pod11.py, così il motore di
simulazione resta invariato. Classificazione EURISTICA: una bussola relativa
coerente tra mazzi, NON una verita carta-per-carta. Limiti dichiarati in fondo.

Output: profiles.json  ->  { "tag/slug": {name, tag, ...campi profilo...} }
"""
import json, os, re, glob, statistics

ROOT = os.path.dirname(__file__)
CACHE = json.load(open(os.path.join(ROOT, "scryfall_cache.json"), encoding="utf-8"))
COMBOS = json.load(open(os.path.join(ROOT, "combo_cache.json"), encoding="utf-8"))
DECKS = os.path.join(ROOT, "decks")

# carte-pezzo note di combo infinite/quasi (lista curata, non esaustiva)
COMBO_PIECES = {c.lower() for c in [
 "Thassa's Oracle","Demonic Consultation","Tainted Pact","Laboratory Maniac","Jace, Wielder of Mysteries",
 "Dramatic Reversal","Isochron Scepter","Kiki-Jiki, Mirror Breaker","Splinter Twin","Pestermite","Deceiver Exarch",
 "Zealous Conscripts","Village Bell-Ringer","Restoration Angel","Felidar Guardian","Exquisite Blood","Sanguine Bond",
 "Cruel Celebrant","Mindcrank","Bloodchief Ascension","Walking Ballista","Heliod, Sun-Crowned","Triskelion",
 "Mikaeus, the Unhallowed","Nim Deathmantle","Ashnod's Altar","Phyrexian Altar","Pitiless Plunderer",
 "Grand Architect","Pili-Pala","Intruder Alarm","Sliver Queen","Food Chain","Squee, the Immortal","Eternal Scourge",
 "Worldgorger Dragon","Animate Dead","Dance of the Dead","Necromancy","Aggravated Assault","Bear Umbra","Sword of Feast and Famine",
 "Reaver Cleaver","Helm of the Host","Godo, Bandit Warlord","Dockside Extortionist","Temur Sabertooth",
 "Cloudstone Curio","Earthcraft","Squirrel Nest","Power Artifact","Basalt Monolith","Rings of Brighthearth","Grim Monolith",
 "Deadeye Navigator","Peregrine Drake","Palinchron","Great Whale","Ghostly Flicker","Archaeomancer","Mnemonic Wall",
 "Curiosity","Niv-Mizzet, the Firemind","Niv-Mizzet, Parun","Ophidian Eye","Tandem Lookout","Glistening Oil",
 "Underworld Breach","Lion's Eye Diamond","Brain Freeze","Seasons Past","Time Sieve","Aetherflux Reservoir","Bolas's Citadel",
 "Sensei's Divining Top","Gilded Lotus","Codie, Vociferous Codex","Helm of Awakening","Future Sight","Aluren",
 "Devoted Druid","Vizier of Remedies","Swift Reconfiguration","Kiki","Twinflame","Dualcaster Mage","Heat Shimmer",
 "Karmic Guide","Reveillark","Saffi Eriksdotter","Renegade Rallier","Boonweaver Giant","Protean Hulk",
 "Hullbreaker Horror","Lotus Petal","Academy Manufactor","Cauldron Familiar","Witch's Oven","Mechanized Production",
 "Terror of the Peaks","Orthion, Hero of Lavabrink","Orcish Bowmasters","Springheart Nantuko","Valley Floodcaller",
]}

TUTOR_RE = re.compile(r"search your library for (a|up to)", re.I)
LANDONLY_RE = re.compile(r"search your library for .{0,40}\bland", re.I)

def deck_files():
    for f in sorted(glob.glob(os.path.join(DECKS, "*.txt"))):
        yield "jimmy", f
    for f in sorted(glob.glob(os.path.join(DECKS, "*", "*.txt"))):
        yield os.path.basename(os.path.dirname(f)), f

def parse(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line: continue
        m = re.match(r"^(\d+)\s+(.*)$", line)
        if m: out.append((int(m.group(1)), m.group(2).strip()))
    return out

def card(nm):
    return CACHE.get(nm.lower())

def is_land(c): return "Land" in c["type_line"]
def is_creature(c): return "Creature" in c["type_line"]

def is_ramp(c, o, t):
    if is_land(c): return False
    if "Add {" in c["oracle"] or re.search(r"add (\{|one|two|three)", o):
        if c["cmc"] <= 4 and not is_creature(c) or (is_creature(c) and c["cmc"] <= 4):
            return True
    if LANDONLY_RE.search(o) and ("onto the battlefield" in o or "put it onto" in o or "put them onto" in o):
        return True
    if "creates a treasure" in o or "create a treasure" in o:
        return c["cmc"] <= 4
    return False

def is_draw(o):
    return ("draw" in o and "card" in o) and "draws a card" != o[:12]

def is_wrath(c, o):
    if re.search(r"(destroy|exile) all (creature|nonland|permanent)", o): return True
    if re.search(r"(destroy|exile) each (creature|nonland|permanent)", o): return True
    if "all creatures get -" in o or "creatures you don't control get -" in o: return True
    if "each player sacrifices" in o and "creature" in o: return True
    if re.search(r"deals \d+ damage to each creature", o): return True
    if "all creatures" in o and "destroy" in o: return True
    return False

def is_spot(c, o):
    ty = c["type_line"]
    txt_hit = bool(re.search(r"(destroy|exile) target", o) or "counter target" in o
                   or re.search(r"return target .{0,30}to (its owner'?s? )?hand", o)
                   or re.search(r"deals \d+ damage to (target|any target)", o)
                   or "fight" in o or "target creature an opponent controls" in o
                   or "target player sacrifices" in o)
    if not txt_hit: return False
    # esclude i wrath (gia contati) e i pump
    if is_wrath(c, o): return False
    return True

def is_prot(c, o):
    ty = c["type_line"]
    prot_words = ("hexproof","indestructible","shroud","protection from","phase out","phases out","can't be countered","ward")
    if not any(w in o for w in prot_words): return False
    yours = ("you control" in o or "your" in o or "target creature you control" in o
             or "Equipment" in ty or "Aura" in ty or "creatures you control" in o)
    return yours

def is_tutor(c, o):
    return bool(TUTOR_RE.search(o)) and not (LANDONLY_RE.search(o) and "card" not in o.split("library for")[-1][:50])

def is_engine(c, o):
    """Motore = permanente non-terra con trigger di valore ricorrente."""
    if is_land(c): return False
    if not any(k in c["type_line"] for k in ("Creature","Enchantment","Planeswalker","Artifact","Battle")):
        return False
    return ("whenever" in o or "at the beginning of" in o
            or re.search(r"\{t\}.*?(draw|create|deal|put|add a|search)", o) is not None)

def profile(tag, path):
    slug = f"{tag}/{os.path.splitext(os.path.basename(path))[0]}"
    cards = parse(path)
    total = sum(q for q, _ in cards)
    BASICS = ("plains","island","swamp","mountain","forest","wastes")
    recs = []; extra_lands = 0
    for q, nm in cards:
        c = card(nm)
        if c: recs.append((q, nm, c))
        elif any(b in nm.lower() for b in BASICS):   # terre base in formato 'X // X'
            extra_lands += q
    # comandante = prima riga (le liste lo mettono in testa)
    cmd = card(cards[0][1]) if cards and card(cards[0][1]) else None
    cmdr_cost = int(round(cmd["cmc"])) if cmd else 4
    cmdr_cost = max(2, min(8, cmdr_cost))

    lands = ramp = draw = wraths = spots = prot = tutors = 0
    creatures = 0
    engine_cre = 0           # motori a creatura (vulnerabili ai wrath)
    engine_cards = []        # (cmc) dei pezzi-motore
    nonland_count = 0
    recur = 0
    for q, nm, c in recs:
        o = c["oracle"].lower()
        if is_land(c):
            lands += q; continue
        nonland_count += q
        if is_creature(c): creatures += q
        ramp_card = is_ramp(c, o, c["type_line"])
        if ramp_card: ramp += q
        if is_draw(o): draw += q
        if is_wrath(c, o): wraths += q
        elif is_spot(c, o): spots += q
        if is_prot(c, o): prot += q
        if is_tutor(c, o): tutors += q
        if "from your graveyard to the battlefield" in o or ("return target" in o and "from your graveyard" in o):
            recur += q
        if is_engine(c, o) and not ramp_card:
            engine_cards.append(c["cmc"])
            if is_creature(c): engine_cre += q

    lands += extra_lands
    engine_n = max(5, min(28, len(engine_cards)))
    need_eng = 1 if engine_n <= 13 else 2
    engine_mana = int(round(statistics.median(engine_cards))) if engine_cards else 5
    engine_mana = max(4, min(7, engine_mana))
    avg_cre_cmc = statistics.mean([c["cmc"] for _,_,c in recs if is_creature(c)]) if creatures else 4

    creature_engine = engine_cre >= max(1, len(engine_cards) * 0.5)
    clock = 3
    if creatures >= 28 and avg_cre_cmc <= 3.0: clock = 2
    elif creatures <= 16: clock = 4
    grind = int(round(max(5, min(9, 5 + draw/6 + recur/3))))
    rebuild = 1 if not creature_engine else 2
    mana_pen = -1 if (lands <= 32 and ramp < 9) else 0

    # combo dai dati reali di Commander Spellbook (find-my-combos)
    cb = COMBOS.get(slug, {})
    n_combos = cb.get("n_combos", 0); pieces = cb.get("pieces", 0)
    mvs = cb.get("mvs", []); wincons = cb.get("wincons", 0)
    if n_combos > 0 and pieces >= 2:
        cn = min(14, pieces)
        cneed = 2
        cmana = int(round(statistics.median(mvs))) if mvs else 6
        cmana = max(3, min(10, cmana))
        cdelay = 0 if wincons > 0 else 1
        ctut = min(8, tutors)
    else:
        cn = 0; cneed = 99; cmana = 99; cdelay = 0; ctut = min(8, tutors)

    return dict(name=os.path.splitext(os.path.basename(path))[0], tag=tag, total=total,
        lands=lands, engine_n=engine_n, need_eng=need_eng, ramp_n=max(4, ramp),
        cmdr_cost=cmdr_cost, engine_mana=engine_mana, draw=1 if draw >= 6 else 0,
        clock=clock, wraths=min(8, wraths), spots=min(12, spots), prot=min(10, prot),
        rebuild=rebuild, grind=grind, creature_engine=bool(creature_engine),
        cn=cn, cneed=cneed, cmana=cmana, cdelay=cdelay, ctut=ctut, mana_pen=mana_pen)

def main():
    profs = {}
    skipped = []
    for tag, path in deck_files():
        cards = parse(path)
        total = sum(q for q, _ in cards)
        if total < 98 or total > 105:      # solo mazzi Commander ~100 carte
            skipped.append((tag, os.path.basename(path), total)); continue
        slug = f"{tag}/{os.path.splitext(os.path.basename(path))[0]}"
        profs[slug] = profile(tag, path)
    json.dump(profs, open(os.path.join(ROOT,"profiles.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=0)
    bytag = {}
    for k, v in profs.items(): bytag.setdefault(v["tag"], 0); bytag[v["tag"]] += 1
    print("profili simulabili:", len(profs), "| per tag:", bytag)
    print("scartati (non ~100c):", len(skipped))
    for t, f, n in skipped: print(f"   {t}/{f}  ({n}c)")

if __name__ == "__main__":
    main()
