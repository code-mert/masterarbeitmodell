import re
from typing import Any, Set

def normalize_raw(s: Any) -> str:
    """
    Converts input to string, converts to lowercase, collapses multiple whitespaces 
    into a single space, and trims leading/trailing spaces.
    No Unicode normalization or synonym mapping is performed.
    """
    if s is None:
        return ""
    s_str = str(s).lower()
    return re.sub(r"\s+", " ", s_str).strip()

def to_set(items: Any, normalizer=normalize_raw) -> Set[str]:
    """
    Converts a collection (list, tuple, set) or a single item into a set of normalized strings.
    Filters out empty strings after normalization.
    """
    if not items:
        return set()
    if not isinstance(items, (list, tuple, set)):
        items = [items]
    return {normalizer(item) for item in items if item is not None and str(item).strip() != ""}
