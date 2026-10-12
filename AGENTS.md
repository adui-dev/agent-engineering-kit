# Agent Engineering Kit · AI 协作规则

## 项目定位

本仓库收录跨技术栈复用的 AI Agent 工程化 Prompt、项目模板及经核查的 Skills。本仓库**不是**由初始化 Prompt 生成的业务应用；不要在这里自动创建虚构业务需求或服务端工程。

## 入口

- [项目初始化 Prompt V2.0](prompts/project-initialization.zh-CN.md)
- [README](README.md)
- [提交规范](CONTRIBUTING.md)
- [git-commit Skill](.agents/skills/git-commit/SKILL.md)

## 开发规则

1. 开发前检查仓库现状与相关文件，只作任务必要的变更。
2. 规范与文档优先使用简体中文；对外必要的英文说明可另行提供。
3. Prompt 必须通用，不预设技术栈，也不虚构项目状态、命令或检查结果。
4. 引入第三方 Skill 前确认来源、安全与许可，保留上游归属。
5. 不提交密钥、Token、私人配置，不覆盖未提交的用户修改。
6. 仅在用户授权时提交或推送；先审查 diff，不绕过 Git hooks。
7. 提交遵循 Conventional Commits：`type(scope): emoji 中文描述`，详情见 CONTRIBUTING.md。
8. 修改 Prompt 应检查结构、链接和内容一致性；修改 Skill 时更新相应来源记录。

## 交付要求

说明修改文件、原因、验证方法与结果，并清晰区分已执行和未执行的工作。

## 更新约定

仓库规则、文档入口、提交约定和安全边界变化时更新本文件；普通内容更新不需重写。