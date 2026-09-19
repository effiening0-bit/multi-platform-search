from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from .dedup import deduplicate
from .models import ProviderStatus, SearchResponse
from .providers import Provider, default_providers
from .ranking import rank
from .routing import rewrite, route

LIMITS = {"quick": 3, "normal": 5, "deep": 10}
class SearchService:
    def __init__(self, providers: dict[str, Provider] | None = None): self.providers = providers or default_providers()
    def search(self, query: str, mode: str = "normal", platforms: list[str] | None = None) -> SearchResponse:
        if mode not in LIMITS: raise ValueError(f"Unsupported mode: {mode}")
        intent, routes = route(query, platforms)
        limit = LIMITS[mode]
        statuses, all_results = [], []
        with ThreadPoolExecutor(max_workers=min(6, len(routes))) as pool:
            futures = {pool.submit(self.providers[p].search, rewrite(query, p, intent), limit): p for p in routes if p in self.providers}
            for future in as_completed(futures):
                provider = futures[future]
                try:
                    values = future.result(); all_results.extend(values); statuses.append(ProviderStatus(provider, "success" if values else "partial", None if values else "no indexed results"))
                except Exception as exc: statuses.append(ProviderStatus(provider, "unavailable", str(exc)))
        return SearchResponse(query, intent, mode, routes, rank(deduplicate(all_results))[:30], sorted(statuses, key=lambda s: routes.index(s.provider)), ["Xiaohongshu is best-effort and uses public search-index discovery only."] if "xiaohongshu" in routes else [])

    def get_search_result(self, result_id: str, response: SearchResponse):
        return next((item for item in response.results if item.id == result_id), None)

    @staticmethod
    def media_inbox_handoff(result) -> dict:
        return {"handoff_type": "media_inbox_ingest_candidate", "source": "multi-platform-search", "url": result.url, "platform": result.platform, "title": result.title, "result_id": result.id}
