# GitHub ecosystem scan — 2026-09-19

Reviewed 51 search results across four discovery workstreams, then read the candidate READMEs below. Stars are context, not a selection signal; dates reflect the retrieved repository metadata.

| Project | Platform / capability | Stars / last signal | License | Auth / remote / MCP / output | Decision and reason |
|---|---|---:|---|---|---|
| [Nemo2011/bilibili-api](https://github.com/Nemo2011/bilibili-api) | Bilibili API wrapper, search/subtitle | 4.1k; active contributors | GPL-3.0 | optional credential; remote possible; no native MCP; Python objects/JSON | **Reference.** Mature, but copyleft plus anti-risk-control/proxy features and broad scope are inappropriate for a small discovery dependency. |
| [haotongliu58-sudo/bilibili-mcp](https://github.com/haotongliu58-sudo/bilibili-mcp) | Bilibili search/info/subtitles MCP | new; 0 stars | MIT | search guest; subtitles require SESSDATA; stdio; structured tools | **Reference.** Clear narrow contract but too new; subtitle cookie conflicts with this project's Stage-A policy. |
| [XZXZZX-Ai/bilibili-mcp](https://github.com/XZXZZX-Ai/bilibili-mcp) | Bilibili search/extraction MCP | 14; current docs | Apache-2.0 | credential setup; local stdio/optional ASR; structured MCP | **Reject.** Requires local credential workflow and goes beyond discovery. |
| [jdepoix/youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) | YouTube transcript | 8.1k; maintained | MIT | no API key/browser; remote possible; no native MCP; structured raw data | **Wrap later.** A good Stage-B extractor, deliberately not in search. |
| [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) | Xiaohongshu MCP | 15.5k; 85 issues | Apache-2.0 | Docker/browser/plugin modes; operational model varies; MCP | **Reject for MVP.** Large, browser-facing and high ToS/anti-bot risk; fails no-cookie/remote simplicity rule. |
| [thehappyboy/web-search-mcp](https://github.com/thehappyboy/web-search-mcp) | multi-source search/RRF/health | new | not established in retrieved metadata | localhost SearXNG plus paid APIs; MCP; JSON | **Reference.** Good health/degradation ideas, but local service dependency and maturity are unsuitable. |
| [jimmytbc/web_search_mcp](https://github.com/jimmytbc/web_search_mcp) | Web + Brave/Exa/Serper fusion | new; 1 issue | not established in retrieved metadata | remote APIs; stdio MCP; JSON | **Reference.** Sound provider design, but not a social-platform solution and too early to adopt. |
| YouTube Data API | YouTube search/metadata | official | Google terms | API key; remote; JSON | **Adopt.** Most stable compliant primary path. |
| Exa API | semantic web search | official | commercial terms | API key; remote; JSON | **Adopt, optional.** Useful semantic complement; never mandatory. |

## Build-from-scratch justification

The only retained custom code is the thin shared schema/router/normalizer plus isolated provider adapters. Mature alternatives either (a) are extraction rather than discovery, (b) require cookies/login/browser automation, (c) are GPL or operationally much broader than needed, (d) impose localhost services, or (e) have insufficient maintenance history. This minimizes the code that must be maintained while preserving a cookie-free remote path.
