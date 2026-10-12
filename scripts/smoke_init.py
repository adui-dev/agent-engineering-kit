#!/usr/bin/env python3
"""Cross-platform, real-subprocess smoke tests for the initialization CLI.

Uses temporary directories only. This does not launch or validate an AI agent.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "init.py"


def run_cli(*args: str, expected: int = 0) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"CLI returned {result.returncode}, expected {expected}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout + result.stderr


def assert_copied(source: Path, destination: Path) -> None:
    if not destination.is_file() or source.read_bytes() != destination.read_bytes():
        raise AssertionError(f"Copy differs: {source} -> {destination}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agent-kit-smoke-") as tmp:
        temp = Path(tmp)
        listing = run_cli("--list-skills")
        for skill in ("git-commit", "github-issues"):
            if skill not in listing.splitlines():
                raise AssertionError(f"Expected skill missing: {skill}")

        # Empty project: dry-run and real English installation.
        fresh = temp / "new-project"
        fresh.mkdir()
        run_cli("--target", str(fresh), "--lang", "en", "--skill", "git-commit")
        if (fresh / ".agents").exists():
            raise AssertionError("Dry-run changed the target")
        run_cli("--target", str(fresh), "--lang", "en", "--skill", "git-commit", "--apply")
        assert_copied(
            ROOT / "prompts/project-initialization.en.md",
            fresh / ".agents/prompts/project-initialization.md",
        )
        assert_copied(
            ROOT / ".agents/skills/git-commit/SKILL.md",
            fresh / ".agents/skills/git-commit/SKILL.md",
        )
        assert_copied(
            ROOT / ".agents/skills/git-commit/THIRD_PARTY_LICENSE.md",
            fresh / ".agents/skills/git-commit/THIRD_PARTY_LICENSE.md",
        )

        # Claude Code: real copy of a Skill with reference resources.
        claude = temp / "claude-project"
        claude.mkdir()
        run_cli(
            "--target", str(claude), "--lang", "zh-CN",
            "--agent", "claude-code", "--skill", "github-issues", "--apply",
        )
        assert_copied(
            ROOT / ".agents/skills/github-issues/SKILL.md",
            claude / ".claude/skills/github-issues/SKILL.md",
        )
        assert_copied(
            ROOT / ".agents/skills/github-issues/references/search.md",
            claude / ".claude/skills/github-issues/references/search.md",
        )
        assert_copied(
            ROOT / ".agents/skills/github-issues/THIRD_PARTY_LICENSE.md",
            claude / ".claude/skills/github-issues/THIRD_PARTY_LICENSE.md",
        )
        if (claude / ".agents/skills").exists():
            raise AssertionError("Claude installation wrote the wrong Skills directory")

        # Codex and OpenCode: paths and actual copies, not Agent execution.
        for agent in ("codex", "opencode"):
            target = temp / f"{agent}-project"
            target.mkdir()
            run_cli(
                "--target", str(target), "--agent", agent,
                "--skill", "git-commit", "--apply",
            )
            assert_copied(
                ROOT / ".agents/skills/git-commit/SKILL.md",
                target / ".agents/skills/git-commit/SKILL.md",
            )

        # Existing project: unchanged application behavior and failure-on-conflict.
        existing = temp / "existing-python"
        shutil.copytree(ROOT / "examples/existing-python", existing)
        original = (existing / "src/app.py").read_bytes()
        run_cli("--target", str(existing), "--lang", "zh-CN", "--apply")
        assert_copied(
            ROOT / "prompts/project-initialization.zh-CN.md",
            existing / ".agents/prompts/project-initialization.md",
        )
        if (existing / "src/app.py").read_bytes() != original:
            raise AssertionError("Existing application source was changed")
        subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(existing / "tests"), "-v"],
            check=True, cwd=existing,
        )
        conflict_output = run_cli("--target", str(existing), "--apply", expected=1)
        if "不会覆盖" not in conflict_output:
            raise AssertionError("Expected a non-overwrite error")
        if (existing / "src/app.py").read_bytes() != original:
            raise AssertionError("Conflict attempt changed application source")

    print("Cross-platform installation smoke test passed (real subprocesses).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
