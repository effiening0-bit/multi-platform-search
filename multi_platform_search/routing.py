from __future__ import annotations
from dataclasses import dataclass

RULES = {
    "medical_research": {"terms": ("医学", "医学生", "科研", "文献", "疾病", "患者", "牙", "临床", "medical", "research"), "platforms": ["web", "exa", "youtube", "bilibili", "zhihu"]},
    "software_tutorial": {"terms": ("ai", "agent", "编程", "代码", "软件", "zotero", "notion", "教程", "workflow", "coding"), "platforms": ["web", "exa", "youtube", "bilibili", "zhihu"]},
    "review": {"terms": ("测评", "体验", "iphone", "手机", "数码", "review"), "platforms": ["bilibili", "youtube", "zhihu", "xiaohongshu", "web"]},
    "lifestyle": {"terms": ("穿", "护肤", "学习经验", "跑步", "生活", "错题", "经验"), "platforms": ["xiaohongshu", "zhihu", "bilibili", "youtube", "web"]},
    "local_travel": {"terms": ("旅行", "探店", "周末", "地方", "附近", "青岛", "酒店"), "platforms": ["xiaohongshu", "bilibili", "web", "youtube", "zhihu"]},
}

def classify_intent(query: str) -> str:
    value = query.lower()
    return next((name for name, rule in RULES.items() if any(term in value for term in rule["terms"])), "general")

def route(query: str, requested: list[str] | None = None) -> tuple[str, list[str]]:
    if requested and "all" not in requested:
        return classify_intent(query), requested
    intent = classify_intent(query)
    return intent, RULES.get(intent, {"platforms": ["web", "youtube", "bilibili", "zhihu"]})["platforms"]

def rewrite(query: str, platform: str, intent: str) -> str:
    additions = {
        "web": "workflow Zotero" if intent == "medical_research" else "",
        "bilibili": "教程" if intent in ("medical_research", "software_tutorial") else "",
        "youtube": "tutorial" if intent == "software_tutorial" else "",
        "zhihu": "经验" if intent not in ("medical_research",) else "经验 科研",
        "xiaohongshu": "经验" if intent != "review" else "测评",
    }
    return " ".join(part for part in (query, additions.get(platform, "")) if part).strip()
