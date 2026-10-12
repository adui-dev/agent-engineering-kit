# 🔧 Agent 工具兼容性矩阵

当前统一的初始化 Prompt 由普通 Markdown 文件提供；CLI 负责安全复制 Prompt 和选定 Skills，**不代表任何工具已完成端到端 Agent 初始化测试**。

| 工具 | Skills 文档目录 | 文件安装与完整性校验 | 客户端发现/调用 | 真实项目初始化 |
| --- | --- | --- | --- | --- |
| Codex | `.agents/skills/` | CI 已验证文件安装 | 待客户端实测 | 待客户端实测 |
| OpenCode | `.agents/skills/` | CI 已验证文件安装 | 待客户端实测 | 待客户端实测 |
| Claude Code | `.claude/skills/` | CI 已验证文件安装 | 待客户端实测 | 待客户端实测 |

## 分层验收

按 [真实 Agent 端到端验收](AGENT_ACCEPTANCE.md) 中的 L1–L5 步骤，先用 [只读完整性检查](../scripts/verify_installation.py) 核对安装文件，再在真实客户端测试 Skill 的自动发现、原生调用及项目初始化。直接读取 `SKILL.md` 不能单独证明客户端的技能发现成功。

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

CLI 的自动化测试已验证文件安装路径，独立完整性校验可比较文件内容哈希；**尚未通过真实客户端启动、Skill 发现与任务执行来验证端到端兼容性**。
