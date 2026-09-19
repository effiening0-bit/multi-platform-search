from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Literal

EvidenceLevel = Literal["official", "academic", "professional", "media", "community", "personal_experience", "unknown"]

@dataclass
class SearchResult:
    id: str
    platform: str
    title: str
    url: str
    author: str | None = None
    published_at: str | None = None
    snippet: str | None = None
    content_type: str = "unknown"
    engagement: dict[str, int | None] = field(default_factory=lambda: {"views": None, "likes": None, "comments": None})
    search_score: float | None = None
    evidence_level: EvidenceLevel = "unknown"
    extraction_available: bool = False
    canonical_url: str | None = None
    duplicate_group_id: str | None = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ProviderStatus:
    provider: str
    status: Literal["success", "partial", "unavailable", "failed"]
    detail: str | None = None

@dataclass
class SearchResponse:
    query: str
    intent: str
    mode: str
    routed_platforms: list[str]
    results: list[SearchResult]
    provider_status: list[ProviderStatus]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {**asdict(self), "results": [item.to_dict() for item in self.results]}
