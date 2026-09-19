# Architecture

`Search Skill -> router/query rewriter -> provider adapters -> normalize/deduplicate/rank -> structured candidates -> optional Media Inbox handoff`.

The core is a dependency-free Python API and CLI. Providers implement `search(query, limit) -> SearchResult[]`; network calls run concurrently and every provider failure is converted to status, never a failed search. Stage A returns metadata only. Stage B is an explicit top-K extraction request, handled by an extractor/Media Inbox. Stage C is reserved for selected high-value sources.

Router defaults are rule-configured: medical/research begins Web/Exa then video/community support; software/tutorial begins Web/Exa then YouTube/Bilibili/Zhihu; reviews begin Bilibili/YouTube; lifestyle and local experience begin Xiaohongshu. Mode caps are quick=3, normal=5, deep=10 per provider and 30 total after deduplication.

`mcp_server.py` exposes `multi_platform_search`, `search_platform`, and `get_search_result` when the optional MCP dependency is installed. Core operation is remote-capable: deploy it as a small service/container with secrets injected by environment, never bundled cookies.
