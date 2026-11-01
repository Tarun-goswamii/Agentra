"""Memory package __init__ (already created but ensure exports are correct)."""
from memory.memory_manager import (
    get_niche_context,
    save_niche_preferences,
    log_content,
    log_performance,
    get_high_performers,
    get_low_performers,
    get_recent_content,
    memory_summary,
    clear_memory,
)

__all__ = [
    "get_niche_context",
    "save_niche_preferences",
    "log_content",
    "log_performance",
    "get_high_performers",
    "get_low_performers",
    "get_recent_content",
    "memory_summary",
    "clear_memory",
]
