from __future__ import annotations
from difflib import SequenceMatcher
from .models import SearchResult
from .normalize import normalize_url, title_key

def deduplicate(results: list[SearchResult]) -> list[SearchResult]:
    groups: list[list[SearchResult]] = []
    for result in results:
        result.canonical_url = normalize_url(result.canonical_url or result.url)
        key = title_key(result.title)
        match = next((group for group in groups if normalize_url(group[0].url) == result.canonical_url or SequenceMatcher(None, title_key(group[0].title), key).ratio() >= .92), None)
        if match: match.append(result)
        else: groups.append([result])
    selected = []
    for index, group in enumerate(groups, 1):
        group_id = f"dup-{index:03d}"
        for item in group: item.duplicate_group_id = group_id
        selected.append(max(group, key=lambda item: item.search_score or 0))
    return selected
