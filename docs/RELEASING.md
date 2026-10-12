# 📦 正式版本发布规范

本仓库的正式版本从 **V1.0** 开始；根目录 [VERSION](../VERSION) 记录展示版本，Git Tag 采用三段式格式。

| VERSION | Release 标题 | Git Tag | Release Notes |
| --- | --- | --- | --- |
| `V1.0` | `V1.0` | `v1.0.0` | [V1.0](releases/V1.0.md) |
| `V1.1` | `V1.1` | `v1.1.0` | [V1.1](releases/V1.1.md) |

映射规则：`V主版本.次版本` → `v主版本.次版本.0`。如未来需要补丁版号，应先更新版本规则、发布脚本和测试。

## 发布前检查

1. 确认中英文初始化 Prompt 在版本、16 个章节、关键安全约束和执行规则上保持一致，并与 Skills、许可证及对外文档一致。
2. 确认 `VERSION`、中英文 README、AGENTS、CHANGELOG 使用同一版本，且两份 README 的发布及功能描述同步。
3. 为本版本创建 `docs/releases/V主版本.次版本.md`，仅包含对外功能、用法和已知限制，不加入内部运维信息。
4. 在仓库根目录运行：

   ```bash
   python scripts/validate_repository.py
   python -m unittest discover -s tests -v
   ```

5. 审核变更并确认 GitHub Actions 质量检查通过，再由维护者在 `main` 上手动运行发布工作流。
6. 发布需要维护者明确授权；不得强制覆盖已有 Tag。

## 手动发布

[正式发布工作流](../.github/workflows/publish-release.yml) **仅支持 GitHub Actions 手动启动（workflow_dispatch）**，并且只允许从 `main` 分支执行发布阶段。普通 Push 或修改 VERSION/Release Notes **不会自动创建 Git Tag 或 Release**。

发布过程包含只读校验阶段和拥有最小写权限（`contents: write`）的 Release 阶段：

1. 校验版本格式和对应发布说明。
2. 运行仓库校验与单元测试。
3. 如果 Release 已存在则跳过，保留原有内容。
4. 如果 Tag 已存在但尚无 Release，则停止，要求人工核对。
5. 使用当次 `main` Commit 创建对应 Tag 与正式 Release，不发布为预发布或草稿。

**维护权限提示：** 发布由维护者明确发起。建议根据 [仓库维护设置](MAINTENANCE.md) 在 GitHub 配置 `main` 分支保护、必需的质量检查和 PR 审批。这项仓库设置需要管理员在 GitHub 中启用；仅增加文档并不会自动配置保护规则。GitHub 会自动生成源码 ZIP/TAR 快照。

## 发布后核对

- 在 [GitHub Releases](https://github.com/adui-dev/agent-engineering-kit/releases) 核实 Release 标题、Tag、状态及可下载源码。
- 确认 Tag 指向完成发布前校验的提交。
- 核实发布说明不包含仅供内部维护者使用的内容。
- 发布失败时先查阅 Actions 日志，不要直接改写已存在的版本 Tag。

## 维护约定

发布版本、工作流或质量门禁变化时同步本文档。历史 Release 和 Tag 不应在无明确理由与授权的情况下重写。
