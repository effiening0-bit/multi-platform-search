# MCP server

The official Python MCP SDK Streamable HTTP app is mounted at `/mcp/`.
Tools: `multi_platform_search` and `search_platform`, both annotated read-only,
non-destructive, idempotent and open-world. They call the existing Search Core.
The Skill supplies strategy; the transport does not replace the strategy.
No media download, extraction or Notion/Media Inbox write occurs.

Allowed hosts include the exact Render hostname and loopback hosts. DNS-rebinding
protection stays enabled. Clients must send `Authorization: Bearer <credential>`.
Stateless Streamable HTTP supports initialize and tools/list using SDK v1; the
server requirements intentionally stay below the SDK v2 major boundary.
`/mcp/` GET may be a long-lived SSE response; acceptance checks its headers
without waiting for the response body to finish. MCP calls use the official
client, not handcrafted protocol payloads.

Public acceptance:
`python scripts/verify_public.py --base-url https://multi-platform-search.onrender.com --output public-evidence.json --rate-limit`

The client reads SERVICE_API_KEY from the process environment or ignored local
.env and never prints it. It sends no provider keys. Rate testing uses only
provider metadata, so it does not spend provider search quota. Run it when the
service's 60-second window is clear. A 429 can temporarily affect other clients
using the same service token.

See `mobile-notion-readiness.md` for actual client connection status.
