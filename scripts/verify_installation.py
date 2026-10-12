#!/usr/bin/env python3
"""Read-only integrity audit of an installed Prompt and selected Skills.

This verifies files, not whether an AI client discovered or executed a Skill.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

from init import AGENT_SKILLS_DIRS, REPOSITORY_ROOT, build_plan


def audit_installation(
    source_root: Path,
    target: Path,
    language: str = "zh-CN",
    agent: str = "generic",
    skills: list[str] | None = None,
) -> dict:
    """Compare installed files to the selected source files without mutation."""
    target = target.absolute()
    report: dict = {
        "ok": False,
        "scope": "file-integrity-only",
        "agent": agent,
        "language": language,
        "selected_skills": sorted(set(skills or [])),
        "checked_files": 0,
        "issues": [],
    }
    try:
        plan = build_plan(source_root, target, language, skills or [], agent)
    except (ValueError, OSError) as exc:
        report["issues"].append(f"无法生成检查计划：{exc}")
        return report

    root = target.resolve()
    for source, dest in plan:
        relative = dest.relative_to(target)
        current = dest
        unsafe = False
        while current != target:
            if current.is_symlink():
                report["issues"].append(f"包含符号链接：{relative}")
                unsafe = True
                break
            current = current.parent
        if unsafe or not dest.resolve().is_relative_to(root):
            if not unsafe:
                report["issues"].append(f"安装路径超出目标：{relative}")
            continue
        if not dest.is_file():
            report["issues"].append(f"缺少安装文件：{relative}")
            continue
        try:
            expected = hashlib.sha256(source.read_bytes()).digest()
            observed = hashlib.sha256(dest.read_bytes()).digest()
        except OSError as exc:
            report["issues"].append(f"读取文件失败：{relative}：{exc}")
            continue
        report["checked_files"] += 1
        if expected != observed:
            report["issues"].append(f"文件与来源不一致：{relative}")

    report["ok"] = not report["issues"]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="只读核对已安装的 Prompt 与 Skills 是否完整，与 Agent 实际执行验证不同"
    )
    parser.add_argument("--target", type=Path, required=True, help="已安装的目标项目目录")
    parser.add_argument("--lang", choices=("zh-CN", "en"), default="zh-CN")
    parser.add_argument("--agent", choices=tuple(AGENT_SKILLS_DIRS), default="generic")
    parser.add_argument("--skill", action="append", default=[], help="安装时所选 Skill，可重复")
    parser.add_argument("--json", action="store_true", help="输出可机器读取的 JSON")
    args = parser.parse_args(argv)

    report = audit_installation(REPOSITORY_ROOT, args.target, args.lang, args.agent, args.skill)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status = "通过" if report["ok"] else "失败"
        print(f"安装文件核对{status}：已检查 {report['checked_files']} 个文件")
        for issue in report["issues"]:
            print(f"ERROR: {issue}", file=sys.stderr)
        print("注意：此检查不代表 Codex/OpenCode/Claude Code 已发现或执行 Skill。")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
