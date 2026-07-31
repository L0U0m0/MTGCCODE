# Migrazione collezione/mazzi su Supabase

Sposta collezione, liste mazzi, note e dati di simulazione da file sparsi
(`decks/**/*.txt`, `*_note.md`, `collection_*.json`, `profiles.json`,
`scryfall_cache.json`, `combo_cache.json`) a un database Postgres unico.

## 1. Crea il progetto (una volta sola)

1. Vai su [supabase.com](https://supabase.com) → **New project**.
2. Nome libero (es. `mtg-consulenza-mazzi`), regione vicina (es. `eu-central-1`),
   password del DB a scelta (non serve per questa pipeline, usiamo l'API REST).
3. Aspetta il provisioning (~2 minuti).

## 2. Applica lo schema

1. Nel progetto: **SQL Editor** → **New query**.
2. Incolla tutto il contenuto di [`schema.sql`](./schema.sql) → **Run**.
3. Verifica in **Table Editor** che siano comparse le tabelle: `players`,
   `decks`, `deck_cards`, `deck_notes`, `collection`, `card_cache`,
   `deck_combo_cache`, `sim_profiles`, `sim_results`.

## 3. Prendi le credenziali

**Project Settings → API**:
- **Project URL** (es. `https://xxxxxxxx.supabase.co`)
- **service_role key** (sezione "Project API keys" — NON la `anon` key: questa
  pipeline scrive dati e deve bypassare la Row Level Security. La service_role
  key va tenuta segreta, non finisce mai su git — è già in `.gitignore`).

## 4. Configura le credenziali in locale

Crea `supabase_credentials.json` nella **root della repo** (`/Users/dfool/Developer/MTGCCODe/`):

```json
{
  "url": "https://xxxxxxxx.supabase.co",
  "service_role_key": "eyJ..."
}
```

Questo file è in `.gitignore`: non viene mai committato né pushato.

## 5. Installa la dipendenza ed esegui la migrazione

```bash
pip install requests
python3 supabase/migrate_all.py
```

Lo script è idempotente: si può rilanciare dopo ogni modifica ai file (nuovo
export collezione, mazzo aggiornato, nuova nota) — cancella e re-inserisce le
righe derivate dai file sorgente senza duplicare nulla.

## Cosa NON è (ancora) migrato

- `edh_pod11.py` / `sim_pods.py` continuano a girare da file locali
  (`profiles.json`) — leggerli da Supabase invece che dal JSON è un secondo
  passo, non incluso qui.
- Il bot Telegram (`bolasscryer-pricebot`) continua a leggere il CLAUDE.md e i
  txt dal clone su EC2: puntarlo a Supabase invece che ai file è fuori da
  questa migrazione (tocca `consulente.py` nell'altra repo, vedi CLAUDE.md §8).
- `MODIFICHE_FISICHE.md` e i file `ordine_proxy*`/`proxy_shopping.md` entrano
  come `deck_notes` a livello giocatore (`deck_id` null) perché non sono legati
  a un mazzo singolo.

## Query utili una volta migrato

Carte libere di pol (possedute meno quelle già in un mazzo qualsiasi):

```sql
select c.card_name, c.quantity - coalesce(used.qty, 0) as libere
from collection c
left join (
  select dc.card_name, sum(dc.quantity) as qty
  from deck_cards dc
  join decks d on d.id = dc.deck_id
  where d.player_id = (select id from players where handle = 'pol')
  group by dc.card_name
) used on used.card_name = c.card_name
where c.player_id = (select id from players where handle = 'pol')
  and c.export_date = (select max(export_date) from collection where player_id = (select id from players where handle='pol'))
  and c.quantity - coalesce(used.qty, 0) > 0
order by libere desc;
```

Carte contese tra più mazzi di pol (stesso nome, in 2+ liste):

```sql
select dc.card_name, count(distinct d.slug) as n_mazzi, array_agg(distinct d.slug) as mazzi
from deck_cards dc
join decks d on d.id = dc.deck_id
where d.player_id = (select id from players where handle = 'pol')
group by dc.card_name
having count(distinct d.slug) > 1
order by n_mazzi desc;
```
