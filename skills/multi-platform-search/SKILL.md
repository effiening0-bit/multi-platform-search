# multi-platform-search

## Trigger

Use when the user asks to search, investigate, find tutorials, reviews, discussions, or community experience across sources—especially “多平台深搜”, Bilibili, Zhihu, Xiaohongshu, or YouTube. Do not use it when a user already supplies a specific media URL: that belongs to Media Inbox.

## Procedure

1. Classify intent and route only relevant providers. Honour an explicit platform request.
2. Use rule-based platform-specific query expansion. Select `quick` (3/provider), `normal` (5/provider), or `deep` (10/provider; nominate only top candidates for later extraction). Stop after 30 deduplicated candidates.
3. Return Stage A metadata/snippets; never bulk-download candidate content.
4. Keep provider failure isolated; surface `provider_status` and continue. Prefer official/API-key providers where configured; use Web-index fallbacks only as clearly marked discovery, never as an assertion of full-platform coverage.
5. Normalize URLs, group probable duplicates, rank results, and label evidence nature. `official/academic/professional/media/community/personal_experience/unknown` describes source nature, not truth.
6. When the user selects a candidate, create the standard Media Inbox handoff object. Do not call Media Inbox automatically.

## Output

Return the unified result schema including platform, canonical URL, title, author, date, snippet, type, nullable engagement, extraction availability, evidence level, score, duplicate group, provider status, and limitations. Do not invent engagement or certainty.

## Boundary

This specification is portable: it names behaviours and schemas rather than a local path, operating system, or client. It governs discovery only; Stage B/C extraction is explicit and selected-candidate-only. Handoff creates a candidate object for Media Inbox and never changes Media Inbox data or Notion automatically.

## Safety

Use public API/index results, rate limit providers, follow platform terms, do not bypass login/paywalls, and never ask for or store cookies. Xiaohongshu is always best-effort unless a compliant provider is separately configured.
