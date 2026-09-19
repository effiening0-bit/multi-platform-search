# Provider notes and compliance

## Web

MVP uses a low-volume RSS search-index adapter to establish a credential-free baseline. A production remote deployment should switch this adapter to a licensed search API (for example Exa) and retain its schema.

## YouTube

The official `search.list` API is the preferred search/metadata path and needs an application API key, not an end-user cookie. The official captions API's listing/download access is authorised; public transcript extraction is therefore a separate, fallible Stage B concern. The MVP falls back to indexed YouTube results when no key is set.

## Bilibili

The open platform is account-authorisation oriented. The MVP confines its use of the public web search endpoint to low-rate title/metadata discovery, marking every returned item as community evidence. No cookie is read from the adjacent Media Inbox directory.

## Zhihu

The stable discovery baseline is `site:zhihu.com` through a web search index. Direct page reading belongs to Stage B and must respect access controls.

## Xiaohongshu

This is a **best-effort** provider only. It uses public search-index discovery of public URLs; no login, cookie, device fingerprinting, or browser automation is present. `unavailable` or `partial` status is expected and never aborts a search.

## Rate limits / privacy

Providers have bounded result counts, per-request timeouts, no credential persistence, and isolated failures. This project must not bypass authentication, paywalls, robots restrictions, or private-content boundaries.
