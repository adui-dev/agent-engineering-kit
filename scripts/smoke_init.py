#!/usr/bin/env python3
"""Cross-platform, real-subprocess smoke tests for the initialization CLI.

Uses temporary directories only. This does not launch or validate an AI agent.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "init.py"
VERIFIER = ROOT / "scripts" / "verify_installation.py"
PREPARER = ROOT / "scripts" / "prepare_agent_acceptance.py"


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


def verify_files(target: Path, *, language: str = "zh-CN",
                 agent: str = "generic", skills: tuple[str, ...] = ()) -> None:
    args = [
        sys.executable, str(VERIFIER), "--target", str(target),
        "--lang", language, "--agent", agent, "--json",
    ]
    for name in skills:
        args += ["--skill", name]
    process = subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=False,
    )
    if process.returncode != 0:
        raise AssertionError("Installation verification failed:\n"
                             + process.stdout + process.stderr)
    result = json.loads(process.stdout)
    if result["scope"] != "file-integrity-only" or not result["ok"]:
        raise AssertionError("Unexpected verification result: " + str(result))


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
        verify_files(fresh, language="en", skills=("git-commit",))

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
        verify_files(claude, language="zh-CN", agent="claude-code",
                     skills=("github-issues",))

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
            verify_files(target, agent=agent, skills=("git-commit",))

        # Disposable client workspaces: CLI dry-run, install and honest evidence.
        for agent in ("codex", "opencode", "claude-code"):
            target = temp / f"acceptance-{agent}"
            arguments = [
                sys.executable, str(PREPARER),
                "--agent", agent, "--output", str(target), "--lang", "zh-CN",
            ]
            environment = os.environ.copy()
            environment["PYTHONUTF8"] = "1"
            environment["PYTHONIOENCODING"] = "utf-8"
            preview = subprocess.run(
                arguments, cwd=ROOT, capture_output=True, text=True,
                encoding="utf-8", errors="replace", check=False, env=environment,
            )
            if preview.returncode != 0 or target.exists():
                raise AssertionError(f"Acceptance dry-run failed for {agent}: {preview.stderr}")
            prepared = subprocess.run(
                arguments + ["--apply"], cwd=ROOT, capture_output=True,
                text=True, encoding="utf-8", errors="replace", check=False, env=environment,
            )
            if prepared.returncode != 0:
                raise AssertionError(f"Acceptance preparation failed for {agent}: {prepared.stderr}")
            report = json.loads(
                (target / "ACCEPTANCE_MANIFEST.json").read_text(encoding="utf-8")
            )
            if report["L1"] != "passed" or any(
                report[level] != "not_tested" for level in ("L2", "L3", "L4", "L5")
            ):
                raise AssertionError(f"Acceptance states are inaccurate for {agent}")
            expected = ROOT / "examples/existing-python/src/app.py"
            assert_copied(expected, target / "src/app.py")
            verify_files(target, agent=agent, skills=("git-commit",))
            rejected = subprocess.run(
                arguments + ["--apply"], cwd=ROOT, capture_output=True,
                text=True, encoding="utf-8", errors="replace", check=False, env=environment,
            )
            if rejected.returncode == 0:
                raise AssertionError("Acceptance preparation unexpectedly overwrote an existing workspace")

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
        verify_files(existing)
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
