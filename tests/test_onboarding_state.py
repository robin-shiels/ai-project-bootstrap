"""Tests for the portable setup state: schema document, example and validator."""

from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "plugins" / "ai-bootstrap" / "skills" / "einrichtung"
sys.path.insert(0, str(SKILL / "scripts"))

import onboarding_state

SCHEMA = json.loads(
    (SKILL / "references" / "STATE.schema.json").read_text(encoding="utf-8")
)
EXAMPLE = json.loads(
    (SKILL / "references" / "STATE.example.json").read_text(encoding="utf-8")
)


class SchemaDocumentTest(unittest.TestCase):
    def test_required_fields_are_the_state_contract(self) -> None:
        self.assertEqual(
            SCHEMA["required"],
            [
                "schema_version",
                "bundle_version",
                "provider_path",
                "platform",
                "current_step",
                "decisions",
                "verifications",
                "blockers",
                "next_action",
            ],
        )

    def test_unknown_is_an_explicit_value(self) -> None:
        self.assertIn("unknown", SCHEMA["properties"]["provider_path"]["enum"])
        self.assertIn("unknown", SCHEMA["properties"]["platform"]["enum"])

    def test_verification_distinguishes_tool_check_and_user_confirmation(self) -> None:
        item = SCHEMA["properties"]["verifications"]["items"]
        self.assertEqual(
            item["properties"]["source"]["enum"], ["tool_check", "user_confirmation"]
        )
        for key in ("step", "checked_at", "scope", "source", "context"):
            self.assertIn(key, item["required"])

    def test_steps_match_skill_step_catalog(self) -> None:
        entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        catalog = re.findall(r"^### `([a-z_]+)`", entry, flags=re.MULTILINE)
        self.assertEqual(catalog, SCHEMA["$defs"]["step"]["enum"])

    def test_bundle_version_matches_version_source(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(EXAMPLE["bundle_version"], version)


class ValidatorTest(unittest.TestCase):
    def errors(self, state: object) -> list[str]:
        return onboarding_state.validate_state(state, SCHEMA)

    def test_example_is_valid(self) -> None:
        self.assertEqual(self.errors(EXAMPLE), [])

    def test_missing_required_field(self) -> None:
        state = copy.deepcopy(EXAMPLE)
        del state["platform"]
        self.assertTrue(any("platform: missing" in e for e in self.errors(state)))

    def test_unknown_value_must_be_explicit_not_free_text(self) -> None:
        state = copy.deepcopy(EXAMPLE)
        state["platform"] = "unknown"
        self.assertEqual(self.errors(state), [])
        state["platform"] = "weiss nicht"
        self.assertTrue(any("platform: unknown value" in e for e in self.errors(state)))

    def test_invalid_types(self) -> None:
        state = copy.deepcopy(EXAMPLE)
        state["decisions"] = "keine"
        state["schema_version"] = "2"
        errors = self.errors(state)
        self.assertTrue(any("decisions: must be a list" in e for e in errors))
        self.assertTrue(any("schema_version: must be 2" in e for e in errors))

    def test_unsupported_schema_version(self) -> None:
        state = copy.deepcopy(EXAMPLE)
        state["schema_version"] = 3
        errors = self.errors(state)
        self.assertEqual(len(errors), 1)
        self.assertIn("not supported", errors[0])

    def test_unknown_field_rejected(self) -> None:
        state = copy.deepcopy(EXAMPLE)
        state["github_token"] = "x"
        self.assertTrue(
            any("github_token: unknown field" in e for e in self.errors(state))
        )

    def test_unknown_step_rejected(self) -> None:
        state = copy.deepcopy(EXAMPLE)
        state["verifications"][0]["step"] = "installed"
        self.assertTrue(any("verifications[0].step" in e for e in self.errors(state)))

    def test_secret_values_rejected(self) -> None:
        for secret in (
            "ghp_" + "a" * 36,
            "github_pat_" + "b" * 40,
            "sk-ant-" + "c" * 30,
            "-----BEGIN OPENSSH " + "PRIVATE KEY-----",
            "Passwort: hunter2",
        ):
            state = copy.deepcopy(EXAMPLE)
            state["next_action"] = secret
            with self.subTest(secret=secret[:12]):
                self.assertTrue(any("secret-looking" in e for e in self.errors(state)))

    def test_example_files_contain_no_secrets(self) -> None:
        for path in SKILL.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                text = path.read_text(encoding="utf-8")
                for pattern in onboarding_state.SECRET_PATTERNS[:6]:
                    self.assertIsNone(
                        pattern.search(text), f"{path}: {pattern.pattern}"
                    )

    def test_cli_exit_codes(self) -> None:
        script = SKILL / "scripts" / "onboarding_state.py"
        ok = subprocess.run(
            [
                sys.executable,
                str(script),
                "validate",
                str(SKILL / "references" / "STATE.example.json"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        usage = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, check=False
        )
        self.assertEqual(usage.returncode, 2)


V1_STATE = {
    "schema_version": 1,
    "bundle_version": "2.1.0",
    "provider_path": "chatgpt-codex",
    "platform": "windows",
    "current_step": "github_cli",
    "decisions": [
        {
            "id": "permission_profile",
            "answer": "standard",
            "source": "user_choice",
            "decided_at": "2026-10-19",
        }
    ],
    "verifications": [
        {
            "step": step,
            "checked_at": "2026-10-19",
            "scope": "host",
            "source": "tool_check",
            "context": "codex@example",
            "result": "ok",
            "detail": step,
        }
        for step in ("local_agent", "wsl", "git", "permissions", "devbox")
    ],
    "blockers": [
        {"step": "devbox", "description": "kein Server", "since": "2026-10-19"},
        {"step": "trial", "description": "Push fehlt", "since": "2026-10-19"},
    ],
    "next_action": "GitHub CLI anmelden",
}


class MigrationTest(unittest.TestCase):
    def test_every_v1_step_is_mapped(self) -> None:
        v1_steps = {
            "start", "context", "path", "save_state", "local_agent", "handover",
            "wsl", "git", "github_account", "github_cli", "git_identity",
            "chat_github", "python", "skills", "permissions", "project", "trial",
            "done", "devbox",
        }  # fmt: skip
        self.assertEqual(set(onboarding_state.V1_TO_V2_STEP), v1_steps)
        allowed = set(SCHEMA["$defs"]["step"]["enum"]) | {None}
        self.assertLessEqual(set(onboarding_state.V1_TO_V2_STEP.values()), allowed)

    def test_v1_state_is_rejected_with_migration_hint(self) -> None:
        errors = onboarding_state.validate_state(V1_STATE, SCHEMA)
        self.assertEqual(len(errors), 1)
        self.assertIn("migrate", errors[0])

    def test_migration_keeps_decisions_and_maps_steps(self) -> None:
        migrated = onboarding_state.migrate_state(copy.deepcopy(V1_STATE))
        self.assertEqual(onboarding_state.validate_state(migrated, SCHEMA), [])
        self.assertEqual(migrated["schema_version"], 2)
        self.assertEqual(migrated["current_step"], "github")
        self.assertEqual(migrated["decisions"], V1_STATE["decisions"])
        self.assertEqual(
            [v["step"] for v in migrated["verifications"]],
            ["start", "gate", "github", "arbeitsweise"],
        )
        self.assertEqual([b["step"] for b in migrated["blockers"]], ["probelauf"])

    def test_only_v1_can_be_migrated(self) -> None:
        with self.assertRaises(ValueError):
            onboarding_state.migrate_state(copy.deepcopy(EXAMPLE))

    def test_cli_migrate(self) -> None:
        script = SKILL / "scripts" / "onboarding_state.py"
        with tempfile.TemporaryDirectory() as tmp:
            old, new = Path(tmp) / "old.json", Path(tmp) / "new.json"
            old.write_text(json.dumps(V1_STATE), encoding="utf-8")
            done = subprocess.run(
                [sys.executable, str(script), "migrate", str(old), str(new)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertEqual(json.loads(new.read_text())["schema_version"], 2)
            again = subprocess.run(
                [sys.executable, str(script), "migrate", str(new), str(old)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(again.returncode, 1)


if __name__ == "__main__":
    unittest.main()
