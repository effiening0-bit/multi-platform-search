"""Run bounded live discovery tests; preserves raw metadata but no extracted content."""
from __future__ import annotations
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from multi_platform_search import SearchService

QUERIES = [
 "医学生如何做 Zotero 文献管理", "口腔医学生怎么整理错题", "牙周病病例汇报怎么做", "医学生怎么高效使用 MarginNote", "医学教材怎么做主动回忆",
 "Notion Agent 使用经验", "Codex workflow", "ChatGPT 学术研究工作流", "AI coding agent 实际使用体验", "Notion 和 Obsidian 医学生怎么选",
 "iPhone 17 Pro 长期使用体验", "大学生冬季跑步怎么穿", "大学生宿舍健身经验", "学生党高性价比降噪耳机", "B站计算机二级 Excel 教程",
 "知乎医学生科研经验", "小红书医学生文献管理", "YouTube Zotero medical student workflow", "青岛周末适合学习的安静地方", "MarginNote 医学生使用经验",
]

def run(start: int = 0, count: int | None = None):
    service, records = SearchService(), []
    output = Path("docs/live-benchmark"); output.mkdir(parents=True, exist_ok=True)
    target = output / "production-providers.json"
    if target.exists(): records = json.loads(target.read_text(encoding="utf-8"))
    existing = {record["query"] for record in records}
    for query in QUERIES[start:(start + count) if count else None]:
        if query in existing: continue
        baseline = service.search(query, "quick", ["web"])
        multi = service.search(query, "quick")
        records.append({"query": query, "timestamp": datetime.now(timezone.utc).isoformat(), "router": {"intent": multi.intent, "platforms": multi.routed_platforms}, "baseline": {"provider_status": [s.__dict__ for s in baseline.provider_status], "raw_candidate_count": len(baseline.results), "deduped_count": len(baseline.results), "top_results": [x.to_dict() for x in baseline.results[:3]]}, "multi_platform": {"provider_status": [s.__dict__ for s in multi.provider_status], "raw_candidate_count": len(multi.results), "deduped_count": len(multi.results), "top_results": [x.to_dict() for x in multi.results[:5]]}, "notes": []})
        target.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(target)
if __name__ == "__main__":
    args = argparse.ArgumentParser(); args.add_argument("--start", type=int, default=0); args.add_argument("--count", type=int)
    parsed = args.parse_args(); run(parsed.start, parsed.count)
