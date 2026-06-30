#!/usr/bin/env python3
"""
edh_pod11.py — Simulatore astratto di pod Commander a 4 giocatori.

Modello: per ogni mazzo si fa un "goldfish" (turno in cui il motore o la combo
vanno online) con mulligan, poi un layer di interazione/wrath/protezione a 4
giocatori decide chi chiude per primo. Pod casuali da 4 mazzi pescati dagli 11
profili, 10.000 partite. Riporta winrate, tasso di mulligan, turno di chiusura
e split combo/motore.

LIMITI (dichiarati): NON simula politica, odio da cimitero, né interazione
carta-per-carta. È una bussola RELATIVA (chi sta sopra/sotto), non una verità
assoluta sui numeri. Le serate reali al tavolo correggono il modello.

Uso:  python3 edh_pod11.py
Richiede solo la standard library (random, statistics, collections).

I profili sono parametrici: per aggiornare un mazzo dopo una modifica, cambia i
suoi valori in P{} (vedi commenti sui campi sotto).
"""
import random, statistics
from collections import Counter, defaultdict

R = random.Random(11112026)  # seme master, per risultati riproducibili

# ---------------------------------------------------------------------------
# CAMPI DEL PROFILO
#   lands        n. terre (più alto = mana più consistente, meno mulligan)
#   engine_n     n. carte-motore nei 99
#   need_eng     quante carte-motore servono per essere "online"
#   ramp_n       n. carte-rampa
#   cmdr_cost    costo del comandante
#   engine_mana  mana per avviare il motore
#   draw         1 se il mazzo pesca extra (quasi tutti)
#   clock        turni dal motore-online alla chiusura
#   wraths       n. board wipe che il mazzo può lanciare contro il leader
#   spots        n. rimozioni/counter mirati
#   prot         n. pezzi di protezione del proprio piano
#   rebuild      quanto è lento a riprendersi da un wrath
#   grind        forza nel lungo (decide le partite che vanno a oltranza)
#   creature_engine  True se il motore è a creature (vulnerabile ai wrath)
#   cn/cneed/cmana/cdelay/ctut  parametri della combo:
#       cn=carte-combo nei 99, cneed=pezzi da pescare, cmana=mana per innescare,
#       cdelay=turni dall'assemblaggio al kill, ctut=tutor utilizzabili.
#       cn=0 => il mazzo non ha combo infinite (vince di motore/combat).
#   mana_pen     penalità di mana opzionale (manabase imperfetta)
# ---------------------------------------------------------------------------
P = {
"Deadpool":     dict(lands=36,engine_n=19,need_eng=2,ramp_n=10,cmdr_cost=4,engine_mana=6,draw=1,clock=3,wraths=4,spots=6,prot=4,rebuild=2,grind=8,creature_engine=True, cn=5,cneed=3,cmana=8,cdelay=0,ctut=0),
"Glarb":        dict(lands=36,engine_n=11,need_eng=1,ramp_n=15,cmdr_cost=3,engine_mana=6,draw=1,clock=2,wraths=2,spots=8,prot=6,rebuild=1,grind=9,creature_engine=False,cn=11,cneed=3,cmana=7,cdelay=0,ctut=5),
"Toph":         dict(lands=37,engine_n=10,need_eng=1,ramp_n=8, cmdr_cost=4,engine_mana=5,draw=1,clock=3,wraths=3,spots=6,prot=8,rebuild=1,grind=7,creature_engine=True, cn=8,cneed=2,cmana=6,cdelay=1,ctut=1),
"Vincent":      dict(lands=38,engine_n=12,need_eng=1,ramp_n=8, cmdr_cost=4,engine_mana=5,draw=1,clock=3,wraths=2,spots=8,prot=4,rebuild=2,grind=8,creature_engine=True, cn=2,cneed=2,cmana=7,cdelay=0,ctut=6),
"Y'shtola":     dict(lands=33,engine_n=27,need_eng=2,ramp_n=10,cmdr_cost=4,engine_mana=5,draw=1,clock=3,wraths=4,spots=8,prot=6,rebuild=1,grind=9,creature_engine=True, cn=2,cneed=2,cmana=4,cdelay=2,ctut=2),
"First Sliver": dict(lands=33,engine_n=28,need_eng=2,ramp_n=13,cmdr_cost=5,engine_mana=5,draw=1,clock=2,wraths=2,spots=3,prot=6,rebuild=2,grind=8,creature_engine=True, cn=6,cneed=3,cmana=8,cdelay=1,ctut=2),
"Sonic":        dict(lands=34,engine_n=12,need_eng=2,ramp_n=8, cmdr_cost=4,engine_mana=6,draw=1,clock=3,wraths=4,spots=7,prot=6,rebuild=2,grind=7,creature_engine=True, cn=8,cneed=2,cmana=6,cdelay=0,ctut=1,mana_pen=-1),
"Sam&Frodo":    dict(lands=36,engine_n=12,need_eng=1,ramp_n=10,cmdr_cost=3,engine_mana=4,draw=1,clock=4,wraths=3,spots=6,prot=3,rebuild=1,grind=8,creature_engine=True, cn=13,cneed=2,cmana=5,cdelay=0,ctut=4),
"Shroofus":     dict(lands=32,engine_n=24,need_eng=2,ramp_n=12,cmdr_cost=3,engine_mana=5,draw=1,clock=3,wraths=4,spots=3,prot=5,rebuild=2,grind=7,creature_engine=True, cn=0,cneed=99,cmana=99,cdelay=0,ctut=0),
"Mimeoplasm":   dict(lands=36,engine_n=14,need_eng=1,ramp_n=12,cmdr_cost=5,engine_mana=5,draw=1,clock=2,wraths=3,spots=7,prot=5,rebuild=2,grind=6,creature_engine=True, cn=8,cneed=2,cmana=5,cdelay=1,ctut=2),
# Obeka: aggiornato all'ultima revisione (38 terre, counter snelliti)
"Obeka":        dict(lands=38,engine_n=14,need_eng=1,ramp_n=11,cmdr_cost=4,engine_mana=5,draw=1,clock=4,wraths=4,spots=7,prot=6,rebuild=1,grind=8,creature_engine=False,cn=2,cneed=2,cmana=10,cdelay=0,ctut=2),
}
NAMES = list(P)


