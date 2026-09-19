# Provider hardening report

Benchmark-driven changes only:

1. The index adapter now rejects generic RSS/news-feed responses unless their title/snippet contains a query term; CJK pair matching closes the prior Chinese-query gap.
2. Site fallbacks validate the returned hostname, preventing `site:`-ignored results from being mislabeled Zhihu/Xiaohongshu/Bilibili.
3. Bilibili 412/transport errors fall back to a bounded `bilibili.com` index query, marking each returned candidate with `metadata.fallback`. No cookie, proxy bypass, Selenium, or retry loop was added.
4. `scripts/live_benchmark.py` preserves each completed query atomically, so a later interruption does not discard already observed live evidence.

Remaining: a licensed Web search API should replace the RSS adapter; Bilibili remains region/IP sensitive; Xiaohongshu stays public-index-first; official YouTube/Exa require keys. These are deliberately statuses, not hidden retries or fabricated results.
