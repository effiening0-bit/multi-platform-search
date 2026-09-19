# Media Inbox boundary

Multi-platform Search is discovery only. Its output is a candidate URL and metadata; it does not alter Media Inbox's registry, processing budget, extraction pipeline, or Notion SOP.

On user/agent selection, call `SearchService.media_inbox_handoff(result)`. The resulting object has `handoff_type=media_inbox_ingest_candidate`, URL, platform, title, and result id. The receiving Media Inbox instance decides whether and how to ingest it.
