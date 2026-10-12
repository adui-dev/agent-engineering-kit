"""Tests for safe, optional Agent Engineering Kit installation."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from init import apply_plan, available_skills, build_plan, check_conflicts


class InitTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.source = root / "kit"
        self.target = root / "project"
        self.source.mkdir()
        self.target.mkdir()
        (self.source / "prompts").mkdir()
        (self.source / "prompts/project-initialization.zh-CN.md").write_text("中文 Prompt", encoding="utf-8")
        (self.source / "prompts/project-initialization.en.md").write_text("English Prompt", encoding="utf-8")
        skill = self.source / ".agents/skills/example"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: example\ndescription: Test\n---\n", encoding="utf-8")
        (skill / "THIRD_PARTY_LICENSE.md").write_text("MIT\n", encoding="utf-8")
        (skill / "references/usage.md").write_text("# Details\n", encoding="utf-8")

    def test_discovers_skills(self):
        self.assertEqual(available_skills(self.source), ["example"])

    def test_preview_does_not_write(self):
        plan = build_plan(self.source, self.target, "zh-CN", [])
        self.assertEqual(len(plan), 1)
        self.assertEqual(check_conflicts(self.target, plan), [])
        self.assertFalse((self.target / ".agents").exists())

    def test_applies_english_prompt(self):
        plan = build_plan(self.source, self.target, "en", [])
        apply_plan(self.target, plan)
        self.assertEqual(
            (self.target / ".agents/prompts/project-initialization.md").read_text(encoding="utf-8"),
            "English Prompt",
        )

    def test_installs_selected_skill_with_references_and_license(self):
        plan = build_plan(self.source, self.target, "zh-CN", ["example", "example"])
        self.assertEqual(len(plan), 4)
        apply_plan(self.target, plan)
        self.assertTrue((self.target / ".agents/skills/example/SKILL.md").exists())
        self.assertTrue((self.target / ".agents/skills/example/THIRD_PARTY_LICENSE.md").exists())
        self.assertTrue((self.target / ".agents/skills/example/references/usage.md").exists())

    def test_existing_files_are_never_overwritten(self):
        dest = self.target / ".agents/prompts/project-initialization.md"
        dest.parent.mkdir(parents=True)
        dest.write_text("my own prompt", encoding="utf-8")
        plan = build_plan(self.source, self.target, "en", ["example"])
        self.assertTrue(any("不会覆盖" in e for e in check_conflicts(self.target, plan)))
        self.assertEqual(dest.read_text(encoding="utf-8"), "my own prompt")
        self.assertFalse((self.target / ".agents/skills/example").exists())

    def test_exclusive_creation_rejects_race(self):
        plan = build_plan(self.source, self.target, "en", [])
        dest = self.target / ".agents/prompts/project-initialization.md"
        dest.parent.mkdir(parents=True)
        dest.write_text("original", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            apply_plan(self.target, plan)
        self.assertEqual(dest.read_text(encoding="utf-8"), "original")

    def test_rejects_unrecognized_and_traversal_skills(self):
        for name in ["missing", "../../private", "not-valid!"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                build_plan(self.source, self.target, "zh-CN", [name])

    def test_rejects_missing_target(self):
        with self.assertRaises(ValueError):
            build_plan(self.source, self.target / "nonexistent", "en", [])

    def test_rejects_toolkit_itself_as_target(self):
        with self.assertRaises(ValueError):
            build_plan(self.source, self.source, "en", [])

    def test_claude_code_places_skills_in_claude_directory(self):
        plan = build_plan(self.source, self.target, "en", ["example"], agent="claude-code")
        apply_plan(self.target, plan)
        self.assertTrue((self.target / ".claude/skills/example/SKILL.md").exists())
        self.assertTrue((self.target / ".claude/skills/example/references/usage.md").exists())
        self.assertTrue((self.target / ".claude/skills/example/THIRD_PARTY_LICENSE.md").exists())
        self.assertFalse((self.target / ".agents/skills").exists())

    def test_codex_and_opencode_use_agent_skills(self):
        for agent in ("codex", "opencode", "generic"):
            with self.subTest(agent=agent):
                plan = build_plan(self.source, self.target, "zh-CN", ["example"], agent=agent)
                self.assertTrue(any(
                    path == self.target / ".agents/skills/example/SKILL.md"
                    for _, path in plan
                ))

    def test_rejects_invalid_agent(self):
        with self.assertRaises(ValueError):
            build_plan(self.source, self.target, "en", [], agent="unknown")

    def test_rejects_nested_target_inside_toolkit(self):
        nested = self.source / "some-project"
        nested.mkdir()
        with self.assertRaises(ValueError):
            build_plan(self.source, nested, "en", [])

    def test_rejects_target_containing_toolkit(self):
        with self.assertRaises(ValueError):
            build_plan(self.source, self.source.parent, "en", [])

    def test_rejects_source_skill_symlinks(self):
        ref = self.source / ".agents/skills/example/references/outside"
        try:
            ref.symlink_to(self.source / "prompts/project-initialization.en.md")
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not available")
        with self.assertRaises(ValueError):
            build_plan(self.source, self.target, "en", ["example"])

    def test_rejects_symlinked_destination_parent(self):
        outside = self.target.parent / "outside"
        outside.mkdir()
        try:
            (self.target / ".agents").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation not available")
        plan = build_plan(self.source, self.target, "en", [])
        self.assertTrue(any("符号链接" in msg for msg in check_conflicts(self.target, plan)))

    def test_rollback_when_later_source_read_fails(self):
        plan = build_plan(self.source, self.target, "en", ["example"])
        missing = self.source / "prompts/missing-late.md"
        # Force a read failure after some output files have been created.
        plan.append((missing, self.target / "last.md"))
        with self.assertRaises(FileNotFoundError):
            apply_plan(self.target, plan)
        self.assertFalse((self.target / ".agents").exists())
        self.assertFalse((self.target / "last.md").exists())


if __name__ == "__main__":
    unittest.main()
