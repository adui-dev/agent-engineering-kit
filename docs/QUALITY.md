# ✅ 仓库质量检查与版本维护

## 版本管理

[VERSION](../VERSION) 为当前版本的唯一来源，首个正式版本为 **V1.0**，记录见 [CHANGELOG](../CHANGELOG.md)。

## 运行方式

要求 Python 3.10+，**仅使用标准库，不需要额外安装依赖**。在仓库根目录执行：

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

Linux 环境可以用 `python3` 替代 `python`。校验脚本支持 `--root`，主要用于测试。

## 校验范围

| 检查 | 范围 |
| --- | --- |
| 核心文件 | VERSION、Prompt、README、AGENTS、CHANGELOG、Skills 索引和两个 Actions 工作流等 |
| 版本 | README、AGENTS、CHANGELOG、Prompt 与 VERSION 一致 |
| 本地链接 | 一方 Markdown 文件和各 Skill 主入口 SKILL.md 中的相对路径；排除外部地址和围栏代码示例 |
| Skills | 检查 `SKILL.md` frontmatter 的 name、description、目录名与索引、第三方许可文件 |
| 测试 | unittest 覆盖正常流程、错误链接、版本不一致、元数据错误及许可缺失 |

**不自动覆盖**：Markdown 锚点、外部网址可用性、第三方所有 reference 文件的语义校验、业务逻辑、实际 Actions 安全审计或运行效果。

## GitHub Actions

[质量检查工作流](../.github/workflows/quality.yml) 在 `main` 推送、针对 `main` 的 PR 和手动启动时运行。只有 `contents: read` 权限，不读取或传递 `CNB_TOKEN`。

[CNB 同步工作流](../.github/workflows/sync-cnb.yml) 独立执行；质量检查不会阻断同步。若希望通过强制通过检查才能合并，需要由仓库管理员在 Branch Ruleset 中配置必需检查。

## 提交前检查

1. 检查文件是否属于当前任务，是否无意修改了上游 Skills。
2. 运行两条本地检查命令。
3. 涉及 Actions 时额外审查事件触发权限、未经信任的输入、Secrets、checkout 凭据和 action 的固定 SHA。
4. 按 [中文 Emoji 提交规范](../CONTRIBUTING.md) 提交，查看 CI 结果。

## 更新约定

新增校验规则时同步更新 `scripts/validate_repository.py`、`tests/` 和本文档。不能为使校验通过而跳过真实错误，也不能将静态通过描述为全面运行验证。
