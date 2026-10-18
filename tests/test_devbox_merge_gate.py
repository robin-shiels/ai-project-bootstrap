"""Tests for templates/devbox_merge_gate.py.

Run with ``python3 -m unittest discover -s tests -v`` (standard library only).
Every test uses a temporary bare repository as ``origin``, a fake GitHub with
server-side compare-and-swap semantics and a fake host. No network, no real
GitHub ref, no hosted runner minutes and no host services are used.
"""

from __future__ import annotations

import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "templates" / "devbox_merge_gate.py"
EXAMPLE = ROOT / "templates" / "devbox_merge_gate.example.toml"

_spec = importlib.util.spec_from_file_location("devbox_merge_gate", SCRIPT)
assert _spec is not None and _spec.loader is not None
gate = importlib.util.module_from_spec(_spec)
sys.modules["devbox_merge_gate"] = gate
_spec.loader.exec_module(gate)

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Gate Test",
    "GIT_AUTHOR_EMAIL": "gate-test@example.invalid",
    "GIT_COMMITTER_NAME": "Gate Test",
    "GIT_COMMITTER_EMAIL": "gate-test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}
FAIL_STEP = "import pathlib, sys; sys.exit(1 if pathlib.Path('FAIL').exists() else 0)"
LEAK_STEP = "print('token ghp_' + 'A' * 36)"
SLEEP_STEP = "import time; time.sleep(30)"
SCRIPT_PATH = ".github/scripts/devbox_merge_gate.py"
CONFIG_PATH = ".github/devbox_merge_gate.toml"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def config_text(state_dir: Path, **overrides: str) -> str:
    values = {
        "untrusted_code": '"refuse"',
        "forbidden_uids": "[]",
        "must_not_read": "[]",
        "merge_heads": '["agent/*"]',
        "markers": '["app.py", "tests"]',
        "exceptions": "",
        "extra_steps": "",
    }
    values.update(overrides)
    return (
        textwrap.dedent(
            f"""\
        schema_version = 1

        [repository]
        slug = "example-owner/example-repo"
        remote = "origin"
        integration_ref = "refs/heads/main"

        [contract]
        gate_script = "{SCRIPT_PATH}"
        gate_config = "{CONFIG_PATH}"

        [authorization]
        trusted_authors = ["example-owner"]
        check_head_patterns = ["agent/*"]
        merge_head_patterns = {values["merge_heads"]}
        done_statuses = ["DONE"]
        require_merge_ready = true
        never_merge_heads = ["agent/gate-bootstrap"]
        {values["exceptions"]}

        [isolation]
        untrusted_code = {values["untrusted_code"]}
        forbidden_uids = {values["forbidden_uids"]}
        must_not_read = {values["must_not_read"]}

        [paths]
        docs_only = ["README.md", "docs/*.md"]
        force_full = ["docs/*GATE*"]
        merge_excluded = [".github/*", "migrations/*"]

        [application]
        markers = {values["markers"]}

        [resources]
        min_mem_available_mib = 100
        min_swap_free_mib = 0
        heavy_process_patterns = []
        systemd_scope = false
        scope_properties = []
        watched_user_services = []

        [state]
        dir = "{state_dir}"
        temp_ref_prefix = "refs/heads/merge-gate/"

        [environment]
        pass = []
        set = {{ GATE_RUN = "{{run_id}}" }}

        [logs]
        extra_secret_patterns = []

        [[steps]]
        name = "diff check"
        argv = ["git", "diff", "--check", "{{base}}", "{{target}}"]
        timeout_s = 60
        plans = ["docs-only", "full", "release"]
        application = false

        [[steps]]
        name = "app tests"
        argv = ["{sys.executable}", "-c", "{FAIL_STEP}"]
        timeout_s = 60
        plans = ["full", "release"]
        application = true
        {values["extra_steps"]}
        """
        ).rstrip()
        + "\n"
    )


class FakeHost:
    def __init__(self) -> None:
        self.mem_kib = 10 * 1024 * 1024
        self.heavy: list[str] = []
        self.user_id = 4242
        self.readable_paths: set[str] = set()

    def resources(self) -> object:
        return gate.ResourceSnapshot(self.mem_kib, 1024 * 1024, list(self.heavy), {})

    def uid(self) -> int:
        return self.user_id

    def readable(self, path: str) -> bool:
        return path in self.readable_paths


