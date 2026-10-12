# 🚀 Agent Engineering Kit

**简体中文** · [English](README.en.md)

[![Release](https://img.shields.io/github/v/release/adui-dev/agent-engineering-kit?label=Release)](https://github.com/adui-dev/agent-engineering-kit/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![质量检查](https://github.com/adui-dev/agent-engineering-kit/actions/workflows/quality.yml/badge.svg)](https://github.com/adui-dev/agent-engineering-kit/actions/workflows/quality.yml)

**让 AI Agent 不只是生成代码，而是理解项目、遵守规范、验证结果，并持续维护工程上下文。**

Agent Engineering Kit 是一套**技术栈无关、面向长期开发**的 AI Agent 工程化工具包。提供通用项目初始化 Prompt、可复用 Skills、协作约定和基础质量检查，适用于新建项目、已有代码仓库及 Monorepo。

> **当前版本：V1.1** · [正式发布](https://github.com/adui-dev/agent-engineering-kit/releases/tag/v1.1.0) · [更新日志](CHANGELOG.md)
>
> 这是供其他项目使用的**工程工具包**，不是业务应用框架。不会仅靠复制文档就自动生成可运行的业务系统。

## ✨ 能解决什么问题？

| 常见问题 | 本仓库提供的方案 |
| --- | --- |
| 新 Agent 接手项目缺少上下文 | 统一协作入口、项目状态与代码库索引 |
| 需求、架构与实现逐渐脱节 | 明确文档职责、需求追溯和更新约定 |
| 每次开发都要重复说明规则 | 通过 AGENTS 和按需加载的 Skills 复用流程 |
| AI 生成代码却没有经过验证 | 使用 Harness、真实测试和质量检查形成反馈闭环 |
| 新项目与现有项目需求不同 | 先识别实际仓库，再最小化增量初始化 |

适用对象：AI 编程工具使用者、独立开发者、团队工程项目及多 Agent 协作场景。支持 Web、移动端、后端、桌面端、游戏、工具库等项目，不绑定语言或框架。

## 🚀 3 步快速开始

**1. 打开目标项目**

在 Codex、OpenCode、Claude Code 或其他支持项目文件访问的 AI 编程工具中，打开你希望初始化的**目标项目工作区**，而不是本工具包仓库。

**2. 复制初始化指令**

选择并打开 **[📋 中文初始化 Prompt V1.1](prompts/project-initialization.zh-CN.md)** 或 **[English Prompt V1.1](prompts/project-initialization.en.md)**，将对应语言的完整指令发送给 AI Agent。两版均覆盖相同的 16 个章节和核心工程约束。

**3. 审核实际交付**

Agent 应先检查目标仓库，再根据真实需求创建或补全必要文档、Skills 与 Harness，执行能够运行的检查，并说明修改文件、验证结果和待确认事项。

你可以附加这段任务要求：

> 请按上述项目初始化 Prompt V1.1 执行。先分析当前仓库及已有规范，保持最小必要改动，区分已实现、规划中与待确认内容；实际创建所需文件并验证，不要只输出通用模板。

**重要：** 目标工具必须具备相应的文件读写和执行权限；不能执行时应如实说明。完整流程由目标项目自行维护，不要求将本仓库整体复制进去。

## 🧰 可选：命令行安全初始化

如果希望在目标项目中保存 Prompt 或安装指定 Skills，可使用无外部依赖的 Python 初始化工具（Python 3.10+）：

```powershell
# 预览（默认不写入）
python scripts/init.py --target ../my-project --lang zh-CN --skill git-commit

# 确认无冲突后应用
python scripts/init.py --target ../my-project --lang zh-CN --skill git-commit --apply
```

可以加上 `--agent codex`、`--agent opencode` 或 `--agent claude-code`，选择适配的 Skills 目录（Claude Code 使用 `.claude/skills/`）。脚本只负责复制选定的 Prompt 与 Skills，**不自动生成项目文档、执行 Skill 或覆盖已有文件**。本仓库还提供 Windows/Linux/macOS 均可执行的 `python scripts/smoke_init.py` 安装验收及 [只读文件完整性校验](scripts/verify_installation.py)。详见 [安装使用说明](docs/INSTALLATION.md)、[可运行示例与验收](docs/EXAMPLES.md)。

## 🧭 八大核心工程资产

| 资产 | 解决的问题 |
| --- | --- |
| **AGENTS** | AI Agent 如何协作、遵循哪些规则 |
| **REQUIREMENTS** | 项目要实现什么，以及如何验收 |
| **SDD** | 模块、接口、数据和核心流程如何设计 |
| **ARCHITECTURE** | 系统如何组织，技术方案为何这样选择 |
| **PROJECT_CONTEXT** | 项目背景、真实进度、决策和遗留事项 |
| **CODEBASE_MAP** | 关键代码、配置、模块在哪里 |
| **Skills** | 哪些任务具有可复用的专项工作流 |
| **Harness** | 如何启动、检查、测试和验证修改 |

按项目实际情况还可加入 **ADR（架构决策记录）** 和 **Documentation Validation（文档自动校验）**，不为凑齐文件而增加无效模板。

**持续开发闭环：**

```text
理解需求 → 加载上下文 → 设计与影响分析 → 最小实现
   ↑                                      ↓
交付结果 ← 更新相关文档 ← 测试与质量验证
```

## 🧩 内置 Skills

仓库当前收录 **8 项项目级 Skills**，按需使用：

| 类别 | Skills |
| --- | --- |
| Git 提交 | [git-commit](.agents/skills/git-commit/SKILL.md)、[conventional-commit](.agents/skills/conventional-commit/SKILL.md) |
| Issues | [github-issues](.agents/skills/github-issues/SKILL.md)、[根据实施计划创建 Issues](.agents/skills/create-github-issues-feature-from-implementation-plan/SKILL.md) |
| Pull Requests | [根据规格说明创建 PR](.agents/skills/create-github-pull-request-from-specification/SKILL.md) |
| GitHub Actions | [安全加固](.agents/skills/github-actions-hardening/SKILL.md)、[效率优化](.agents/skills/github-actions-efficiency/SKILL.md)、[工作流规格说明](.agents/skills/create-github-action-workflow-specification/SKILL.md) |

详细的来源、版本、许可与适用限制参见 [Skills 索引](docs/SKILLS.md)。

Skills 存放在 `.agents/skills/`。**能否自动发现由所用 AI 编程工具决定**；需要额外的 GitHub 连接或执行权限时，应单独配置。部分上游技能为历史版本，使用前请核对兼容性。

## 📁 仓库导航

| 路径 | 内容 |
| --- | --- |
| [中文初始化 Prompt](prompts/project-initialization.zh-CN.md) / [English Prompt](prompts/project-initialization.en.md) | 对应语言的完整项目初始化与持续开发指令 |
| [AGENTS.md](AGENTS.md) | 本仓库的 Agent 协作规则 |
| [Skills 索引](docs/SKILLS.md) | 技能使用方式、来源与维护约定 |
| [质量检查说明](docs/QUALITY.md) | 本地验证、CI 和检查边界 |
| [CLI 安装说明](docs/INSTALLATION.md) | 安全预览、选择语言与 Skills、拒绝覆盖 |
| [示例与验收](docs/EXAMPLES.md) | 空仓库与已有 Python 项目示例、自动验证 |
| [工具兼容性](docs/COMPATIBILITY.md) | Codex、OpenCode、Claude Code 的待验证项 |
| [端到端验收](docs/AGENT_ACCEPTANCE.md) | 客户端发现、Skill 调用和真实初始化验收 |
| [验收工作区准备工具](scripts/prepare_agent_acceptance.py) | 在仓库外安全创建 Codex/OpenCode/Claude Code 测试项目 |
| [安全政策](SECURITY.md) | 私密漏洞报告和供应链风险说明 |
| [仓库维护设置](docs/MAINTENANCE.md) | 主分支保护、必需 CI 与发布审批操作 |
| [贡献指南](CONTRIBUTING.md) | 中文、Emoji 和 Conventional Commits 规范 |
| [发布说明](docs/RELEASING.md) | 版本管理、发布检查与 Release 工作流程 |
| [更新日志](CHANGELOG.md) | 已发布版本与后续未发布变更 |
| `.agents/skills/` | 项目级 Skills 与其参考资料 |
| `scripts/`、`tests/` | 仓库质量检查脚本与测试 |

以上为**面向使用者的主要入口**，不是完整文件树。

## ✅ 质量检查

贡献本仓库时，使用 **Python 3.10+**，无需安装额外 Python 依赖：

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

检查覆盖版本一致性、相对 Markdown 链接、Skills 基础结构和许可证文件，并通过 GitHub Actions 在 Push / Pull Request 时运行。静态检查**不等于**业务功能测试、Agent 工具兼容性测试或全面安全审计。

## 📦 版本、贡献与许可证

- **当前开发分支**：`main`；**最新正式发布**：[V1.1 / v1.1.0](https://github.com/adui-dev/agent-engineering-kit/releases/tag/v1.1.0)；[首个正式版本 V1.0](https://github.com/adui-dev/agent-engineering-kit/releases/tag/v1.0.0)。
- **注意版本差异**：`main` 会持续更新，`v1.1.0` 与 `v1.0.0` 对应的 Release 源码快照不会随之改变。
- **贡献方式**：请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，提交格式为 `type(scope): emoji 中文描述`。
- **开源许可**：[MIT License](LICENSE)。第三方 Skills 保留各自的版权和许可声明。

如需协助或反馈，可以在 [GitHub Issues](https://github.com/adui-dev/agent-engineering-kit/issues) 提出问题或建议。
