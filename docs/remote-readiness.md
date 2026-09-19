# Remote readiness audit

**Current level: `remote_capable`, not `remote_ready`.** The core has no filesystem, browser, localhost, or cookie dependency; it is stateless per request, accepts environment secrets, has bounded thread concurrency/timeouts, and can be wrapped by MCP. It is therefore deployable in a container/service after adding a transport.

It is not remote-ready because it lacks a Dockerfile, HTTP authentication/rate limit, persistent provider-health metrics, secret-manager integration, structured observability, and a remote MCP transport configuration. The current MCP adapter is stdio, suitable for a host-side process—not a public endpoint. Never place keys in the repository; inject `YOUTUBE_API_KEY`/`EXA_API_KEY` from the deployment secret store.
