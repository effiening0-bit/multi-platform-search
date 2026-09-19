"""Official MCP SDK adapter. Search business logic remains in SearchService."""
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from multi_platform_search import SearchService

# Configure the SDK's route path at the constructor level.  The returned
# Starlette app is mounted by ``remote_api`` at ``/mcp``; using ``/`` here
# avoids the SDK default ``/mcp`` being appended a second time.
mcp = FastMCP(
    "multi-platform-search",
    stateless_http=True,
    json_response=True,
    mount_path="/mcp",
    streamable_http_path="/",
    transport_security=TransportSecuritySettings(
        allowed_hosts=[
            "multi-platform-search.onrender.com",
            "localhost:*",
            "127.0.0.1:*",
        ],
    ),
)
service = SearchService()

@mcp.tool(description="Discovery-layer search across Tavily/Web, YouTube, Bilibili, Zhihu, Xiaohongshu and optional Exa. Provider partial failures remain warnings; community sources are not final medical fact authority; full text/transcript extraction belongs to a later layer.")
def multi_platform_search(query: str, mode: str = "normal", platforms: list[str] | None = None, max_results: int | None = None) -> dict:
    response = service.search(query, mode, platforms)
    results = response.results[:max_results] if max_results else response.results
    return {"request_id": "mcp-local", "status": "success" if all(s.status == "success" for s in response.provider_status) else "partial", "query": query, "mode": mode, "results": [r.to_dict() for r in results], "providers": [s.__dict__ for s in response.provider_status], "warnings": response.warnings, "meta": {"candidate_count": len(response.results), "deduped_count": len(response.results)}}

@mcp.tool(description="Search exactly one supported platform through the shared multi-platform Search Core.")
def search_platform(query: str, platform: str, mode: str = "normal") -> dict:
    return multi_platform_search(query, mode, [platform], None)

def app():
    # The parent FastAPI app mounts this child at /mcp, while the SDK route
    # itself is configured as /. The public endpoint is therefore exactly
    # /mcp (not /mcp/mcp).
    return mcp.streamable_http_app()
