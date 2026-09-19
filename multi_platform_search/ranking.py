from .models import SearchResult

WEIGHTS = {"official": .25, "academic": .23, "professional": .18, "media": .12, "community": .08, "personal_experience": .06, "unknown": .05}

def rank(results: list[SearchResult]) -> list[SearchResult]:
    for item in results:
        base = item.search_score if item.search_score is not None else .5
        item.search_score = round(min(.99, base + WEIGHTS[item.evidence_level]), 3)
    return sorted(results, key=lambda item: item.search_score or 0, reverse=True)
