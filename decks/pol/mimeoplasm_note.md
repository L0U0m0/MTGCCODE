# The Mimeoplasm — stato e ottimizzazione

_2026-07-02 · Sultai · B3 basso (GC 1: Crop Rotation) · lettura DA VALIDARE_

## Strategia (come la leggo)
Graveyard-copy con wincon **infect**: riempi il cimitero (Buried Alive, Grisly Salvage, Mulch,
Winternight Stories, Windfall/Tolarian Winds, Jarad's Orders), poi Mimeoplasm entra come
copia del bestione migliore (Ghoultree, Doomgape, Jokulmorder, Titanoth, Yargle&Multani) coi
counter dell'infect creature esiliata — o direttamente come Skithiryx pompato. 11 creature
infect + proliferate (Thrummingbird, Tezzeret's Gambit, Experimental Augury, Vat Emergence)
chiudono a veleno. Ruling chiave (CLAUDE.md): le CDA valgono anche da cimitero/esilio.

## Stato: 7/10 — il più "fair" dei dieci, identità chiara
- Numeri: terre 36 · ramp 11 · draw 15 · wrath 1 · spot 8 (post +Trophy/Downfall)
- Difetti: wrath 1; il piano B (infect beatdown senza Mimeoplasm grosso) è lento;
  self-mill buono ma non ottimo.

## Upgrade dalla collezione (liberi) — AGGIORNATO 2026-07-31
_Fonte collezione: nuovo export Deckbox (tool "Mythic"), niente più box (vedi CLAUDE.md §5).
**0% delle carte del mazzo manca dal nuovo export**, dati puliti, tutti i suggerimenti sotto
sono riconfermati liberi:_

| Carta | Libere | Perché |
|---|--:|---|
| **Hedron Crab** | 2 | landfall self-mill — riempie il cimitero gratis |
| **Stitcher's Supplier** | 2 | idem on-body (mill 3+3) |
| **Life from the Loam** | 2 | recupera terre dal self-mill, motore di lungo |
| **Contagion Clasp** | 1 | proliferate ripetibile (veleno!) + spot piccolo |
| Altar of the Brood | 1 | mill avversari (sinergia trigger multipli) |
| Dread Summons | 2 | mill tutti + token |
| Culling Ritual | 2 | il wrath che manca (asimmetrico a curva bassa) |
| **Toxic Deluge** | **1** | ✅ ora davvero libera (nel giro precedente il conteggio era sballato da un file bozza duplicato) — è il wrath premium mancante, aggiungila |
| **Golgari Grave-Troll** | 1 | era in shopping, in realtà è **già posseduta e libera** — dredge 6 + bestione da copiare, zero spesa |

## Shopping fuori collezione (Cardmarket, ricontrollato 2026-07-31)
| € | Carta | Ruolo |
|--:|---|---|
| ~4 | Triumph of the Hordes | finisher infect di massa (prezzo varia per stampa) |
| 1,60 | Stinkweed Imp | dredge 5 — self-mill ripetibile |
| 14,03 | Entomb | tutor-cimitero istantaneo (copia posseduta in Vincent) — lusso |

## Aperture
- Validare la lettura infect-first vs copy-first (cambia le priorità di upgrade).
- Con Toxic Deluge + Culling Ritual + Golgari Grave-Troll dentro, il wrath sale da 1 a 2 e il
  self-mill si rinforza parecchio: vale un giro di verifica dei numeri (`build_profiles.py` +
  `sim_pods.py`) dopo l'aggiornamento fisico del txt.
