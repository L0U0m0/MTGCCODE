# The Vision and Scarlet Witch — mono-R spellslinger/storm ("Total eclipse of the heart")

Comandante: **The Vision and Scarlet Witch** `{2}{R}{R}` — Legendary Artifact Creature — Mutant
Hero, volare. *"Ogni volta che lanci una magia, aggiungi {R} e metti un +1/+1 su di lui."*

**2026-08-12: il txt ora riflette la build viva su Mythic Tools**
(`mythic.tools/user/6y3MWu/deck/6uf2yK`, "Total eclipse of the heart"), ottimizzata con la
collezione: la build Mythic era a 98 carte con 9 non montabili (6 mai possedute + 3 impegnate
in mazzi reali). La vecchia versione del txt (build teorica 2026-07-07/08, mai montata così)
è sostituita — storia nel git log.

## BRACKET: B4 DICHIARATO (deciso da pol 2026-08-12: Grinning Ignus resta)

**Decisione presa**: pol tiene Grinning Ignus → il loop col comandante resta e il mazzo **è
B4, dichiarato apertamente**. Nota: tagliare Birgi non sarebbe servito comunque (Ignus +
comandante è già infinito da solo); Birgi resta anche lei. Contesto storico sotto.

### Contesto (analisi 2026-08-12, pre-decisione)

La build Mythic reintroduce **Grinning Ignus E Birgi, God of Storytelling insieme**. Il
2026-07-07 pol aveva **rimosso Ignus di proposito** perché col comandante è un infinito a
1 carta (verificato allora su Commander Spellbook) — era ciò che rendeva il mazzo B4. Con
Birgi in più il loop è ancora più largo (Ignus si rilancia in mana-positivo → storm infinito
con qualsiasi payoff: Guttersnipe/Firebrand Archer/Witty Roastmaster = danno infinito).
GC attuali: **1 solo (Mana Vault)** — ma il conteggio GC non salva il bracket: come Vincent,
è **B4 di fatto per combo cheap**. Per tornare B3: fuori Grinning Ignus (o Birgi).
**Non deciso qui — va scelto da pol.**

## Swap applicati 2026-08-12 (build Mythic → montabile con la collezione)

Non possedute (6):
| Fuori | Dentro | Note |
|---|---|---|
| Ragavan, Nimble Pilferer | Conspiracy Theorist | downgrade secco, Ragavan non ha sostituto — in shopping |
| Jeska's Will (GC) | Wheel of Fortune | refill; Wheel NON è GC (lista ufficiale) |
| Aetherflux Reservoir | Electrodominance | finisher X + free cast |
| Ruby Medallion | Mana Vault (4 libere) | fast mana, unico GC della build |
| The Last Agni Kai | Chaos Warp (7 libere) | removal flessibile |
| Fogwell's Gym | Flamekin Village | terra utility (haste) |

Impegnate in mazzi reali (3):
| Fuori | Dentro | Contesa evitata |
|---|---|---|
| Ancient Tomb (GC) | Cryptic Caves | in deadpool |
| The Fire Crystal | Commander's Sphere (10 libere) | in deadpool |
| Impact Tremors | Defense Grid | in edgar_markov+deadpool; ridondante con Guttersnipe/Firebrand/Roastmaster |

Aggiunte per arrivare a 100 (la build Mythic era 98, "Not Legal"):
**Faithless Looting** (filtraggio) + **Blasphemous Act** (secondo sweeper, 9 libere).

Effetto collaterale positivo: la vecchia build txt impegnava The One Ring e Ancient Tomb via
proxy — la nuova non li usa, si alleggeriscono le contese segnalate in `deadpool_note.md`.

## Verifica montabilità (collezione export 2026-08-12)

**Tutte le 100 carte possedute e libere** dopo gli swap (Mountain: servono 25, possedute 111).
Nessuna contesa con i 10 mazzi reali.

## Shopping se vuoi la build Mythic com'era (Cardmarket, prezzi da confermare)
| Carta | Ruolo | Stima |
|---|---|---|
| Ragavan, Nimble Pilferer | aggressione T1 + treasure | ~40€ |
| Jeska's Will | ritual+impulse (GC — attenzione al conteggio) | ~8-10€ |
| Aetherflux Reservoir | wincon storm alternativa | ~3-4€ |
| Ruby Medallion | riduttore | ~5-6€ |
| The Last Agni Kai / Fogwell's Gym | fight+ramp / terra | ? |

## Piano di gioco

Invariato nell'idea: rocce+comandante presto, catena di magie a basso costo — ogni cast cresce
il comandante (+1/+1 e {R}) e pinga via Guttersnipe/Firebrand Archer/Witty Roastmaster, Torbran
amplifica. Refill con Wheel/Faithless Looting/Big Score. Chiusure: comandante gigante volante +
Embercleave, o turno storm → Grapeshot/Crackle with Power/Electrodominance. Con Ignus+Birgi in
lista la chiusura "fair" diventa opzionale: il loop è la linea più forte (ed è il problema
bracket di cui sopra).

## Aperti

1. ~~Ignus vs Birgi~~ — **risolto 2026-08-12: Ignus resta, B4 dichiarato** (vedi sezione Bracket).
2. Sim da rifare (`build_profiles.py` + `sim_pods.py`) sulla lista nuova.
3. Il mazzo su Mythic è a 98: allineare l'app alla lista qui (100) quando pol applica gli swap.
