from __future__ import annotations
import html, json, os, re
from abc import ABC, abstractmethod
from urllib.parse import quote_plus, urlsplit
from urllib.request import Request, urlopen
from .models import SearchResult
from .config import load_local_env

load_local_env()

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"

def fetch_json(url: str, timeout: int = 8) -> dict:
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

class Provider(ABC):
    name: str
    @abstractmethod
    def search(self, query: str, limit: int) -> list[SearchResult]: ...

class BingRssProvider(Provider):
    """Low-volume public index fallback. Replace with a licensed web API in production."""
    name = "web"
    def __init__(self, site: str | None = None, name: str = "web"):
        self.site, self.name = site, name
    def search(self, query: str, limit: int) -> list[SearchResult]:
        scoped = f"site:{self.site} {query}" if self.site else query
        text = urlopen(Request("https://www.bing.com/search?format=rss&q=" + quote_plus(scoped), headers={"User-Agent": UA}), timeout=8).read().decode("utf-8", "replace")
        entries = re.findall(r"<item>(.*?)</item>", text, re.S)
        results = []
        required_latin_terms = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", query.lower())
        cjk_pairs = set(re.findall(r"[\u4e00-\u9fff]{2}", query))
        for index, item in enumerate(entries):
            def tag(name: str) -> str:
                found = re.search(fr"<{name}>(.*?)</{name}>", item, re.S)
                return html.unescape(re.sub("<.*?>", "", found.group(1))).strip() if found else ""
            title, url = tag("title"), tag("link")
            snippet = tag("description")
            # Search-index outages can emit a generic regional news feed. Reject it
            # rather than letting irrelevant results masquerade as query matches.
            if required_latin_terms and not any(term in (title + " " + snippet).lower() for term in required_latin_terms): continue
            if cjk_pairs and not required_latin_terms and not any(term in (title + " " + snippet) for term in cjk_pairs): continue
            host = urlsplit(url).netloc.lower().removeprefix("www.")
            if self.site and not (host == self.site or host.endswith("." + self.site) or host.startswith(self.site + "/")): continue
            if url: results.append(SearchResult(id=f"{self.name}-{index}", platform=self.name, title=title, url=url, snippet=snippet, content_type="article", search_score=max(.1, .8-index*.05), evidence_level="community" if self.name != "web" else "unknown", extraction_available=True, metadata={"source_type": "public_index_fallback"}))
            if len(results) >= limit: break
        return results

class BilibiliProvider(Provider):
    name = "bilibili"
    def search(self, query: str, limit: int) -> list[SearchResult]:
        endpoint = "https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=" + quote_plus(query)
        req = Request(endpoint, headers={"User-Agent": UA, "Referer": "https://search.bilibili.com/", "Accept": "application/json"})
        try:
            with urlopen(req, timeout=8) as response: payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return self._index_fallback(query, limit, "public_api_failure")
        if payload.get("code") != 0:
            return self._index_fallback(query, limit, "public_api_rejected")
        items = payload.get("data", {}).get("result", [])[:limit]
        if not items:
            return self._index_fallback(query, limit, "public_api_empty")
        output = []
        for index, item in enumerate(items):
            bvid = item.get("bvid", "")
            output.append(SearchResult(id=f"bilibili-{bvid or index}", platform="bilibili", title=re.sub("<.*?>", "", item.get("title", "")), url=f"https://www.bilibili.com/video/{bvid}" if bvid else item.get("arcurl", ""), author=item.get("author"), published_at=item.get("pubdate"), snippet=re.sub("<.*?>", "", item.get("description", "")), content_type="video", engagement={"views": int(item["play"]) if str(item.get("play", "")).isdigit() else None, "likes": None, "comments": None}, search_score=max(.1, .85-index*.05), evidence_level="community", extraction_available=True, metadata={"bvid": bvid}))
        return output

    @staticmethod
    def _index_fallback(query: str, limit: int, reason: str) -> list[SearchResult]:
        # Reuse the existing API/key with one basic search, then the free RSS
        # fallback. No cookies, browser sessions, extraction or paid upgrade.
        results = []
        if os.getenv("TAVILY_API_KEY"):
            try:
                results = TavilyProvider(site="bilibili.com", name="bilibili").search(query, limit)
            except Exception:
                pass
        if not results:
            results = BingRssProvider("bilibili.com", "bilibili").search(query, limit)
        for result in results:
            result.metadata["fallback"] = "web_index_after_public_api_failure"
            result.metadata["fallback_reason"] = reason
        return results

