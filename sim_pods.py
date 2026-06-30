#!/usr/bin/env python3
"""sim_pods.py — fa girare due simulazioni sui profili auto-dedotti (profiles.json).

  POD A "serata reale": ogni partita = 1 mazzo a testa pescato a caso dai 4
          giocatori (jimmy/saverio/rocchi/tommaso). Misura la forza per GIOCATORE
          e quali suoi mazzi rendono di piu.
  POD B "tutti contro tutti": ogni partita = 4 mazzi pescati a caso dall'intero
          pool, indipendentemente dal proprietario. Misura la POTENZIALITA' di
          ogni singolo mazzo (ranking assoluto).

Stesso motore astratto di edh_pod11.py (goldfish + layer interazione/wrath).
BUSSOLA RELATIVA, non verita': niente politica, odio da cimitero, interazione
carta-per-carta. Profili dedotti da euristiche (vedi build_profiles.py).

Uso:  python sim_pods.py [n_partite]
"""
import json, os, sys, random, statistics
from collections import Counter, defaultdict

try: sys.stdout.reconfigure(encoding="utf-8")   # evita mojibake su console Windows
except Exception: pass

ROOT = os.path.dirname(__file__)
P = json.load(open(os.path.join(ROOT, "profiles.json"), encoding="utf-8"))
R = random.Random(11112026)


def goldfish(p, rng):
    n = 99; lands = min(p['lands'], 45)
    lib = list(range(n)); rng.shuffle(lib)
    landset = set(lib[:lands]); rng.shuffle(lib)
    hand = lib[:7]; rest = lib[7:]
    nl = lambda h: sum(1 for x in h if x in landset)
    m = 0
    while (nl(hand) < 2 or nl(hand) > 5) and m < 2:
        rng.shuffle(lib); hand = lib[:7]; rest = lib[7:]; m += 1
    nonland = [x for x in range(n) if x not in landset]
    eng = set(nonland[:p['engine_n']])
    rmp = set(nonland[p['engine_n']:p['engine_n'] + p['ramp_n']])
    base = p['engine_n'] + p['ramp_n']
    cmb = set(nonland[base:base + p['cn']])
    tut = set(nonland[base + p['cn']:base + p['cn'] + p['ctut']])
    drawn = set(hand)
    se = len(drawn & eng); sr = len(drawn & rmp); sc = len(drawn & cmb); st = len(drawn & tut)
    inp = 0; li = 0; cmdr = False; eng_t = None; cmb_t = None
    for t in range(1, 13):
        if t > 1 and li < len(rest):
            c = rest[li]; li += 1; drawn.add(c)
            se += c in eng; sr += c in rmp; sc += c in cmb; st += c in tut
        if p['draw'] and t >= 3 and li < len(rest):
            c = rest[li]; li += 1; drawn.add(c)
            se += c in eng; sr += c in rmp; sc += c in cmb; st += c in tut
        if inp < nl(drawn): inp += 1
        mana = inp + min(sr, 3) + p.get('mana_pen', 0)
        if not cmdr and mana >= p['cmdr_cost']: cmdr = True
        if eng_t is None and cmdr and se >= p['need_eng'] and mana >= p['engine_mana']:
            eng_t = t
        if p['cn'] > 0:
            missing = max(0, p['cneed'] - sc); used = min(missing, st)
            if cmb_t is None and missing - used <= 0 and mana >= p['cmana'] + 2 * used and t >= 3:
                cmb_t = t
    return eng_t or 13, cmb_t or 99


def pod_game(decks, rng):
    fin = {}; via = {}; online = {}
    for nm in decks:
        p = P[nm]; e, c = goldfish(p, rng)
        ef = e + p['clock']; cf = (c + p['cdelay']) if c < 99 else 99
        online[nm] = min(e, c if c < 99 else 99)
        if cf < ef: fin[nm] = cf; via[nm] = 'combo'
        else:       fin[nm] = ef; via[nm] = 'engine'
    prot = {nm: P[nm]['prot'] for nm in decks}
    spots = {nm: P[nm]['spots'] for nm in decks}
    wr = {nm: P[nm]['wraths'] for nm in decks}
    for t in range(2, 15):
        leader = min(decks, key=lambda nm: fin[nm])
        if online[leader] <= t and fin[leader] <= t + 2:
            for opp in decks:
                if opp == leader: continue
                if spots[opp] > 0 and rng.random() < min(0.45, spots[opp] * 0.07):
                    spots[opp] -= 1
                    if prot[leader] > 0 and rng.random() < 0.5: prot[leader] -= 1
                    else: fin[leader] += 1
                if wr[opp] > 0 and P[leader]['creature_engine'] and via[leader] == 'engine' \
                   and rng.random() < min(0.30, wr[opp] * 0.08):
                    wr[opp] -= 1
                    if prot[leader] > 0 and rng.random() < 0.4: prot[leader] -= 1
                    else: fin[leader] += P[leader]['rebuild']
        w = min(decks, key=lambda nm: fin[nm])
        if fin[w] <= t:
            return w, via[w], t
    w = max(((P[nm]['grind'] * rng.random(), nm) for nm in decks))[1]
    return w, 'grind', 15


