# Simulazione pod Commander — `edh_pod11.py`

Simulatore astratto di pod a 4 giocatori per confrontare la forza relativa degli
11 mazzi del parco. Pesca pod casuali da 4 mazzi, gioca 10.000 partite con
mulligan, e riporta winrate, tasso di mulligan, turno di chiusura e split
combo/motore.

## Uso

```bash
python3 edh_pod11.py
```

Nessuna dipendenza esterna: solo la standard library di Python 3.

## Come funziona

Per ogni mazzo si calcola un **goldfish**: il turno in cui il motore (o la combo)
va online, partendo da una mano di 7 carte con regola di mulligan (tieni 2-5
terre, max 2 mulligan). Poi un **layer di interazione a 4 giocatori** fa reagire
il tavolo al leader: rimozioni/counter mirati ritardano chi sta per chiudere, i
board wipe colpiscono i mazzi a motore-creature, la protezione assorbe. Chi
"finisce" per primo vince; se nessuno chiude entro il T15 vince chi macina di più.

## Limiti (importanti)

Il modello **NON** simula:
- politica e accordi al tavolo,
- odio da cimitero (penalizza in modo specifico Mimeoplasm, Vincent, Sam&Frodo),
- interazione carta-per-carta (è parametrico, non legge le 99 carte).

Va usato come **bussola relativa** (chi sta sopra/sotto la media del 25%), non
come previsione assoluta. Le serate reali correggono il modello — è già successo.

## Aggiornare un mazzo dopo una modifica

I mazzi sono profili parametrici nel dizionario `P{}` in cima allo script. Dopo
una revisione, aggiorna i campi rilevanti. I più usati:

- `lands` — più terre = mana più consistente, meno mulligan (es. Obeka 35→38).
- `spots` / `wraths` — quanta interazione mirata / di massa.
- `cn`, `cneed`, `cmana`, `cdelay`, `ctut` — parametri della combo
  (`cn=0` = nessuna combo infinita).
- `creature_engine` — `True` se il motore è a creature (vulnerabile ai wrath).

I commenti nello script spiegano ogni campo.

## Caveat sui profili

I valori sono **stime calibrate** sull'analisi dei mazzi, non misure esatte. Due
mazzi con lo stesso winrate possono comportarsi diversamente al tavolo. Quando
una lista cambia in modo sostanziale, riaggiorna il profilo e rigira: il valore
sta nel **confronto prima/dopo**, non nel numero assoluto.
