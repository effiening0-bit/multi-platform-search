from __future__ import annotations
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING = {"spm", "from", "feature", "si", "utm_source", "utm_medium", "utm_campaign", "share_source"}

def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    path = re.sub(r"/+", "/", parts.path).rstrip("/") or "/"
    params = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in TRACKING and not k.lower().startswith("utm_")]
    return urlunsplit((parts.scheme.lower() or "https", host, path, urlencode(sorted(params)), ""))

def title_key(title: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", title.lower())
