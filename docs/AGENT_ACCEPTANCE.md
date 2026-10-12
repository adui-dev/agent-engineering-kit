# 🧪 Codex / OpenCode / Claude Code 端到端验收

本说明用于 **V1.2 发布前的真实客户端验收**。仓库 CI 已验证 Prompt 和 Skills 的文件复制；只有在对应客户端**实际发现、读取并按约束执行**后，才可在 [兼容性矩阵](COMPATIBILITY.md) 中把端到端状态改为“已验证”。

> 本仓库不保存 AI 服务密钥或登录状态，也不为验收自动启动付费 Agent。以下命令需要用户在自己的已安装、已登录客户端中运行。请避免将敏感项目、对话、密钥或原始日志上传到公开仓库。

## 验收层级

| 层级 | 验收内容 | 判断依据 |
| --- | --- | --- |
| L1 文件安装 | Prompt、Skill、许可证和引用资源是否完整 | `verify_installation.py` 成功 |
| L2 Skill 发现 | 客户端是否将 Skill 列为可用技能 | 客户端实际输出或技能目录/列表 |
| L3 Skill 调用 | Agent 是否真的加载 Skill 并阅读入口/引用资料 | 实际工具调用或可核查的交互记录 |
| L4 初始化工作流 | Agent 在示例项目上是否遵守 Prompt 的约束、产生正确工程资产 | 文件 diff、命令日志与人工检查 |
| L5 安全和回归 | 是否未破坏既有代码、未泄露凭据，且可用测试通过 | 执行日志、版本控制差异与测试输出 |

**必须区分：** L1 自动通过不等于 L2–L5 通过；直接要求 Agent 打开 `SKILL.md`，也不能单独证明它能**自动发现**该 Skill。

## 1. 准备独立测试项目

从工具包根目录复制 [已有 Python 示例](../examples/existing-python/README.md) 到工具包**外部**的新目录。Windows PowerShell 示例：

```powershell
Copy-Item -Recurse .\examples\existing-python ..\aek-e2e-codex
python scripts/init.py --target ..\aek-e2e-codex --lang zh-CN --agent codex --skill git-commit
python scripts/init.py --target ..\aek-e2e-codex --lang zh-CN --agent codex --skill git-commit --apply
python scripts/verify_installation.py --target ..\aek-e2e-codex --lang zh-CN --agent codex --skill git-commit --json
```

为另两款客户端分别创建单独副本，并将 `aek-e2e-codex` 与 `--agent codex` 替换为：

- `aek-e2e-opencode`、`--agent opencode`
- `aek-e2e-claude`、`--agent claude-code`

仅验收临时副本，不要在生产仓库上进行实验。

## 2. 启动真实客户端

在对应**测试项目目录**中运行以下命令之一，先执行客户端的 `--version` 并记录输出：

```powershell
# Codex：在测试项目目录中执行
codex

# OpenCode
opencode

# Claude Code
claude
```

也可在客户端当前版本支持、且已配置账号与模型的情况下，使用非交互命令 `codex exec "..." `、`opencode run "..."` 或 `claude -p "..."` 进行只读验收。注意非交互命令可能产生 API 费用；先确认权限和费用。CLI 选项以各工具本机 `--help` 为准。

官方参考：[Codex](https://developers.openai.com/codex/cli)、[OpenCode](https://opencode.ai/docs/cli/)、[Claude Code](https://code.claude.com/docs/en/cli-reference)。

## 3. 按顺序执行三项验收任务

**A. Skill 自动发现（只读）**

向 Agent 输入：

> 请列出你在当前项目中通过原生 Skill 发现机制识别到的技能及其名称，不要直接从文件系统猜测，也不要修改或提交任何文件。说明是否发现 `git-commit`，并指出实际发现机制；如果无法确认，请明确说明。

**B. Skill 实际加载（只读）**

> 请使用你所在工具的原生 Skill 加载机制加载 `git-commit`，说明你读取到的 `SKILL.md` 主要工作约束。不要创建提交、推送代码、安装依赖或修改文件。无法使用原生 Skill 工具时，请说明受限原因；单纯直接读文件不算调用成功。

**C. Prompt 项目初始化（允许仅在测试副本中写文件）**

> 请阅读当前仓库的 `.agents/prompts/project-initialization.md`，先审查真实项目和已有测试，再按照其中规定，以最小改动建立适用的工程资产。不要编造业务事实，不要进行 Git commit/push，不要修改原有 `src/app.py` 的行为。执行实际可用的测试，报告新增/修改文件和没有执行的检查。

随后在测试目录执行：

```powershell
python -m unittest discover -s tests -v
git status --short
git diff -- src/app.py
```

若测试目录没有初始化 Git，可先在**临时副本**内建立 Git 仓库并提交一份干净基线，或通过文件哈希比对源代码。不要把“未发现差异”当成已完成测试。

## 4. 结果与证据

每个工具分别记录：客户端及版本、操作系统、模型、测试日期、安装命令、`verify_installation.py` 结果、L1–L5 的状态、Skill 发现和加载证据、项目文件 diff、实际测试输出、权限限制、费用注意事项，以及失败和解决方式。

允许的状态：**通过 / 失败 / 阻塞 / 未测试**。未记录证据时保留“未测试”，不要自行勾选“通过”。

公开提交时只保留脱敏的摘要、版本与必要结论；不要公开原始聊天日志、访问令牌、账户信息或生产项目细节。

## 5. 当前完成情况

- L1：CLI 文件安装与跨平台 Smoke Test 已有自动化覆盖（本页也提供独立只读核验）。
- L2–L5：**需要各客户端真实运行后才能确认**。
- V1.2 尚未发布，兼容性矩阵的“真实端到端”列不应因新增本指南而自动变为“已验证”。
