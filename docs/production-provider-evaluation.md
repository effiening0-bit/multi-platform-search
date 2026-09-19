# Production provider evaluation

Configured environment check on 2026-09-19: `YOUTUBE_API_KEY`, `EXA_API_KEY`, and `WEB_SEARCH_API_KEY` were absent. No secrets were read or recorded. Therefore official YouTube, Exa, and Brave adapter live verification, the requested production-provider benchmark comparison, cost-per-100 calculation, and Go decision are **NOT YET** possible.

Implemented credential-safe behaviour: YouTube now returns `unavailable` with `missing_credentials` rather than silently falling back and claiming an official source. Web uses Brave when `WEB_SEARCH_API_KEY` exists, otherwise candidate metadata states `source_type=public_index_fallback`. `.env.example` and `.gitignore` are present.

When keys are supplied via environment, rerun `python scripts/live_benchmark.py`; preserve the prior JSON before rerunning to create an explicit comparison artifact.
