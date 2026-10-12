# 🛡️ GitHub 仓库保护与维护设置

本文件记录在 GitHub 网站中由仓库管理员**手动启用**的设置。仓库中新增 CI 文件并不自动开启分支保护。

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

- [ ] `main` 的规则集处于 Active 状态。
- [ ] GitHub 显示三个必需的质量检查，提交测试 PR 时按预期运行。
- [ ] 强制推送和删除分支被拒绝（只需检查规则，不要在正式仓库实际试运行破坏性命令）。
- [ ] 经过验证，合法贡献流程仍可正常合并。
- [ ] 发布工作流不会在普通 Push 中自行运行。
- [ ] 如需发布审批，发布环境限制已通过一次安全测试。

**现状声明：** 自动化工具能够创建和验证工作流，但本仓库的 Rulesets 与 Environment 审批等管理员设置必须在 GitHub 侧另行确认，不将这份文档视为已启用分支保护的证据。