class YouTubeProvider(Provider):
    name = "youtube"
    def search(self, query: str, limit: int) -> list[SearchResult]:
        key = os.getenv("YOUTUBE_API_KEY")
        if not key: raise RuntimeError("missing_credentials: YOUTUBE_API_KEY")
        payload = fetch_json("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=" + str(limit) + "&q=" + quote_plus(query) + "&key=" + quote_plus(key))
        return [SearchResult(id="youtube-" + item["id"]["videoId"], platform="youtube", title=item["snippet"]["title"], url="https://www.youtube.com/watch?v=" + item["id"]["videoId"], author=item["snippet"].get("channelTitle"), published_at=item["snippet"].get("publishedAt"), snippet=item["snippet"].get("description"), content_type="video", search_score=max(.1, .85-index*.05), evidence_level="community", extraction_available=True, metadata={"source_type": "official_api"}) for index, item in enumerate(payload.get("items", []))]

class TavilyProvider(Provider):
    name = "web"
    def __init__(self, site: str | None = None, name: str = "web"):
        self.site, self.name = site, name

    def search(self, query: str, limit: int) -> list[SearchResult]:
        key = os.getenv("TAVILY_API_KEY")
        if not key: return BingRssProvider(self.site, self.name).search(query, limit)
        payload = {"query": query, "max_results": limit, "search_depth": "basic",
                   "auto_parameters": False, "include_answer": False, "include_raw_content": False}
        if self.site:
            payload["include_domains"] = [self.site]
        req = Request("https://api.tavily.com/search", data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json", "Authorization": "Bearer " + key, "User-Agent": UA})
        with urlopen(req, timeout=10) as response: response_data = json.loads(response.read())
        results = []
        for index, item in enumerate(response_data.get("results", [])):
            url = item.get("url", "")
            try:
                parts = urlsplit(url)
                host = (parts.hostname or "").lower()
                if parts.scheme not in ("http", "https"):
                    continue
            except ValueError:
                continue
            if self.site and host != self.site and not host.endswith("." + self.site):
                continue
            results.append(SearchResult(
                id=f"{self.name}-{index}", platform=self.name, title=item.get("title", url), url=url,
                published_at=item.get("published_date"), snippet=item.get("content"),
                content_type="video" if self.name == "bilibili" and "/video/" in parts.path else "article",
                search_score=item.get("score", max(.1, .8-index*.05)),
                evidence_level="community" if self.site else "unknown", extraction_available=True,
                metadata={"source_type": "public_index_fallback" if self.site else "third_party_api", "provider": "tavily"}))
            if len(results) >= limit:
                break
        return results

class ExaProvider(Provider):
    name = "exa"
    def search(self, query: str, limit: int) -> list[SearchResult]:
        key = os.getenv("EXA_API_KEY")
        if not key: raise RuntimeError("EXA_API_KEY is not configured")
        req = Request("https://api.exa.ai/search", data=json.dumps({"query": query, "numResults": limit, "contents": {"highlights": {"maxCharacters": 600}}}).encode(), headers={"x-api-key": key, "content-type": "application/json", "User-Agent": UA})
        with urlopen(req, timeout=12) as response: payload = json.loads(response.read())
        return [SearchResult(id=f"exa-{index}", platform="exa", title=item.get("title", item["url"]), url=item["url"], published_at=item.get("publishedDate"), snippet=" ".join(item.get("highlights", [])), content_type="article", search_score=item.get("score", .7), evidence_level="unknown", extraction_available=True) for index, item in enumerate(payload.get("results", []))]

def default_providers() -> dict[str, Provider]:
    return {"web": TavilyProvider(), "youtube": YouTubeProvider(), "bilibili": BilibiliProvider(), "zhihu": BingRssProvider("zhihu.com", "zhihu"), "xiaohongshu": BingRssProvider("xiaohongshu.com", "xiaohongshu"), "exa": ExaProvider()}
