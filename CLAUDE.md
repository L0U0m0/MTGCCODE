# CLAUDE.md — Progetto consulenza mazzi Magic: The Gathering (Commander)

Contesto per qualunque istanza di Claude (chat o Claude Code) che lavora su questo
progetto. Aggiornato: 2026-07-01 (censimento mazzi di **pol**, verificato carta per
carta via Scryfall sui file reali della repo). **Le liste qui sotto sono fotografie:
i mazzi cambiano, verifica sempre sui txt aggiornati nella repo, non su questo file.**

**Struttura repo: ora multi-giocatore.** I mazzi stanno in `decks/<giocatore>/`:
`casagrande/` (37), `rocchi/` (45), `tommaso/` (20), `pol/` (13), `saverio/` (10),
`montauti/` (7), `g_prete/` (5), `sbernuz/` (3). La sezione 3 sotto è il censimento
del solo **pol** (ex-tag `jimmy`). Gli altri folder NON sono ancora stati auditati.

**Pulizia 2026-07-01:** i vecchi mazzi "teorici" senza lista fisica (inalla, yuna,
norin, noctis, azlask, azula, teval, yshtola_staxgoad, first_sliver_slayer, zevlor
+ i 3 Pauper fury_burn/mono_g_pauper_infect/rakdoss_madness) sono stati **rimossi
dalla repo** su richiesta di pol: non corrispondevano a nulla di montato né di
verificabile. Se pol li rimonta, andranno ripassati carta per carta come gli altri.

---

## 1. Come lavorare con il giocatore (handle: JimmyDfOOL, ora taggato `pol`)

- **Lingua: italiano**, sempre, in ogni risposta.
- **Formato: conciso.**
- **Stile richiesto (vincolante):**
  1. Mai aprire con accordo o lusinghe; la prima frase sfida un'assunzione o espone una lacuna.
  2. Tag di confidenza: `(certo)` / `(probabile)` / `(ipotesi)`.
  3. Disaccordo strutturato; verità scomoda per prima.
  4. Niente preamboli; niente frasi-riempitivo ("ottima domanda", ecc.).
  5. Mantenere la posizione sotto pushback, salvo informazioni genuinamente nuove
     (quando ha ragione, concedere subito e correggersi).
- **Regola d'oro operativa:** verificare via web search **ogni carta non nota con
  certezza PRIMA di giudicarla**, specie i comandanti. Le note invecchiano: i mazzi
  evolvono. Controllare sempre la **lista reale**, mai la memoria.

---

## 2. Framework di deckbuilding

### Formato
Commander/EDH. Singleton (1 copia per carta tranne terre base). 100 carte incluso il comandante.

### Template Command Zone (default battlecruiser, da adattare per archetipo)
| Ruolo | Target |
|---|---|
| Terre | 38 |
| Ramp | 10 |
| Card advantage | 12 |
| Disruption mirata | 12 |
| Disruption di massa | 6 |
| Carte-piano | ~30 |

Le caselle si **sovrappongono** (una carta può coprire più ruoli), quindi la somma supera 100.
**Aggiustamenti per archetipo (il template NON è dogma):**
- **Combo** → meno disruption di massa, più tutor e protezione.
- **Aggro go-wide** → ~33-35 terre, pochissimi wrath (uccidono il tuo board), più minacce + finisher.
- **Voltron** → pochi wrath, molta protezione del comandante.

### Bracket (basato sui TURNI)
- **B3**: ≤ 3 Game Changer; combo da poche carte ammesse solo se non scattano "a buon mercato" prima di ~T6.
- **B4**: 4+ Game Changer (per conteggio), oppure win consistente entro ~T4-5.
- Il comandante-GC conta nei 3.

### Game Changers (GC)
Lista ufficiale **53 carte**, verificabile via Scryfall (`is:gamechanger`). **Sono LEGALI**,
contano solo per il bracket. Lista completa (ricontrollata 2026-07-01, non fidarsi di un
elenco a memoria: mancavano diversi nomi in una versione precedente di questo file):

