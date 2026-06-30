# Pipeline simulazione pod multi-giocatore (Strada 1)

Deduce automaticamente un profilo di simulazione da ogni lista `decks/**/*.txt`
e fa girare due tornei. **Bussola RELATIVA**, non verità assoluta: il modello non
simula politica, odio da cimitero, né interazione carta-per-carta.

## Flusso

```
decks/**/*.txt
   │  fetch_scryfall.py   → scryfall_cache.json   (tipo/costo/testo carte, batch da 75)
   │  fetch_combos.py     → combo_cache.json      (combo reali via Commander Spellbook)
   ▼
build_profiles.py         → profiles.json         (euristiche → parametri per mazzo)
   ▼
sim_pods.py [n_partite]   → due simulazioni
```

Rilanciare dopo aver aggiunto/cambiato mazzi:
```
python fetch_scryfall.py      # incrementale (solo carte nuove)
python fetch_combos.py         # incrementale; rilancia 2-3 volte (rate-limit Spellbook)
python build_profiles.py
python sim_pods.py 20000
```

## Le due simulazioni

- **POD A — serata reale**: ogni partita siedono 4 giocatori a caso (degli 8 tag),
  un mazzo a testa pescato dal loro pool. Misura la forza **per giocatore**.
- **POD B — tutti contro tutti**: 4 mazzi a caso dall'intero pool, ignorando il
  proprietario. Misura la **potenzialità del singolo mazzo** (ranking assoluto).

## Come sono dedotti i parametri (euristiche)

| Campo | Segnale |
|---|---|
| `lands` | type_line contiene Land (+ terre base in formato `X // X`) |
| `ramp_n` | abilità di mana cmc≤4, fetch di terre, treasure |
| `engine_n` | permanenti con trigger ricorrente (`whenever`, `at the beginning of`, `{T}:` valore) |
| `wraths` / `spots` | board wipe vs rimozione/counter mirati (regex su oracle text) |
| `prot` | hexproof/indestructible/protection/ward sul proprio piano |
| `cn/cneed/cmana/cdelay` | **combo reali da Commander Spellbook** (find-my-combos) |
| `ctut` | tutor (`search your library for a card`, esclusi solo-terra) |
| `clock/grind/creature_engine/rebuild` | curva creature, card advantage, ricorsione |

**Anello debole onesto**: `engine_n`, `clock`, `grind` restano stime grezze.
Le combo invece sono dato reale (non euristica). Filtro: solo mazzi Commander
~100 carte (98–105); i 60/75c e le liste incomplete vengono scartati.