class FakeGitHub:
    """GitHub double with updateRefs semantics: beforeOid must match, force=false."""

    def __init__(self, bare: Path) -> None:
        self.bare = bare
        self.prs: dict[int, object] = {}
        self.comments: list[tuple[int, str]] = []
        self.update_calls: list[tuple[str, str, str]] = []
        self.before_update: Callable[[], None] | None = None
        self.on_comment: Callable[[], None] | None = None
        self.ambiguous_after_apply = False

    def pull_request(self, number: int) -> object:
        return self.prs[number]

    def comment(self, number: int, body: str) -> None:
        self.comments.append((number, body))
        if self.on_comment is not None:
            self.on_comment()

    def repository_id(self) -> str:
        return "R_example"

    def _current(self, ref: str) -> str | None:
        result = subprocess.run(
            ("git", "rev-parse", "--verify", "-q", ref),
            cwd=self.bare,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or None

    def update_ref(self, repository_id: str, ref: str, before: str, after: str) -> None:
        self.update_calls.append((ref, before, after))
        if self.before_update is not None:
            self.before_update()
        current = self._current(ref)
        if current != before:
            raise gate.GateStop(
                gate.Code.REF_UPDATE_REJECTED, "updateRefs rejected: stale beforeOid"
            )
        if after == gate.ZERO_OID:
            git(self.bare, "update-ref", "-d", ref, before)
            return
        is_ff = (
            subprocess.run(
                ("git", "merge-base", "--is-ancestor", before, after),
                cwd=self.bare,
                check=False,
            ).returncode
            == 0
        )
        if not is_ff:
            raise gate.GateStop(
                gate.Code.REF_UPDATE_REJECTED, "updateRefs rejected: not a fast-forward"
            )
        git(self.bare, "update-ref", ref, after, before)
        for number, pr in self.prs.items():
            contained = (
                subprocess.run(
                    ("git", "merge-base", "--is-ancestor", pr.head_oid, after),
                    cwd=self.bare,
                    check=False,
                ).returncode
                == 0
            )
            if pr.state == "OPEN" and contained:
                self.prs[number] = replace(pr, state="MERGED")
        if self.ambiguous_after_apply:
            raise gate.GateStop(
                gate.Code.REF_UPDATE_REJECTED, "updateRefs ambiguous: timeout"
            )


class GateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._env = dict(os.environ)
        os.environ.update(GIT_ENV)
        self.tmp = Path(tempfile.mkdtemp(prefix="gate-test-"))
        self.state = self.tmp / "state"
        self.bare = self.tmp / "origin.git"
        self.work = self.tmp / "work"
        self.checkout = self.tmp / "gate"
        subprocess.run(
            ("git", "init", "-q", "--bare", "-b", "main", str(self.bare)), check=True
        )
        subprocess.run(
            ("git", "clone", "-q", str(self.bare), str(self.work)),
            check=True,
            capture_output=True,
        )
        git(self.work, "checkout", "-q", "-b", "main")
        self.host = FakeHost()
        self.github = FakeGitHub(self.bare)
        self.next_pr = 1

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._env)
        for path in self.tmp.rglob("*"):
            try:
                path.chmod(0o700)
            except OSError:
                pass
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- fixtures -------------------------------------------------------------

    def write(self, files: dict[str, str]) -> None:
        for name, content in files.items():
            path = self.work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    def commit(self, message: str, files: dict[str, str]) -> str:
        self.write(files)
        git(self.work, "add", "-A")
        git(self.work, "commit", "-q", "-m", message)
        return git(self.work, "rev-parse", "HEAD")

    def init_main(
        self, with_contract: bool = True, application: bool = True, **cfg: str
    ) -> None:
        self.config_body = config_text(self.state, **cfg)
        self.commit("init", {"README.md": "# Example\n"})
        self.commit("docs", {"docs/guide.md": "Guide\n"})
        files = {"docs/more.md": "More\n"}
        if application:
            files |= {"app.py": "print('app')\n", "tests/test_app.py": "\n"}
        if with_contract:
            files |= {SCRIPT_PATH: SCRIPT.read_text(), CONFIG_PATH: self.config_body}
        self.commit("contract", files)
        git(self.work, "push", "-q", "origin", "main")
        subprocess.run(
            ("git", "clone", "-q", str(self.bare), str(self.checkout)),
            check=True,
            capture_output=True,
        )
        self.config_file = self.tmp / "gate.toml"
        self.config_file.write_text(self.config_body)

    def main_sha(self) -> str:
        return git(self.bare, "rev-parse", "refs/heads/main")

    def open_pr(
        self,
        files: dict[str, str],
        branch: str | None = None,
        author: str = "example-owner",
        fork: bool = False,
        draft: bool = False,
        body: str | None = None,
        base_commit: str | None = None,
    ) -> object:
        number = self.next_pr
        self.next_pr += 1
        branch = branch or f"agent/task-{number}"
        git(self.work, "fetch", "-q", "origin")
        git(self.work, "checkout", "-q", "-B", branch, base_commit or self.main_sha())
        head = self.commit(f"task {number}", files)
        git(self.work, "push", "-q", "-f", "origin", f"{branch}:refs/heads/{branch}")
        git(self.bare, "update-ref", f"refs/pull/{number}/head", head)
        git(self.work, "checkout", "-q", "main")
        if body is None:
            body = f"Task\n\nSTATUS: DONE\nCOMMIT: {head}\nBLOCKER: none\nMERGE_READY: yes\n"
        pr = gate.PullRequest(
            number,
            "OPEN",
            draft,
            "main",
            branch,
            head,
            author,
            fork,
            f"Task {number}",
            body,
        )
        self.github.prs[number] = pr
        return pr

    def run_gate(
        self,
        mode: str,
        pr: int | None = None,
        main_sha: str | None = None,
        confirm: int | None = None,
        config_body: str | None = None,
        environ: dict[str, str] | None = None,
        expect_head: str | None = None,
    ) -> tuple[int, object]:
        path = self.config_file
        if config_body is not None:
            path = self.tmp / "alt.toml"
            path.write_text(config_body)
        config = gate.load_config(path)
        options = gate.RunOptions(
            mode=mode,
            repo_dir=self.checkout,
            pr=pr,
            main_sha=main_sha,
            confirm_own_task_pr=confirm,
            expect_head=expect_head,
        )
        instance = gate.Gate(
            config,
            options,
            self.github,
            gate.ProcessStepRunner(False, ()),
            self.host,
            lambda: {"git": "test"},
            environ={"PATH": os.environ["PATH"]} if environ is None else environ,
            script_bytes=lambda: SCRIPT.read_bytes(),
            sleep=lambda _: None,
        )
        instance.out = io.StringIO()
        code = instance.execute()
        return code, instance

    def assert_stop(self, code: int, instance: object, expected: object) -> None:
        self.assertEqual(code, int(expected), instance.out.getvalue())
        self.assertEqual(instance.record.stop_code, expected.name)

    def ran_steps(self, instance: object) -> list[str]:
        return [
            s["name"]
            for s in instance.record.steps
            if s["state"] in {"PASSED", "FAILED"}
        ]


