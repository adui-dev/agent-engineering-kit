from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_repository import REQUIRED_FILES, check_repository, markdown_targets


class RepositoryValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in REQUIRED_FILES:
            file = self.root / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text("# 示例\n", encoding="utf-8")
        (self.root / "VERSION").write_text("V1.0\n", encoding="utf-8")
        (self.root / "README.md").write_text("# V1.0\n[指南](docs/QUALITY.md)\n", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("# V1.0\n", encoding="utf-8")
        (self.root / "CHANGELOG.md").write_text("# V1.0\n", encoding="utf-8")
        (self.root / "prompts/project-initialization.zh-CN.md").write_text("版本：V1.0\n", encoding="utf-8")
        (self.root / "docs/SKILLS.md").write_text("[skill](../.agents/skills/example/SKILL.md)\n", encoding="utf-8")
        folder = self.root / ".agents/skills/example"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("---\nname: example\ndescription: example task\n---\n", encoding="utf-8")
        (folder / "THIRD_PARTY_LICENSE.md").write_text("MIT\n", encoding="utf-8")

    def test_valid_minimal_repository(self):
        self.assertEqual(check_repository(self.root), [])

    def test_broken_relative_link(self):
        (self.root / "README.md").write_text("# V1.0\n[失效](docs/missing.md)\n", encoding="utf-8")
        self.assertTrue(any("无效文件链接" in e for e in check_repository(self.root)))

    def test_version_mismatch(self):
        (self.root / "prompts/project-initialization.zh-CN.md").write_text("版本：V2.0\n", encoding="utf-8")
        self.assertTrue(any("当前版本 V1.0" in e for e in check_repository(self.root)))

    def test_skill_name_mismatch(self):
        file = self.root / ".agents/skills/example/SKILL.md"
        file.write_text("---\nname: not-example\ndescription: example\n---\n", encoding="utf-8")
        self.assertTrue(any("name 与目录不一致" in e for e in check_repository(self.root)))

    def test_missing_license(self):
        (self.root / ".agents/skills/example/THIRD_PARTY_LICENSE.md").unlink()
        self.assertTrue(any("许可证" in e for e in check_repository(self.root)))

    def test_skips_fenced_links_and_external_url(self):
        source = "~~~md\n[示例](no-file.md)\n~~~\n[外部](https://example.com/)\n[内部](docs/QUALITY.md)\n"
        self.assertEqual(list(markdown_targets(source)), ["https://example.com/", "docs/QUALITY.md"])

    def test_skill_reference_link(self):
        entry = self.root / ".agents/skills/example/SKILL.md"
        entry.write_text(entry.read_text(encoding="utf-8") + "[参考](references/missing.md)\n", encoding="utf-8")
        self.assertTrue(any("无效文件链接" in e for e in check_repository(self.root)))


if __name__ == "__main__":
    unittest.main()
