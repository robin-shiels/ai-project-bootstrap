"""Tests for the ai-bootstrap plugin: marketplace, manifest and skills."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN = ROOT / "plugins" / "ai-bootstrap"
SKILLS = PLUGIN / "skills"
EXPECTED_SKILLS = ["arbeitsweise", "einrichtung", "projekt-start"]
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if match is None:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


class PluginManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.plugin = json.loads(
            (PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

    def test_marketplace_required_fields(self) -> None:
        self.assertEqual(self.marketplace["name"], "ai-bootstrap")
        self.assertTrue(self.marketplace["owner"]["name"])
        self.assertTrue(self.marketplace["description"])

    def test_marketplace_entry_points_to_plugin(self) -> None:
        (entry,) = self.marketplace["plugins"]
        self.assertEqual(entry["name"], self.plugin["name"])
        self.assertTrue(entry["source"].startswith("./"))
        self.assertNotIn("..", entry["source"])
        self.assertEqual((ROOT / entry["source"]).resolve(), PLUGIN.resolve())

    def test_versions_follow_version_file(self) -> None:
        (entry,) = self.marketplace["plugins"]
        self.assertEqual(entry["version"], self.version)
        self.assertEqual(self.plugin["version"], self.version)

    def test_plugin_name_is_kebab_case(self) -> None:
        self.assertRegex(self.plugin["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")


class SkillTest(unittest.TestCase):
    def test_expected_skills_exist(self) -> None:
        found = sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
        self.assertEqual(found, EXPECTED_SKILLS)

    def test_frontmatter_has_matching_name_and_description(self) -> None:
        for name in EXPECTED_SKILLS:
            fields = frontmatter(SKILLS / name / "SKILL.md")
            with self.subTest(skill=name):
                self.assertEqual(set(fields), {"name", "description"})
                self.assertEqual(fields["name"], name)
                self.assertGreater(len(fields["description"]), 80)
                self.assertLess(len(fields["description"]), 1024)

    def test_referenced_skill_files_exist(self) -> None:
        pattern = re.compile(r"`((?:references|scripts)/[A-Za-z0-9_.-]+)`")
        for name in EXPECTED_SKILLS:
            skill = SKILLS / name
            for ref in pattern.findall((skill / "SKILL.md").read_text("utf-8")):
                with self.subTest(skill=name, ref=ref):
                    self.assertTrue((skill / ref).is_file(), ref)

    def test_referenced_repository_files_exist(self) -> None:
        pattern = re.compile(r"`((?:templates/[A-Za-z0-9_.-]+)|[A-Z_]+\.md)`")
        for path in SKILLS.rglob("*.md"):
            for ref in pattern.findall(path.read_text("utf-8")):
                if ref in {"SKILL.md", "AGENTS.md", "CLAUDE.md"}:
                    continue
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue((ROOT / ref).is_file(), ref)

    def test_question_format_is_defined_once_and_used(self) -> None:
        rules = (SKILLS / "arbeitsweise" / "SKILL.md").read_text("utf-8")
        self.assertIn("Frage X von Y: FRAGE", rules)
        self.assertIn("Empfehlung:", rules)
        self.assertIn("Du kannst auch eine eigene Antwort schreiben.", rules)

    def test_light_merge_conditions_bind_to_checked_commit(self) -> None:
        rules = (SKILLS / "arbeitsweise" / "SKILL.md").read_text("utf-8")
        self.assertIn("--match-head-commit", rules)
        self.assertIn("git merge-base --is-ancestor origin/main HEAD", rules)
        self.assertIn("kein Fork", rules)

    def test_personal_rules_block_is_marked_and_versioned(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        text = (SKILLS / "einrichtung" / "references" / "PERSONAL_RULES.md").read_text(
            "utf-8"
        )
        self.assertIn(f"<!-- ai-bootstrap:begin v{version} -->", text)
        self.assertIn("<!-- ai-bootstrap:end -->", text)
        self.assertIn("Frage X von Y", text)

    def test_permission_profiles_block_dangerous_pushes(self) -> None:
        claude = (SKILLS / "einrichtung" / "references" / "claude-code.md").read_text(
            "utf-8"
        )
        codex = (SKILLS / "einrichtung" / "references" / "chatgpt-codex.md").read_text(
            "utf-8"
        )
        for fragment in ("git push --force", "git push * main", "--admin"):
            self.assertIn(fragment, claude)
        for fragment in (
            '"--force"], decision="forbidden"',
            '"main"], decision="forbidden"',
        ):
            self.assertIn(fragment, codex)
        self.assertNotIn('"Bash(gh pr merge*)"', claude)


if __name__ == "__main__":
    unittest.main()
