# Multi-platform Search

An independent, provider-based discovery layer for agents. It finds candidate sources; it does not ingest or organise media. See `docs/` for the architecture and provider decisions.

```powershell
python cli.py search "医学生如何做 Zotero 文献管理" --mode normal --json
```

No cookie is read or stored. `YOUTUBE_API_KEY` and `EXA_API_KEY` are optional enhancements; without them, the relevant providers use a search-index fallback where available.
