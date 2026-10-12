#!/usr/bin/env python3
"""Dependency-free structural checks for Agent Engineering Kit."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED_FILES = (
    "VERSION",
    "README.md",
    "README.en.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    "prompts/project-initialization.zh-CN.md",
    "prompts/project-initialization.en.md",
    "docs/SKILLS.md",
    "docs/QUALITY.md",
    ".github/workflows/quality.yml",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\((<?[^\s)]+>?)(?:\s+['\"][^'\"]+['\"])?\)")
META_PATTERN = re.compile(r"^([a-z][a-z_-]*):\s*(.*)$", re.MULTILINE)
VERSION_PATTERN = re.compile(r"^V\d+\.\d+$")


def markdown_targets(source: str):
    """Extract inline links outside fenced code blocks (not external media)."""
    fence = None
    for line in source.splitlines():
        stripped = line.lstrip()
        match = re.match(r"^(\x60{3,}|~{3,})", stripped)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        for found in LINK_PATTERN.finditer(line):
            yield found.group(1).strip("<>")


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"缺少必需文件：{relative}")

    version_file = root / "VERSION"
    version = version_file.read_text(encoding="utf-8").strip() if version_file.is_file() else ""
    if not VERSION_PATTERN.fullmatch(version):
        errors.append("VERSION 必须是 V主版本.次版本，例如 V1.0")

    checks = {
        "README.md": version,
        "README.en.md": version,
        "AGENTS.md": version,
        "CHANGELOG.md": version,
        "prompts/project-initialization.zh-CN.md": f"版本：{version}",
        "prompts/project-initialization.en.md": f"Version: {version}",
    }
    if version:
        for relative, marker in checks.items():
            path = root / relative
            if path.is_file() and marker not in path.read_text(encoding="utf-8"):
                errors.append(f"{relative} 未体现当前版本 {version}")


    # Check bilingual prompt structure; this does not guarantee semantic equivalence.
    zh_file = root / "prompts/project-initialization.zh-CN.md"
    en_file = root / "prompts/project-initialization.en.md"
    if zh_file.is_file() and en_file.is_file():
        zh_text = zh_file.read_text(encoding="utf-8")
        en_text = en_file.read_text(encoding="utf-8")
        expected_zh = [
            "一", "二", "三", "四", "五", "六", "七", "八",
            "九", "十", "十一", "十二", "十三", "十四", "十五", "十六",
        ]
        zh_sections = re.findall(r"(?m)^## ([一二三四五六七八九十]+)、", zh_text)
        en_sections = [int(n) for n in re.findall(r"(?m)^## ([0-9]+)\. ", en_text)]
        if zh_sections != expected_zh:
            errors.append("中文 Prompt 主章节必须按顺序包含一至十六章")
        if en_sections != list(range(1, 17)):
            errors.append("英文 Prompt 主章节必须按顺序包含 1 至 16 章")
        for name, body in (("中文", zh_text), ("英文", en_text)):
            assets = re.findall(r"(?m)^### 5\.([0-9]+)\s", body)
            if assets != [str(n) for n in range(1, 9)]:
                errors.append(f"{name} Prompt 必须按顺序包含 5.1 至 5.8 八个核心资产")

    skill_dir = root / ".agents" / "skills"
    skills = sorted(p for p in skill_dir.iterdir() if p.is_dir()) if skill_dir.is_dir() else []
    if not skills:
        errors.append("未找到任何项目级 Skill（.agents/skills/*/SKILL.md）")

    indexed = (root / "docs" / "SKILLS.md").read_text(encoding="utf-8") if (root / "docs" / "SKILLS.md").is_file() else ""
    names: set[str] = set()
    for folder in skills:
        entry = folder / "SKILL.md"
        license_file = folder / "THIRD_PARTY_LICENSE.md"
        if not entry.is_file():
            errors.append(f"缺少 Skill 入口：{entry.relative_to(root)}")
            continue
        if not license_file.is_file():
            errors.append(f"缺少第三方许可证声明：{license_file.relative_to(root)}")
        content = entry.read_text(encoding="utf-8")
        m = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.DOTALL)
        if not m:
            errors.append(f"Skill 缺少 YAML frontmatter：{entry.relative_to(root)}")
        else:
            meta = {k: v.strip().strip("'\"") for k, v in META_PATTERN.findall(m.group(1))}
            if meta.get("name") != folder.name:
                errors.append(f"Skill name 与目录不一致：{entry.relative_to(root)}")
            if not meta.get("description"):
                errors.append(f"Skill description 不能为空：{entry.relative_to(root)}")
        if folder.name in names:
            errors.append(f"重复 Skill 名称：{folder.name}")
        names.add(folder.name)
        if f".agents/skills/{folder.name}/SKILL.md" not in indexed:
            errors.append(f"Skills 索引缺少：{folder.name}")

    markdown_files = sorted(root.glob("*.md")) + sorted((root / "docs").glob("*.md"))
    markdown_files += sorted((root / "prompts").glob("*.md"))
    markdown_files += [folder / "SKILL.md" for folder in skills if (folder / "SKILL.md").is_file()]
    for file in markdown_files:
        for url in markdown_targets(file.read_text(encoding="utf-8")):
            if url.startswith("#") or ("$" + "{") in url or "<" in url:
                continue
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = unquote(parsed.path)
            resolved = (root / dest.lstrip("/")).resolve() if dest.startswith("/") else (file.parent / dest).resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"链接超出仓库范围：{file.relative_to(root)} -> {url}")
            elif not resolved.exists():
                errors.append(f"无效文件链接：{file.relative_to(root)} -> {url}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校验项目版本、Markdown 链接和 Skills 结构")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors = check_repository(args.root)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(f"校验失败：{len(errors)} 个问题", file=sys.stderr)
        return 1
    print("校验通过：文件、版本、Markdown 链接及 Skills 基础结构均有效。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
