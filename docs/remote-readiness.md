# Public service status — 2026-10-27

The existing Render service is reachable at https://multi-platform-search.onrender.com.
The canonical MCP endpoint is `https://multi-platform-search.onrender.com/mcp/`.
The original Host fix `39671c4` was pushed normally, preserving all history.
Public tests using the official Python MCP SDK passed initialize, tools/list,
both search tools, HTTP search, missing/wrong-token 401, and 429 with Retry-After.
See `acceptance/public-2026-10-27.json`. This is dated evidence, not a permanent
uptime guarantee. `/health` and `/ready` now expose Render's `RENDER_GIT_COMMIT`
as `release`, so callers can verify the actual running commit.

Authentication is required by default. Put `SERVICE_API_KEY` and the existing
provider keys in Render environment secrets. No keys belong in Git or plugin
archives. Bearer authentication is a fixed API-key mechanism, not an OAuth flow.
Rate limiting is per token and per process, with an in-memory 60-second window;
it resets on restart and is not a distributed quota or billing cap.

Render Free can cold-start. No paid upgrade, scheduler, keep-alive service, or
auto-recharge was added. Existing provider billing/auto-recharge settings still
need account-level verification. The code does not enforce a monetary budget.
`/ready` is process readiness, not a live probe of provider quotas or credentials.
