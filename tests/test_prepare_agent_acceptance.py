"""Tests for disposable Agent client acceptance workspace preparation."""

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

import prepare_agent_acceptance as acceptance


class PrepareAgentAcceptanceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="aek-e2e-test-")
        self.addCleanup(tmp.cleanup)
        self.parent = Path(tmp.name)
        self.source = Path(__file__).resolve().parents[1]
        self.target = self.parent / "new-client-test"

    def test_preview_does_not_create_files(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = acceptance.main(["--agent", "codex", "--output", str(self.target)])
        self.assertEqual(result, 0)
        self.assertIn("预览，不写入", buf.getvalue())
        self.assertFalse(self.target.exists())

    def test_codex_has_real_baseline_and_no_client_claim(self):
        result = acceptance.prepare_workspace(self.source, self.target, agent="codex")
        self.assertEqual(result["L1"], "passed")
        for level in ("L2", "L3", "L4", "L5"):
            self.assertEqual(result[level], "not_tested")
        self.assertEqual(result["scope"], "local-acceptance-preparation")
        self.assertTrue((self.target / ".agents/skills/git-commit/SKILL.md").is_file())
        self.assertEqual(
            (self.target / "src/app.py").read_bytes(),
            (self.source / "examples/existing-python/src/app.py").read_bytes(),
        )
        self.assertEqual(json.loads((self.target / acceptance.MANIFEST_NAME).read_text(encoding="utf-8")), result)
        self.assertIn("未测试", (self.target / acceptance.CHECKLIST_NAME).read_text(encoding="utf-8"))
        self.assertEqual(len(result["source_hashes"]), 2)

    def test_opencode_uses_agent_skills(self):
        report = acceptance.prepare_workspace(self.source, self.target, agent="opencode", language="en")
        self.assertEqual(report["language"], "en")
        self.assertTrue((self.target / ".agents/skills/git-commit/THIRD_PARTY_LICENSE.md").exists())

    def test_claude_code_uses_claude_skills(self):
        report = acceptance.prepare_workspace(self.source, self.target, agent="claude-code")
        self.assertTrue(report["checked_install_files"] >= 3)
        self.assertTrue((self.target / ".claude/skills/git-commit/SKILL.md").exists())
        self.assertFalse((self.target / ".agents/skills").exists())

    def test_refuses_existing_target_without_modification(self):
        self.target.mkdir()
        marker = self.target / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            acceptance.prepare_workspace(self.source, self.target)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_rejects_source_subdirectory(self):
        not_yet_created = self.source / "tests" / "not-a-real-acceptance-target"
        with self.assertRaises(ValueError):
            acceptance.checked_output(self.source, not_yet_created, "zh-CN", "codex", "git-commit")
        self.assertFalse(not_yet_created.exists())

    def test_unknown_skill_or_agent_is_rejected(self):
        for agent, skill in (("wrong-agent", "git-commit"), ("codex", "missing-skill")):
            with self.subTest(agent=agent, skill=skill), self.assertRaises(ValueError):
                acceptance.checked_output(self.source, self.target, "en", agent, skill)
        self.assertFalse(self.target.exists())

    def test_missing_parent_is_rejected(self):
        with self.assertRaises(ValueError):
            acceptance.checked_output(self.source, self.parent / "missing" / "test", "en", "codex", "git-commit")

    def test_failed_install_rolls_back_new_workspace(self):
        with mock.patch.object(acceptance, "apply_plan", side_effect=OSError("fake install failure")):
            with self.assertRaises(OSError):
                acceptance.prepare_workspace(self.source, self.target)
        self.assertFalse(self.target.exists())

    def test_failed_copy_rolls_back_new_workspace(self):
        with mock.patch.object(acceptance.shutil, "copytree", side_effect=OSError("fake copy failure")):
            with self.assertRaises(OSError):
                acceptance.prepare_workspace(self.source, self.target)
        self.assertFalse(self.target.exists())

    def test_apply_cli_does_not_launch_client(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = acceptance.main(["--agent", "codex", "--output", str(self.target), "--apply"])
        self.assertEqual(result, 0)
        self.assertIn("L1 通过", buf.getvalue())
        self.assertIn("L2-L5", buf.getvalue())
        self.assertTrue((self.target / acceptance.MANIFEST_NAME).is_file())

    def test_no_overwrite_second_cli_run(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(acceptance.main(["--agent", "codex", "--output", str(self.target), "--apply"]), 0)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(acceptance.main(["--agent", "codex", "--output", str(self.target), "--apply"]), 1)
        self.assertIn("拒绝覆盖", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
