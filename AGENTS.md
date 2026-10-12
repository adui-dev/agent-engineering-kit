# Agent Engineering Kit · AI 协作规则（V1.1）

## 项目定位

本仓库收录跨技术栈复用的 AI Agent 工程化 Prompt、项目模板及经核查的 Skills。本仓库**不是**由初始化 Prompt 生成的业务应用；不要在这里自动创建虚构业务需求或服务端工程。

## 入口

- [中文初始化 Prompt V1.1](prompts/project-initialization.zh-CN.md)
- [English Initialization Prompt V1.1](prompts/project-initialization.en.md)
- [中文 README](README.md)
- [English README](README.en.md)
- [提交规范](CONTRIBUTING.md)
- [Skills 清单与使用边界](docs/SKILLS.md)
- [版本与更新日志](CHANGELOG.md)
- [质量检查规范](docs/QUALITY.md)
- [版本发布规范](docs/RELEASING.md)
- [CLI 安全安装](docs/INSTALLATION.md)
- [示例与验收](docs/EXAMPLES.md)
- [安全政策](SECURITY.md)
- [GitHub 仓库保护设置](docs/MAINTENANCE.md)
- [git-commit Skill](.agents/skills/git-commit/SKILL.md)

## 开发规则

1. 开发前检查仓库现状与相关文件，只作任务必要的变更。
2. 规范与文档优先使用简体中文；对外必要的英文说明可另行提供。
3. Prompt 必须通用，不预设技术栈，也不虚构项目状态、命令或检查结果。
4. 引入第三方 Skill 前确认来源、安全与许可，保留上游归属。
5. 不提交密钥、Token、私人配置，不覆盖未提交的用户修改。
6. 仅在用户授权时提交或推送；先审查 diff，不绕过 Git hooks。
7. 提交遵循 Conventional Commits：`type(scope): emoji 中文描述`，详情见 CONTRIBUTING.md。
8. 修改 Prompt 应检查结构、链接和内容一致性；修改 Skill 时同步更新 [Skills 索引](docs/SKILLS.md) 与来源记录。
9. 根据任务按需加载 Skills，保留上游文档原文。若 Skill 示例与本仓库提交规范或用户授权要求冲突，以本仓库安全与协作规则为准。
10. Issue 创建/更新、PR 创建/发布、代码提交/推送以及工作流变更属于外部或仓库写入操作，必须以用户授权为前提；不得因为 Skill 中写有“自动执行”就跳过授权。
11. 仓库正式版本以根目录 `VERSION` 为准，当前 V1.1。版本变化应同步 Prompt、README 和 CHANGELOG。
12. 创建 Release 前核对版本、发布说明、质量检查和授权；禁止覆盖历史 Tag，发布规范详见 [docs/RELEASING.md](docs/RELEASING.md)。
13. README.md 与 README.en.md 分别提供中文和英文说明；中文 Prompt `prompts/project-initialization.zh-CN.md` 与英文 Prompt `prompts/project-initialization.en.md` 必须章节完整、语义一致、版本同步。翻译仅改变语言，不得放宽权限、安全、测试和交付要求。
14. CLI 安装工具默认 dry-run，不覆盖已有项目文件。Release 只能在获授权后手动启动，日常 Push 不得自动发布。
15. 修改项目文档或 Skills 后，运行 `python scripts/validate_repository.py` 和 `python -m unittest discover -s tests -v`；检查的静态结果不能替代真实运行测试或安全审计。

## 交付要求

说明修改文件、原因、验证方法与结果，并清晰区分已执行和未执行的工作。

## 更新约定

仓库规则、文档入口、提交约定和安全边界变化时更新本文件；普通内容更新不需重写。
