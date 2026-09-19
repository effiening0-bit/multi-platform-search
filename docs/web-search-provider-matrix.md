# Production Web Search API matrix — checked 2026-09-19

| Provider | General Web / filtering | Metadata / remote | Current pricing / limits | Decision |
|---|---|---|---|---|
| Brave Search API | Independent general index; web/news/image, filtering and safe-search options | JSON, SDK ecosystem, remote friendly | $5/1k requests, $5 monthly credit, 50 QPS | **Primary** |
| Tavily | Agent-oriented web search; domain include/exclude | JSON/Python/JS, remote friendly | Free 1,000 credits/month; PAYG $0.008/credit | **Fallback candidate** |
| Exa | Semantic general web, not keyword-primary | JSON/official SDK, remote friendly | account-priced; use as optional semantic complement | **Keep optional** |
| Google Custom Search JSON | Custom engine/site search | JSON, API key | New customers closed; existing ends 2027-01-01 | **Reject** |
| Bing Search API | Retired product | no new standard result API | retired 2025-08-11 | **Reject** |
| SerpAPI / Serper | Google-result intermediaries | JSON, remote | verify commercial plan before procurement | **Backup research only** |

Brave is selected for a stable, directly consumable production Web API; Tavily is the fallback candidate for agent-optimized retrieval. Chinese quality must be measured with the supplied benchmark after credentials are configured; it is not inferred from marketing claims.
