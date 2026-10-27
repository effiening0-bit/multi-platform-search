# Multi-platform Search｜Work 接管与验收报告

2026-10-27。公网服务已通过验收；跨端安装和账号授权仍未完成，不能标记为全端接入成功。

## GitHub 与 Render

继续使用原仓库和 canonical 本地目录，没有重建项目。原修复提交 `39671c4` 已正常推送；随后功能提交 `31647af` 已自动部署，`/health` 和 `/ready` 实测返回完整的 `31647afd2f5133ae90bd709ab4d97d80daff1df3`。后续验收文档提交不修改运行代码，最终运行提交可直接查 `/health` 的 `release`。

GitHub 连接器核实仓库当前为 **public**，与任务说明中的“私有”不同。本轮未修改可见性。接管时工作区干净、无未提交修改。受限终端的 DNS 失败未在宿主运行环境复现；通过可用网络正常推送，未修改 VPN、系统代理或 Git 网络配置，也未强制推送、重置或覆盖已有提交。

## 公网协议与安全

端点：`https://multi-platform-search.onrender.com/mcp/`。
使用官方 Python MCP Client 1.29.0，服务 SDK 返回 1.30.0，协商协议 `2025-11-25`。

| 验收项 | 实际结果 |
|---|---|
| `/health`、`/ready` | 200，运行提交一致 |
| `/v1/search` | 200，3 条真实 Web 结果 |
| `/mcp/`、initialize、tools/list | 通过，无 421 |
| `multi_platform_search` | 返回 12 条；Web、Exa、YouTube、B站、知乎成功，小红书 partial |
| `search_platform` | YouTube 返回 3 条 |
| 无 token / 错 token / 缺 Bearer 前缀 | HTTP 与 MCP 均 401 |
| 限流 | 429，`Retry-After: 60`；用元数据请求测试，无额外搜索调用 |
| 只读工具标记 | 两项工具均通过 |
| 本地回归 | 10/10 通过 |
| 密钥审计 | 跟踪文件及 Git 历史未检出配置中的真实密钥或常见密钥格式；`.env` 未跟踪 |

公网 16 项检查全部通过，原始脱敏结果见 [最终公网证据](acceptance/public-final-2026-10-27.json)。第一次验收与回归日志也保留在 `acceptance/`。未把历史 20 条基准或 Docker 构建结果冒充本轮重测。

本轮修正了原认证实现会接受无 Bearer 前缀 token 的问题；不同大小写的 Bearer 头现在共用同一限流桶。限流仍为单进程内存窗口，重启后重置；`/ready` 不代表各 Provider 的额度或账号健康。审计不是对未知凭证和所有历史泄露的绝对保证。

## 各端实际接入

| 端 | 当前状态 |
|---|---|
| ChatGPT Web | 私有个人插件已创建，MCP URL、Bearer API-key 配置和 Skill 已核实保存；安装、授权和会话内工具调用未验收 |
| ChatGPT Mobile | 官方插件文档支持账户可用插件在移动端使用；本项目手机端工具调用仍待实际测试 |
| Codex | 可使用同一插件；当前会话未出现其工具，安装授权和新会话调用未验收 |
| Claude Web / Mobile | 官方支持 Remote MCP 与固定请求头；本轮未在 Claude 账号中添加或授权 |
| Notion Agent Skill | 项目内已保留可移植 Skill；未写入 Notion，未标记为已安装 |
| Notion Agent MCP | 官方要求 Business/Enterprise；实际套餐、管理员权限及连接未核实 |
| Notion Custom Agent MCP | 支持自定义服务与 Bearer 请求头，但需要 Business/Enterprise，运行还涉及积分；未启用 |

[打开 Multi-platform Search 私有插件](https://chatgpt.com/plugins/plugins_6ae07ee703088191bc6e129d10416226)。创建成功不等于已安装或已完成认证。只在官方安全字段填写现有 SERVICE_API_KEY，Provider 密钥留在 Render。

ChatGPT 的直接自定义 MCP 连接说明与完整插件的移动端说明不同；本轮采用已实际创建成功的私有插件路径，不据此宣称移动端已通过。Notion MCP 供外部 Agent 访问 Notion，与让 Notion Agent 调用本搜索服务是两个方向；Skill 本身不会建立实时连接。

浏览器界面操作因无法可靠确认当前 URL 被安全机制停止，未继续操作登录、凭证输入或授权界面。Render 控制台当前停在登录页，因此免费套餐、环境配置完整清单与账单状态未在控制台复核；运行版本和服务认证已通过真实公网响应核实。

## 开源采用与零成本

已重新检查官方 MCP Python SDK、Tavily MCP、Exa MCP：MIT 许可、未归档，最近提交分别为 10月24日、10月26日、10月19日。保留官方 SDK，参考两个 Provider 项目；它们不能直接替代现有六平台 Search Core。本轮没有引入套娃 MCP、Cookie 采集、视频下载或媒体整理功能，也未合并 Media Inbox。

继续沿用 Render Free 和已有 API 额度；本轮未购买服务、升级套餐或设置自动充值。没有定时保活。Tavily/Exa 账号原有账单与自动充值状态尚未核实，应用也没有金额预算硬限制，不能承诺无限调用永远免费。新增连接不应开启任何付费选项。

## 下一步（最多三项）

1. 在私有插件页面完成安装及服务 token 连接，再分别验收 ChatGPT Web、手机和 Codex 新会话的真实工具调用。
2. 在 Claude 添加同一 Remote MCP，在固定请求头中安全配置现有 Bearer token，再测试一条检索；账号登录和授权由本人操作。
3. 核对现有 Notion 套餐和自定义 MCP 权限；只有已具备所需套餐及免费可用权限时才连接。否则保留 Skill 工作流，不为本项目升级或购买积分。

## 官方依据

- [ChatGPT / Codex 插件与移动端](https://learn.chatgpt.com/docs/plugins)
- [插件 MCP 的 Bearer API-key 声明](https://developers.openai.com/plugins/build/plugins)
- [直接自定义 MCP 的限制](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
- [Claude Remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Notion Skills](https://www.notion.com/help/create-and-manage-skills)
- [Notion Agent MCP](https://www.notion.com/help/connect-mcp-servers-to-your-notion-agent)
- [Notion Custom Agent MCP](https://www.notion.com/help/mcp-connections-for-custom-agents)
- [Notion 积分与费用](https://www.notion.com/help/buy-and-track-notion-credits-for-custom-agents)
