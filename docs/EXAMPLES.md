# 🧪 使用示例与实际验收

本仓库提供可重复的**安装与已有代码回归验证**，而非未经测试的 Agent 自动生成项目演示。

## 示例

| 场景 | 示例 | 验证目的 |
| --- | --- | --- |
| 全新项目 | [greenfield](../examples/greenfield/README.md) | 未确定业务/技术栈时，Agent 应提出待决策问题，不创建虚假文件 |
| 已有 Python 项目 | [existing-python](../examples/existing-python/README.md) | 确认已有代码、运行方式和测试结果不被初始化操作破坏 |

## 自动验证（Python 3.10+）

从仓库根目录执行：

```bash
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python -m unittest discover -s examples/existing-python/tests -v
python scripts/smoke_init.py
bash scripts/smoke_init.sh
```

Python Smoke Test 跨平台运行真实 CLI 子进程，在临时目录中验证：dry-run 不写入文件、三类 Agent 目录适配、Prompt 内容完整、第三方许可及引用资料被保留、已有 Python 项目测试仍通过、重复安装被阻止。Bash 版本额外覆盖 Linux 场景。

## 实际客户端验收准备

可用 [准备工具](../scripts/prepare_agent_acceptance.py) 基于已有 Python 示例创建仓库外的临时测试项目，生成源代码哈希基线与未测试状态清单；不会调用 Agent。具体步骤见 [端到端验收](AGENT_ACCEPTANCE.md)。

## Agent 实际初始化的人工验收

自动脚本**不会模拟或假称已成功调用 AI Agent**。在实际工具中用 Prompt 初始化一个示例项目后，请核对：

- [ ] 已检查现有仓库，没有虚构需求、已实现功能或测试结果。
- [ ] 清楚列出新增/修改文件，解释为什么需要它们。
- [ ] AGENTS 仅作为入口，其他正式文档职责明确。
- [ ] CODEBASE_MAP 引用真实的路径；未确定的目录标记为规划。
- [ ] Skills 按任务选择，不是全部自动安装。
- [ ] Harness 含可运行的命令，无法执行时明确说明。
- [ ] 执行实际测试并报告结果，不能把建议当成运行成功。
- [ ] 不覆盖现有工作，不强制提交或发布。

三款工具的实测步骤见 [Agent 端到端验收](AGENT_ACCEPTANCE.md)，只读安装核验见 [verify_installation.py](../scripts/verify_installation.py)。将脱敏证据结论写入 [兼容性矩阵](COMPATIBILITY.md)；未实测时保留“待验证”状态。
