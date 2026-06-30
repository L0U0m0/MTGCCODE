# CLAUDE.md — Progetto consulenza mazzi Magic: The Gathering (Commander)

Contesto per qualunque istanza di Claude (chat o Claude Code) che lavora su questo
progetto. Aggiornato: 2026-06-30. **Le liste qui sotto sono fotografie: i mazzi
cambiano, verifica sempre sui txt aggiornati nella repo, non su questo file.**

---

## 1. Come lavorare con il giocatore (handle: JimmyDfOOL)

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
Lista ufficiale di 53 carte, aggiornata feb 2026. **Sono LEGALI**, contano solo per il bracket.
GC rilevanti già emersi: Mana Vault, Ancient Tomb, Gaea's Cradle, Seedborn Muse, Crop Rotation,
Rhystic Study, Bolas's Citadel, The One Ring, Force of Will, Fierce Guardianship, Smothering Tithe,
Vampiric Tutor, Imperial Seal, Demonic/Mystical/Enlightened/Worldly Tutor, Jeska's Will, Necropotence,
Aura Shards, Opposition Agent, Teferi's Protection, Biorhythm, Natural Order.
**NON sono GC**: Esper Sentinel, Grim Tutor, Sol Ring, Food Chain (rimossa ott 2025).

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

## 3. I mazzi (11) — stato all'ultimo audit (verifica sui txt!)

| # | Comandante | Colori | Archetipo | GC | Bracket | Stato |
|---|---|---|---|---|---|---|
| 1 | Deadpool, Trading Card | Rakdos BR | copie/burn | 2 | B3 | lista vecchia; mancano tutor |
| 2 | Glarb, Calamity's Augur | Sultai BUG | landfall/value | 3 | B3 | ✅ a posto |
| 3 | Toph, the First Metalbender | Naya RGW | lands | 3 | B3 | ✅ a posto |
| 4 | Vincent Valentine | mono-B | aristocrats/Yawgmoth | 3 | ~B4 | ✅ tirato |
| 5 | Y'shtola, Night's Blessed | Esper WUB | drain/mill | 4 | ⚠️ B4 | 4 GC: tagliarne 1 per B3 |
| 6 | The First Sliver | 5c WUBRG | cascade/sliver | 2 | B3 | ✅ a posto |
| 7 | Sonic the Hedgehog | Jeskai WUR | treasures | 3 | B3 | ⚠️ manabase (5 tapland) |
| 8 | Sam & Frodo | Abzan WBG | Food combo | 2 | B3-4 | ✅ il più forte (52% sim) |
| 9 | Shroofus Sproutsire | mono-G | Saproling aggro | 2 | B3 | ✅ finalizzato |
| 10 | The Mimeoplasm | Sultai BUG | infect one-shot | ~1 | B3-4 | ⚠️ pacchetto infect da chiudere |
| 11 | Obeka, Splitter of Seconds | Grixis UBR | upkeep voltron | 3 | B3 | ✅ finalizzato (`obeka_decklist.txt`) |

### Combo chiave per mazzo
- **Deadpool**: Nim Deathmantle + Ashnod's Altar + Orcish Bowmasters (danno infinito); Orthion + Terror of the Peaks.
- **Glarb**: Hullbreaker Horror + rocks + Lotus Petal (mana infinito); Valley Floodcaller + Knack.
- **Toph**: Springheart Nantuko hub (token/landfall infiniti); Toph + Bumi + Liquimetal (kill); Toph + Stasis Coffin (protezione).
- **Vincent**: Exquisite Blood + Enduring Tenacity (drain infinito); motori Yawgmoth/Grave Pact.
- **Y'shtola**: Bloodchief Ascension + Mindcrank (infinito). Triangolo Papalymo→Emet-Selch→Hope Estheim.
- **First Sliver**: Sliver Queen + Intruder Alarm + 2 mana-Sliver (token infiniti).
- **Sonic**: Reaver Cleaver + Aggravated Assault; Faerie Mastermind + Smothering Tithe + Goldspan; Sonic + Krark-Clan Shaman + Flawless/Unbreakable. Payoff: Mechanized Production (8 Treasure = win).
- **Sam & Frodo**: 20 combo, hub Peregrin Took / Warren Soultrader / Academy Manufactor / Cauldron Familiar.
- **Mimeoplasm**: copia Blighted Agent (imbloccabile infect) + contatori = forza di Lord of Extinction → one-shot da veleno.
- **Obeka**: Exquisite Blood + Sanguine Bond; Mechanized Production sui Treasure; voltron (Eldrazi Conscription/Super State).

---

## 4. Lavori in sospeso (priorità ROI)

1. **Sonic** — fix manabase. FUORI: Evolving Wilds, Mystic Monastery, Perilous Landscape, Raugrin Triome,
   Terramorphic Expanse. DENTRO: Seachrome Coast (✓ ho), Spirebluff Canal (★ compra), Inspiring Vantage (★),
   Ponder/Brainstorm/Opt (✓), Storm-Kiln Artist (✓).
2. **Y'shtola** — 4 GC → se vuoi B3 taglia Vampiric Tutor (il meno sinergico). +2 terre (era a ~33).
3. **Mimeoplasm** — chiudi il pacchetto infect: Lord of Extinction (✓), Worldly Tutor (✓), Vile Entomber (✓),
   Birds of Paradise (✓), Llanowar Elves (✓), Whispersilk Cloak (✓), Contagion Clasp (✓), Evolution Sage (✓).
4. **Deadpool** — serve la lista AGGIORNATA prima dei tagli puntuali; aggiunte sicure: Dualcaster Mage (✓),
   Faithless Looting (✓); tutor da comprare (★).

Mazzi che NON vanno toccati: Glarb, Toph, Vincent, First Sliver, Sam & Frodo (già a template/bracket).

---

## 5. Collezione

- File: `collection_export_1781254993.csv` (3041 copie). Colonne: Card Name, Quantity, Set Code,
  Container Name, Rarity. `Container Name` indica box o mazzo.
- **Attenzione**: non tutti i mazzi montati sono nel CSV; alcune carte sono singoli condivisi tra mazzi
  (es. Mechanized Production sta in Sonic; metterla in Obeka significa spostarla o comprarne una seconda).
- In Commander le quantità ×N servono a rifornire PIÙ mazzi, non a giocare copie multiple.

---

## 6. Simulazione (`edh_pod11.py`)

Modello astratto: goldfish "motore/combo online" + layer interazione/wrath/protezione, pod casuali 4p,
10.000 partite, con mulligan. **NON** simula politica, odio da cimitero, né interazione carta-per-carta:
usalo come bussola relativa (chi è sopra/sotto), non come verità assoluta.

Ultimo risultato (winrate | mulligan), media chiusura T7:
Sam&Frodo 52% · Glarb 40% · Mimeoplasm 32% · Sonic 23% · Y'shtola 23% · Toph 23% ·
Obeka 20% (mull 18%) · First Sliver 18% · Vincent 16% · Shroofus 15% · Deadpool 11%.

---

## 7. Workflow consigliato per la repo

- Una lista per file, nominata col comandante: `sonic.txt`, `vincent.txt`, ...
- Formato: `1 Nome Carta` per riga (set code tra parentesi opzionale), **terre base incluse**, niente categorie.
- Export Archidekt/Moxfield vanno bene così come sono.
- Quando un mazzo cambia in modo sostanziale, **riaggiorna il txt**: questo file e i txt sono fotografie,
  non collegamenti vivi.
- Fonti dati carte: Scryfall, EDHREC, Commander Spellbook (combo), Moxfield, MTGGoldfish.
