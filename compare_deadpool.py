#!/usr/bin/env python3
"""A/B controllato: pol/deadpool (base) vs pol/deadpool_b3opt.
Stessi 3 avversari casuali per partita; misura win% dello slot Deadpool,
turno di chiusura mediano e come vince (combo/engine/grind).
Uso: python compare_deadpool.py [n_partite]
"""
import sys, random, statistics
from collections import Counter
import sim_pods as S

P = S.P
NG = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
A, B = "pol/deadpool", "pol/deadpool_b3opt"
pool = [k for k in P if k not in (A, B)]
R = random.Random(11112026)

def run(slot, opp, seed):
    rng = random.Random(seed)
    w, via, t = S.pod_game([slot] + opp, rng)
    return (w == slot), via, t

win = {A: 0, B: 0}
via = {A: Counter(), B: Counter()}
endt = {A: [], B: []}
for _ in range(NG):
    opp = R.sample(pool, 3)
    seed = R.randrange(10**9)
    for slot in (A, B):
        won, v, t = run(slot, opp, seed)
        if won:
            win[slot] += 1
            via[slot][v] += 1
        endt[slot].append(t)

print(f"A/B controllato — {NG} partite, pod 4p (Deadpool + 3 avversari casuali identici)\n")
print(f"{'versione':24}{'win%':>7}{'T mediano':>11}   vittorie per tipo")
for slot in (A, B):
    wr = 100 * win[slot] / NG
    med = statistics.median(endt[slot])
    vd = ", ".join(f"{k} {v}" for k, v in via[slot].most_common())
    print(f"{slot:24}{wr:6.1f}%{med:>11.0f}   {vd}")
delta = 100 * (win[B] - win[A]) / NG
print(f"\nDelta win% (B3-opt - base): {delta:+.1f} punti")
