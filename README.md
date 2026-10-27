# Multi-platform Search

An independent discovery service shared through Skill -> MCP -> Search Core ->
Providers. It finds public candidate sources across Tavily/Web, Exa, YouTube,
Bilibili, Zhihu and Xiaohongshu. Social-platform coverage is best-effort.
Media Inbox remains a separate project. No automatic media download or Notion write.

- Public service: https://multi-platform-search.onrender.com
- Authenticated MCP: https://multi-platform-search.onrender.com/mcp/
- Private ChatGPT plugin: https://chatgpt.com/plugins/plugins_6ae07ee703088191bc6e129d10416226
- [Client connection status](docs/mobile-notion-readiness.md)
- [MCP transport and acceptance](docs/mcp-server.md)
- [Deployment status and limits](docs/remote-readiness.md)
- [Dated public test evidence](docs/acceptance/public-2026-10-27.json)
- [Open-source adoption decisions](docs/github-ecosystem-scan.md)

Run the core CLI: `python cli.py search "Zotero tutorials" --mode quick --json`.
For the HTTP/MCP server, install `requirements-server.txt` and inject secrets
through Render environment settings. Local .env is ignored; never commit it.