Ad Nauseam, Ancient Tomb, Aura Shards, Biorhythm, Bolas's Citadel, Braids Cabal Minion,
Chrome Mox, Coalition Victory, Consecrated Sphinx, Crop Rotation, Cyclonic Rift, Demonic Tutor,
Drannith Magistrate, Enlightened Tutor, **Farewell**, Field of the Dead, Fierce Guardianship,
Force of Will, Gaea's Cradle, Gamble, Gifts Ungiven, Glacial Chasm, Grand Arbiter Augustin IV,
Grim Monolith, Humility, Imperial Seal, Intuition, Jeska's Will, Lion's Eye Diamond, Mana Vault,
Mishra's Workshop, Mox Diamond, Mystical Tutor, Narset Parter of Veils, Natural Order, Necropotence,
Notion Thief, Opposition Agent, Orcish Bowmasters, Panoptic Mirror, Rhystic Study, Seedborn Muse,
Serra's Sanctum, Smothering Tithe, Survival of the Fittest, Teferi's Protection, Tergrid God of
Fright, Thassa's Oracle, The One Ring, The Tabernacle at Pendrell Vale, Underworld Breach,
Vampiric Tutor, Worldly Tutor.

**NON sono GC**: Esper Sentinel, Grim Tutor, Sol Ring, Doubling Season, Mechanized Production,
Wheel of Fortune, Demonic Consultation, Food Chain, Toxic Deluge, Peerless Recycling.
Trappola: il GC è **Braids, Cabal Minion**, NON Braids, Arisen Nightmare (in Vincent, non conta).
**Farewell è GC** — attenzione, si tende a dimenticarlo perché "sembra solo un wrath".

### Banlist (ILLEGALI, non confondere con i GC)
Mana Crypt, Jeweled Lotus, Dockside Extortionist, Nadu. **Mana Vault NON è bandita** (è un GC legale).

### Rulings verificati
- Orcish Bowmasters ammassa anche all'ETB → combo Nim Deathmantle + Ashnod's Altar + Bowmasters = danno infinito.
- The Mimeoplasm: entra come copia di una creatura dal cimitero + contatori = forza di un'altra.
  Le caratteristiche definite (CDA, es. Lord of Extinction) valgono anche dall'esilio/cimitero.
