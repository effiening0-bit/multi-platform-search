# Live benchmark — 2026-09-19

Raw, per-query preservation is [latest.json](live-benchmark/latest.json). It contains 20 requested real queries, router decision, per-provider status, counts, top metadata, and failures; it stores no full content.

## Baseline vs multi-platform

The baseline was Web-only/quick; multi-platform used the rule router/quick. Multi-platform returned more candidates on **8 of 20** queries, equal counts on 5, and zero candidates on 7. This is a host-and-time snapshot, not a quality claim. Gains occurred chiefly in Chinese study/medical and AI-workflow queries; several lifestyle/local/platform-specific queries had no reliable indexed result.

| Reliability snapshot | Observed status counts |
|---|---|
| Bilibili | 6 success, 10 partial, 4 unavailable |
| Web | 8 success, 9 partial, 3 unavailable |
| YouTube fallback | 1 success, 15 partial, 4 unavailable |
| Zhihu fallback | 1 success, 15 partial, 4 unavailable |
| Xiaohongshu | 0 routed in these rules; no claim of coverage |
| Exa | 14 unavailable because `EXA_API_KEY` was absent; remaining queries did not route it |

### Interpretation

Coverage and diversity increase when Bilibili succeeds, but the free index is noisy/variable. Evidence safety remained intact: all platform UGC stays `community`; no benchmark result is promoted to factual authority. URL/title deduplication prevented repeated indexed copies, but the small result counts do not establish a robust semantic-dedup score. The benchmark is evidence that degradation is visible and non-fatal, not evidence of production search quality.

## Credential-limited checks

`YOUTUBE_API_KEY` and `EXA_API_KEY` were both absent, so their **project adapters could not be live-validated**. The connected Exa research tool itself returned results during this audit, but that does not validate the project's credentialed Exa adapter. Configure keys and rerun `python scripts/live_benchmark.py` before any production claim.
