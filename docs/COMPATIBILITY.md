# 🔧 Agent 工具兼容性矩阵

当前统一的初始化 Prompt 由普通 Markdown 文件提供；CLI 负责安全复制 Prompt 和选定 Skills，**不代表任何工具已完成端到端 Agent 初始化测试**。

| 工具 | Prompt 阅读 | `.agents/skills/` 自动发现 | 实际端到端初始化 |
| --- | --- | --- | --- |
| Codex | 需通过对应工作区/提示词入口使用 | `.agents/skills/`（文档适配，未实测） | 待验证 |
| OpenCode | 需通过对应工作区/提示词入口使用 | `.agents/skills/`（官方文档支持，未实测） | 待验证 |
| Claude Code | 需通过对应工作区/提示词入口使用 | `.claude/skills/`（官方文档支持，未实测） | 待验证 |

## 建议实测方法

1. 在干净的、可丢弃的目标仓库中使用 [CLI](../scripts/init.py) 和 `--agent codex|opencode|claude-code` 安装中文或英文 Prompt 及必要 Skills。
2. 根据目标工具的正式说明核对可用 Skills 位置及实际权限，不盲目假设通用发现规则。
3. 由 Agent 读取 Prompt 并完成工程审查，记录真实新增文件与运行结果。
4. 根据 [示例验收标准](EXAMPLES.md) 核验真实目录、命令、测试及文档同步。
5. 记录工具版本、操作系统、安装方法、可用权限、失败原因和验证日期，再更新矩阵。

兼容性状态应基于**实际执行结果**更新；不要将“文档提到支持某工具”或“目录中存在 Skill”当作通过测试。

## 可核查的官方路径说明

- [OpenCode：Agent Skills](https://opencode.ai/docs/skills) 明确列出项目兼容目录 `.agents/skills/<name>/SKILL.md`。
- [Claude Code：Skills](https://code.claude.com/docs/en/skills) 使用项目级 `.claude/skills/<name>/SKILL.md`。
- [Codex：Agent Skills](https://developers.openai.com/codex/skills) 请按当前官方版本核对发现目录及加载行为。

CLI 的自动化测试已验证文件被复制到对应路径；**尚未通过各客户端真实启动、Skill 发现和任务执行来验证端到端兼容性**。
