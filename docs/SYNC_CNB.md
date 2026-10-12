# 🔄 GitHub → CNB 仓库单向同步

> 状态：工作流已配置；首次远端同步是否成功，以 GitHub Actions 运行结果为准。

## 同步目标

- 源仓库：[adui-dev/agent-engineering-kit](https://github.com/adui-dev/agent-engineering-kit)。
- 目标仓库：[adui-studio/agent-engineering-kit](https://cnb.cool/adui-studio/agent-engineering-kit)。
- 配置文件：[sync-cnb.yml](../.github/workflows/sync-cnb.yml)。
- 同步方向：GitHub → CNB，仅将 GitHub `main` 分支推送到 CNB `main`。
- 触发方式：GitHub `main` Push 自动触发；可从 Actions 页面使用 `Run workflow` 手动执行。
- 检出完整 Git 历史，但不推送其他分支或 Tags。不会删除目标仓库已有分支、Tag 或其他内容。

## 凭据与权限

工作流使用 GitHub 仓库 `Settings → Secrets and variables → Actions → Repository secrets` 中的 `CNB_TOKEN`。

CNB 官方 Git HTTPS 认证采用用户名 `cnb`、密码为访问令牌。**CNB 访问令牌需要对目标仓库具备推送（写入）权限**；只读的部署令牌不能用于该工作流。

- Token 仅在推送步骤的环境变量中使用。
- Git remote URL 不包含 Token；通过临时 `GIT_ASKPASS` 文件读取环境变量完成认证。
- 工作流结束即删除临时脚本；不在仓库中保存凭据。
- GitHub `GITHUB_TOKEN` 只申请 `contents: read` 权限。

## 第一次运行

1. 确保目标 CNB 仓库已经创建且允许此 Token 推送。
2. 打开 [GitHub Actions](https://github.com/adui-dev/agent-engineering-kit/actions/workflows/sync-cnb.yml)。
3. 选择 `🔄 同步代码至 CNB` → `Run workflow` → `main`。
4. 打开运行日志，确认 `🚀 推送 main 分支至 CNB` 成功。
5. 打开 [CNB 仓库](https://cnb.cool/adui-studio/agent-engineering-kit) 对比 `main` HEAD 的 Commit SHA。

后续 GitHub `main` 分支每次推送都会自动触发同步。

## 失败排查

| 现象 | 处理方法 |
| --- | --- |
| `CNB_TOKEN` 为空 | 检查 Repository Secrets 名称是否严格为 `CNB_TOKEN`，并确认可用于该 Actions 工作流。 |
| HTTP 401 / 403 | 检查 Token 是否过期、是否具备目标仓库代码写权限；不要在日志中打印 Token。 |
| `non-fast-forward` / `fetch first` | CNB `main` 含有 GitHub 没有的提交（例如 CNB 初始化 README）。**不会自动强制推送**。先备份并人工审查差异，再决定如何处理；不要直接在工作流中增加 `--force`。 |
| 网络或服务端错误 | 在 Actions 页面重试，检查 CNB 服务和外部网络。 |
| 手动同步时分支不一致 | `Run workflow` 选择 `main`，不要从其他分支运行。 |

## 安全与维护约定

- 同步流程仅对受控的 `main` 变更运行，避免在来自 Fork 的 Pull Request 环境中暴露密钥。
- 不使用 `--mirror` 或 `--force`，避免删除或覆盖 CNB 的独立历史。
- 使用锁定 SHA 的官方 `actions/checkout`，关闭凭据持久化；同步任务无需依赖安装、构建或执行仓库脚本。
- 更改同步范围、分支策略、令牌名称或认证方式时，同步更新此文档并运行 YAML/脚本语法与安全检查。
- 本文不表示已经成功访问目标 CNB 仓库或确认目标分支历史。

参考：[CNB Git 地址与认证说明](https://docs.cnb.cool/zh/guide/git-access.html)、[CNB 访问令牌](https://docs.cnb.cool/zh/guide/access-token.html)。
