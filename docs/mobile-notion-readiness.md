# Client connection status — 2026-10-27

Use the same HTTPS MCP endpoint for all clients:
`https://multi-platform-search.onrender.com/mcp/`.
Only the service Bearer credential is supplied to clients. Provider credentials
stay on Render. Do not put tokens in URLs, Git, Skill text, or plugin archives.

| Client | Verified now | Remaining work |
|---|---|---|
| ChatGPT | Private personal plugin created with the verified MCP URL and bearer API-key auth; bundled Skill retained | User installation and credential connection; a real tool call in Web and Mobile remains unverified |
| Codex | Same private plugin can carry the Skill and MCP connection; official MCP client protocol passed | Installation/credential connection and a new-session tool call remain unverified |
| Claude Web / Mobile | Official remote connector supports fixed request headers and shared cloud connections | User must add connector and supply Authorization header; no Claude session test performed |
| Notion Agent Skill | Project Skill is a reusable strategy; Notion treats skills as pages | Not imported into Notion or marked as a skill; not a live connection |
| Notion Agent MCP | Official docs require Business/Enterprise and allow custom servers when the admin permits | Actual workspace plan, permissions, authorization and tool invocation unverified |
| Notion Custom Agent MCP | Official docs support bearer/header authentication on Business/Enterprise | Custom Agent usage consumes credits; not enabled under the zero-extra-spend constraint |

Private ChatGPT plugin:
https://chatgpt.com/plugins/plugins_6ae07ee703088191bc6e129d10416226

Install it from its details page and connect the existing service credential in
the host's secure field. Then open a new chat and request a quick Zotero search.
Repeat on mobile with the same account, checking that the actual tool call is
shown. Creation of the plugin is not proof that installation, auth or mobile
execution has completed.

Current OpenAI Learn documentation says account-available plugins work in Chat
and Work on Web/Desktop/Mobile. The legacy Help Center custom-MCP page separately
says direct custom MCP connections are Web-only and has plan restrictions.
This project uses the private plugin package path; mobile behavior must still be
tested with this account, rather than inferred from either document alone.

For Claude, Customize > Connectors > Add custom connector, use this endpoint.
Choose the fixed-header/no-OAuth method and enter the existing service token
only in the secure request-header field as `Authorization: Bearer <credential>`.
Do not distribute the provider API keys to Claude. No third-party login or
consent was completed on the user's behalf.

Notion MCP at `https://mcp.notion.com/mcp` is the other direction: external agents
access Notion. It does not, by itself, enable Notion Agent to call this search
server. A Skill page also cannot install or authenticate an MCP connection.
No Notion pages or Media Inbox data were automatically written.

Official sources checked 2026-10-27:
- https://learn.chatgpt.com/docs/plugins
- https://developers.openai.com/plugins/build/plugins
- https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- https://www.notion.com/help/create-and-manage-skills
- https://www.notion.com/help/connect-mcp-servers-to-your-notion-agent
- https://www.notion.com/help/mcp-connections-for-custom-agents
- https://www.notion.com/help/buy-and-track-notion-credits-for-custom-agents
