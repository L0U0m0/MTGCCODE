# Shroofus Sproutsire — stato e ottimizzazione

_2026-07-02 · mono-G · B3 (GC 2: Seedborn Muse, Gaea's Cradle) · lettura DA VALIDARE con pol_
_Aggiornato 2026-07-31: giro "chiudi il buco delle rimozioni" — vedi Fatto sotto._

## Strategia (come la leggo)
Saproling go-wide con trigger moltiplicatore: ogni danno da combattimento di un Saprolingo
= altrettanti token. **I combat trick sono moltiplicatori di token, non filler** (Echoing
Courage su 5 Saprolingi non bloccati = +10 token). Doubler (Doubling Season, Parallel Lives,
Second Harvest) + anthem (Coat of Arms, Beastmaster Ascension, Eldrazi Monument) + Maskwood
Nexus (tutto è Saprolingo) + Finale of Devastation come tutor/finisher. Gaea's Cradle esplode.

## Stato: 8/10 — risposte vere aggiunte
- Numeri: terre 36 · ramp 11 · draw 12 · wrath 0 (scelta go-wide corretta) · **spot 5** (era 2,
  il peggiore dei 10 — Longstalk Brawl + Beast Within + Voracious Hydra + Bite Down + Tenderize)
- Difetti residui: niente grave-hate; manabase ancora da controllare per true dual/fetch (non
  fatto in questo giro).

## Fatto 2026-07-31 — chiusura buco rimozioni + The Great Henge
4 swap, tutti da collezione libera (verificato su export 2026-07-31), nessuna nuova contesa
con mazzi reali. Le due rimozioni esistenti (Longstalk Brawl, Beast Within) potevano già
colpire creature; il buco vero era **quantità**, non tipo — quindi ho aggiunto rimozione
efficiente a una faccia (il tuo corpo non rischia nulla nel fight), non condizionale:
- -Peerless Recycling +**Voracious Hydra** (fight + corpo grosso che raddoppia i counter)
- -Banner of Kinship +**Bite Down** (fight one-sided, {2}, istantaneo)
- -Konda's Banner +**Tenderize** (fight one-sided, {2}, istantaneo)
- -Elvish Farmer +**The Great Henge** (priorità già segnalata in CLAUDE.md §4 — "va in main")

Banner of Kinship/Konda's Banner erano il 3°/4° effetto anthem sovrapposto (con Coat of Arms +
Patchwork Banner già in lista) — tagliati per ridondanza, non per debolezza intrinseca.
Elvish Farmer era il generatore di token più lento del mazzo (1 Saproling ogni 3 turni).

⚠️ Great Henge: costa {7}{G}{G} ridotto dalla forza del corpo più grande — Mycoloth/Vigor/
Tendershoot Dryad danno abbastanza corpi grossi da renderlo giocabile presto, ma non
ricalcolato con precisione. Verificare in prova.

## Fatto 2026-07-31 (round 2) — Roaming Throne
-Overwhelming Instinct +**Roaming Throne** (ward 2, sceglie Saproling: raddoppia i trigger
delle abilità innescate di ogni altro Saprolingo — si somma ai doubler di token già in lista).
⚠️ **NON posseduta libera** (2 copie possedute, entrambe già impegnate su `toph.txt` e
`yshtola.txt`) — **serve comprare una terza copia, ~37,97€ Cardmarket** (nettamente più cara
delle altre voci shopping di questo mazzo). Il txt è già aggiornato ma non giocabile finché
non arriva la copia fisica.

## Upgrade dalla collezione (liberi, ancora da valutare)
| Carta | Libere | Perché |
|---|--:|---|
| Pest Infestation | 2 | X removal artefatti/incantesimi + genera token — non creature-removal, lasciata fuori da questo giro |
| Steelbane Hydra | 2 | removal artefatti/incantesimi ripetibile — idem |
| Scavenging Ooze | 1 | grave-hate on-body |
| Saproling Migration | 1 | altri token tribali |
| Awaken the Woods | 1 | X terre-creature (Cradle!) |
| Snakeskin Veil | 5 | protezione a 1 mana |

## Shopping fuori collezione (Cardmarket)
| € | Carta | Ruolo |
|--:|---|---|
| 0,98 | Kenrith's Transformation | neutralizza qualsiasi comandante + cantrip |
| 0,52 | Krosan Grip | artefatti/incantesimi split second |
| 5,17 | Song of the Dryads | removal universale mono-G |
| 0,81 | Esika's Chariot | token + copia token |
| 14,10 | Heroic Intervention | anti-wrath (il mazzo muore ai wrath) — lusso |

## Aperture
- Validare la lettura strategica.
- Grave-hate ancora assente (Scavenging Ooze libera, non ancora inserita).
- Manabase: non controllata per true dual/fetch in questo giro (vedi precedente su mimeoplasm
  per il metodo — probabile esito simile: poche/nessuna libera).
- **Numeri da riconfermare**: rilanciare `build_profiles.py` + `sim_pods.py` dopo questo giro.
