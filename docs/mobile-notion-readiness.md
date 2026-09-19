# Mobile and Notion readiness

**ChatGPT mobile readiness: `architecture_ready`.** `SKILL.md` is a portable policy/workflow specification; it does not install into ChatGPT Mobile or execute providers. A future remote MCP/HTTP tool layer could use this same stateless backend without a local Windows machine or user cookie. Integration is not ready until authenticated remote transport is deployed and an approved ChatGPT integration surface exists.

**Notion Skill readiness: ready as a portable specification.** It documents triggers, routing, stage boundaries, evidence policy, fallback, stopping caps, and the Media Inbox handoff without CLI-specific paths.

**Notion MCP readiness: not ready for remote deployment.** The tool names/schema are suitable, but the adapter is stdio only and needs remote transport, auth, secrets, rate limits, and observability. Skill and MCP are separate: one guides an agent; the other performs live calls.
