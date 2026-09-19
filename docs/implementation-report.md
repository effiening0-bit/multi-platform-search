# Multi-platform Search Implementation Report

## 1. Existing System Audit

Media Inbox remains untouched at the sibling `media-inbox/extraction` directory. It receives known URLs for extraction/Notion workflow. This project discovers unknown candidate URLs only.

## 2–5. Ecosystem research, matrix, architecture, decisions

See [provider matrix](provider-matrix.md) and [architecture](multi-platform-search-architecture.md). The explicit outcome is Adopt: YouTube Data API + Exa; Wrap: public Bilibili search and search-index fallbacks; Reference: MCP/transcript patterns; Reject: XHS login automation.

## 6–10. Implemented providers, router, expansion, deduplication, evidence

`web`, `youtube`, `bilibili`, `zhihu`, `xiaohongshu`, and optional `exa` share `SearchResult`. The rule router and rewriter are in `routing.py`; URL and high-title-similarity grouping are in `normalize.py`/`dedup.py`; `ranking.py` uses source-nature weights. Evidence labels describe evidence nature, never factual truth.

## 11–12. Progressive retrieval and boundary

Stage A is the implemented metadata search. Stage B is only for user/agent-selected top candidates; Stage C is rare full extraction. `media_inbox_handoff` produces an explicit handoff object without importing or changing Media Inbox.

## 13. Tests

`python -m unittest discover -s tests -v` passed 6 tests on 2026-09-19: URL normalization, query rewrite/routing, dedup, ranking-through-service, timeout isolation, cross-platform contract/XHS degradation. The hardening pass added a preserved 20-query live benchmark; see [live benchmark report](live-benchmark-report.md).

## 14–18. Limitations, credentials, readiness, next step

Xiaohongshu is search-index-only best effort. YouTube quality is best with `YOUTUBE_API_KEY`; Exa requires `EXA_API_KEY`; neither needs user cookies. Core is remote-capable and the optional FastMCP adapter makes it mobile-agent-capable through a hosted service. It is ready for a Notion Agent to call via MCP/Skill, but does not auto-write Notion. Recommended next step: configure a licensed web-search/YouTube key in the target deployment and add a compliant Media Inbox Stage-B handoff client after its ingest API is confirmed.
