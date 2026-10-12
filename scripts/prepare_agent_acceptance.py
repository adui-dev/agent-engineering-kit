#!/usr/bin/env python3
"""Prepare a disposable real-client acceptance workspace, never launch an Agent.

Dry-run by default. Creates a NEW target only with --apply; never overwrites.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from init import AGENT_SKILLS_DIRS, REPOSITORY_ROOT, available_skills, apply_plan, build_plan
from verify_installation import audit_installation

EXAMPLE_REL = Path("examples/existing-python")
MANIFEST_NAME = "ACCEPTANCE_MANIFEST.json"
CHECKLIST_NAME = "ACCEPTANCE_CHECKLIST.md"
ACCEPTANCE_AGENTS = ("codex", "opencode", "claude-code")


def checked_output(source_root: Path, output: Path, language: str, agent: str, skill: str) -> Path:
    """Validate before any writes, including target overlaps and Skill selection."""
    source = source_root.resolve()
    target = output.absolute()
    parent = target.parent
    if language not in ("zh-CN", "en"):
        raise ValueError("仅支持 zh-CN 或 en")
    if agent not in ACCEPTANCE_AGENTS:
        raise ValueError(f"未知客户端：{agent}")
    if skill not in available_skills(source_root):
        raise ValueError(f"不存在的 Skill：{skill}")
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"目标已存在，拒绝覆盖：{target}")
    if not parent.is_dir() or parent.is_symlink():
        raise ValueError("目标父目录必须已存在，且不能是符号链接")
    actual = target.resolve()
    if actual.is_relative_to(source) or source.is_relative_to(actual):
        raise ValueError("验收目录不能是工具包仓库或其父子目录")

    example = source_root / EXAMPLE_REL
    if not example.is_dir() or example.is_symlink():
        raise ValueError("缺少安全的已有项目示例")
    for item in example.rglob("*"):
        if item.is_symlink():
            raise ValueError(f"示例包含符号链接：{item.relative_to(example)}")
    for needed in ("src/app.py", "tests/test_app.py"):
        if not (example / needed).is_file():
            raise ValueError(f"示例文件缺失：{needed}")
    return target


def checklist(agent: str) -> str:
    return f"""# {agent}：实际客户端验收清单（未测试）

> 此文件由 Agent Engineering Kit 准备工具生成，**不代表 Agent 已运行**。
> 仅在本测试副本操作；不得上传账号、密钥、模型响应原文或敏感日志。

## L1：安装文件

安装完整性及源代码基线记录在 \`{MANIFEST_NAME}\`。L1 文件通过不等于后续通过。

## L2：Skill 自动发现（需实际客户端）

在此测试目录启动 {agent}，让客户端**通过原生发现机制**列出可用 Skills，
确认是否发现所选 Skill。不得直接读取磁盘文件来冒充自动发现。

## L3：Skill 原生调用（只读）

要求 Agent **使用原生 Skill 加载方式**查看 Skill 约束；不得提交、推送、
安装额外依赖或修改项目。只有原生加载证据才能标为通过。

## L4：项目初始化（测试副本内）

让 Agent 阅读 \`.agents/prompts/project-initialization.md\`，先审查现有
\`src/app.py\` 和 \`tests/test_app.py\`，再最小化建立真实工程资产。
禁止编造业务需求、运行结果，禁止 Git commit/push。

## L5：安全与回归

在此测试目录执行：

\`\`\`powershell
python -m unittest discover -s tests -v
\`\`\`

对比 \`{MANIFEST_NAME}\` 中的 \`source_hashes\`，
确保已有 \`src/app.py\` 行为及代码没有被无意更改。

## 结果记录

- L1：通过（仅验证文件内容；以 MANIFEST 为准）
- L2：未测试
- L3：未测试
- L4：未测试
- L5：未测试

填写客户端版本、模型、操作系统、测试时间和脱敏证据摘要后，
再由维护者人工决定是否更新正式 [兼容性矩阵]。
不能把本文件中的待测项自动变为“通过”。
"""


def prepare_workspace(
    source_root: Path, output: Path, language: str = "zh-CN",
    agent: str = "codex", skill: str = "git-commit",
) -> dict:
    """Prepare a fresh acceptance workspace and roll back on failure."""
    dest = checked_output(source_root, output, language, agent, skill)
    source_example = source_root / EXAMPLE_REL
    created = False
    try:
        # mkdir() is exclusive. Only clean up after we own this new directory.
        dest.mkdir()
        created = True
        shutil.copytree(
            source_example,
            dest,
            dirs_exist_ok=True,
            symlinks=False,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".git"),
        )
        plan = build_plan(source_root, dest, language, [skill], agent)
        apply_plan(dest, plan)
        audit = audit_installation(source_root, dest, language, agent, [skill])
        if not audit["ok"]:
            raise RuntimeError("安装完整性校验失败：" + "; ".join(audit["issues"]))

        hashes = {}
        for rel in ("src/app.py", "tests/test_app.py"):
            hashes[rel] = hashlib.sha256((dest / rel).read_bytes()).hexdigest()

        manifest = {
            "schema_version": 1,
            "scope": "local-acceptance-preparation",
            "agent": agent,
            "language": language,
            "skill": skill,
            "L1": "passed",
            "L2": "not_tested",
            "L3": "not_tested",
            "L4": "not_tested",
            "L5": "not_tested",
            "checked_install_files": audit["checked_files"],
            "source_hashes": hashes,
        }
        (dest / MANIFEST_NAME).write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (dest / CHECKLIST_NAME).write_text(checklist(agent), encoding="utf-8")
        return manifest
    except Exception:
        if created:
            shutil.rmtree(dest)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="准备 Codex/OpenCode/Claude Code 独立验收项目")
    parser.add_argument("--agent", choices=ACCEPTANCE_AGENTS, required=True)
    parser.add_argument("--output", type=Path, required=True, help="新的项目目录，不得已存在")
    parser.add_argument("--lang", choices=("zh-CN", "en"), default="zh-CN")
    parser.add_argument("--skill", default="git-commit")
    parser.add_argument("--apply", action="store_true", help="确认创建；默认仅预览")
    args = parser.parse_args(argv)
    try:
        dest = checked_output(REPOSITORY_ROOT, args.output, args.lang, args.agent, args.skill)
        print(f"{'准备创建' if args.apply else '预览，不写入'}：{dest}")
        print(f"  示例：{EXAMPLE_REL.as_posix()}")
        print(f"  Prompt：{args.lang}")
        print(f"  Skill：{args.skill} -> {AGENT_SKILLS_DIRS[args.agent].as_posix()}")
        print(f"  验收清单：{CHECKLIST_NAME}；基线：{MANIFEST_NAME}")
        if args.apply:
            summary = prepare_workspace(REPOSITORY_ROOT, dest, args.lang, args.agent, args.skill)
            print(f"文件验收 L1 通过，已核对 {summary['checked_install_files']} 个安装文件。")
            print(f"请在目标目录中运行 {args.agent} 客户端完成 L2-L5；目前全部未测试。")
        else:
            print("确认后加 --apply 创建。此命令不会启动 Agent。")
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
