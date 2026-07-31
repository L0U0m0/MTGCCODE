-- Schema Supabase per Consulenza-Mazzi (MTGCCODe)
-- Incolla questo per intero nell'SQL Editor del progetto Supabase (una volta sola).
-- Sostituisce: decks/**/*.txt (liste), decks/pol/*_note.md (note), profiles.json
-- (simulazione), scryfall_cache.json / combo_cache.json (cache), collection_*.csv.

create table if not exists players (
  id bigint generated always as identity primary key,
  handle text unique not null,          -- casagrande, rocchi, tommaso, pol, saverio, montauti, g_prete, sbernuz
  audited boolean not null default false, -- true solo per pol al momento (censimento CLAUDE.md)
  created_at timestamptz not null default now()
);

create table if not exists decks (
  id bigint generated always as identity primary key,
  player_id bigint not null references players(id) on delete cascade,
  slug text not null,                   -- nome file senza .txt, es. 'sam_frodo'
  source_file text not null,            -- path relativo nella repo
  commander text,
  commander2 text,                      -- seconda metà di un comandante partner, se presente
  colors text,                          -- es. 'Abzan', 'Sultai', 'Rakdos'
  archetype text,
  status text check (status in ('reale','teorico')),
  bracket text,
  gc_count int,
  gc_names text[],
  critical_node text,                   -- "nodo critico" del censimento CLAUDE.md
  card_count int,
  updated_at timestamptz not null default now(),
  unique (player_id, slug)
);
create index if not exists idx_decks_player on decks(player_id);

create table if not exists deck_cards (
  id bigint generated always as identity primary key,
  deck_id bigint not null references decks(id) on delete cascade,
  card_name text not null,
  quantity int not null default 1,
  is_commander boolean not null default false
);
create index if not exists idx_deck_cards_deck on deck_cards(deck_id);
create index if not exists idx_deck_cards_name on deck_cards(card_name);

-- note libere: *_note.md per mazzo, o note a livello giocatore/repo (deck_id null)
create table if not exists deck_notes (
  id bigint generated always as identity primary key,
  deck_id bigint references decks(id) on delete cascade,
  player_id bigint references players(id) on delete cascade,
  title text not null,
  content text not null,                -- markdown grezzo
  source_file text not null,
  updated_at timestamptz not null default now()
);
create index if not exists idx_deck_notes_deck on deck_notes(deck_id);

-- collezione posseduta (una riga per carta canonica per export)
create table if not exists collection (
  id bigint generated always as identity primary key,
  player_id bigint not null references players(id) on delete cascade,
  card_name text not null,              -- nome canonico Scryfall (inglese)
  quantity int not null,
  source text not null default 'deckbox_export',
  export_date date not null,
  updated_at timestamptz not null default now(),
  unique (player_id, card_name, export_date)
);
create index if not exists idx_collection_player_card on collection(player_id, card_name);

-- cache dati Scryfall (sostituisce scryfall_cache.json)
create table if not exists card_cache (
  card_name text primary key,           -- lowercase
  display_name text not null,
  cmc numeric,
  type_line text,
  oracle_text text,
  keywords text[],
  color_identity text[],
  updated_at timestamptz not null default now()
);

-- cache combo per mazzo (sostituisce combo_cache.json): conteggi grezzi da
-- Commander Spellbook usati da build_profiles.py per derivare cn/cneed/cmana/
-- cdelay/ctut in sim_profiles.params. Non e' la lista delle combo carta-per-
-- carta (quella si consulta live su Commander Spellbook quando serve).
create table if not exists deck_combo_cache (
  deck_id bigint primary key references decks(id) on delete cascade,
  raw jsonb not null,                   -- {n_combos, pieces, mvs, wincons}
  updated_at timestamptz not null default now()
);

-- profili di simulazione (sostituisce profiles.json), un profilo per mazzo
create table if not exists sim_profiles (
  deck_id bigint primary key references decks(id) on delete cascade,
  params jsonb not null,
  updated_at timestamptz not null default now()
);

-- storico run di edh_pod11.py / sim_pods.py
create table if not exists sim_results (
  id bigint generated always as identity primary key,
  run_at timestamptz not null default now(),
  n_games int,
  kind text,                            -- es. 'serata_a_eliminazione', 'pod_b_random'
  results jsonb not null
);

-- RLS: chiuso di default, solo la service_role key (usata dagli script) bypassa RLS.
alter table players enable row level security;
alter table decks enable row level security;
alter table deck_cards enable row level security;
alter table deck_notes enable row level security;
alter table collection enable row level security;
alter table card_cache enable row level security;
alter table deck_combo_cache enable row level security;
alter table sim_profiles enable row level security;
alter table sim_results enable row level security;
