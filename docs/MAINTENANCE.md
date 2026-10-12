# 🛡️ GitHub 仓库保护与维护设置

本文件说明由仓库管理员在 GitHub 网站配置的分支保护。代码和 CI 文件**不会自动启用 Ruleset**。本仓库的 `Protect main` 已启用；每次调整规则后都应重新确认实际配置。

## 当前已核实的保护规则（2026-10-12）

通过 [GitHub Ruleset #24911726](https://github.com/adui-dev/agent-engineering-kit/rules/24911726) 的配置核对：

| 配置 | 已核实状态 |
| --- | --- |
| Ruleset / 分支 | `Protect main` / 默认分支 `main` |
| 状态 | `Active` |
| 禁止删除 / 强制推送 | 已开启 |
| 必须通过 PR | 已开启，普通 PR 审批人数为 `0` |
| 三项必需 CI | Ubuntu Python 3.10、Ubuntu Python 3.13、Windows Python 3.13 |
| Bypass | 无绕过成员 |
| 分支必须同步最新 main | 未开启（可在无冲突时合并） |

**合并验收已完成：** [PR #1](https://github.com/adui-dev/agent-engineering-kit/pull/1) 在三个必需检查成功后通过正常 Squash Merge 合并至 `main`（合并 SHA `f6b37ca801705bab8e37b29223e0129950f7c7d1`）。[合并后 CI](https://github.com/adui-dev/agent-engineering-kit/actions/runs/38213891837) 三个平台再次全部通过。

## 1. 保护主分支

打开 [Settings → Rules → Rulesets](https://github.com/adui-dev/agent-engineering-kit/settings/rules)，新建 **Branch ruleset**，命名为 `Protect main`，目标选择默认分支 `main`。

建议开启：

- 禁止删除保护分支及强制推送。
- 要求质量检查通过后才允许合并。
- 团队协作时要求通过 Pull Request 合并，必要时要求至少一位非作者审核者。
- 不为自动化机器人授予不必要的绕过权限。

**个人维护特别注意：** 强制“至少 1 位审核者”会影响单人仓库的日常合并；请根据实际协作人数调整。启用禁止直接推送或必需检查会改变既有 `main` 直接提交流程，应先确认自己能够通过 PR 正常合并。

## 2. 必需 CI 检查

参照 [质量检查工作流](../.github/workflows/quality.yml)，在规则设置里选择**最近成功运行**的三个检查：

- Ubuntu / Python 3.10
- Ubuntu / Python 3.13
- Windows / Python 3.13

以 GitHub 实际显示的检查名称为准，不要凭文档猜测精确状态名称；首次运行完成后再设为 Required checks。可选择阻止检查未通过的合并。

## 3. 发布审批

[发布工作流](../.github/workflows/publish-release.yml) 仅支持维护者手动触发。进一步控制时，可在 Settings → Environments 配置 `release` 环境与审批者，并同步为工作流的发布作业增加 `environment: release`。**两处都配置并经过一次验证**，才能认为环境审批生效；仅设置名称没有强制审核效果。

## 4. 安全与协作入口

- 检查 Settings → Code security 中的漏洞私密报告与秘密扫描功能是否可用、是否启用。
- 保留 [SECURITY.md](../SECURITY.md)、Issue Templates、PR Template 和 CODEOWNERS 的准确性。
- 对依赖与第三方 Skills 定期进行来源、许可和执行风险复核。
- 不在公开 Issue、PR、Actions 日志和版本说明中粘贴访问令牌。

## 5. 启用后的人工验收

- [x] `main` 的规则集处于 Active 状态。
- [x] GitHub 显示三个必需的质量检查，提交测试 PR 时按预期运行。
- [ ] 强制推送和删除分支被拒绝（只需检查规则，不要在正式仓库实际试运行破坏性命令）。
- [x] 经过验证，合法贡献流程仍可正常合并（[PR #1](https://github.com/adui-dev/agent-engineering-kit/pull/1)）。
- [x] 发布工作流只提供手动触发，测试 PR 合并后未生成新的 Tag 或 Release。
- [ ] 如需发布审批，发布环境限制已通过一次安全测试。

## 6. 小型 PR 的真实验收流程

在功能或文档分支中提交**有实际用途的最小变更**，通过 Pull Request 合并至 `main`，不再直接推送受保护分支。

1. 基于当前 `main` 创建 `docs/…` 或 `feat/…` 分支，并在分支中提交修改。
2. 创建非 Draft PR，Base 指向 `main`，填写变更内容、验证范围和风险。
3. 在 PR 的 Checks 中核对三项精确名称：`✅ 质量检查 (ubuntu-latest, Python 3.10)`、`✅ 质量检查 (ubuntu-latest, Python 3.13)`、`✅ 质量检查 (windows-latest, Python 3.13)`。
4. 三项均完成并通过之前，**不要尝试绕过保护规则合并**；若结果失败，应修复分支后重新等待 CI。
5. CI 成功后由维护者通过正常 Merge/Squash 按钮合并，检查 PR 的 `merged` 状态和 `main` 新 Commit。
6. 合并后检查主分支质量工作流，记录 PR URL、实际检查结果、Merge SHA。合并不会自动发布 Git Tag 或 Release。

不要通过试验性强制推送/删除 `main` 来验证保护。遇到权限错误应停止并明确报告，不要添加机器人 Bypass 绕过规则。

**现状说明：** Ruleset、三个必需检查和真实 PR 合并已经完成验证。Release 环境审批功能尚未确认启用，不应宣称已配置。V1.2 的完整验收进度见 [发布前清单](V1.2_ACCEPTANCE.md)。
