# 🚀 Agent Engineering Kit

**当前版本：V1.0（首个正式版本）** · [更新日志](CHANGELOG.md)

一套技术栈无关、可持续维护的 **AI Agent 工程化开发指令、可复用 Skills 与质量约束**。

面向 Codex、OpenCode、Claude Code 等能够读取项目工作区的 AI 编程工具，适用于新建项目、已有项目和 Monorepo。

## 🎯 定位与范围

本仓库是供其他项目**复制、参考和接入**的工程工具包，**不是**实际业务应用。初始化 Prompt 版本从 **V1.0** 起算，和此前讨论草稿的迭代编号无关。

工程体系包括需求、详细设计、架构、项目上下文、代码索引、Skills、Harness 以及 AGENTS 协作约定；可按需求扩展 ADR 和自动文档校验。

## ✨ 核心能力

- 📋 **八大工程资产**：AGENTS、REQUIREMENTS、SDD、ARCHITECTURE、PROJECT_CONTEXT、CODEBASE_MAP、Skills、Harness。
- 🧭 **识别项目状态**：区分空仓库、已有工程、已有部分规范和 Monorepo。
- 🏗️ **可追溯的工程决策**：需求、设计、实现、测试和 ADR。
- 🧩 **8 个项目级 Skills**：Git、GitHub Issues、PR、GitHub Actions 安全与效率。
- ✅ **轻量质量检查**：自动校验版本、Markdown 相对链接、Skills 元数据及许可声明。

## 🚀 快速使用

1. 在 AI 编程工具中打开**需要初始化的目标项目**，不要把本仓库当作业务项目。
2. 复制 [通用项目初始化 Prompt V1.0](prompts/project-initialization.zh-CN.md) 全文，并发送给有权限读写目标仓库的 Agent。
3. 要求 Agent 先检查真实代码、项目背景、已有配置和文档，再最小化生成八大资产及适用的增强机制。
4. 审核 Agent 的变更文件、真实检查结果、待决策事项和后续维护建议。生成结果应保存在**目标仓库**中。

**示例指令：**

> 请执行我提供的「AI Agent 驱动项目工程体系初始化与持续开发总指令 V1.0」。先审查当前仓库，再按实际情况建立工程资产与必要配置。只做必要修改，不编造未确认的业务信息，执行可用检查并提交完整结果报告。

注意：仅复制 Prompt 不等于已经执行初始化。若 Agent 无法访问仓库或运行命令，必须明确告知限制。

## 📁 面向使用者的仓库结构

```text
agent-engineering-kit/
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── VERSION
├── CHANGELOG.md
├── LICENSE
├── prompts/
│   └── project-initialization.zh-CN.md
├── docs/
│   ├── SKILLS.md
│   └── QUALITY.md
├── .agents/
│   └── skills/                 # 8 个项目级 Skills
├── scripts/
│   └── validate_repository.py
├── tests/
│   └── test_validate_repository.py
└── .github/
    └── workflows/
        └── quality.yml
```

以上为面向使用者的主要文件索引，并非完整仓库文件树。

## 🧩 Skills

项目已有 8 个 Skills，包含 `git-commit`、`conventional-commit`、`github-issues` 及 GitHub Actions 专项能力。详见 [Skills 索引](docs/SKILLS.md)，包含来源版本、历史 Skill 风险及使用边界。

仓库中的 Skills **不保证自动被所有工具发现**；使用者需要根据 Agent 工具的机制确认发现目录、外部连接及执行权限。

## ✅ 本地质量检查

使用 **Python 3.10+**，不依赖外部 Python 包，在仓库根目录运行：

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

GitHub Actions 会在提交至 `main`、面向 `main` 的 Pull Request 以及手动触发时运行相同检查；详见 [质量检查说明](docs/QUALITY.md)。

## 🤝 贡献与版本维护

默认采用**简体中文 + Emoji Conventional Commits**，规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

当前版本由 [VERSION](VERSION) 确定，发布记录与更新约定见 [CHANGELOG.md](CHANGELOG.md)。

## 📄 License

本仓库使用 [MIT License](LICENSE)。第三方 Skills 各自目录中的 `THIRD_PARTY_LICENSE.md` 保留上游授权及归属信息。
