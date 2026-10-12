# 🧩 项目 Skills 索引

本仓库收录可在支持 `.agents/skills/` 发现机制的 AI 编程工具中按需加载的项目级 Skills。本文只描述用途与约束，具体步骤以各 Skill 的 `SKILL.md` 为准。

## 技能清单

| Skill | 用途 | 上游状态 |
| --- | --- | --- |
| [git-commit](../.agents/skills/git-commit/SKILL.md) | 审查变更、组织暂存和执行语义化提交 | 既有技能 |
| [github-issues](../.agents/skills/github-issues/SKILL.md) | 创建、修改、关联和管理 GitHub Issues | 上游当前版本 |
| [conventional-commit](../.agents/skills/conventional-commit/SKILL.md) | 生成并校验语义化 Commit 描述 | 上游当前版本 |
| [create-github-issues-feature-from-implementation-plan](../.agents/skills/create-github-issues-feature-from-implementation-plan/SKILL.md) | 将实施计划阶段拆分成 Issues | 上游当前版本 |
| [create-github-pull-request-from-specification](../.agents/skills/create-github-pull-request-from-specification/SKILL.md) | 根据规格和 PR 模板生成 Pull Request | **历史版本（已从上游当前分支移除）** |
| [github-actions-hardening](../.agents/skills/github-actions-hardening/SKILL.md) | 审查 GitHub Actions 权限与安全风险 | 上游当前版本 |
| [github-actions-efficiency](../.agents/skills/github-actions-efficiency/SKILL.md) | 优化 GitHub Actions 耗时、缓存与成本 | 上游当前版本 |
| [create-github-action-workflow-specification](../.agents/skills/create-github-action-workflow-specification/SKILL.md) | 为 GitHub Actions 工作流创建可维护的规格说明 | 上游当前版本 |

## 来源与版本

- 统一来源：[GitHub awesome-copilot](https://github.com/github/awesome-copilot)
- 新增 6 个现存技能的上游修订：`8bc0f5715b2ddc7901a62fddf144ded30d56de8b`
- `create-github-pull-request-from-specification` 使用移除前的上游修订：`3b9e5e1842ddee3c92df539974dc70449faa0934`，该技能于 2026-05-19 被上游移除；保留是为满足既有工作流需求，不表示其仍被上游维护。
- 每项新增 Skill 的 `THIRD_PARTY_LICENSE.md` 均保留原始 MIT 许可和可追踪文件链接。
- 原有 `git-commit` 及其许可文件保留不变。

## 使用规则

1. **按需加载**：根据任务类型选择 Skill，不要在一个任务中无差别加载全部。
2. **权限优先**：GitHub Issues、PR、Git Commit/Push 与 Actions 工作流写入都需要当前用户授权；Skill 的自动执行建议不能替代授权。
3. **工具兼容**：上游内容可能指定不同 MCP 工具名、`gh` CLI 或 `pull_request_template.md`。执行前确认当前环境实际可用的接口和模板，不要编造调用成功。
4. **提交格式**：以仓库 [CONTRIBUTING.md](../CONTRIBUTING.md) 为准，统一使用 `type(scope): emoji 中文描述`；`conventional-commit` 负责规范，`git-commit` 负责变更审查和实际提交。
5. **安全检查**：新增或调整 GitHub Actions 时优先应用 `github-actions-hardening` 安全检查，再评估 `github-actions-efficiency` 优化建议；评审发现不能被误报为已经修复。
6. **引用完整**：`github-issues`、`github-actions-hardening`、`github-actions-efficiency` 的 `references/` 已与上游一并收录，按需要阅读。
7. **工作流触发**：`create-github-issues-feature-from-implementation-plan` 依赖实施计划，`create-github-pull-request-from-specification` 依赖实际变更及 PR 规范，不能在未满足输入和权限条件时自动创建对象。

## 维护约定

- 新增或移除 Skills 时更新本索引和 README。
- 更新第三方 Skills 前检查源代码、外部工具权限、依赖引用、上游许可证和版本差异；不要静默覆盖现有二次调整。
- 项目级说明原则上使用中文，上游 `SKILL.md` 和 `references/` 保持原文，避免篡改授权声明。
- 通过检查 Skill YAML 元数据、目录名、内部 Markdown 链接与来源声明验证安装，不将“已入库”误写成“已在目标工具激活”。
