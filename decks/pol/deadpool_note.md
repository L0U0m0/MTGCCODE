# Deadpool, Trading Card — stato e ottimizzazione

_2026-07-02 · Rakdos · B3 alto (GC 3/3: Ancient Tomb, The One Ring, Orcish Bowmasters)_
_Strategia VALIDATA con pol._

## Strategia
Copy-burn + aristocrats. Copie temporanee (Orthion, Twinflame, Heat Shimmer, Electroduplicate,
Jaxis, Fire Crystal, Blade of Selves, Saw in Half) alimentano Terror of the Peaks/Purphoros/
Impact Tremors; le morti a fine turno pagano Mayhem Devil/Bastion/Plunderer. Sundial of the
Infinite rende permanenti le copie. **Il comandante è uno spot-removal no-target ricaricabile**
(ruling verificato): scambio textbox as-enters, bypassa shroud/ward, persiste dopo la morte,
ogni rientro = nuovo scambio → blink/reanimation = removal engine.
Combo: Orthion+Terror; Nim Deathmantle+Ashnod's Altar+Bowmasters.

## Stato: 8.5/10 — il più rifinito
- Numeri: terre 38 · ramp 7 · draw 10 · wrath 3 · spot 9 (post +Terminate)
- Difetti: **ramp 7 sotto target** (le linee Orthion vogliono 6+ mana); zero tutor (per scelta:
  quelli buoni sono GC e il tetto è pieno); dipendenza dal cimitero (Bojuka Bog fa male).

## Upgrade dalla collezione (liberi) — AGGIORNATO 2026-07-31
_Fonte collezione: nuovo export Deckbox (tool "Mythic"), niente più posizione/box (vedi
CLAUDE.md §5) — colonna "Dove" sostituita da quantità libera. Dati puliti per questo mazzo:
**0% delle carte del mazzo manca dal nuovo export**, quindi le quantità sotto sono affidabili._

**Ramp (fix diretto al difetto "ramp 7 sotto target", serve +3 per arrivare a 10):**
| Carta | Libere | Perché |
|---|--:|---|
| Talisman of Indulgence | 2 | rocce on-color, fixa B/R |
| Wayfarer's Bauble | 2 | ramp+fix, sac synergy nulla ma pulito |
| Burnished Hart | 2 | ramp+fix E si sacrifica da solo → trigger Mayhem Devil/Purphoros/Impact Tremors gratis |
| Pentad Prism | 1 | ramp esplosivo T1-2 |
| Star Compass | 1 | ramp condizionale ma gratis |

Consiglio: **Talisman of Indulgence + Burnished Hart + Wayfarer's Bauble** (i 3 con più sinergia
reale, Burnished Hart in particolare regala un trigger morte extra) portano ramp 7→10 esatto sul
target del template.

**Altri upgrade liberi:**
| Carta | Libere | Perché |
|---|--:|---|
| Burst Lightning | 9 (di 12) | spot a 1 mana, kicker late |
| Swiftfoot Boots | 1 (di 7 possedute — 6 impegnate in altri mazzi) | protegge Orthion/Terror nel turno chiave |
| Tormod's Crypt | 2 | grave-hate gratis (meta dipendente) |
| Dualcaster Mage | 1 | ⚠️ **NON aggiungere**: con Twinflame+Heat Shimmer già in lista fa token infiniti, sfora il B3 |

⚠️ **Lightning Bolt non è più libera** (era il suggerimento precedente): le 2 copie possedute
sono ora impegnate in `vision_scarlet_witch` e `muddle`. Se le vuoi qui, va tolta da uno dei due.

⚠️ **Witty Roastmaster non è più libera** (l'unica copia è finita in `vision_scarlet_witch`) —
torna shopping, non upgrade gratuito.

## Contese reali — verifica 2026-07-31 su export + decks/pol/*.txt

Ogni carta già presente in `deadpool.txt` incrociata con la domanda degli **altri 9 mazzi
REALI** (sezione 3 CLAUDE.md) sulla stessa collezione. **11 carte** risultano con copie
possedute insufficienti a coprire tutti i mazzi reali che le vogliono contemporaneamente —
prima di questa verifica solo Damnation era documentata, le altre 10 sono nuove:

| Carta | Possedute | Richieste (da reali) | Contendenti |
|---|--:|--:|---|
| Badlands | 2 | 3 | edgar_markov, first_sliver |
| Black Market Connections | 4 | 5 | edgar_markov, yshtola, sam_frodo, vincent |
| Blood Crypt | 2 | 3 | edgar_markov, first_sliver |
| Bloodstained Mire | 3 | 4 | edgar_markov, first_sliver, vincent |
| Damnation | 1 | 2 | yshtola |
| Idol of Oblivion | 2 | 3 | edgar_markov, sam_frodo |
| Malakir Rebirth // Malakir Mire | 1 | 2 | vincent |
| Mana Confluence | 1 | 3 | edgar_markov, yshtola |
| Nykthos, Shrine to Nyx | 1 | 3 | toph, vincent |
| Raucous Theater | 1 | 2 | edgar_markov |
| **The One Ring** | 1 | 3 | toph, yshtola |

⚠️ **The One Ring è uno dei 3 GC dichiarati di deadpool** (vedi intestazione) ed è il conflitto
più grave: 3 mazzi reali lo vogliono, 1 sola copia posseduta. Non è un dettaglio, va deciso.

A rischio aggiuntivo se `vision_scarlet_witch` risulta effettivamente reale (non ancora
classificato in CLAUDE.md §3): **Ancient Tomb** (l'altro GC di deadpool, possedute=1, reali=1
già al limite) e **Impact Tremors** (possedute=2, reali=2 già al limite).

Nessuna decisione presa qui su chi tiene cosa — sono fotografie di conflitto, non priorità.

## Shopping fuori collezione (Cardmarket, ricontrollato 2026-07-31)
| € | Carta | Ruolo |
|--:|---|---|
| 2,42 | Goblin Bombardment | sac outlet gratuito per le copie (removal continuo) |
| ~1-2 | Witty Roastmaster | Impact Tremors n°2 — ora serve ricomprarla |
| 8,76 | Fable of the Mirror-Breaker | copia+filtraggio+ramp, tutto on-plan |
| 6,05 | Warleader's Call | Tremors+anthem |

## Aperture
- ~~`deadpool_b3opt.txt` bozza alternativa~~ — risolto 2026-07-31: era un ramo abbandonato
  (toccato una sola volta, mai aggiornato dopo la verifica iniziale carta-per-carta), superato
  dagli swap successivi già applicati su `deadpool.txt` (incluso Terminate). Rimosso dalla repo.
- Tagli da concordare con pol per ogni entrata (lezione sinergie: qui quasi tutto è motore).
