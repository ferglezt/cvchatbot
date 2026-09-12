"""
Lightweight daily per-IP token usage tracking, persisted to a local JSON
file and guarded by an in-process lock.

This is a practical cost guard for a single-process deployment (e.g.
Streamlit Community Cloud), not a hardened distributed rate limiter: usage
resets if the app process restarts, and concurrent multi-process
deployments would each track their own counts.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import date

import config

_lock = threading.Lock()


def _today() -> str:
    return date.today().isoformat()


def _load() -> dict:
    if not os.path.exists(config.USAGE_STORE_PATH):
        return {"date": _today(), "usage": {}}
    try:
        with open(config.USAGE_STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"date": _today(), "usage": {}}
    if data.get("date") != _today():
        return {"date": _today(), "usage": {}}
    return data


def _save(data: dict) -> None:
    tmp_path = config.USAGE_STORE_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp_path, config.USAGE_STORE_PATH)


def get_usage(client_id: str) -> int:
    with _lock:
        return _load()["usage"].get(client_id, 0)


def add_usage(client_id: str, tokens: int) -> int:
    if tokens <= 0:
        return get_usage(client_id)
    with _lock:
        data = _load()
        new_total = data["usage"].get(client_id, 0) + tokens
        data["usage"][client_id] = new_total
        _save(data)
        return new_total


def is_over_limit(client_id: str) -> bool:
    return get_usage(client_id) >= config.MAX_TOKENS_PER_IP_PER_DAY
