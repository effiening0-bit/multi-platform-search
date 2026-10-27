# Bilibili zero-result fallback — 2026-10-27

A Notion Agent test reported `partial / no indexed results` for `search_platform`,
platform `bilibili`, query `Zotero 入门教程`, mode `quick`. That report alone does
not independently verify Notion's tool execution; the Notion tool-call record
remains the client-side evidence.

Reproduced the same query through the official Python MCP Client against the
public Render endpoint: Bilibili returned zero results, while the existing Web
provider found three Bilibili links for a domain-scoped version of the query.
The Bilibili adapter previously retried network failures with Bing RSS only,
and did not use index fallback for nonzero API response codes or empty success.

The adapter now keeps the direct public endpoint first, then tries one existing
Tavily basic search restricted to `bilibili.com`, then the existing free RSS
fallback. Missing Tavily credentials skip that paid-API-capable path entirely.
No new provider account, library, cookies or browser session is required.
Tavily uses `search_depth=basic`, `auto_parameters=false`, and no raw-content
extraction. This consumes existing API search quota when fallback is needed;
it does not change provider billing settings or enforce a monetary cap.

Post-filter result hostnames as well as sending `include_domains`, retain the
Bilibili platform label, and mark fallback results as `public_index_fallback`
with the provider and the reason. Index hits are not represented as direct
platform API results. Zero results remain a valid partial response.

Six additional tests cover HTTP failure, API rejection, empty success, direct
success without Tavily usage, Tavily failure/empty results to RSS, missing keys,
and domain/cost/source metadata. The complete regression suite passes 16 tests.

Reviewed existing official implementation/docs before changing the wrapper:
- https://github.com/tavily-ai/tavily-mcp/blob/main/src/index.ts
- https://docs.tavily.com/documentation/api-reference/endpoint/search

The MCP endpoint, tool schemas and credentials are unchanged. No reconnect or
new API key should be necessary in Notion. Automatic selection of the tool is
still a separate client instruction/permission setting, not verified by this
provider fix.
