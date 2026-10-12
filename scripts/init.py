#!/usr/bin/env python3
"""Safely prepare an existing project for Agent Engineering Kit prompts and Skills.

Dry-run by default. Only --apply writes files; existing files are never replaced.
This command does NOT invent project-specific engineering documents.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PROMPT_RELATIVE = Path(".agents/prompts/project-initialization.md")
SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
AGENT_SKILLS_DIRS = {
    "generic": Path(".agents/skills"),
    "codex": Path(".agents/skills"),
    "opencode": Path(".agents/skills"),
    "claude-code": Path(".claude/skills"),
}


def available_skills(source_root: Path = REPOSITORY_ROOT) -> list[str]:
    directory = source_root / ".agents" / "skills"
    if not directory.is_dir():
        return []
    return sorted(p.name for p in directory.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def build_plan(
    source_root: Path, target: Path, language: str, skill_names: list[str], agent: str = "generic"
) -> list[tuple[Path, Path]]:
    """Build a complete copy plan without touching the target."""
    if language not in {"zh-CN", "en"}:
        raise ValueError("语言只能是 zh-CN 或 en")
    if agent not in AGENT_SKILLS_DIRS:
        raise ValueError(f"未知 Agent 类型：{agent}")
    if target.is_symlink() or not target.is_dir():
        raise ValueError("目标必须是已存在、非符号链接的目录")
    target_resolved = target.resolve()
    source_resolved = source_root.resolve()
    if target_resolved.is_relative_to(source_resolved) or source_resolved.is_relative_to(target_resolved):
        raise ValueError("目标目录不得与工具包仓库重合或相互包含")

    prompt = source_root / "prompts" / f"project-initialization.{language}.md"
    if not prompt.is_file() or prompt.is_symlink():
        raise ValueError(f"初始化 Prompt 不存在或不是安全的普通文件：{prompt}")
    plan: list[tuple[Path, Path]] = [(prompt, target / PROMPT_RELATIVE)]
    seen = set()
    installed = available_skills(source_root)
    skill_root = source_root / ".agents" / "skills"

    for name in skill_names:
        if not SKILL_NAME.fullmatch(name) or name not in installed:
            raise ValueError(f"未知 Skill：{name}（使用 --list-skills 查看）")
        if name in seen:
            continue
        seen.add(name)
        folder = skill_root / name
        if folder.is_symlink():
            raise ValueError(f"Skill 目录不允许符号链接：{name}")
        for item in sorted(folder.rglob("*")):
            if item.is_symlink():
                raise ValueError(f"Skill 内存在符号链接：{item}")
            if item.is_file():
                relative = item.relative_to(skill_root)
                plan.append((item, target / AGENT_SKILLS_DIRS[agent] / relative))
    return plan


def check_conflicts(target: Path, plan: list[tuple[Path, Path]]) -> list[str]:
    """Reject all existing outputs and symlinked parent directories."""
    errors: list[str] = []
    for _, dest in plan:
        if dest.exists() or dest.is_symlink():
            errors.append(f"已存在，不会覆盖：{dest.relative_to(target)}")
        current = dest.parent
        while current != target and current.is_relative_to(target):
            if current.is_symlink():
                errors.append(f"目标父目录是符号链接：{current.relative_to(target)}")
                break
            if current.exists() and not current.is_dir():
                errors.append(f"目标路径不是目录：{current.relative_to(target)}")
                break
            current = current.parent
    return sorted(set(errors))


def apply_plan(target: Path, plan: list[tuple[Path, Path]]) -> None:
    """Write exclusively; roll back files created by this invocation on failure."""
    written: list[Path] = []
    created_dirs: list[Path] = []
    try:
        for source, dest in plan:
            missing = []
            parent = dest.parent
            while parent != target and not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for folder in reversed(missing):
                folder.mkdir()
                created_dirs.append(folder)
            # Exclusive creation prevents replacing an existing file, even if one
            # appears between the initial check and the write.
            with dest.open("xb") as output:
                written.append(dest)
                output.write(source.read_bytes())
    except Exception:
        for file in reversed(written):
            file.unlink(missing_ok=True)
        for folder in reversed(created_dirs):
            try:
                folder.rmdir()
            except OSError:
                pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="安全复制项目初始化 Prompt 和可选 Skills（默认仅预览）"
    )
    parser.add_argument("--target", type=Path, help="已存在的目标项目目录")
    parser.add_argument("--lang", choices=("zh-CN", "en"), default="zh-CN")
    parser.add_argument(
        "--agent", choices=tuple(AGENT_SKILLS_DIRS), default="generic",
        help="目标 Agent（决定 Skills 安装路径；默认 generic）",
    )
    parser.add_argument("--skill", action="append", default=[], help="可重复指定多个 Skill")
    parser.add_argument("--list-skills", action="store_true", help="列出可安装 Skills")
    parser.add_argument("--apply", action="store_true", help="确认写入，默认只预览")
    args = parser.parse_args(argv)

    if args.list_skills:
        for skill in available_skills():
            print(skill)
        return 0
    if args.target is None:
        parser.error("请通过 --target 指定目标项目目录")
    target = args.target.absolute()
    try:
        plan = build_plan(REPOSITORY_ROOT, target, args.lang, args.skill, args.agent)
        conflicts = check_conflicts(target, plan)
        if conflicts:
            for conflict in conflicts:
                print(f"ERROR: {conflict}", file=sys.stderr)
            return 1
        mode = "写入" if args.apply else "预览（不会修改文件）"
        print(f"{mode}：{target}")
        for _, destination in plan:
            print(f"  + {destination.relative_to(target)}")
        if args.apply:
            apply_plan(target, plan)
            print(f"已创建 {len(plan)} 个文件。下一步：让 AI Agent 阅读 Prompt 并分析目标项目。")
        else:
            print("确认无冲突后追加 --apply 执行。")
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