class PositiveTests(GateTestCase):
    def test_check_only_pr_checks_merge_commit_and_never_writes_main(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr({"app.py": "print('changed')\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        record = run.record
        self.assertEqual(record.result, "PASS")
        self.assertEqual(record.base, before)
        self.assertEqual(record.head, pr.head_oid)
        parents = git(
            self.checkout, "rev-list", "--parents", "-n", "1", record.merge_commit
        ).split()[1:]
        self.assertEqual(parents, [before, pr.head_oid])
        self.assertEqual(
            git(self.checkout, "rev-parse", f"{record.merge_commit}^{{tree}}"),
            record.tree,
        )
        self.assertEqual(record.classification, "full")
        self.assertEqual(self.ran_steps(run), ["diff check", "app tests"])
        self.assertEqual(self.main_sha(), before)
        self.assertEqual(self.github.update_calls, [])
        self.assertTrue((run.run_dir / "SHA256SUMS").exists())
        self.assertEqual(run._digest_now(), run.log_digest)
        self.assertFalse(record.contract_on_base is None)

    def test_check_only_main_requires_exact_remote_sha(self) -> None:
        self.init_main()
        code, run = self.run_gate("check-only-main", main_sha=self.main_sha())
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertEqual(run.record.classification, "release")
        self.assertEqual(self.ran_steps(run), ["diff check", "app tests"])
        stale = git(self.bare, "rev-parse", "main~1")
        code, run = self.run_gate("check-only-main", main_sha=stale)
        self.assert_stop(code, run, gate.Code.BASE_MOVED)
        code, run = self.run_gate("check-only-main", main_sha="abc123")
        self.assert_stop(code, run, gate.Code.USAGE)

    def test_merge_ff_moves_main_by_cas_to_exact_checked_commit(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr({"app.py": "print('feature')\n"})
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        merge = run.record.merge_commit
        self.assertEqual(self.main_sha(), merge)
        self.assertEqual(git(self.bare, "rev-parse", "main^{tree}"), run.record.tree)
        self.assertEqual(self.github.update_calls, [("refs/heads/main", before, merge)])
        self.assertEqual(self.github.prs[pr.number].state, "MERGED")
        self.assertEqual(len(self.github.comments), 1)
        self.assertIn(run.log_digest, self.github.comments[0][1])
        self.assertNotIn("print('feature')", self.github.comments[0][1])
        completion = (run.run_dir / "completion.json").read_text()
        self.assertIn('"result": "MERGED"', completion)
        refs = git(
            self.bare, "for-each-ref", "--format=%(refname)", "refs/heads/merge-gate/"
        )
        self.assertEqual(refs, "")
        self.assertIn("own task branch", run.record.authorization)

    def test_docs_only_plan_is_classified_inside_the_merge_tree(self) -> None:
        self.init_main()
        pr = self.open_pr({"docs/new.md": "New\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertEqual(run.record.classification, "docs-only")
        states = {s["name"]: s["state"] for s in run.record.steps}
        self.assertEqual(
            states, {"diff check": "PASSED", "app tests": "SKIPPED_DOCS_ONLY"}
        )
        self.assertIn(
            "Not run (never counted as passed): app tests",
            (run.run_dir / "summary.md").read_text(),
        )

    def test_gate_documents_count_as_full(self) -> None:
        self.init_main()
        pr = self.open_pr({"docs/MERGE_GATE.md": "Rules\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assertEqual(code, 0)
        self.assertEqual(run.record.classification, "full")

    def test_absent_application_is_reported_not_present(self) -> None:
        self.init_main(application=False)
        pr = self.open_pr({"src.txt": "x\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertEqual(run.record.application, "absent")
        states = {s["name"]: s["state"] for s in run.record.steps}
        self.assertEqual(states["app tests"], "NOT_PRESENT")
        self.assertNotIn("app tests", self.ran_steps(run))

    def test_configuration_changes_repository_commands_and_state_without_code_change(
        self,
    ) -> None:
        self.init_main()
        other_state = self.tmp / "other-state"
        body = (
            config_text(other_state)
            .replace(
                'slug = "example-owner/example-repo"', 'slug = "other-owner/other-repo"'
            )
            .replace(
                'trusted_authors = ["example-owner"]',
                'trusted_authors = ["other-owner"]',
            )
        )
        body = body.replace('"git", "diff", "--check"', '"git", "diff", "--stat"')
        pr = self.open_pr({"app.py": "x = 1\n"}, author="other-owner")
        code, run = self.run_gate("check-only-pr", pr=pr.number, config_body=body)
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertEqual(run.record.repository, "other-owner/other-repo")
        self.assertTrue(run.run_dir.is_relative_to(other_state))
        self.assertTrue((other_state / "gate.lock").exists())
        self.assertEqual(run.record.steps[0]["command"][:3], ["git", "diff", "--stat"])

    def test_owner_exception_allows_one_named_pr_only(self) -> None:
        exc = textwrap.dedent(
            """\
            [[authorization.exceptions]]
            pr = 1
            head_ref = "feature/chain-1"
            author = "example-owner"
            decision = "Owner decision 2026-01-01: named chain"
            """
        )
        self.init_main(exceptions=exc)
        pr = self.open_pr({"app.py": "y = 2\n"}, branch="feature/chain-1")
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertIn("project exception PR #1", run.record.authorization)
        other = self.open_pr({"app.py": "y = 3\n"}, branch="feature/chain-2")
        code, run = self.run_gate("check-only-pr", pr=other.number)
        self.assert_stop(code, run, gate.Code.ISOLATION_REQUIRED)

    def test_probe_ref_cas_uses_only_a_temporary_ref(self) -> None:
        self.init_main()
        config = gate.load_config(self.config_file)
        before = self.main_sha()
        cases = gate.probe_ref_cas(
            config,
            gate.Git(self.checkout),
            self.github,
            "refs/heads/merge-gate/probe-test",
        )
        self.assertTrue(all(case.ok for case in cases), [vars(c) for c in cases])
        self.assertEqual(self.main_sha(), before)
        self.assertTrue(
            all(
                call[0] == "refs/heads/merge-gate/probe-test"
                for call in self.github.update_calls
            )
        )
        with self.assertRaises(gate.GateStop):
            gate.probe_ref_cas(
                config, gate.Git(self.checkout), self.github, "refs/heads/main"
            )


class NegativeTests(GateTestCase):
    def assert_main_unchanged(self, before: str) -> None:
        self.assertEqual(self.main_sha(), before)

    def test_stale_base_although_fast_forward_would_succeed(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr({"app.py": "z = 1\n"})
        # After the checks the integration ref moves to H itself: a plain push
        # of M would still be a fast-forward, the gate must stop anyway.
        self.github.on_comment = lambda: git(
            self.bare, "update-ref", "refs/heads/main", pr.head_oid
        )
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop_after_seal(code, run, gate.Code.BASE_MOVED)
        self.assertEqual(self.main_sha(), pr.head_oid)
        self.assertNotEqual(self.main_sha(), run.record.merge_commit)
        self.assertEqual(self.github.update_calls, [])
        self.assertNotEqual(before, pr.head_oid)

    def test_cas_rejects_race_inside_update(self) -> None:
        self.init_main()
        pr = self.open_pr({"app.py": "z = 2\n"})
        self.github.before_update = lambda: git(
            self.bare, "update-ref", "refs/heads/main", pr.head_oid
        )
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop_after_seal(code, run, gate.Code.REF_UPDATE_REJECTED)
        self.assertEqual(self.main_sha(), pr.head_oid)
        self.assertIn(pr.head_oid, (run.run_dir / "completion.json").read_text())

    def test_ambiguous_answer_reports_actual_ref(self) -> None:
        self.init_main()
        pr = self.open_pr({"app.py": "z = 3\n"})
        self.github.ambiguous_after_apply = True
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop_after_seal(code, run, gate.Code.POST_VERIFY)
        self.assertEqual(self.main_sha(), run.record.merge_commit)
        self.assertEqual(len(self.github.update_calls), 1)

    def assert_stop_after_seal(self, code: int, run: object, expected: object) -> None:
        self.assertEqual(code, int(expected), run.out.getvalue())
        self.assertIn(expected.name, (run.run_dir / "completion.json").read_text())

    def test_fork_and_foreign_prs_run_no_code_without_isolation(self) -> None:
        self.init_main()
        before = self.main_sha()
        for kwargs in (
            {"fork": True},
            {"author": "someone-else"},
            {"branch": "random/x"},
        ):
            pr = self.open_pr({"app.py": "evil = 1\n"}, **kwargs)
            code, run = self.run_gate("check-only-pr", pr=pr.number)
            self.assert_stop(code, run, gate.Code.ISOLATION_REQUIRED)
            self.assertEqual(run.record.steps, [])
            self.assertIsNone(run.worktree)
        self.assert_main_unchanged(before)

    def test_isolated_environment_is_verified_and_never_merges(self) -> None:
        self.init_main(
            untrusted_code='"check-only-in-isolated-env"',
            forbidden_uids="[1000]",
            must_not_read='["/secret/hosts.yml"]',
        )
        pr = self.open_pr({"app.py": "ext = 1\n"}, fork=True)
        self.host.readable_paths = {"/secret/hosts.yml"}
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.ISOLATION_REQUIRED)
        self.host.readable_paths = set()
        self.host.user_id = 1000
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.ISOLATION_REQUIRED)
        self.host.user_id = 4242
        code, run = self.run_gate(
            "check-only-pr",
            pr=pr.number,
            environ={"PATH": os.environ["PATH"], "GH_TOKEN": "x"},
        )
        self.assert_stop(code, run, gate.Code.ISOLATION_REQUIRED)
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertIn("verified isolated", run.record.isolation)
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop(code, run, gate.Code.NOT_AUTHORIZED)

    def test_excluded_path_blocks_merge(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr({"migrations/001.sql": "create table x();\n"})
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop(code, run, gate.Code.EXCLUDED_PATHS)
        self.assert_main_unchanged(before)

    def test_gate_pr_cannot_authorize_itself(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr(
            {CONFIG_PATH: self.config_body.replace("timeout_s = 60", "timeout_s = 61")}
        )
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop(code, run, gate.Code.NOT_AUTHORIZED)
        self.assertIn("cannot authorize itself", run.record.stop_reason)
        pilot = self.open_pr({"app.py": "p = 1\n"}, branch="agent/gate-bootstrap")
        code, run = self.run_gate("merge-ff", pr=pilot.number, confirm=pilot.number)
        self.assert_stop(code, run, gate.Code.NOT_AUTHORIZED)
        self.assert_main_unchanged(before)

    def test_merge_locked_until_contract_is_on_base(self) -> None:
        self.init_main(with_contract=False)
        before = self.main_sha()
        pr = self.open_pr({"app.py": "q = 1\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assertEqual(code, 0, run.out.getvalue())
        self.assertFalse(run.record.contract_on_base)
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop(code, run, gate.Code.NOT_AUTHORIZED)
        self.assertIn("not integrated on B", run.record.stop_reason)
        self.assert_main_unchanged(before)

    def test_running_config_must_equal_config_on_base(self) -> None:
        self.init_main()
        pr = self.open_pr({"app.py": "c = 1\n"})
        changed = self.config_body.replace("timeout_s = 60", "timeout_s = 59")
        code, run = self.run_gate(
            "merge-ff", pr=pr.number, confirm=pr.number, config_body=changed
        )
        self.assert_stop(code, run, gate.Code.NOT_AUTHORIZED)
        self.assertIn("differs from the one on B", run.record.stop_reason)

    def test_merge_authorization_conditions(self) -> None:
        self.init_main()
        before = self.main_sha()
        cases = [
            ({"draft": True}, None, gate.Code.NOT_AUTHORIZED),
            (
                {
                    "body": "STATUS: DONE\nCOMMIT: 0000000\nBLOCKER: none\nMERGE_READY: yes\n"
                },
                None,
                gate.Code.HEAD_MISMATCH,
            ),
            (
                {
                    "body": "STATUS: BLOCKED\nCOMMIT: {head}\nBLOCKER: none\nMERGE_READY: yes\n"
                },
                None,
                gate.Code.NOT_AUTHORIZED,
            ),
            (
                {
                    "body": "STATUS: DONE\nCOMMIT: {head}\nBLOCKER: owner decision open\nMERGE_READY: yes\n"
                },
                None,
                gate.Code.NOT_AUTHORIZED,
            ),
            (
                {"body": "STATUS: DONE\nCOMMIT: {head}\nBLOCKER: none\n"},
                None,
                gate.Code.NOT_AUTHORIZED,
            ),
            ({}, 999, gate.Code.NOT_AUTHORIZED),
        ]
        for kwargs, confirm, expected in cases:
            with self.subTest(kwargs=kwargs, confirm=confirm):
                pr = self.open_pr(
                    {"app.py": f"n = {self.next_pr}\n"},
                    **{k: v for k, v in kwargs.items() if k != "body"},
                )
                if "body" in kwargs:
                    self.github.prs[pr.number] = replace(
                        pr, body=kwargs["body"].format(head=pr.head_oid)
                    )
                code, run = self.run_gate(
                    "merge-ff", pr=pr.number, confirm=confirm or pr.number
                )
                self.assert_stop(code, run, expected)
        self.assert_main_unchanged(before)

    def test_merge_heads_may_be_empty(self) -> None:
        self.init_main(merge_heads="[]")
        pr = self.open_pr({"app.py": "m = 1\n"})
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop(code, run, gate.Code.NOT_AUTHORIZED)

    def test_failed_step_stops_and_keeps_main(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr({"FAIL": "1\n"})
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assert_stop(code, run, gate.Code.GATE_FAILED)
        self.assert_main_unchanged(before)
        self.assertEqual(self.github.comments, [])

    def test_timeout_is_a_failure(self) -> None:
        extra = textwrap.dedent(
            f"""\
            [[steps]]
            name = "slow"
            argv = ["{sys.executable}", "-c", "{SLEEP_STEP}"]
            timeout_s = 1
            plans = ["full", "release"]
            application = false
            """
        )
        self.init_main(extra_steps=extra)
        pr = self.open_pr({"app.py": "t = 1\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.GATE_FAILED)
        self.assertIn("timeout", run.record.stop_reason)

    def test_oom_and_missing_step_results_stop(self) -> None:
        self.init_main()
        pr = self.open_pr({"app.py": "o = 1\n"})

        class OomRunner:
            def run(self, invocation: object, cwd: Path, log: Path) -> object:
                log.write_text("")
                return gate.StepResult(
                    invocation.name,
                    invocation.kind,
                    invocation.argv,
                    "FAILED",
                    None,
                    1.0,
                    "",
                    None,
                    True,
                    False,
                )

        config = gate.load_config(self.config_file)
        options = gate.RunOptions(
            mode="check-only-pr", repo_dir=self.checkout, pr=pr.number
        )
        run = gate.Gate(
            config,
            options,
            self.github,
            OomRunner(),
            self.host,
            dict,
            environ={},
            script_bytes=SCRIPT.read_bytes,
        )
        run.out = io.StringIO()
        self.assertEqual(run.execute(), int(gate.Code.GATE_FAILED))
        self.assertIn("OOM", run.record.stop_reason)

    def test_secret_in_log_blocks_publication_and_merge(self) -> None:
        extra = textwrap.dedent(
            f"""\
            [[steps]]
            name = "leaky"
            argv = ["{sys.executable}", "-c", "{LEAK_STEP}"]
            timeout_s = 30
            plans = ["full", "release"]
            application = false
            """
        )
        self.init_main(extra_steps=extra)
        before = self.main_sha()
        pr = self.open_pr({"app.py": "s = 1\n"})
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assertEqual(code, int(gate.Code.LOG_INTEGRITY), run.out.getvalue())
        self.assertEqual(self.github.comments, [])
        self.assert_main_unchanged(before)

    def test_held_lock_and_low_resources_stop(self) -> None:
        self.init_main()
        pr = self.open_pr({"app.py": "l = 1\n"})
        import fcntl

        self.state.mkdir(parents=True, exist_ok=True)
        with (self.state / "gate.lock").open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.RESOURCES)
        self.host.mem_kib = 1024
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.RESOURCES)
        self.host.mem_kib = 10 * 1024 * 1024
        self.host.heavy = ["123: pytest"]
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.RESOURCES)

    def test_head_moves_or_handoff_changes_before_update(self) -> None:
        self.init_main()
        before = self.main_sha()
        pr = self.open_pr({"app.py": "h = 1\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number, expect_head="f" * 40)
        self.assert_stop(code, run, gate.Code.HEAD_MISMATCH)

        def move_head() -> None:
            self.github.prs[pr.number] = replace(
                self.github.prs[pr.number], head_oid="e" * 40
            )

        self.github.on_comment = move_head
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assertEqual(code, int(gate.Code.HEAD_MISMATCH))
        self.github.prs[pr.number] = pr

        def edit_handoff() -> None:
            self.github.prs[pr.number] = replace(
                pr, body=pr.body + "BLOCKER: new question\n"
            )

        self.github.on_comment = edit_handoff
        code, run = self.run_gate("merge-ff", pr=pr.number, confirm=pr.number)
        self.assertEqual(code, int(gate.Code.HEAD_MISMATCH))
        self.assert_main_unchanged(before)
        self.assertEqual(self.github.update_calls, [])

    def test_conflict_stops(self) -> None:
        self.init_main()
        base = self.main_sha()
        self.commit("main change", {"app.py": "print('main')\n"})
        git(self.work, "push", "-q", "origin", "main")
        pr = self.open_pr({"app.py": "print('branch')\n"}, base_commit=base)
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.MERGE_TOPOLOGY)

    def test_incomplete_application_markers_stop(self) -> None:
        self.init_main(application=False)
        pr = self.open_pr({"app.py": "only = 1\n"})
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.PRECONDITION)

    def test_wrong_base_or_closed_pr_stops(self) -> None:
        self.init_main()
        pr = self.open_pr({"app.py": "b = 1\n"})
        self.github.prs[pr.number] = replace(pr, base_ref="develop")
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.PRECONDITION)
        self.github.prs[pr.number] = replace(pr, state="CLOSED")
        code, run = self.run_gate("check-only-pr", pr=pr.number)
        self.assert_stop(code, run, gate.Code.PRECONDITION)


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="gate-config-"))
        self.body = config_text(self.tmp / "state")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def load(self, body: str) -> object:
        path = self.tmp / "c.toml"
        path.write_text(body)
        return gate.load_config(path)

    def test_example_config_is_valid_and_placeholder_only(self) -> None:
        config = gate.load_config(EXAMPLE)
        self.assertEqual(config.slug, "example-owner/example-repo")
        self.assertEqual(config.untrusted_code, "refuse")

    def test_strictness(self) -> None:
        self.load(self.body)
        broken = {
            "unknown key": self.body.replace(
                "[repository]\n", '[repository]\ncolour = "red"\n'
            ),
            "missing key": self.body.replace("require_merge_ready = true\n", ""),
            "shell string": self.body.replace(
                'argv = ["git", "diff", "--check", "{base}", "{target}"]',
                'argv = "git diff --check"',
            ),
            "placeholder": self.body.replace("{target}", "{HOME}"),
            "wildcard": self.body.replace(
                'check_head_patterns = ["agent/*"]', 'check_head_patterns = ["*"]'
            ),
            "credential pass": self.body.replace("pass = []", 'pass = ["GH_TOKEN"]'),
            "credential env": self.body.replace(
                'GATE_RUN = "{run_id}"', 'API_TOKEN = "x"'
            ),
            "bad plan": self.body.replace(
                'plans = ["full", "release"]', 'plans = ["fast"]'
            ),
            "no release step": self.body.replace(
                'plans = ["full", "release"]', 'plans = ["full"]'
            ).replace(
                'plans = ["docs-only", "full", "release"]',
                'plans = ["docs-only", "full"]',
            ),
            "temp prefix": self.body.replace(
                'temp_ref_prefix = "refs/heads/merge-gate/"',
                'temp_ref_prefix = "refs/heads/"',
            ),
            "isolation incomplete": self.body.replace(
                'untrusted_code = "refuse"',
                'untrusted_code = "check-only-in-isolated-env"',
            ),
            "relative state": self.body.replace(
                f'dir = "{self.tmp / "state"}"', 'dir = "state"'
            ),
            "schema": self.body.replace("schema_version = 1", "schema_version = 2"),
        }
        for name, body in broken.items():
            with self.subTest(name=name):
                self.assertNotEqual(body, self.body, name)
                with self.assertRaises(gate.ConfigError):
                    self.load(body)

    def test_cli_requires_explicit_mode(self) -> None:
        result = subprocess.run(
            (sys.executable, str(SCRIPT), "--config", str(EXAMPLE)),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, int(gate.Code.USAGE))
        result = subprocess.run(
            (sys.executable, str(SCRIPT), "--config", str(EXAMPLE), "validate-config"),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class PureHelperTests(unittest.TestCase):
    def test_handoff_parsing(self) -> None:
        handoff = gate.parse_handoff(
            "STATUS: WIP\nSTATUS: DONE\nCOMMIT: `abcdef1`\nBLOCKER: keine\nMERGE_READY: yes\n"
        )
        self.assertEqual(handoff.status, "DONE")
        self.assertEqual(handoff.commit, "abcdef1")
        self.assertTrue(gate.blocker_is_none(handoff.blocker))
        self.assertFalse(gate.blocker_is_none("none yet, waiting for owner"))
        self.assertFalse(gate.blocker_is_none(None))

    def test_step_environment_drops_credentials(self) -> None:
        config = gate.load_config(EXAMPLE)
        env = gate.step_environment(
            config,
            {"PATH": "/bin", "HOME": "/h", "GH_TOKEN": "x", "SSH_AUTH_SOCK": "s"},
        )
        self.assertEqual(set(env), {"PATH", "HOME", "LANG", "NO_COLOR", "FORCE_COLOR"})


class TemplateHygieneTests(unittest.TestCase):
    FORBIDDEN_EVENTS = re.compile(
        r"(?m)^\s+(push|pull_request|pull_request_target|merge_group|schedule|workflow_run|"
        r"check_suite|check_run|issue_comment|repository_dispatch|release|deployment)\s*:"
    )

    def test_workflow_examples_are_dispatch_only(self) -> None:
        workflows = sorted((ROOT / "templates").glob("*.yml")) + sorted(
            (ROOT / ".github").rglob("*.yml")
        )
        self.assertTrue(workflows, "no workflow example found")
        for path in workflows:
            if path.parts[-2] == "workflows" and ".github" in path.parts:
                self.fail(f"this repository must not carry an active workflow: {path}")
            text = "\n".join(
                line
                for line in path.read_text().splitlines()
                if not line.lstrip().startswith("#")
            )
            self.assertRegex(text, r"(?m)^on:\s*\n\s+workflow_dispatch:", path.name)
            self.assertIsNone(self.FORBIDDEN_EVENTS.search(text), path.name)
            self.assertNotIn("self-hosted", text)
            self.assertNotIn("secrets.", text)


if __name__ == "__main__":
    unittest.main()
