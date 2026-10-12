# 🚀 Agent Engineering Kit

一套技术栈无关、可持续维护的 **AI Agent 工程化开发指令与协作规范**。

面向 Codex、OpenCode、Claude Code 及其他支持读取项目文件的 AI 编程工具，帮助全新项目、已有项目和 Monorepo 建立长期可维护的工程体系。

## ✨ 核心能力

- 📋 八大核心资产：AGENTS、REQUIREMENTS、SDD、ARCHITECTURE、PROJECT_CONTEXT、CODEBASE_MAP、Skills、Harness
- 🧭 兼容空仓库、已有代码和多模块项目
- 🏗️ ADR：重要架构决策的可追溯记录
- ✅ Documentation Validation：可逐步落地的文档与链接检查
- 🔄 需求、设计、实现、测试与文档同步闭环
- 📝 git-commit、conventional-commit + Emoji 与中文 Conventional Commits 规范
- 🔗 GitHub Issues、PR 自动化和 GitHub Actions 安全与效率 Skills

## 🚀 快速使用

1. 打开希望初始化的**目标项目**工作区，而不是本仓库。
2. 复制 [通用初始化 Prompt V2.0](prompts/project-initialization.zh-CN.md) 全文。
3. 发送给你使用的 AI 编程 Agent，要求其检查目标仓库、按需生成工程规范并实际验证。
4. 每个项目的结果由各自仓库保存和维护，不应反向覆盖本仓库的通用 Prompt。

## 📁 仓库内容

```text
AGENTS.md
CONTRIBUTING.md
README.md
docs/
  SKILLS.md
prompts/
  project-initialization.zh-CN.md
.agents/skills/
  git-commit/
  github-issues/
  conventional-commit/
  create-github-issues-feature-from-implementation-plan/
  create-github-pull-request-from-specification/
  github-actions-hardening/
  github-actions-efficiency/
  create-github-action-workflow-specification/
```

## 🧩 Skills 一览

已收录 8 项项目级 Skills（含既有的 git-commit）。请查看 [Skills 索引](docs/SKILLS.md)，包含功能说明、上游版本、兼容性提示及使用约束。

注意：Skills 仅随仓库分发，能否在目标 AI 编程工具中自动发现，取决于该工具对 `.agents/skills` 的支持；GitHub 操作也需要相应连接、凭据和明确授权。

## 🔄 GitHub → CNB 自动同步

每次推送 GitHub `main` 分支时，自动使用 Actions Secret `CNB_TOKEN` 将该分支同步至 [CNB 镜像仓库](https://cnb.cool/adui-studio/agent-engineering-kit)。也支持手动运行，不使用强制推送。首次运行与冲突排查见 [同步说明](docs/SYNC_CNB.md)。

## 🛠️ 开发与提交

仓库贡献约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。默认使用中文和 Emoji 提交消息；引入第三方 Skills 必须注明上游及许可。

## 📄 License

本仓库采用 MIT License，详见已有的 [LICENSE](LICENSE)。第三方 Skill 的版权及许可另见其目录中的来源声明。
