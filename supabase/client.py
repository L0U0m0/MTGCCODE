#!/usr/bin/env python3
"""Client minimale PostgREST per Supabase, stesso stile di
claude-tools/memoria_supabase/client.py ma per questo progetto.
Standard library + requests (gia' usato altrove nella repo)."""
import json
import os
import requests

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "supabase_credentials.json")


class ConfigNonValidaError(Exception):
    pass


def carica_config(percorso: str = CONFIG_PATH) -> dict:
    if not os.path.isfile(percorso):
        raise ConfigNonValidaError(
            f"File credenziali non trovato: {percorso}\n"
            "Crealo con: {\"url\": \"https://xxxx.supabase.co\", \"service_role_key\": \"...\"}"
        )
    with open(percorso, encoding="utf-8") as f:
        dati = json.load(f)
    for campo in ("url", "service_role_key"):
        if not dati.get(campo):
            raise ConfigNonValidaError(f"Campo obbligatorio mancante: {campo}")
    dati["url"] = dati["url"].rstrip("/")
    return dati


class SupabaseClient:
    def __init__(self, config: dict = None):
        self.cfg = config or carica_config()
        self.base = f"{self.cfg['url']}/rest/v1"
        self.headers = {
            "apikey": self.cfg["service_role_key"],
            "Authorization": f"Bearer {self.cfg['service_role_key']}",
            "Content-Type": "application/json",
        }

    def upsert(self, table: str, rows: list, on_conflict: str = None, returning: bool = True):
        """Upsert (insert o update) via header Prefer: resolution=merge-duplicates.
        on_conflict deve combaciare con un vincolo UNIQUE/PK della tabella."""
        if not rows:
            return []
        params = {}
        if on_conflict:
            params["on_conflict"] = on_conflict
        prefer = "resolution=merge-duplicates" + (",return=representation" if returning else "")
        headers = {**self.headers, "Prefer": prefer}
        out = []
        for i in range(0, len(rows), 500):
            chunk = rows[i:i + 500]
            r = requests.post(f"{self.base}/{table}", headers=headers, params=params,
                               data=json.dumps(chunk), timeout=60)
            if r.status_code >= 300:
                raise RuntimeError(f"upsert {table} fallito ({r.status_code}): {r.text[:500]}")
            if returning:
                out.extend(r.json())
        return out

    def select(self, table: str, **params):
        r = requests.get(f"{self.base}/{table}", headers=self.headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def delete(self, table: str, **params):
        r = requests.delete(f"{self.base}/{table}", headers=self.headers, params=params, timeout=30)
        if r.status_code >= 300:
            raise RuntimeError(f"delete {table} fallito ({r.status_code}): {r.text[:500]}")
