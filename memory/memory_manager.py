"""Memory Manager — JSON-based persistent memory for the agent system."""

import json
import os
from datetime import datetime
from typing import Any, Optional

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory_store.json")

_DEFAULT_SCHEMA = {
    "niches": {},
    "content_log": [],
    "performance_log": [],
    "high_performers": [],
    "low_performers": [],
    "last_updated": None,
}


def _load() -> dict:
    if not os.path.exists(MEMORY_FILE):
        _save(_DEFAULT_SCHEMA.copy())
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_niche_context(niche: str) -> dict:
    """Return stored preferences and history for a niche."""
    data = _load()
    return data["niches"].get(niche, {})


def save_niche_preferences(niche: str, preferences: dict) -> None:
    data = _load()
    if niche not in data["niches"]:
        data["niches"][niche] = {}
    data["niches"][niche].update(preferences)
    data["niches"][niche]["last_used"] = datetime.now().isoformat()
    _save(data)


def log_content(niche: str, platform: str, content: dict) -> str:
    """Save a generated content entry. Returns its unique ID."""
    data = _load()
    entry = {
        "id": f"content_{len(data['content_log']) + 1:04d}",
        "niche": niche,
        "platform": platform,
        "timestamp": datetime.now().isoformat(),
        "score": None,
        **content,
    }
    data["content_log"].append(entry)
    _save(data)
    return entry["id"]


def log_performance(content_id: str, score: float, notes: str) -> None:
    """Record performance feedback for a piece of content."""
    data = _load()
    entry = {
        "content_id": content_id,
        "score": score,
        "notes": notes,
        "timestamp": datetime.now().isoformat(),
    }
    data["performance_log"].append(entry)
    for item in data["content_log"]:
        if item["id"] == content_id:
            item["score"] = score
            if score >= 7.0:
                data["high_performers"].append(item)
            elif score <= 3.0:
                data["low_performers"].append(item)
            break
    _save(data)


def get_high_performers(niche: Optional[str] = None, limit: int = 5) -> list:
    data = _load()
    items = data["high_performers"]
    if niche:
        items = [i for i in items if i.get("niche") == niche]
    return items[-limit:]


def get_low_performers(niche: Optional[str] = None, limit: int = 5) -> list:
    data = _load()
    items = data["low_performers"]
    if niche:
        items = [i for i in items if i.get("niche") == niche]
    return items[-limit:]


def get_recent_content(niche: Optional[str] = None, limit: int = 10) -> list:
    data = _load()
    items = data["content_log"]
    if niche:
        items = [i for i in items if i.get("niche") == niche]
    return items[-limit:]


def clear_memory() -> None:
    _save(_DEFAULT_SCHEMA.copy())


def memory_summary() -> dict:
    data = _load()
    return {
        "total_content": len(data["content_log"]),
        "high_performers": len(data["high_performers"]),
        "low_performers": len(data["low_performers"]),
        "niches_tracked": list(data["niches"].keys()),
        "last_updated": data["last_updated"],
    }
