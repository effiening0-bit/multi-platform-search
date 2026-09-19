import argparse, json, sys
from multi_platform_search import SearchService

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

parser = argparse.ArgumentParser(description="Independent multi-platform discovery")
sub = parser.add_subparsers(dest="command", required=True)
search = sub.add_parser("search"); search.add_argument("query"); search.add_argument("--platform", action="append", choices=["all", "web", "youtube", "bilibili", "zhihu", "xiaohongshu", "exa"]); search.add_argument("--mode", choices=["quick", "normal", "deep"], default="normal"); search.add_argument("--json", action="store_true")
args = parser.parse_args()
response = SearchService().search(args.query, args.mode, args.platform)
if args.json: print(json.dumps(response.to_dict(), ensure_ascii=False, indent=2))
else:
    for status in response.provider_status: print(f"[{status.provider}] {status.status}" + (f": {status.detail}" if status.detail else ""))
    for item in response.results: print(f"{item.platform:12} {item.title}\n  {item.url}")