- Obeka: upkeep extra = sua forza; saltano untap e pesca; abilità innescata COPIABILE.
- Frodo, Adventurous Hobbit: solo pescata, nessuna wincon (quella è su Frodo, Sauron's Bane).
- Delney raddoppia i trigger di creature forza ≤2; NON raddoppia i trigger di emblemi (Anello).

---

## 3. I mazzi di pol — censimento `decks/pol/` (2026-07-01, verifica sui txt!)

**10 mazzi REALI** (fisicamente montati, liste confermate da pol carta per carta contro la sua
collezione) + **4 mazzi TEORICI con lista** (non ancora montati, verificati solo per legalità).
Tutti 100 carte incluso il comandante, salvo dove segnalato. GC contati sulla lista ufficiale
53 carte (sezione 2), bracket e combo verificati su Scryfall.

### Reali

| File | Comandante | Colori | Archetipo | GC | Bracket | Nodo critico |
|---|---|---|---|---|---|---|
| `deadpool` | Deadpool, Trading Card | Rakdos | copie ETB + burn | 3 (da riverificare c/ lista 53) | B3 alto | completo, legale; combo sotto |
| `sam_frodo` | Frodo + Sam (partner) | Abzan | Food/drain combo | 2 (Smothering Tithe, Aura Shards) | B3 spinto | tutto passa da Warren Soultrader; poca rimozione |
| `shroofus` | Shroofus Sproutsire | mono-G | Saproling go-wide/token | 2 (Seedborn Muse, Gaea's Cradle) | B3 | rimozione mirata quasi assente (1 sola carta, Longstalk Brawl) |
| `toph` | Toph, the First Metalbender | Naya | lands/landfall | 3 (Crop Rotation, The One Ring, Field of the Dead) | B3 | 3 Toph extra nel main (legale, insolito); rimozione mirata sotto target |
| `vincent` | Vincent Valentine // Galian Beast | mono-B | aristocrats/drain | 3 (Vampiric Tutor, Imperial Seal, Necropotence) | **B4 di fatto** | ha ancora Exquisite Blood+Enduring Tenacity: combo cheap nonostante GC≤3 |
| `sonic` | Sonic the Hedgehog | Jeskai | treasure/haste-flash | 3 (Enlightened Tutor, Jeska's Will, Smothering Tithe) | B3 | manabase: duali originali sostituite con painland (vedi §4) |
| `first_sliver` | The First Sliver | 5c | sliver tribal fair | **0** | B2-B3 | combo storica (Intruder Alarm+Sliver Overlord) **rimossa** dal fisico: verificare se voluto |
| `yshtola` | Y'shtola, Night's Blessed | Esper | drain/control | 3 (The One Ring, Bolas's Citadel, Rhystic Study) | B3 | combo Bloodchief Ascension+Mindcrank confermata presente |
| `edgar_markov` | Edgar Markov | Mardu | Vampiri go-wide | 3 (Demonic Tutor, Necropotence, Farewell) | **B3** (era B4 nel vecchio audit — già sistemato!) | niente più fast mana né combo Exquisite Blood/Sanguine Bond/Vito |
| `mimeoplasm` | The Mimeoplasm | Sultai | graveyard/copia + **infect** | 1 (Crop Rotation) | B3 basso | wincon veleno via creature infect copiate/ingrandite dal cimitero |

### Teorici (lista ricevuta, non montati — NON auditati in profondità)

| File | Comandante | Colori | Nota |
|---|---|---|---|
| `ultron` | Ultron, Artificial Malevolence | incolore/artefatti | **101 carte**, da tagliare di 1 prima di montarlo. Shell Urza-lands/Eldrazi/Ugin |
| `obeka` | Obeka, Splitter of Seconds | Grixis | drain (Vito/Aclazotz/Exquisite Blood+Sanguine Bond) + pacchetto controspell gratuiti/economici + sottotema Gates/Maze's End |
| `ms_bumbleflower` | Ms. Bumbleflower | Bant | +1/+1 counters, stessa famiglia archetipica di Yuna (ora rimossa dalla repo, vedi nota pulizia) |
| `serpent_society` | The Serpent Society | Golgari | deathtouch-aristocrats/edict, **B3 alto** (GC: Tergrid+Worldly Tutor+Mana Vault). **Montabile al 100% da collezione sciolta** (costruito 2026-07-02). Il comandante è un Grave Pact in command zone; Ophiomancer+sac outlet = edict/turno; Tergrid ruba i sacrifici. Nota: Dina contesa con l'upgrade sam_frodo. Sim: 19.7% ma il modello non vede il testo del comandante (sottostimato); debolezza reale: prot~1, fragile ai wrath |
| `coulson` | Agent Phil Coulson | mono-W | **Hero tribal** (+1/+1 counter su ogni altro Hero), **B3** (GC: 1 solo, Smothering Tithe). Costruito 2026-07-03: 21/63 Hero mono-W già in collezione libera, 9 aggiunte a shopping economico (~75€ tot, dominato da Eiganjo 6,58€ — scartato apposta Cavern of Souls 39€, inutile in mono-colore). Contese: Adaptive Automaton e Coat of Arms possedute ma già impegnate altrove, da ricomprare. Nodo: Coulson attiva 1 counter/turno da solo, serve Metallic Mimic/Doctor Spectrum/Falcon Sam Wilson/Cap. Steve Rogers come motore secondario. **Variante `coulson_premium.txt`** (2026-07-04, proxy ammessi): 12 swap, GC=3 esatti (+Teferi's Protection +The One Ring), Cathars' Crusade/Ozolith/Elesh Norn come motori counter — vedi `coulson_note.md` |

**Nota Sonic — manabase:** il vecchio audit raccomandava di tagliare le tapland per le duali
originali (Tundra/Plateau/Volcanic Island). **È successo il contrario**: pol ha sostituito le
duali originali con **painland** (Adarkar Wastes/Shivan Reef/Battlefield Forge). Le painland non
hanno i tipi di terra base, quindi Evolving Wilds/Terramorphic Expanse (presenti nel mazzo) non
possono più fetcharle — downgrade di manabase, probabilmente per motivi di collezione/valore.

### Combo chiave per mazzo (verificate sui txt reali)
- **Deadpool**: Orthion+Terror of the Peaks e Nim Deathmantle+Ashnod's Altar+Bowmasters **confermate in lista**.
  Sundial of the Infinite rende permanenti le copie temporanee (termina il turno prima del trigger).
  **Il comandante è uno spot-removal no-target** (ruling verificato): lo scambio textbox è "as enters",
  non fa target né usa la pila → bypassa shroud/hexproof/ward; lo scambio PERSISTE se Deadpool lascia
  il campo (la creatura avversaria resta neutralizzata col "perdi 3 vite/upkeep" addosso), e Deadpool
  rientrato è un oggetto nuovo → nuovo scambio. Blink/reanimation = removal ricaricabile.
- **Sam & Frodo**: Warren Soultrader + Cauldron Familiar + (Academy Manufactor / Peregrin Took) drain infinito, **confermato presente**; manca ancora Pitiless Plunderer per il loop con Ashnod's Altar.
  Direzione upgrade voluta da pol: convertitori "lifegain→drain". Liberi in collezione: Sanguine Bond
  (nel maybeboard fisico!), Marauding Blight-Priest x3, Dina Soul Steeper (2° sac outlet), South Wind
  Avatar, Gyome/Well of Lost Dreams/Dawn of Hope. ⚠️ Exquisite Blood è sciolta nei box: +Sanguine Bond
  = infinito a 2 carte → sforerebbe il B3. Tagli da decidere con pol (candidati non valutabili senza
  di lui: Mutagen Man, Blossoming Bogbeast, Queen Allenal, Quina).
- **Shroofus**: nessun infinito; motore go-wide Shroofus+doubler+anthem, Gaea's Cradle come accelerante.
- **Toph**: Springheart Nantuko + (Lotus Cobra / Tireless Provisioner) landfall infinito, **confermato presente**; Toph+Bumi+Liquimetal Coating.
- **Vincent**: Exquisite Blood + Enduring Tenacity (drain infinito), **confermato presente** — motivo per cui resta B4 di fatto pur avendo solo 3 GC.
- **Sonic**: The Reaver Cleaver + Aggravated Assault (combat/treasure infiniti), **confermato presente**; Mechanized Production su Treasure.
- **First Sliver**: la vecchia combo Intruder Alarm+Sliver Queen+Sliver Overlord **NON è più nel mazzo fisico** — sostituita con più Sliver "fair" (Blur/Crypt/Hibernation/Horned/Regal/Sentinel/Taunting) + Food Chain (non-GC). Chiedere a pol se è una scelta voluta di derating verso B2-B3.
- **Y'shtola**: Bloodchief Ascension + Mindcrank (infinito), **confermato presente**; triangolo Papalymo→Emet-Selch→Hope Estheim. Delney raddoppia il suo trigger (forza 2).
- **Edgar Markov**: **nessuna combo** nel fisico (Exquisite Blood/Sanguine Bond/Vito assenti) — il mazzo è stato derated volontariamente da B4 a B3.
- **Mimeoplasm**: nessun infinito; wincon via infect (11 creature infect in lista) copiate/ingrandite da Mimeoplasm. Lord of Extinction NON presente, quindi la ruling CDA-dal-cimitero (sezione 2) non si applica a questa build specifica.

---

## 4. Lavori in sospeso pol (priorità ROI)

1. **First Sliver — combo rimossa**: verificare con pol se è voluto. Se vuole tornare a B3-alto/B4
   con l'infinito, reinserire Intruder Alarm + Sliver Overlord (tagliati insieme a Fierce
   Guardianship/Teferi's Protection, che erano GC).
2. **Sonic — manabase**: valutare se tornare alle duali originali (Tundra/Plateau/Volcanic Island)
   per riabilitare i fetch (Evolving Wilds/Terramorphic Expanse), a scapito di rivendere le painland.
3. **Vincent — bracket**: dichiarare B4 di fatto nonostante 3 GC, per via della combo Exquisite
   Blood+Enduring Tenacity tutorabile presto. Per portarlo a B3 vero: tagliare la combo.
4. **Interazione mirata scarsa** (pattern ricorrente): Shroofus (1 sola rimozione mirata in tutto
   il mazzo), Toph, Sam & Frodo → +rimozione in-color (Swords/Path/Beast Within/Generous Gift).
5. **Shroofus — completamento**: The Great Henge è in maybeboard invece che in main (ROI alto,
   va dentro); Firdoch Core/Phyrexian Altar/Wolfwillow Haven in maybeboard sono filler deboli per
   l'archetipo, meglio lasciarli fuori.
6. **Ultron**: ora 100 carte (tagliato Idol of Oblivion). Per montarlo: 79 nomi mancanti ≈ 581€
   (≈318€ condividendo 11 carte già in altri mazzi) — dettaglio in `decks/pol/ultron_mancanti.md`.
7. **Analisi approfondita strategica in corso** (2026-07-02, pol valida le letture una per una):
   fatta Deadpool (lettura confermata + correzione sul comandante-removal) e Sam & Frodo (confermata,
   upgrade lifegain→drain individuati, tagli in sospeso). Prossimi: shroofus, toph, vincent, sonic,
   first_sliver, yshtola, edgar_markov, mimeoplasm.
8. **Modifiche fisiche pendenti**: vedi `decks/pol/MODIFICHE_FISICHE.md` (10 swap da applicare).
9. **File di ottimizzazione per mazzo** (2026-07-02): ogni mazzo reale ha il suo
   `decks/pol/<mazzo>_note.md` con stato, difetti, upgrade dalla collezione libera (con
   posizione box) e shopping fuori collezione (prezzi Cardmarket). Strategie validate con
   pol solo per Deadpool e Sam&Frodo; le altre 8 letture sono da validare una per una.
   Contese di copie singole segnate nei file (Dina, Sanguine Bond, Lightning Bolt, ecc.).

**Buona notizia:** Edgar Markov era segnalato B4 nel vecchio audit — il mazzo fisico di pol lo ha
**già derated a B3** (via GC=3, niente fast mana, niente combo). Lavoro già fatto, nessuna azione.

---

## 5. Collezione

- **Cambio fonte dati (2026-07-31): da Moxfield a Deckbox-format via tool "Mythic".** pol ha
  cambiato app di tracking collezione. File attuale: `decks/pol/collection_2026-07-31.csv`
  (6.762 righe). Sostituisce l'export Moxfield del 2026-07-02 (rimosso — **quando arriva un
  nuovo export, sostituire non affiancare**, come sempre).
- **Colonne (formato Deckbox, DIVERSO da Moxfield)**: Count, Tradelist Count, Name, Edition,
  Condition, Language, Foil, Tags, Last Modified, Collector Number, Alter, Proxy, Purchase
  Price. **Non ha più `Scryfall ID` né `Container Type`/`Container Name`.**
- **Risoluzione nomi (metodo cambiato)**: senza Scryfall ID, le carte non-inglesi si risolvono
  via `set code + collector number` sull'endpoint `/cards/collection` (identifiers
  `{"set":..., "collector_number":...}`), non più per nome. Script: `import_collection_deckbox.py`
  (root repo) → produce `decks/pol/collection_normalized_<data>.json` ({nome canonico: quantità
  totale}). Cache di risoluzione in `decks/pol/collection_resolve_cache.json`.
- **Niente più `Container Type`**: non si distingue più box/bulk da mazzo/maybeboard nell'export.
  Non è una perdita grave — Moxfield non era comunque affidabile per questo (vedi sotto) — ma
  "dove si trova fisicamente la carta" (box specifico) non è più deducibile dai dati, solo
  "posseduta sì/no e quanto". I riferimenti a box nei vecchi `*_note.md` (Avatarcommander,
  Spiderman, ProXy, Foundation, bulk...) restano validi come storico ma non più verificabili.
- ⚠️ **Anomalia riscontrata 2026-07-31, da confermare con pol/app**: la % di carte-mazzo "non
  trovate" nel nuovo export varia moltissimo tra mazzi — 0% su deadpool/mimeoplasm/shroofus,
  ma 20-53% su sam_frodo/toph/vincent/sonic/edgar_markov/yshtola/first_sliver, **incluso il
  comandante stesso su yshtola** (Y'shtola, Night's Blessed risulta 0 posseduta) e staple come
  Rhystic Study/Sheoldred/Bolas's Citadel. Non è verosimile che siano state vendute. **Ipotesi
  più probabile**: l'app "Mythic" esclude dall'export le carte già assegnate a un mazzo
  registrato al suo interno, quindi l'export cattura solo il binder libero per i mazzi "pieni"
  che pol ha anche costruito nell'app, mentre i mazzi con meno carte doppione/registrate
  risultano completi per caso. **Non trattare "0 possedute" su carte-cardine come dato reale**
  senza verifica — vedi i note file dei mazzi coinvolti per il dettaglio.
- Fonte di verità sul contenuto dei mazzi restano sempre e solo i txt in `decks/pol/*.txt`
  (mai il conteggio di un tracker esterno, Moxfield o Deckbox che sia).
- In Commander le quantità ×N servono a rifornire PIÙ mazzi, non a giocare copie multiple
  (eccetto Pauper, dove ×4 è normale).
- **Migrazione in corso verso Supabase** (decisa da pol 2026-07-31): collezione + mazzi + note +
  profili di simulazione si spostano da file sparsi a un database Postgres unico. Schema e
  script in `supabase/` (vedi `supabase/README.md` per i passi di setup — richiede un progetto
  Supabase e le sue credenziali, non ancora fornite). Finché la migrazione non è completata e
  verificata, i file in `decks/` restano la fonte di verità operativa.

---

## 6. Simulazione (`edh_pod11.py`)

Modello astratto: goldfish "motore/combo online" + layer interazione/wrath/protezione, pod casuali 4p,
10.000 partite, con mulligan. **NON** simula politica, odio da cimitero, né interazione carta-per-carta:
usalo come bussola relativa (chi è sopra/sotto), non come verità assoluta.

Ultimo risultato (winrate | mulligan), media chiusura T7 — **DATI VECCHI, roster pre-pulizia
2026-07-01**: include Glarb (ora in `casagrande/`, non più in pol). Mimeoplasm e Shroofus sono
rientrati come mazzi **reali**, Obeka come **teorico**; da rigenerare sui 10 mazzi reali attuali:
Sam&Frodo 52% · Glarb 40% · Mimeoplasm 32% · Sonic 23% · Y'shtola 23% · Toph 23% ·
Obeka 20% (mull 18%) · First Sliver 18% · Vincent 16% · Shroofus 15% · Deadpool 11%.

---

## 7. Workflow consigliato per la repo

- Una lista per file, nominata col comandante, dentro il folder del giocatore: `decks/pol/sonic.txt`, ...
- Formato: `1 Nome Carta` per riga (set code tra parentesi opzionale), **terre base incluse**, niente categorie.
- **Tracker modifiche fisiche**: ogni swap deciso in chat sui mazzi REALI di pol va registrato in
  `decks/pol/MODIFICHE_FISICHE.md` (FUORI/DENTRO + dove trovare la carta in collezione) — i txt
  cambiano subito, le deckbox no; il tracker è il ponte finché pol non applica fisicamente.
- Export Archidekt/Moxfield vanno bene così come sono.
- Quando un mazzo cambia in modo sostanziale, **riaggiorna il txt**: questo file e i txt sono fotografie,
  non collegamenti vivi.
- Fonti dati carte: Scryfall, EDHREC, Commander Spellbook (combo), Moxfield, MTGGoldfish.

---

## 8. Consulente Telegram (dal 2026-07-03)

Questa repo alimenta anche il **consulente `/consulente` del bot BolasScryer** (EC2, solo
admin, Claude Agent SDK con abbonamento Max): il server ha un clone in
`/opt/pricebot/consulenza` aggiornato da un timer ogni 6 ore, e l'agente legge questo
CLAUDE.md, le liste `decks/pol/*.txt` e le note `*_note.md` come contesto.

**Divisione delle responsabilità (decisa da pol):**
- **Questa repo (Consulenza-Mazzi)** = il "cervello" del consulente: contesto, regole,
  liste, note, profili di simulazione. Le modifiche al comportamento consulenziale
  (cosa sa, come giudica i mazzi) si fanno QUI.
- **Repo BolasScryer-PriceBot** = comandi e funzionalità del bot: handler Telegram,
  system prompt dell'agente (`consulente.py`), tool MCP (`scryfall_mcp.py`,
  `torneo.py`), deploy. Le modifiche a comandi/tool si fanno LÀ.

**Conseguenze operative:**
1. **Il commit qui non basta per il bot: serve il PUSH su origin (MTGCCODE)** —
   il clone su EC2 si aggiorna dal remoto (timer 00/06/12/18:15, o a mano con
   `git -C /opt/pricebot/consulenza pull`). Ai checkpoint orari: commit+push.
2. `profiles.json` committato = i dati che usa `/torneo` e il tool `simula_torneo`
   sul server: rigenerarlo (build_profiles.py) quando le liste cambiano.
3. Tutto ciò che si scrive in questo file e nelle note è **anche prompt-context del
   consulente Telegram**: mantenerlo fattuale e aggiornato.
