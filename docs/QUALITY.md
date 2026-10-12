# ✅ 仓库质量检查与版本维护

## 版本管理

[VERSION](../VERSION) 为当前版本的唯一来源，首个正式版本为 **V1.0**，当前版本为 **V1.1**；版本记录见 [CHANGELOG](../CHANGELOG.md)。

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
| 核心文件 | VERSION、双语 Prompt/README、AGENTS、CHANGELOG、Skills 索引、初始化 CLI 和质量检查工作流等 |
| 版本 | 两份 README、中英文 Prompt、AGENTS、CHANGELOG 与 VERSION 一致 |
| 本地链接 | 根目录 Markdown（包含中英文 README）、docs、prompts 和 Skill 主入口 SKILL.md 的相对路径；排除外部地址和围栏代码示例 |
| Skills | 检查 `SKILL.md` frontmatter 的 name、description、目录名与索引、第三方许可文件 |
| 测试 | unittest 覆盖仓库结构及 CLI 的预览、冲突、符号链接、回滚等安全路径；Smoke Test 验证真实文件复制和已有项目回归 |

**不自动覆盖**：Markdown 锚点、外部网址可用性、第三方所有 reference 文件的语义校验、业务逻辑、实际 Actions 安全审计或运行效果。

## 双语文档约定

[中文 README](../README.md) 为 GitHub 默认入口，[English README](../README.en.md) 提供英文介绍。两份 README 应互相链接，并保证版本、功能范围和使用说明一致。校验脚本检查英文 README 是否存在、版本标识及相对链接；**内容的语义对齐仍需人工审查**。完整项目初始化 Prompt 同时维护 [中文](../prompts/project-initialization.zh-CN.md) 和 [英文](../prompts/project-initialization.en.md) 两个版本。校验会核对两版版本号与主章节、八类资产对应的子章节；**自动结构校验不能代替翻译语义审查**。

## 安全初始化与使用验收

安装命令和覆盖防护见 [安装说明](INSTALLATION.md)；空项目、可执行的既有代码示例及验收边界见 [示例与验收](EXAMPLES.md)。自动脚本仅验证复制/现有项目测试，不能宣称已经实际运行 AI Agent。

## GitHub Actions

[质量检查工作流](../.github/workflows/quality.yml) 在 `main` 推送、针对 `main` 的 PR 和手动启动时运行。只有 `contents: read` 权限。

如需通过强制质量检查才能合并，需要由仓库管理员在 Branch Ruleset 中配置必需检查。

质量检查会执行：

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s examples/existing-python/tests -v
bash scripts/smoke_init.sh
```

其中 `bash` 检查用于 Linux CI 或 Bash 环境；Windows 可运行 Python 部分。

## 版本发布检查

首个稳定版为 **V1.0**（Git Tag `v1.0.0`）。[发布规范](RELEASING.md) 要求在创建 Tag 与 Release 前校验当前版本、发布说明、Skills 和单元测试；发布工作流具有独立只读验证与最小写权限的发布步骤，不修改已有 Release。

## 提交前检查

1. 检查文件是否属于当前任务，是否无意修改了上游 Skills。
2. 运行两条本地检查命令。
3. 涉及 Actions 时额外审查事件触发权限、未经信任的输入、Secrets、checkout 凭据和 action 的固定 SHA。
4. 按 [中文 Emoji 提交规范](../CONTRIBUTING.md) 提交，查看 CI 结果。

## 更新约定

新增校验规则时同步更新 `scripts/validate_repository.py`、`tests/` 和本文档。不能为使校验通过而跳过真实错误，也不能将静态通过描述为全面运行验证。
