#!/usr/bin/env python3
"""Migra tutto il patrimonio dati file-based della repo su Supabase:
decks/**/*.txt -> decks + deck_cards
decks/pol/*_note.md (+ altri .md sciolti) -> deck_notes
decks/pol/collection_normalized_*.json -> collection
profiles.json -> sim_profiles
combo_cache.json -> deck_combo_cache
scryfall_cache.json -> card_cache

Idempotente: ogni run cancella e re-inserisce le righe derivate dai file
(deck_cards, deck_notes, sim_profiles, deck_combo_cache), upserta players/decks/
card_cache per nome, e aggiunge una NUOVA riga in collection per ogni export
(chiave unica include export_date, cosi' si tiene lo storico).

Richiede supabase_credentials.json in root repo (vedi supabase/README.md) e lo
schema gia' applicato (supabase/schema.sql) nel progetto.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from client import SupabaseClient, ConfigNonValidaError  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(__file__))
DECKS = os.path.join(ROOT, "decks")

# Metadata curata dal censimento CLAUDE.md (sezione 3) — solo pol e' auditato.
# slug -> dict con i campi noti; tutto il resto resta null (non auditato).
POL_CENSITO = {
    "deadpool": dict(colors="Rakdos", archetype="copie ETB + burn", status="reale",
                      bracket="B3 alto", gc_count=3, critical_node="completo, legale; combo sotto"),
    "sam_frodo": dict(colors="Abzan", archetype="Food/drain combo", status="reale",
                        bracket="B3 spinto", gc_count=2,
                        critical_node="tutto passa da Warren Soultrader; poca rimozione",
                        commander="Frodo, Adventurous Hobbit", commander2="Sam, Loyal Attendant"),
    "shroofus": dict(colors="mono-G", archetype="Saproling go-wide/token", status="reale",
                       bracket="B3", gc_count=2,
                       critical_node="rimozione mirata quasi assente (1 sola carta, Longstalk Brawl)"),
    "toph": dict(colors="Naya", archetype="lands/landfall", status="reale", bracket="B3", gc_count=3,
                  critical_node="3 Toph extra nel main (legale, insolito); rimozione mirata sotto target"),
    "vincent": dict(colors="mono-B", archetype="aristocrats/drain", status="reale",
                      bracket="B4 di fatto", gc_count=3,
                      critical_node="Exquisite Blood+Enduring Tenacity: combo cheap nonostante GC<=3"),
    "sonic": dict(colors="Jeskai", archetype="treasure/haste-flash", status="reale", bracket="B3",
                   gc_count=3, critical_node="manabase: duali originali sostituite con painland"),
    "first_sliver": dict(colors="5c", archetype="sliver tribal fair", status="reale",
                           bracket="B2-B3", gc_count=0,
                           critical_node="combo storica (Intruder Alarm+Sliver Overlord) rimossa dal fisico"),
    "yshtola": dict(colors="Esper", archetype="drain/control", status="reale", bracket="B3",
                      gc_count=3, critical_node="combo Bloodchief Ascension+Mindcrank confermata presente"),
    "edgar_markov": dict(colors="Mardu", archetype="Vampiri go-wide", status="reale", bracket="B3",
                           gc_count=3, critical_node="niente piu' fast mana ne' combo Exquisite Blood/Sanguine Bond/Vito"),
    "mimeoplasm": dict(colors="Sultai", archetype="graveyard/copia + infect", status="reale",
                         bracket="B3 basso", gc_count=1,
                         critical_node="wincon veleno via creature infect copiate/ingrandite dal cimitero"),
    "ultron": dict(colors="incolore/artefatti", archetype="Urza-lands/Eldrazi/Ugin shell", status="teorico"),
    "obeka": dict(colors="Grixis", archetype="drain + controspell gratuiti/economici + Gates/Maze's End",
                   status="teorico"),
    "ms_bumbleflower": dict(colors="Bant", archetype="+1/+1 counters", status="teorico"),
    "serpent_society": dict(colors="Golgari", archetype="deathtouch-aristocrats/edict", status="teorico",
                              bracket="B3 alto", gc_count=3),
    "coulson": dict(colors="mono-W", archetype="Hero tribal", status="reale", bracket="B3", gc_count=1),
}


def parse_deck_file(path):
    """Ritorna (righe [(qty, nome), ...]). La prima riga e' per convenzione il
    comandante (vedi CLAUDE.md sezione 7)."""
    rows = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(\d+)\s+(.+)$", line)
        if m:
            rows.append((int(m.group(1)), m.group(2).strip()))
    return rows


# File .txt in decks/pol/ che NON sono liste mazzo: liste-spesa/ordine proxy (formato
# diverso, non "N Nome Carta") e varianti-bozza di un mazzo gia' censito sotto un altro
# slug (creerebbero un secondo mazzo fantasma con le stesse carte duplicate).
NON_DECK_FILES = {
    "ordine_proxy.txt", "ordine_proxy_gruppo.txt", "ordine_proxy_gruppo_soli_nomi.txt",
    "deadpool_b3opt.txt",  # bozza alternativa di deadpool, non un mazzo fisico distinto
    "coulson_premium.txt",  # variante proxy di coulson, non ancora montata fisicamente
}


def deck_files():
    for player_dir in sorted(glob.glob(os.path.join(DECKS, "*"))):
        if not os.path.isdir(player_dir):
            continue
        player = os.path.basename(player_dir)
        for f in sorted(glob.glob(os.path.join(player_dir, "*.txt"))):
            if os.path.basename(f) in NON_DECK_FILES:
                continue
            yield player, f


def main():
    try:
        sb = SupabaseClient()
    except ConfigNonValidaError as e:
        print("ERRORE CONFIG:", e)
        sys.exit(1)

    # --- players ---
    players = sorted({p for p, _ in deck_files()})
    prows = sb.upsert("players", [
        {"handle": p, "audited": p == "pol"} for p in players
    ], on_conflict="handle")
    player_id = {r["handle"]: r["id"] for r in prows}
    print("players:", player_id)

    # --- decks + deck_cards ---
    deck_id = {}  # (player, slug) -> id
    all_deck_rows = []
    per_deck_cards = {}
    for player, path in deck_files():
        slug = os.path.splitext(os.path.basename(path))[0]
        rows = parse_deck_file(path)
        if not rows:
            print("  WARN: vuoto:", path)
            continue
        meta = POL_CENSITO.get(slug, {}) if player == "pol" else {}
        commander = meta.get("commander") or rows[0][1]
        commander2 = meta.get("commander2")
        rel = os.path.relpath(path, ROOT)
        all_deck_rows.append({
            "player_id": player_id[player],
            "slug": slug,
            "source_file": rel,
            "commander": commander,
            "commander2": commander2,
            "colors": meta.get("colors"),
            "archetype": meta.get("archetype"),
            "status": meta.get("status"),
            "bracket": meta.get("bracket"),
            "gc_count": meta.get("gc_count"),
            "critical_node": meta.get("critical_node"),
            "card_count": sum(q for q, _ in rows),
        })
        per_deck_cards[(player, slug)] = rows

    drows = sb.upsert("decks", all_deck_rows, on_conflict="player_id,slug")
    # ri-seleziona per ottenere (player handle, slug) -> id in modo affidabile
    all_decks = sb.select("decks", select="id,player_id,slug")
    handle_by_id = {v: k for k, v in player_id.items()}
    for d in all_decks:
        h = handle_by_id.get(d["player_id"])
        if h:
            deck_id[(h, d["slug"])] = d["id"]
    print(f"decks upsertati: {len(drows)}")

    # pulizia orfani: mazzi su Supabase di giocatori GESTITI DA QUESTA REPO
    # (hanno un folder in decks/) i cui file .txt non esistono piu'. Il delete
    # cascata su deck_cards/sim_profiles/deck_combo_cache. Giocatori importati
    # da altre fonti (es. bot BolasScryer) NON vengono toccati: non hanno folder.
    local_slugs = {(p, s) for (p, s) in per_deck_cards}
    orphans = [d for d in all_decks
               if handle_by_id.get(d["player_id"]) in {p for p, _ in local_slugs}
               and (handle_by_id[d["player_id"]], d["slug"]) not in local_slugs]
    kept = 0
    for d in orphans:
        # prima le tabelle derivate NOSTRE (nessun vincolo esterno)
        for t in ("sim_profiles", "deck_combo_cache", "deck_cards"):
            sb.delete(t, deck_id=f"eq.{d['id']}")
        # poi la riga mazzo: puo' essere referenziata da tabelle create dal bot
        # (es. deck_values, fuori dal nostro schema) -> in quel caso la lasciamo
        try:
            sb.delete("decks", id=f"eq.{d['id']}")
        except RuntimeError:
            kept += 1
        deck_id.pop((handle_by_id[d["player_id"]], d["slug"]), None)
    if orphans:
        print(f"decks orfani ripuliti: {len(orphans)}"
              + (f" (di cui {kept} righe-mazzo lasciate: referenziate da tabelle del bot)" if kept else ""))

    for (player, slug), rows in per_deck_cards.items():
        did = deck_id.get((player, slug))
        if did is None:
            continue
        sb.delete("deck_cards", deck_id=f"eq.{did}")
        cards = []
        commander_names = set()
        meta = POL_CENSITO.get(slug, {}) if player == "pol" else {}
        commander_names.add((meta.get("commander") or rows[0][1]))
        if meta.get("commander2"):
            commander_names.add(meta["commander2"])
        for qty, name in rows:
            cards.append({"deck_id": did, "card_name": name, "quantity": qty,
                           "is_commander": name in commander_names})
        sb.upsert("deck_cards", cards, returning=False)
    print("deck_cards caricate.")

    # --- deck_notes (solo pol ha .md) ---
    note_rows = []
    for path in sorted(glob.glob(os.path.join(DECKS, "pol", "*.md"))):
        base = os.path.basename(path)
        content = open(path, encoding="utf-8").read()
        matched_slug = None
        for slug in per_deck_cards:
            if slug[0] != "pol":
                continue
            s = slug[1]
            if base == f"{s}_note.md" or base.startswith(f"{s}_"):
                matched_slug = s
                break
        did = deck_id.get(("pol", matched_slug)) if matched_slug else None
        note_rows.append({
            "deck_id": did,
            "player_id": player_id["pol"],
            "title": base.replace(".md", ""),
            "content": content,
            "source_file": os.path.relpath(path, ROOT),
        })
    # idempotenza: cancella tutte le note di pol e re-inserisce
    sb.delete("deck_notes", player_id=f"eq.{player_id['pol']}")
    sb.upsert("deck_notes", note_rows, returning=False)
    print(f"deck_notes caricate: {len(note_rows)}")

    # --- collection ---
    # prende l'export normalizzato piu' recente per data (nome file: collection_normalized_YYYY-MM-DD.json)
    # idempotenza: cancella solo le righe di QUESTA export_date e re-inserisce (niente
    # vincolo UNIQUE su (player_id,card_name,export_date) nel DB live, quindi niente upsert
    # con on_conflict -- lo storico delle date precedenti resta intatto)
    norm_candidates = sorted(glob.glob(os.path.join(DECKS, "pol", "collection_normalized_*.json")))
    if norm_candidates:
        norm_path = norm_candidates[-1]
        export_date = os.path.basename(norm_path).replace("collection_normalized_", "").replace(".json", "")
        owned = json.load(open(norm_path, encoding="utf-8"))
        crows = [{"player_id": player_id["pol"], "card_name": name, "quantity": qty,
                   "source": "deckbox_export", "export_date": export_date}
                  for name, qty in owned.items()]
        sb.delete("collection", player_id=f"eq.{player_id['pol']}", export_date=f"eq.{export_date}")
        sb.upsert("collection", crows, returning=False)
        print(f"collection caricata: {len(crows)} carte distinte (export {export_date})")
    else:
        print("WARN: nessuna collection normalizzata trovata in decks/pol/")

    # --- sim_profiles (profiles.json) ---
    prof_path = os.path.join(ROOT, "profiles.json")
    if os.path.exists(prof_path):
        profiles = json.load(open(prof_path, encoding="utf-8"))
        srows = []
        skipped = 0
        for key, params in profiles.items():
            player, slug = key.split("/", 1)
            did = deck_id.get((player, slug))
            if did is None:
                skipped += 1
                continue
            srows.append({"deck_id": did, "params": params})
        sb.upsert("sim_profiles", srows, on_conflict="deck_id", returning=False)
        print(f"sim_profiles caricati: {len(srows)} (saltati, mazzo non in decks/: {skipped})")

    # --- deck_combo_cache (combo_cache.json) ---
    combo_path = os.path.join(ROOT, "combo_cache.json")
    if os.path.exists(combo_path):
        combos = json.load(open(combo_path, encoding="utf-8"))
        crows = []
        skipped = 0
        for key, raw in combos.items():
            player, slug = key.split("/", 1)
            did = deck_id.get((player, slug))
            if did is None:
                skipped += 1
                continue
            crows.append({"deck_id": did, "raw": raw})
        sb.upsert("deck_combo_cache", crows, on_conflict="deck_id", returning=False)
        print(f"deck_combo_cache caricati: {len(crows)} (saltati, mazzo rimosso dalla repo: {skipped})")

    # --- card_cache (scryfall_cache.json) ---
    sc_path = os.path.join(ROOT, "scryfall_cache.json")
    if os.path.exists(sc_path):
        cache = json.load(open(sc_path, encoding="utf-8"))
        rows = []
        for key, rec in cache.items():
            rows.append({
                "card_name": key,
                "display_name": rec.get("name", key),
                "cmc": rec.get("cmc"),
                "type_line": rec.get("type_line"),
                "oracle_text": rec.get("oracle"),
                "keywords": rec.get("keywords") or [],
                "color_identity": rec.get("ci") or [],
            })
        sb.upsert("card_cache", rows, on_conflict="card_name", returning=False)
        print(f"card_cache caricata: {len(rows)} carte")

    print("\nMigrazione completata.")


if __name__ == "__main__":
    main()
