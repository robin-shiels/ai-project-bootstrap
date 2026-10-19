"""Tests for scripts/build_bootstrap_bundle.py and the bundle's consistency.

The bundle is built from a snapshot commit of the current working tree
(temporary index, no ref or worktree change), so these tests check the files
as they are now, exactly as a real build reads them from a commit.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_bootstrap_bundle as bundle
import onboarding_state

LINK = re.compile(r"\]\(([^)\s]+)\)")


def snapshot_commit() -> str:
    """Commit object of the working tree, created without touching any ref."""
    with tempfile.TemporaryDirectory() as tmp:
        env = {
            **os.environ,
            "GIT_INDEX_FILE": str(Path(tmp) / "index"),
            "GIT_AUTHOR_NAME": "bundle-test",
            "GIT_AUTHOR_EMAIL": "bundle-test@example.invalid",
            "GIT_COMMITTER_NAME": "bundle-test",
            "GIT_COMMITTER_EMAIL": "bundle-test@example.invalid",
            "GIT_AUTHOR_DATE": "2026-10-19T00:00:00Z",
            "GIT_COMMITTER_DATE": "2026-10-19T00:00:00Z",
        }

        def run(*args: str, stdin: str | None = None) -> str:
            return subprocess.run(
                ("git", *args),
                cwd=ROOT,
                env=env,
                input=stdin,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        run("add", "-A")
        tree = run("write-tree")
        return run("commit-tree", tree, stdin="bundle test snapshot\n")


class BundleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.commit = snapshot_commit()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "a"
        cls.result = bundle.build(cls.out, cls.commit)
        cls.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        cls.zip_path = cls.out / f"AI-Bootstrap-{cls.version}.zip"
        cls.archive = zipfile.ZipFile(cls.zip_path)
        cls.top = f"AI-Bootstrap-{cls.version}/"
        cls.files = {
            name.removeprefix(cls.top): cls.archive.read(name)
            for name in cls.archive.namelist()
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.archive.close()
        cls.tmp.cleanup()

    def test_outputs_exist(self) -> None:
        names = sorted(p.name for p in self.out.iterdir())
        self.assertEqual(
            names,
            ["AI-Bootstrap-" + self.version + ".zip", "SHA256SUMS", "START_HIER.md"],
        )

    def test_repeated_build_is_byte_identical(self) -> None:
        second = Path(self.tmp.name) / "b"
        bundle.build(second, self.commit)
        for name in ("START_HIER.md", self.zip_path.name, "SHA256SUMS"):
            self.assertEqual(
                (self.out / name).read_bytes(), (second / name).read_bytes(), name
            )

    def test_checksums_match(self) -> None:
        lines = (self.out / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        for line in lines:
            digest, name = line.split("  ", 1)
            self.assertEqual(
                hashlib.sha256((self.out / name).read_bytes()).hexdigest(), digest
            )

    def test_all_required_files_inside_one_top_folder(self) -> None:
        for name in self.archive.namelist():
            self.assertTrue(name.startswith(self.top), name)
            self.assertNotIn("..", Path(name).parts)
            self.assertFalse(name.startswith("/") or "\\" in name, name)
        expected = {*bundle.BUNDLE_FILES, "START_HIER.md", "BUNDLE_MANIFEST.json"}
        self.assertEqual(sorted(self.files), sorted(expected))

    def test_zip_start_file_equals_standalone_start_file(self) -> None:
        self.assertEqual(
            self.files["START_HIER.md"], (self.out / "START_HIER.md").read_bytes()
        )

    def test_manifest_names_exact_source_and_hashes(self) -> None:
        manifest = json.loads(self.files["BUNDLE_MANIFEST.json"])
        self.assertEqual(manifest["source_commit"], self.commit)
        self.assertEqual(manifest["bundle_version"], self.version)
        self.assertEqual(manifest["standard_version"], self.version)
        listed = {entry["path"]: entry for entry in manifest["files"]}
        self.assertEqual(set(listed), set(self.files) - {"BUNDLE_MANIFEST.json"})
        for path, entry in listed.items():
            data = self.files[path]
            self.assertEqual(entry["sha256"], hashlib.sha256(data).hexdigest(), path)
            self.assertEqual(entry["size"], len(data), path)

    def test_sources_come_from_the_commit(self) -> None:
        for path in bundle.BUNDLE_FILES:
            blob = subprocess.run(
                ("git", "show", f"{self.commit}:{path}"),
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(self.files[path], blob, path)

    def test_start_file_embeds_entry_and_paths(self) -> None:
        start = self.files["START_HIER.md"].decode("utf-8")
        for path in bundle.EMBEDDED:
            source = (ROOT / path).read_text(encoding="utf-8").rstrip("\n")
            self.assertIn(f"<!-- BEGIN {path} -->", start)
            self.assertIn(source, start, path)
        self.assertIn(self.commit, start)

    def test_start_file_first_step_needs_no_repository_or_zip(self) -> None:
        start = self.files["START_HIER.md"].decode("utf-8")
        head = start.split("<!-- BEGIN", 1)[0]
        self.assertIn("Lade diese Datei", head)
        self.assertIn("kopiere ihren ganzen Inhalt", head)
        self.assertNotRegex(head, r"(?i)github|repository verbinden")
        self.assertIn("Fragen stellen", start)
        self.assertIn("Frage X von Y", start)
        self.assertIn("Behaupte nicht, das ZIP gelesen zu haben", start)

    def test_internal_links_resolve_inside_the_bundle(self) -> None:
        for path, data in self.files.items():
            if not path.endswith(".md") or path == "START_HIER.md":
                continue
            for target in LINK.findall(data.decode("utf-8")):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0]
                resolved = os.path.normpath(Path(path).parent / relative)
                self.assertTrue(resolved in self.files, f"{path} -> {target}")

    def test_no_private_data_or_work_state(self) -> None:
        for path, data in self.files.items():
            self.assertFalse(
                path.startswith(("docs/", "tasks/", "research/", "dist/")), path
            )
            text = data.decode("utf-8")
            for pattern in onboarding_state.SECRET_PATTERNS[:6]:
                self.assertIsNone(pattern.search(text), f"{path}: {pattern.pattern}")
            self.assertNotRegex(text, r"/home/[a-z]|C:\\Users\\[A-Za-z]", path)

    def test_versions_agree_with_version_file(self) -> None:
        checks = {
            "README.md": rf"\*\*Current standard:\*\* v{re.escape(self.version)}\b",
            "UNIVERSAL_PROJECT_BOOTSTRAP.md": rf"\*\*Version:\*\* {re.escape(self.version)}\b",
            "DEVBOX_GATE_POLICY.md": rf"Universal Project Bootstrap v{re.escape(self.version)}\b",
            "skills/SKILL_MANIFEST.md": rf"\*\*Bootstrap standard:\*\* v{re.escape(self.version)}\b",
            "templates/PROJECT_DISCOVERY.md": rf"\*\*Bootstrap standard:\*\* v{re.escape(self.version)}\b",
            "templates/CODEX_BOOTSTRAP_PROMPT.md": rf"\*\*Bootstrap standard:\*\* v{re.escape(self.version)}\b",
            "CHANGELOG.md": rf"(?m)\A# Changelog\s+## {re.escape(self.version)} ",
        }
        for path, pattern in checks.items():
            self.assertRegex(self.files[path].decode("utf-8"), pattern, path)

    def test_builder_uses_no_network(self) -> None:
        source = (ROOT / "scripts" / "build_bootstrap_bundle.py").read_text()
        for module in ("urllib", "http.client", "socket", "requests"):
            self.assertNotIn(f"import {module}", source)

    def test_zip_entries_are_stored_with_fixed_metadata(self) -> None:
        stamps = {info.date_time for info in self.archive.infolist()}
        self.assertEqual(len(stamps), 1)
        for info in self.archive.infolist():
            self.assertEqual(info.compress_type, zipfile.ZIP_STORED)

    def test_cli_builds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                (
                    sys.executable,
                    str(ROOT / "scripts" / "build_bootstrap_bundle.py"),
                    "--output-dir",
                    tmp,
                    "--source-ref",
                    self.commit,
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                (Path(tmp) / "START_HIER.md").read_bytes(),
                (self.out / "START_HIER.md").read_bytes(),
            )

    def test_zip_extracts_and_state_tool_runs_from_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(io.BytesIO(self.zip_path.read_bytes())) as archive:
                archive.extractall(tmp)
            base = Path(tmp) / self.top
            completed = subprocess.run(
                (
                    sys.executable,
                    "-I",
                    str(base / "scripts" / "onboarding_state.py"),
                    "validate",
                    str(base / "onboarding" / "STATE.example.json"),
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                completed.returncode, 0, completed.stdout + completed.stderr
            )


class GateHostProbeTest(unittest.TestCase):
    SCRIPT = ROOT / "scripts" / "probe_gate_host.py"

    def test_probe_runs_on_this_host(self) -> None:
        completed = subprocess.run(
            (sys.executable, str(self.SCRIPT)),
            capture_output=True,
            text=True,
            check=False,
        )
        if sys.platform.startswith("linux") or sys.platform == "darwin":
            self.assertEqual(
                completed.returncode, 0, completed.stdout + completed.stderr
            )
            self.assertIn("preflight: ok", completed.stdout)
            self.assertIn("memory available:", completed.stdout)
        else:
            self.assertEqual(completed.returncode, 10, completed.stdout)

    def test_probe_reports_native_windows_stop(self) -> None:
        import probe_gate_host

        probe_gate_host.load_gate()  # import every dependency on the real platform
        original = sys.platform
        sys.platform = "win32"
        try:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                code = probe_gate_host.main([])
        finally:
            sys.platform = original
        self.assertEqual(code, 10, out.getvalue())
        self.assertIn("STOP PRECONDITION", out.getvalue())
        self.assertIn("WSL 2", out.getvalue())


if __name__ == "__main__":
    unittest.main()