def goldfish(p, rng, track_keep=None):
    """Restituisce (turno motore-online, turno combo-pronta). Gestisce il mulligan."""
    n = 99; lands = p['lands']
    lib = list(range(n)); rng.shuffle(lib)
    landset = set(lib[:lands]); rng.shuffle(lib)
    hand = lib[:7]; rest = lib[7:]
    nl = lambda h: sum(1 for x in h if x in landset)
    m = 0
    while (nl(hand) < 2 or nl(hand) > 5) and m < 2:          # mulligan: tieni 2-5 terre
        rng.shuffle(lib); hand = lib[:7]; rest = lib[7:]; m += 1
    if track_keep is not None:
        track_keep.append(0 if m == 0 else 1)
    nonland = [x for x in range(n) if x not in landset]
    eng = set(nonland[:p['engine_n']])
    rmp = set(nonland[p['engine_n']:p['engine_n']+p['ramp_n']])
    base = p['engine_n'] + p['ramp_n']
    cmb = set(nonland[base:base+p['cn']])
    tut = set(nonland[base+p['cn']:base+p['cn']+p['ctut']])
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
            if cmb_t is None and missing - used <= 0 and mana >= p['cmana'] + 2*used and t >= 3:
                cmb_t = t
    return eng_t or 13, cmb_t or 99


def pod_game(decks, rng):
    """Simula un pod a 4. Restituisce (vincitore, via, turno)."""
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
        if online[leader] <= t and fin[leader] <= t + 2:          # il tavolo reagisce al leader
            for opp in decks:
                if opp == leader: continue
                if spots[opp] > 0 and rng.random() < min(0.45, spots[opp]*0.07):
                    spots[opp] -= 1
                    if prot[leader] > 0 and rng.random() < 0.5: prot[leader] -= 1
                    else: fin[leader] += 1
                if wr[opp] > 0 and P[leader]['creature_engine'] and via[leader] == 'engine' \
                   and rng.random() < min(0.30, wr[opp]*0.08):
                    wr[opp] -= 1
                    if prot[leader] > 0 and rng.random() < 0.4: prot[leader] -= 1
                    else: fin[leader] += P[leader]['rebuild']
        w = min(decks, key=lambda nm: fin[nm])
        if fin[w] <= t:
            return w, via[w], t
    # nessuno ha chiuso: vince chi macina di più
    w = max(((P[nm]['grind']*rng.random(), nm) for nm in decks))[1]
    return w, 'grind', 15


def main(NG=10000):
    # tassi di mulligan (loop dedicato, semi deterministici)
    keep = {nm: [] for nm in NAMES}
    for nm in NAMES:
        for i in range(20000):
            goldfish(P[nm], random.Random(i*13+7), track_keep=keep[nm])

    wins = Counter(); appear = Counter(); endt = []; viac = Counter()
    for _ in range(NG):
        rng = random.Random(R.randrange(10**9))
        pod = rng.sample(NAMES, 4)
        for nm in pod: appear[nm] += 1
        w, v, t = pod_game(pod, rng); wins[w] += 1; endt.append(t); viac[v] += 1

    print(f"=== POD CASUALI 4p — {NG} partite, {len(NAMES)} mazzi ===\n")
    print(f"{'MAZZO':14s}{'winrate':>9s}{'mull%':>8s}")
    for nm in sorted(NAMES, key=lambda x: -wins[x]/appear[x]):
        print(f"{nm:14s}{100*wins[nm]/appear[nm]:8.1f}%{100*sum(keep[nm])/len(keep[nm]):7.1f}%")
    print(f"\nChiusura: mediana T{int(statistics.median(endt))}, media T{sum(endt)/len(endt):.1f}")
    tot = sum(viac.values())
    print(f"Vittorie via: combo {100*viac['combo']/tot:.0f}% | "
          f"engine {100*viac['engine']/tot:.0f}% | grind {100*viac['grind']/tot:.0f}%")
    print("\n[bussola relativa: winrate atteso in pod equo = 25%; "
          "il modello non vede politica né odio da cimitero]")


if __name__ == "__main__":
    main()
