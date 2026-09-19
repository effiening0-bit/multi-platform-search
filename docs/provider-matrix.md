# Provider matrix (research checked 2026-09-19)

The hardening-time repository evidence, maintenance signals, authentication/deployment assessment, and build-vs-adopt decisions are expanded in [GitHub ecosystem scan](github-ecosystem-scan.md). This matrix remains the runtime-provider decision record.

| Project / tool | URL | Platform | Type | Search / read | Login / cookie | Official API | Output | Deploy | Activity / license | Stability / anti-bot | Use | Decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| YouTube Data API v3 | https://developers.google.com/youtube/v3/docs/search/list | YouTube | API | Search + metadata; caption tracks require authorised access | key / No | Yes | JSON | remote | Google terms | Low / Low | primary search | Adopt |
| youtube-transcript-api | https://github.com/jdepoix/youtube-transcript-api | YouTube | Python | public transcript fallback | No / No | No | Python / JSON | local, remote | active; MIT | Medium / Medium | Stage B fallback | Wrap later |
| Bilibili Open Platform | https://open.bilibili.com/doc | Bilibili | API | authorised account/video management, not general public discovery | authorisation / No | Yes | JSON | remote | platform terms | Low / Low | creator integrations | Reference |
| bilibili-mcp-server | https://github.com/Zijian-Ni/bilibili-mcp-server | Bilibili | MCP | public video search, metadata, comments | No / No by default | Partial / undocumented endpoints | JSON | local, remote | license in repo; recently updated | Medium / Medium | feature reference | Reference |
| Bilibili public search endpoint | https://github.com/1665169869/bilibili-api-docs/blob/master/api.search.md | Bilibili | HTTP endpoint | public video discovery | No / No | No | JSON | remote | unofficial docs | Medium / Medium | MVP search | Wrap |
| Bing RSS public index | https://www.bing.com/search | Web / Zhihu / XHS | indexed search | title, URL, snippet | No / No | Partial | RSS/XML | remote | service terms | Medium / Low | fallback discovery | Wrap, replace in production |
| Exa Search API | https://docs.exa.ai/reference/search | Web | API | semantic search, highlights / contents | key / No | Yes | JSON | remote | commercial terms | Low / Low | optional enrichment | Adopt |
| xiaohongshu-mcp | https://github.com/xpzouying/xiaohongshu-mcp | Xiaohongshu | MCP | varies; often endpoint/browser dependent | varies / may be needed | No | JSON | local | license in repo | High / High | research only | Reject for MVP |

“Official API” refers to an API sanctioned for the stated discovery capability, not merely any platform API. The Bilibili official platform documents account authorisation and content-management capabilities; it is intentionally not treated as a public global-search API. Activity and licenses must be re-checked and pinned before a production dependency is adopted.

## Decisions

- **Adopt:** YouTube Data API and Exa as opt-in credentialed providers.
- **Wrap:** Bilibili public search (small, isolated adapter); public web-index fallback for Web, Zhihu, and Xiaohongshu.
- **Reference:** Bilibili MCP/project patterns and YouTube transcript library, without copying their scraping/log-in behaviour.
- **Reject:** Xiaohongshu cookie/browser automation and any provider requiring default user session tokens.
