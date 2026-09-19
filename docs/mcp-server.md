# MCP server

The service mounts the official MCP Python SDK Streamable HTTP application at `/mcp`. SSE is not the primary transport. `mcp_adapter.py` is an adapter only: tools call the existing `SearchService` and reuse its result schema. Tools are `multi_platform_search` and `search_platform`; no extraction or Notion/Media Inbox writes occur.
