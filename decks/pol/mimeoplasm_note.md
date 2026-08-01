# The Mimeoplasm — stato e ottimizzazione

_2026-07-02 · Sultai · **B2 (GC 0)** — era B3 basso con 1 GC (Crop Rotation), tagliato 2026-07-31
in favore di Toxic Deluge (il wrath premium mancante, vedi sotto) · lettura DA VALIDARE_

## Strategia (come la leggo)
Graveyard-copy con wincon **infect via voltron sul comandante**: riempi il cimitero (Buried
Alive, Grisly Salvage, Mulch, Winternight Stories, Jarad's Orders), poi Mimeoplasm entra come
copia del bestione migliore (Ghoultree, Doomgape, Jokulmorder, Titanoth, Yargle&Multani) coi
counter dell'infect creature esiliata — o direttamente come Skithiryx pompato. 11 creature
infect + proliferate (Thrummingbird, Tezzeret's Gambit, Experimental Augury, Vat Emergence)
chiudono a veleno. **Aggiornamento 2026-07-31**: pacchetto protezione+controllo per portare a
segno il colpo — Lightning Greaves (shroud+haste, sinergico coi rientri di Mimeoplasm) e
Whispersilk Cloak (unblockable+shroud, garantisce il danno) tengono in vita il comandante-copia;
Counterspell+Arcane Denial proteggono il turno del colpo. Ruling chiave (CLAUDE.md): le CDA
valgono anche da cimitero/esilio.

## Stato: 8/10 — voltron/protezione aggiunto, identità più chiusa
- Numeri (circa, da confermare con build_profiles.py dopo l'aggiornamento): terre 38 (era 36,
  +Command Tower +Exotic Orchard) · ramp 13 (+Sol Ring +Arcane Signet) · draw ~12 (-3 pezzi
  deboli) · wrath 2 · spot ~7 · **protezione 2 (nuovo)** · **counterspell 2 (nuovo)**
- Difetti: il piano B (infect beatdown senza Mimeoplasm grosso) è lento; self-mill buono ma
  non ottimo; manabase ancora senza true dual/fetch Sultai (vedi Aperture — nessuna libera in
  collezione, solo shopping).

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
| Culling Ritual | 2 | il wrath che manca ancora per arrivare a 3 (asimmetrico a curva bassa) |
| **Golgari Grave-Troll** | 1 | era in shopping, in realtà è **già posseduta e libera** — dredge 6 + bestione da copiare, zero spesa |

**Fatto 2026-07-31 (round 1, bracket)**: -Crop Rotation +**Toxic Deluge** — Crop Rotation era
l'unico GC del mazzo, tagliato per portarlo da B3 basso a **B2 pulito**. Wrath 1→2.

**Fatto 2026-07-31 (round 2, voltron/protezione)**: 8 swap, tutti da collezione libera, nessuna
nuova contesa con mazzi reali (verificato):
- -Death's Shadow +**Arcane Signet** (Death's Shadow è -X/-X con X=vita totale, quasi sempre
  morto a 40 vite di partenza in Commander; contrastava anche col lifegain di Fangkeeper's Familiar)
- -Myr Convert +**Sol Ring** (rocca ridondante una volta dentro ramp vero)
- -Tolarian Winds +**Whispersilk Cloak**
- -Heritage Reclamation +**Command Tower**
- -Aspirant's Ascent +**Exotic Orchard**
- -Frantic Search +**Arcane Denial**
- -Grapple with the Past +**Counterspell**
- -Windfall +**Lightning Greaves**

⚠️ **Vile Entomber e Fierce Empath (tutor non-GC, liberi) restano fuori**: non ho trovato un
secondo taglio pulito senza intaccare carte già ben sinergiche col piano proliferate/veleno
(controllate una per una: Prologue to Phyresis, Experimental Augury, Tainted Observer,
Fangkeeper's Familiar, Cankerbloom, Kheru Goldkeeper, Vivisurgeon's Insight, Blackcleave Goblin,
Lotuslight Dancers, Greenseeker sono tutte on-plan). Se li vuoi dentro, serve una decisione tua
su cosa sacrificare.

## Shopping fuori collezione (Cardmarket, ricontrollato 2026-07-31)
| € | Carta | Ruolo |
|--:|---|---|
| ~4 | Triumph of the Hordes | finisher infect di massa (prezzo varia per stampa) |
| 1,60 | Stinkweed Imp | dredge 5 — self-mill ripetibile |
| 14,03 | Entomb | tutor-cimitero istantaneo (copia posseduta in Vincent) — lusso |
| — | **True dual/fetch Sultai** | richiesti per la manabase ma **nessuna libera**: Underground Sea/Tropical Island/Bayou a 0 possedute o già impegnate (Bayou libere=0), stesso per Polluted Delta/Verdant Catacombs/Misty Rainforest — prezzi da controllare se si vuole comprare |

## Aperture
- Validare la lettura infect-first vs copy-first (cambia le priorità di upgrade).
- Con Culling Ritual + Golgari Grave-Troll dentro, il wrath salirebbe da 2 a 3 e il self-mill
  si rinforzerebbe parecchio.
- Vile Entomber/Fierce Empath: decidere cosa tagliare per farli entrare (vedi sopra).
- True dual/fetch Sultai: valutare acquisto, o spostare una copia da un mazzo reale meno
  bisognoso (nessuno controllato finora — richiede audit).
- **Numeri da riconfermare**: rilanciare `build_profiles.py` + `sim_pods.py` dopo questo giro
  di modifiche — quelli sopra sono stime a occhio, non calcolati.
- Bracket B2 confermato solo su GC=0: non ho riverificato che il resto del mazzo rispetti
  anche gli altri paletti B1/B2 ufficiali (nessun 2-card combo, nessun extra turno, nessuna
  mass land denial) — verifica veloce ma da fare prima di dichiararlo B2 a pol/gruppo.
