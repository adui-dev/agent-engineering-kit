"""Tests for the read-only installation integrity checker."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify_installation
from init import apply_plan, build_plan


class VerifyInstallationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.source = root / "kit"
        self.target = root / "project"
        self.target.mkdir()
        (self.source / "prompts").mkdir(parents=True)
        for language in ("en", "zh-CN"):
            (self.source / "prompts" / f"project-initialization.{language}.md").write_text(
                f"Prompt {language}\n", encoding="utf-8"
            )
        skill = self.source / ".agents/skills/sample-skill"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: demo\n---\n", encoding="utf-8"
        )
        (skill / "references/info.md").write_text("Reference\n", encoding="utf-8")
        (skill / "THIRD_PARTY_LICENSE.md").write_text("MIT\n", encoding="utf-8")

    def install(self, agent="generic", skills=None):
        apply_plan(self.target, build_plan(
            self.source, self.target, "en", skills or [], agent
        ))

    def audit(self, agent="generic", skills=None):
        return verify_installation.audit_installation(
            self.source, self.target, "en", agent, skills or []
        )

    def test_verifies_prompt_only(self):
        self.install()
        result = self.audit()
        self.assertTrue(result["ok"])
        self.assertEqual(result["checked_files"], 1)
        self.assertEqual(result["scope"], "file-integrity-only")

    def test_verifies_claude_skill_and_all_resources(self):
        self.install(agent="claude-code", skills=["sample-skill"])
        result = self.audit(agent="claude-code", skills=["sample-skill"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["checked_files"], 4)

    def test_catches_missing_prompt(self):
        result = self.audit()
        self.assertFalse(result["ok"])
        self.assertTrue(any("缺少安装文件" in s for s in result["issues"]))

    def test_detects_changed_prompt(self):
        self.install()
        (self.target / ".agents/prompts/project-initialization.md").write_text(
            "changed\n", encoding="utf-8"
        )
        self.assertTrue(any("不一致" in s for s in self.audit()["issues"]))

    def test_detects_missing_reference(self):
        self.install(skills=["sample-skill"])
        (self.target / ".agents/skills/sample-skill/references/info.md").unlink()
        self.assertTrue(any("references/info.md" in s for s in
                            self.audit(skills=["sample-skill"])["issues"]))

    def test_rejects_symlink_in_installation(self):
        self.install()
        outside = self.target.parent / "other.md"
        outside.write_text("secret\n", encoding="utf-8")
        prompt = self.target / ".agents/prompts/project-initialization.md"
        prompt.unlink()
        try:
            prompt.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable")
        self.assertFalse(self.audit()["ok"])
        self.assertTrue(any("符号链接" in s for s in self.audit()["issues"]))

    def test_rejects_wrong_agent_location(self):
        self.install(agent="generic", skills=["sample-skill"])
        report = self.audit(agent="claude-code", skills=["sample-skill"])
        self.assertFalse(report["ok"])
        self.assertTrue(any("缺少安装文件" in s for s in report["issues"]))

    def test_rejects_unknown_skill(self):
        self.install()
        report = self.audit(skills=["does-not-exist"])
        self.assertFalse(report["ok"])
        self.assertTrue(any("未知 Skill" in s for s in report["issues"]))

    def test_json_cli_reports_files_only(self):
        self.install()
        buf = io.StringIO()
        with mock.patch.object(verify_installation, "REPOSITORY_ROOT", self.source):
            with contextlib.redirect_stdout(buf):
                code = verify_installation.main([
                    "--target", str(self.target), "--lang", "en", "--json"
                ])
        self.assertEqual(code, 0)
        result = json.loads(buf.getvalue())
        self.assertTrue(result["ok"])
        self.assertEqual(result["scope"], "file-integrity-only")


if __name__ == "__main__":
    unittest.main()
