"""Small dependency-free local .env loader; environment always takes precedence."""
from __future__ import annotations
import os
from pathlib import Path

def load_local_env() -> None:
    path = Path(__file__).resolve().parents[1] / ".env"
    if not path.is_file(): return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line: continue
        key, value = line.split("=", 1)
        if key in {"TAVILY_API_KEY", "EXA_API_KEY", "YOUTUBE_API_KEY"}:
            os.environ.setdefault(key.strip(), value.strip())