def by_tag():
    d = defaultdict(list)
    for k, v in P.items(): d[v['tag']].append(k)
    return d


def sim_A(NG, seats=4):
    tags = by_tag()
    players = sorted(tags)
    wins_tag = Counter(); app_tag = Counter()
    wins_deck = Counter(); app_deck = Counter(); endt = []
    for _ in range(NG):
        rng = random.Random(R.randrange(10**9))
        chosen = rng.sample(players, min(seats, len(players)))  # 4 giocatori a caso
        pod = [rng.choice(tags[t]) for t in chosen]
        for t in chosen: app_tag[t] += 1
        for nm in pod: app_deck[nm] += 1
        w, v, t = pod_game(pod, rng)
        wins_tag[P[w]['tag']] += 1; wins_deck[w] += 1; endt.append(t)
    print(f"\n=== POD A — serata reale: {seats} giocatori a caso degli {len(players)}, "
          f"1 mazzo a testa, {NG} partite ===")
    print(f"{'GIOCATORE':11}{'winrate':>9}{'mazzi':>7}   (atteso equo {100//seats}%)")
    for t in sorted(players, key=lambda x: -wins_tag[x]/max(1, app_tag[x])):
        print(f"{t:11}{100*wins_tag[t]/max(1,app_tag[t]):8.1f}%{len(tags[t]):7}")
    print(f"\nMiglior mazzo per giocatore (winrate sulle sue apparizioni):")
    for t in sorted(players):
        best = max(tags[t], key=lambda nm: wins_deck[nm]/max(1, app_deck[nm]))
        wr = 100*wins_deck[best]/max(1, app_deck[best])
        print(f"  {t:11} {best.split('/')[1]:34} {wr:5.1f}%")
    print(f"Chiusura mediana T{int(statistics.median(endt))}")


def sim_B(NG):
    names = list(P)
    wins = Counter(); app = Counter(); endt = []; viac = Counter()
    for _ in range(NG):
        rng = random.Random(R.randrange(10**9))
        pod = rng.sample(names, 4)
        for nm in pod: app[nm] += 1
        w, v, t = pod_game(pod, rng); wins[w] += 1; endt.append(t); viac[v] += 1
    print(f"\n=== POD B — 4 mazzi a caso dal pool ({len(names)} mazzi), {NG} partite ===")
    rank = sorted(names, key=lambda nm: -wins[nm]/max(1, app[nm]))
    print("Top 15 potenziale:")
    print(f"{'#':>3} {'winrate':>8}  {'tag':8} mazzo")
    for i, nm in enumerate(rank[:15], 1):
        print(f"{i:3} {100*wins[nm]/max(1,app[nm]):7.1f}%  {P[nm]['tag']:8} {nm.split('/')[1]}")
    print("Bottom 5:")
    for nm in rank[-5:]:
        print(f"    {100*wins[nm]/max(1,app[nm]):7.1f}%  {P[nm]['tag']:8} {nm.split('/')[1]}")
    tot = sum(viac.values())
    print(f"\nChiusura mediana T{int(statistics.median(endt))} | "
          f"via: combo {100*viac['combo']/tot:.0f}% engine {100*viac['engine']/tot:.0f}% grind {100*viac['grind']/tot:.0f}%")
    return rank, wins, app


def main():
    NG = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    print(f"Pool: {len(P)} mazzi | profili EURISTICI (bussola relativa, non verita')")
    sim_A(NG)
    sim_B(NG)
    print("\n[limiti: niente politica/odio da cimitero/interazione carta-per-carta; "
          "combo da Commander Spellbook, resto da euristiche su dati Scryfall]")


if __name__ == "__main__":
    main()
