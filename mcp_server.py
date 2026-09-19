"""Optional MCP adapter; core CLI/API remains dependency-free.

Install `mcp` and run: python mcp_server.py
"""
from multi_platform_search import SearchService

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as error:
    raise SystemExit("Install optional dependency: pip install mcp") from error

mcp = FastMCP("multi-platform-search")
service = SearchService()
_responses = {}

@mcp.tool()
def multi_platform_search(query: str, mode: str = "normal", platforms: list[str] | None = None) -> dict:
    """Discover public candidate sources across routed platforms; no deep extraction."""
    response = service.search(query, mode, platforms)
    _responses[query] = response
    return response.to_dict()

@mcp.tool()
def search_platform(query: str, platform: str, mode: str = "normal") -> dict:
    return service.search(query, mode, [platform]).to_dict()

@mcp.tool()
def get_search_result(query: str, result_id: str) -> dict | None:
    response = _responses.get(query)
    result = service.get_search_result(result_id, response) if response else None
    return result.to_dict() if result else None

if __name__ == "__main__": mcp.run()
