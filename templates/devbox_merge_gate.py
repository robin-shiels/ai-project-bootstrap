#!/usr/bin/env python3
"""Dev-box merge and release gate — product-neutral reference CLI.

Contract: ``DEVBOX_GATE_POLICY.md``. Configuration: a strictly validated TOML
file (see ``devbox_merge_gate.example.toml``). Python >= 3.12, standard
library only; external tools are ``git`` and ``gh`` (plus ``systemd-run`` when
the configuration asks for resource scopes).

The gate is started deliberately. It never deploys and never runs without an
explicit mode:

* ``check-only --pr N`` builds the merge commit ``M`` of the current
  integration ref ``B`` and the PR head ``H`` in a fresh worktree and runs the
  configured plan on ``M``. Nothing is written to the integration ref.
* ``check-only --main SHA`` runs the release plan on exactly the current
  remote integration commit.
* ``merge-ff --pr N --confirm-own-task-pr N`` runs the same PR gate and then
  moves the integration ref from ``B`` to the tested ``M`` with one
  server-side compare-and-swap (GitHub GraphQL ``updateRefs`` with
  ``beforeOid=B``, ``afterOid=M``, ``force=false``). There is no fallback to a
  plain push, a force push, an admin bypass or the pull-request merge API.
* ``probe-ref-cas`` checks compare-and-swap semantics and the token's
  permission on a fresh temporary ref only; never on the integration ref.
* ``validate-config`` parses and validates the configuration, nothing else.

Project code runs under the caller's UID. The scrubbed environment only
prevents accidental credential use; it is no isolation boundary. Code of
untrusted origin is therefore refused with ``ISOLATION_REQUIRED`` unless the
configuration declares an isolated check-only environment whose isolation the
gate verifies before running anything.

Platforms: Linux is the reference. macOS runs natively through a small host
adapter (memory from ``vm_stat``/``sysctl``, processes from ``ps``) and
refuses systemd-only options instead of ignoring them. Native Windows is not
supported; the gate stops with ``PRECONDITION`` and names WSL 2, where the
Linux path runs unchanged.
"""

from __future__ import annotations

import argparse
import datetime as dt
import enum
import fnmatch
import hashlib
import json
import os
import re
import shutil
import signal
import stat
import string
import subprocess
import sys
import threading
import time
import tomllib
import uuid
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import IO, Protocol

try:
    import fcntl
except ImportError:  # native Windows: platform_preflight() stops before any use
    fcntl = None  # type: ignore[assignment]

SCHEMA_VERSION = 1
ZERO_OID = "0" * 40
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REF_RE = re.compile(r"^refs/heads/[A-Za-z0-9._/-]+$")
ENV_NAME_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")
# Inherited variables with these names are never passed to project code.
CREDENTIAL_ENV_RE = re.compile(
    r"(TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|API_KEY|PRIVATE_KEY|^GH_|^GITHUB_"
    r"|^SSH_AUTH_SOCK$|^SSH_AGENT|^GIT_ASKPASS$|^SSH_ASKPASS$|^AWS_|^GOOGLE_APPLICATION)"
)
PLANS = ("docs-only", "full", "release")
PLACEHOLDERS = frozenset({"base", "target", "worktree", "run_id", "run_dir"})

BUILTIN_SECRET_PATTERNS = (
    r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"AKIA[0-9A-Z]{16}",
    r"(?i)authorization:\s*(bearer|token|basic)\s+\S+",
    r"(?i)password=\S{6,}",
    r"xox[abprs]-[A-Za-z0-9-]{10,}",
)
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
COUNT_LINE = re.compile(r"\b\d+ (passed|failed|tests?|errors?)\b")


class Code(enum.IntEnum):
    """Process exit codes. Every stop before the ref update leaves it unchanged."""

    PASS = 0
    USAGE = 2
    CONFIG = 3
    PRECONDITION = 10
    HEAD_MISMATCH = 11
    BASE_MOVED = 12
    NOT_AUTHORIZED = 13
    EXCLUDED_PATHS = 14
    ISOLATION_REQUIRED = 15
    RESOURCES = 16
    MERGE_TOPOLOGY = 17
    GATE_FAILED = 20
    LOG_INTEGRITY = 21
    REF_UPDATE_REJECTED = 30
    POST_VERIFY = 31
    ERROR = 40


class GateStop(Exception):
    """A stop condition. The message is safe to print and to log."""

    def __init__(self, code: Code, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class StepSpec:
    name: str
    argv: tuple[str, ...]
    timeout_s: int
    plans: tuple[str, ...]
    application: bool
    env: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class OwnerException:
    pr: int
    head_ref: str
    author: str
    decision: str


@dataclass(frozen=True)
class Config:
    source: Path
    raw_sha256: str
    slug: str
    remote: str
    integration_ref: str
    gate_script: str
    gate_config: str
    trusted_authors: tuple[str, ...]
    check_head_patterns: tuple[str, ...]
    merge_head_patterns: tuple[str, ...]
    done_statuses: tuple[str, ...]
    require_merge_ready: bool
    never_merge_heads: tuple[str, ...]
    exceptions: tuple[OwnerException, ...]
    untrusted_code: str
    forbidden_uids: tuple[int, ...]
    must_not_read: tuple[str, ...]
    docs_only: tuple[str, ...]
    force_full: tuple[str, ...]
    merge_excluded: tuple[str, ...]
    application_markers: tuple[str, ...]
    min_mem_available_mib: int
    min_swap_free_mib: int
    heavy_process_patterns: tuple[str, ...]
    systemd_scope: bool
    scope_properties: tuple[str, ...]
    watched_user_services: tuple[str, ...]
    state_dir: Path
    temp_ref_prefix: str
    env_pass: tuple[str, ...]
    env_set: tuple[tuple[str, str], ...]
    secret_patterns: tuple[str, ...]
    setup: tuple[StepSpec, ...]
    steps: tuple[StepSpec, ...]
    teardown: tuple[StepSpec, ...]

    @property
    def base_branch(self) -> str:
        return self.integration_ref.removeprefix("refs/heads/")

    @property
    def probe_ref_prefix(self) -> str:
        return f"{self.temp_ref_prefix}probe-"

    @property
    def contract_paths(self) -> tuple[str, str]:
        return (self.gate_script, self.gate_config)


class _Table:
    """Strict reader for one TOML table: unknown keys and wrong types fail."""

    def __init__(self, data: object, where: str) -> None:
        if not isinstance(data, dict):
            raise ConfigError(f"{where}: table expected")
        self.data: dict[str, object] = data
        self.where = where
        self.used: set[str] = set()

    def _get(self, key: str) -> object:
        if key not in self.data:
            raise ConfigError(f"{self.where}.{key}: required key missing")
        self.used.add(key)
        return self.data[key]

    def has(self, key: str) -> bool:
        return key in self.data

    def text(self, key: str, pattern: re.Pattern[str] | None = None) -> str:
        value = self._get(key)
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(f"{self.where}.{key}: non-empty string expected")
        if pattern is not None and not pattern.match(value):
            raise ConfigError(f"{self.where}.{key}: invalid value {value!r}")
        return value

    def flag(self, key: str) -> bool:
        value = self._get(key)
        if not isinstance(value, bool):
            raise ConfigError(f"{self.where}.{key}: boolean expected")
        return value

    def number(self, key: str, minimum: int = 0, maximum: int | None = None) -> int:
        value = self._get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ConfigError(f"{self.where}.{key}: integer >= {minimum} expected")
        if maximum is not None and value > maximum:
            raise ConfigError(f"{self.where}.{key}: integer <= {maximum} expected")
        return value

    def strs(self, key: str, non_empty: bool = False) -> tuple[str, ...]:
        value = self._get(key)
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            raise ConfigError(f"{self.where}.{key}: list of non-empty strings expected")
        if non_empty and not value:
            raise ConfigError(f"{self.where}.{key}: must not be empty")
        return tuple(value)

    def ints(self, key: str) -> tuple[int, ...]:
        value = self._get(key)
        if not isinstance(value, list) or not all(
            isinstance(item, int) and not isinstance(item, bool) for item in value
        ):
            raise ConfigError(f"{self.where}.{key}: list of integers expected")
        return tuple(value)

    def table(self, key: str) -> _Table:
        return _Table(self._get(key), f"{self.where}.{key}")

    def tables(self, key: str, required: bool = True) -> list[_Table]:
        if not required and key not in self.data:
            return []
        value = self._get(key)
        if not isinstance(value, list):
            raise ConfigError(f"{self.where}.{key}: array of tables expected")
        return [
            _Table(item, f"{self.where}.{key}[{i}]") for i, item in enumerate(value)
        ]

    def str_map(self, key: str) -> tuple[tuple[str, str], ...]:
        table = self.table(key)
        items: list[tuple[str, str]] = []
        for name, value in table.data.items():
            if not ENV_NAME_RE.match(name) or not isinstance(value, str):
                raise ConfigError(f'{table.where}.{name}: NAME = "string" expected')
            items.append((name, value))
        table.used = set(table.data)
        return tuple(items)

    def done(self) -> None:
        unknown = sorted(set(self.data) - self.used)
        if unknown:
            raise ConfigError(f"{self.where}: unknown key(s) {', '.join(unknown)}")


def _check_placeholders(text: str, where: str) -> None:
    for literal, name, spec, conversion in string.Formatter().parse(text):
        del literal
        if name is None:
            continue
        if name not in PLACEHOLDERS or spec or conversion:
            raise ConfigError(
                f"{where}: unsupported placeholder {{{name}}}; allowed: "
                + ", ".join(sorted(PLACEHOLDERS))
            )


def _check_patterns(patterns: Sequence[str], where: str) -> None:
    for pattern in patterns:
        if pattern.startswith("/") or ".." in pattern.split("/"):
            raise ConfigError(
                f"{where}: repository-relative pattern expected: {pattern}"
            )


def _step(table: _Table, kind: str) -> StepSpec:
    name = table.text("name")
    argv = table.strs("argv", non_empty=True)
    for part in argv:
        _check_placeholders(part, f"{table.where}.argv")
    if kind == "steps":
        plans = table.strs("plans", non_empty=True)
        bad = [plan for plan in plans if plan not in PLANS]
        if bad:
            raise ConfigError(
                f"{table.where}.plans: unknown plan(s) {bad}; use {PLANS}"
            )
        application = table.flag("application")
    else:
        plans, application = PLANS, False
    env = table.str_map("env") if table.has("env") else ()
    for env_name, value in env:
        if CREDENTIAL_ENV_RE.search(env_name):
            raise ConfigError(f"{table.where}.env.{env_name}: credential-like name")
        _check_placeholders(value, f"{table.where}.env.{env_name}")
    step = StepSpec(
        name=name,
        argv=argv,
        timeout_s=table.number("timeout_s", minimum=1, maximum=24 * 3600),
        plans=plans,
        application=application,
        env=env,
    )
    table.done()
    return step


def load_config(path: Path) -> Config:
    """Parse and strictly validate a gate configuration file."""
    raw = path.read_bytes()
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"{path}: invalid TOML: {error}") from error
    root = _Table(data, "config")
    if root.number("schema_version", minimum=1) != SCHEMA_VERSION:
        raise ConfigError(f"config.schema_version: only {SCHEMA_VERSION} is supported")

    repo = root.table("repository")
    slug = repo.text("slug", REPO_SLUG_RE)
    remote = repo.text("remote", re.compile(r"^[A-Za-z0-9_.-]+$"))
    integration_ref = repo.text("integration_ref", REF_RE)
    repo.done()

    contract = root.table("contract")
    gate_script = contract.text("gate_script")
    gate_config = contract.text("gate_config")
    _check_patterns((gate_script, gate_config), contract.where)
    contract.done()

    auth = root.table("authorization")
    trusted_authors = auth.strs("trusted_authors", non_empty=True)
    check_heads = auth.strs("check_head_patterns", non_empty=True)
    merge_heads = auth.strs("merge_head_patterns")
    done_statuses = auth.strs("done_statuses", non_empty=True)
    require_merge_ready = auth.flag("require_merge_ready")
    never_merge = auth.strs("never_merge_heads")
    for pattern in (*check_heads, *merge_heads):
        if pattern in {"*", "**", "*/*"}:
            raise ConfigError(f"{auth.where}: wildcard-only head pattern {pattern!r}")
    exceptions: list[OwnerException] = []
    for item in auth.tables("exceptions", required=False):
        head_ref = item.text("head_ref")
        if any(char in head_ref for char in "*?[]"):
            raise ConfigError(f"{item.where}.head_ref: exact branch name required")
        exceptions.append(
            OwnerException(
                pr=item.number("pr", minimum=1),
                head_ref=head_ref,
                author=item.text("author"),
                decision=item.text("decision"),
            )
        )
        item.done()
    auth.done()

    iso = root.table("isolation")
    untrusted = iso.text("untrusted_code")
    if untrusted not in {"refuse", "check-only-in-isolated-env"}:
        raise ConfigError(
            f"{iso.where}.untrusted_code: 'refuse' or 'check-only-in-isolated-env'"
        )
    forbidden_uids = iso.ints("forbidden_uids")
    must_not_read = iso.strs("must_not_read")
    if untrusted != "refuse" and (not forbidden_uids or not must_not_read):
        raise ConfigError(
            f"{iso.where}: isolated mode needs forbidden_uids and must_not_read"
        )
    iso.done()

    paths = root.table("paths")
    docs_only = paths.strs("docs_only")
    force_full = paths.strs("force_full")
    merge_excluded = paths.strs("merge_excluded")
    for key, patterns in (
        ("docs_only", docs_only),
        ("force_full", force_full),
        ("merge_excluded", merge_excluded),
    ):
        _check_patterns(patterns, f"{paths.where}.{key}")
    paths.done()

    app = root.table("application")
    markers = app.strs("markers")
    _check_patterns(markers, app.where)
    app.done()

    res = root.table("resources")
    min_mem = res.number("min_mem_available_mib")
    min_swap = res.number("min_swap_free_mib")
    heavy = res.strs("heavy_process_patterns")
    for pattern in heavy:
        try:
            re.compile(pattern)
        except re.error as error:
            raise ConfigError(f"{res.where}.heavy_process_patterns: {error}") from error
    systemd_scope = res.flag("systemd_scope")
    scope_properties = res.strs("scope_properties")
    for prop in scope_properties:
        if not re.match(r"^[A-Za-z]+=[A-Za-z0-9%.]+$", prop):
            raise ConfigError(f"{res.where}.scope_properties: invalid {prop!r}")
    watched = res.strs("watched_user_services")
    res.done()

    state = root.table("state")
    state_dir = Path(state.text("dir")).expanduser()
    if not state_dir.is_absolute():
        raise ConfigError(f"{state.where}.dir: absolute path (or ~/...) expected")
    temp_prefix = state.text("temp_ref_prefix")
    if not temp_prefix.startswith("refs/heads/") or not temp_prefix.endswith("/"):
        raise ConfigError(f"{state.where}.temp_ref_prefix: refs/heads/<name>/ expected")
    if integration_ref.startswith(temp_prefix) or temp_prefix == "refs/heads/":
        raise ConfigError(
            f"{state.where}.temp_ref_prefix: must not cover integration ref"
        )
    state.done()

    env = root.table("environment")
    env_pass = env.strs("pass")
    for name in env_pass:
        if not ENV_NAME_RE.match(name) or CREDENTIAL_ENV_RE.search(name):
            raise ConfigError(f"{env.where}.pass: variable {name!r} not allowed")
    env_set = env.str_map("set")
    for name, value in env_set:
        if CREDENTIAL_ENV_RE.search(name):
            raise ConfigError(f"{env.where}.set.{name}: credential-like name")
        _check_placeholders(value, f"{env.where}.set.{name}")
    env.done()

    logs = root.table("logs")
    secret_patterns = logs.strs("extra_secret_patterns")
    for pattern in secret_patterns:
        try:
            re.compile(pattern)
        except re.error as error:
            raise ConfigError(f"{logs.where}.extra_secret_patterns: {error}") from error
    logs.done()

    setup = tuple(_step(t, "setup") for t in root.tables("setup", required=False))
    steps = tuple(_step(t, "steps") for t in root.tables("steps"))
    teardown = tuple(
        _step(t, "teardown") for t in root.tables("teardown", required=False)
    )
    names = [step.name for step in (*setup, *steps, *teardown)]
    if len(names) != len(set(names)):
        raise ConfigError("config: step names must be unique")
    for plan in ("full", "release"):
        if not any(plan in step.plans for step in steps):
            raise ConfigError(f"config.steps: plan {plan!r} has no step")
    root.done()

    return Config(
        source=path,
        raw_sha256=hashlib.sha256(raw).hexdigest(),
        slug=slug,
        remote=remote,
        integration_ref=integration_ref,
        gate_script=gate_script,
        gate_config=gate_config,
        trusted_authors=trusted_authors,
        check_head_patterns=check_heads,
        merge_head_patterns=merge_heads,
        done_statuses=done_statuses,
        require_merge_ready=require_merge_ready,
        never_merge_heads=never_merge,
        exceptions=tuple(exceptions),
        untrusted_code=untrusted,
        forbidden_uids=forbidden_uids,
        must_not_read=must_not_read,
        docs_only=docs_only,
        force_full=force_full,
        merge_excluded=merge_excluded,
        application_markers=markers,
        min_mem_available_mib=min_mem,
        min_swap_free_mib=min_swap,
        heavy_process_patterns=heavy,
        systemd_scope=systemd_scope,
        scope_properties=scope_properties,
        watched_user_services=watched,
        state_dir=state_dir,
        temp_ref_prefix=temp_prefix,
        env_pass=env_pass,
        env_set=env_set,
        secret_patterns=(*BUILTIN_SECRET_PATTERNS, *secret_patterns),
        setup=setup,
        steps=steps,
        teardown=teardown,
    )


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class PullRequest:
    number: int
    state: str
    is_draft: bool
    base_ref: str
    head_ref: str
    head_oid: str
    author: str
    is_cross_repository: bool
    title: str
    body: str


@dataclass(frozen=True)
class Handoff:
    status: str | None
    commit: str | None
    blocker: str | None
    merge_ready: str | None


@dataclass
class StepResult:
    name: str
    kind: str
    command: list[str]
    state: str  # PASSED | FAILED | NOT_PRESENT | SKIPPED_DOCS_ONLY
    exit_code: int | None
    duration_s: float
    summary: str
    peak_memory_bytes: int | None
    oom_killed: bool
    timed_out: bool


@dataclass
class ResourceSnapshot:
    mem_available_kib: int
    swap_free_kib: int
    heavy_processes: list[str]
    services: dict[str, str]


@dataclass
class RunRecord:
    run_id: str
    mode: str
    repository: str
    integration_ref: str
    config_sha256: str
    started_at: str
    pr: int | None = None
    pr_head_ref: str | None = None
    base: str | None = None
    head: str | None = None
    merge_commit: str | None = None
    tree: str | None = None
    classification: str | None = None
    application: str | None = None  # present | absent | not-configured
    changed_paths: list[str] = field(default_factory=list)
    diff_sha256: str | None = None
    handoff: dict[str, str | None] | None = None
    handoff_matches_head: bool | None = None
    contract_on_base: bool | None = None
    authorization: str | None = None
    isolation: str | None = None
    tools: dict[str, str] = field(default_factory=dict)
    resources_before: dict[str, object] | None = None
    resources_after: dict[str, object] | None = None
    steps: list[dict[str, object]] = field(default_factory=list)
    result: str = "RUNNING"
    stop_code: str | None = None
    stop_reason: str | None = None
    finished_at: str | None = None


# --------------------------------------------------------------------------
# Pure helpers
# --------------------------------------------------------------------------


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def matches_any(path: str, patterns: Sequence[str]) -> bool:
    """fnmatch with ``*`` crossing directory separators."""
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def classify_paths(config: Config, paths: Sequence[str]) -> str:
    """``docs-only`` or ``full``. Empty, unknown and contract paths are ``full``."""
    if not paths:
        return "full"
    for path in paths:
        if (
            not matches_any(path, config.docs_only)
            or matches_any(path, config.force_full)
            or path in config.contract_paths
        ):
            return "full"
    return "docs-only"


def excluded_paths(config: Config, paths: Sequence[str]) -> list[str]:
    return [path for path in paths if matches_any(path, config.merge_excluded)]


def parse_handoff(body: str) -> Handoff:
    """Read the last ``STATUS``/``COMMIT``/``BLOCKER``/``MERGE_READY`` lines."""

    def last(key: str) -> str | None:
        found = re.findall(rf"(?m)^\s*{key}:\s*(.+?)\s*$", body)
        return found[-1] if found else None

    commit_line = last("COMMIT")
    commit = None
    if commit_line is not None:
        match = re.search(r"\b[0-9a-f]{7,40}\b", commit_line)
        commit = match.group(0) if match else None
    return Handoff(
        status=last("STATUS"),
        commit=commit,
        blocker=last("BLOCKER"),
        merge_ready=last("MERGE_READY"),
    )


def handoff_matches(handoff: Handoff, head: str) -> bool:
    return handoff.commit is not None and head.startswith(handoff.commit)


def blocker_is_none(blocker: str | None) -> bool:
    if blocker is None:
        return False
    return re.match(r"(?i)^(none|keine?|-)\s*\.?$", blocker.strip()) is not None


def summarize_output(text: str) -> str:
    """Last test-count line of a step output, if any (no other raw output)."""
    clean = ANSI_ESCAPE.sub("", text)
    lines = [line.strip() for line in clean.splitlines() if COUNT_LINE.search(line)]
    return lines[-1][:160] if lines else ""


def find_secret_patterns(patterns: Sequence[str], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text)]


def step_environment(config: Config, source: Mapping[str, str]) -> dict[str, str]:
    """Minimal environment for project code; never inherits credentials."""
    env = {"LANG": "C.UTF-8", "NO_COLOR": "1", "FORCE_COLOR": "0"}
    # XDG_RUNTIME_DIR locates the user service manager for systemd-run scopes.
    for name in ("PATH", "HOME", "XDG_RUNTIME_DIR", *config.env_pass):
        if name in source and not CREDENTIAL_ENV_RE.search(name):
            env[name] = source[name]
    env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
    return env


def render(text: str, values: Mapping[str, str]) -> str:
    return text.format_map(dict(values))


def select_steps(
    config: Config, plan: str, application: str
) -> list[tuple[StepSpec, str | None]]:
    """Steps of the configured plan with the reason a step does not run.

    Application steps are ``NOT_PRESENT`` while the tree has none of the
    application markers; steps outside a docs-only plan are recorded as
    ``SKIPPED_DOCS_ONLY``. Neither state is ever reported as passed.
    """
    selected: list[tuple[StepSpec, str | None]] = []
    for step in config.steps:
        if plan not in step.plans:
            if plan == "docs-only":
                selected.append((step, "SKIPPED_DOCS_ONLY"))
            continue
        if step.application and application == "absent":
            selected.append((step, "NOT_PRESENT"))
            continue
        selected.append((step, None))
    return selected


def render_summary(record: RunRecord, log_digest: str | None) -> str:
    """Redacted summary for publication. Contains no raw step output."""
    lines = [
        f"### Dev-box merge gate: {record.result}",
        "",
        (
            f"- Mode: `{record.mode}`, run `{record.run_id}`, config sha256 "
            f"`{record.config_sha256[:16]}`"
        ),
    ]
    if record.pr is not None:
        lines.append(f"- PR #{record.pr} (`{record.pr_head_ref}`)")
    lines += [
        f"- Base `B`: `{record.base}`",
        f"- Head `H`: `{record.head}`",
        f"- Checked commit `M`: `{record.merge_commit}`",
        f"- Tree `T`: `{record.tree}`",
        (
            f"- Classification: `{record.classification}`; application: "
            f"`{record.application}`; changed paths: {len(record.changed_paths)}"
        ),
    ]
    if record.handoff is not None:
        lines.append(
            f"- Handoff COMMIT `{record.handoff.get('commit')}` matches H: "
            f"{'yes' if record.handoff_matches_head else 'no'}"
        )
    if record.contract_on_base is not None:
        lines.append(
            "- Gate contract on B: " + ("yes" if record.contract_on_base else "no")
        )
    if record.authorization:
        lines.append(f"- Authorization: {record.authorization}")
    if record.stop_code is not None:
        lines.append(f"- Stop: `{record.stop_code}`: {record.stop_reason}")
    lines += [
        "",
        "| Step | State | Exit | Duration | Result |",
        "| --- | --- | --- | --- | --- |",
    ]
    for step in record.steps:
        duration = step.get("duration_s")
        duration = duration if isinstance(duration, float | int) else 0.0
        lines.append(
            f"| {step['name']} | {step['state']} | {step['exit_code']} | "
            f"{duration:.0f} s | {step.get('summary') or '–'} |"
        )
    not_run = [
        s["name"]
        for s in record.steps
        if s["state"] != "PASSED" and s["state"] != "FAILED"
    ]
    if not_run:
        lines += [
            "",
            "Not run (never counted as passed): " + ", ".join(str(n) for n in not_run),
        ]
    if record.tools:
        lines += [
            "",
            "Tools: " + ", ".join(f"{k} {v}" for k, v in sorted(record.tools.items())),
        ]
    if log_digest is not None:
        lines.append(f"Log checksum (SHA-256 of `SHA256SUMS`): `{log_digest}`")
    lines += [
        "",
        (
            "Raw logs stay on the dev box. They are owned by the same UID as the "
            "checks and therefore not tamper-proof; the checksum makes later "
            "changes detectable."
        ),
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Git, GitHub and host access
# --------------------------------------------------------------------------


def run_text(
    args: Sequence[str], cwd: Path | None = None, env: Mapping[str, str] | None = None
) -> str:
    completed = subprocess.run(
        list(args),
        cwd=cwd,
        env=None if env is None else dict(env),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise subprocess.CalledProcessError(
            completed.returncode, list(args), completed.stdout, completed.stderr
        )
    return completed.stdout


class Git:
    """Thin git wrapper bound to one repository or worktree."""

    def __init__(self, cwd: Path, remote: str = "origin") -> None:
        self.cwd = cwd
        self.remote = remote

    def __call__(self, *args: str) -> str:
        return run_text(("git", *args), cwd=self.cwd).strip()

    def ok(self, *args: str) -> bool:
        return (
            subprocess.run(
                ("git", *args), cwd=self.cwd, capture_output=True, check=False
            ).returncode
            == 0
        )

    def remote_ref(self, ref: str) -> str | None:
        """Exact remote ref value (``ls-remote`` patterns also match suffixes)."""
        for line in self("ls-remote", self.remote, ref).splitlines():
            oid, _, name = line.partition("\t")
            if name == ref:
                return oid
        return None

    def remote_sha(self, ref: str) -> str:
        oid = self.remote_ref(ref) or ""
        if not SHA_RE.match(oid):
            raise GateStop(Code.PRECONDITION, f"remote {ref} is not readable")
        return oid


class GitHub(Protocol):
    def pull_request(self, number: int) -> PullRequest: ...

    def comment(self, number: int, body: str) -> None: ...

    def repository_id(self) -> str: ...

    def update_ref(self, repository_id: str, ref: str, before: str, after: str) -> None:
        """Server-side compare-and-swap with ``force=false``; raises GateStop."""
        ...


UPDATE_REFS_MUTATION = (
    "mutation($repo: ID!, $name: GitRefname!, $before: GitObjectID!, "
    "$after: GitObjectID!) { updateRefs(input: {repositoryId: $repo, "
    "refUpdates: [{name: $name, beforeOid: $before, afterOid: $after, "
    "force: false}]}) { clientMutationId } }"
)


class GhCli:
    """GitHub access through the authenticated ``gh`` CLI of the gate process."""

    def __init__(self, repository: str) -> None:
        self.repository = repository

    def pull_request(self, number: int) -> PullRequest:
        raw = json.loads(
            run_text(
                (
                    "gh",
                    "pr",
                    "view",
                    str(number),
                    "-R",
                    self.repository,
                    "--json",
                    (
                        "number,state,isDraft,baseRefName,headRefName,headRefOid,"
                        "author,isCrossRepository,title,body"
                    ),
                )
            )
        )
        return PullRequest(
            number=int(raw["number"]),
            state=str(raw["state"]),
            is_draft=bool(raw["isDraft"]),
            base_ref=str(raw["baseRefName"]),
            head_ref=str(raw["headRefName"]),
            head_oid=str(raw["headRefOid"]),
            author=str((raw.get("author") or {}).get("login", "")),
            is_cross_repository=bool(raw["isCrossRepository"]),
            title=str(raw.get("title", "")),
            body=str(raw.get("body") or ""),
        )

    def comment(self, number: int, body: str) -> None:
        subprocess.run(
            (
                "gh",
                "pr",
                "comment",
                str(number),
                "-R",
                self.repository,
                "--body-file",
                "-",
            ),
            input=body,
            text=True,
            capture_output=True,
            check=True,
        )

    def repository_id(self) -> str:
        owner, name = self.repository.split("/", 1)
        raw = json.loads(
            run_text(
                (
                    "gh",
                    "api",
                    "graphql",
                    "-f",
                    (
                        "query=query($o: String!, $n: String!) "
                        "{ repository(owner: $o, name: $n) { id } }"
                    ),
                    "-f",
                    f"o={owner}",
                    "-f",
                    f"n={name}",
                )
            )
        )
        return str(raw["data"]["repository"]["id"])

    def update_ref(self, repository_id: str, ref: str, before: str, after: str) -> None:
        completed = subprocess.run(
            (
                "gh",
                "api",
                "graphql",
                "-f",
                f"query={UPDATE_REFS_MUTATION}",
                "-f",
                f"repo={repository_id}",
                "-f",
                f"name={ref}",
                "-f",
                f"before={before}",
                "-f",
                f"after={after}",
            ),
            capture_output=True,
            text=True,
            check=False,
        )
        detail = (completed.stdout + completed.stderr).strip().replace("\n", " ")[:400]
        if completed.returncode != 0:
            raise GateStop(Code.REF_UPDATE_REJECTED, f"updateRefs rejected: {detail}")
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            raise GateStop(
                Code.REF_UPDATE_REJECTED, f"updateRefs answer unreadable: {detail}"
            ) from error
        if payload.get("errors") or "updateRefs" not in (payload.get("data") or {}):
            raise GateStop(Code.REF_UPDATE_REJECTED, f"updateRefs ambiguous: {detail}")


class Host(Protocol):
    def resources(self) -> ResourceSnapshot: ...

    def uid(self) -> int: ...

    def readable(self, path: str) -> bool: ...


def ancestor_pids(pid: int, proc: Path = Path("/proc")) -> set[int]:
    """The process and all its ancestors along the ``PPid`` chain."""
    seen: set[int] = set()
    while pid > 0 and pid not in seen:
        seen.add(pid)
        try:
            status = (proc / str(pid) / "status").read_text()
        except OSError:
            break
        match = re.search(r"(?m)^PPid:\s*(\d+)", status)
        if match is None:
            break
        pid = int(match.group(1))
    return seen


def find_heavy_processes(
    patterns: Sequence[re.Pattern[str]], proc: Path, own_pid: int
) -> list[str]:
    """Other processes whose command line matches a heavy-check pattern.

    The gate and all its ancestors are skipped: the shell that started the
    gate may mention a pattern in its own command line without running it.
    """
    skip = ancestor_pids(own_pid, proc)
    found: list[str] = []
    for entry in proc.iterdir():
        if not entry.name.isdigit() or int(entry.name) in skip:
            continue
        try:
            raw = (entry / "cmdline").read_bytes()
        except OSError:
            continue
        command = raw.replace(b"\0", b" ").decode(errors="replace").strip()
        if command and any(p.search(command) for p in patterns):
            found.append(f"{entry.name}: {command[:120]}")
    return found


def host_platform(system: str | None = None) -> str:
    """``linux``, ``macos`` or ``unsupported`` for a ``sys.platform`` value."""
    system = sys.platform if system is None else system
    if system.startswith("linux"):
        return "linux"
    if system == "darwin":
        return "macos"
    return "unsupported"


def platform_preflight(config: Config, system: str | None = None) -> None:
    """Stop on a host that cannot provide every configured protection."""
    system = sys.platform if system is None else system
    kind = host_platform(system)
    if kind == "unsupported":
        raise GateStop(
            Code.PRECONDITION,
            f"platform {system!r} is not supported natively; on Windows run the gate "
            "inside WSL 2, otherwise use Linux or macOS",
        )
    if kind == "macos":
        if config.systemd_scope:
            raise GateStop(
                Code.PRECONDITION,
                "systemd_scope = true needs systemd (Linux); set systemd_scope = false "
                "on macOS or run the gate on Linux",
            )
        if config.watched_user_services:
            raise GateStop(
                Code.PRECONDITION,
                "watched_user_services needs systemctl --user (Linux); leave it empty "
                "on macOS",
            )


def parse_vm_stat(text: str) -> int:
    """Conservative available memory in KiB: free plus inactive pages."""
    size = re.search(r"page size of (\d+) bytes", text)
    free = re.search(r"(?m)^Pages free:\s+(\d+)\.", text)
    inactive = re.search(r"(?m)^Pages inactive:\s+(\d+)\.", text)
    if size is None or free is None or inactive is None:
        raise GateStop(Code.ERROR, "vm_stat output not understood")
    pages = int(free.group(1)) + int(inactive.group(1))
    return pages * int(size.group(1)) // 1024


def parse_swapusage(text: str) -> int:
    """Free swap in KiB from ``sysctl -n vm.swapusage``."""
    match = re.search(r"free = ([0-9.]+)([KMG])", text)
    if match is None:
        raise GateStop(Code.ERROR, "vm.swapusage output not understood")
    factor = {"K": 1, "M": 1024, "G": 1024 * 1024}[match.group(2)]
    return int(float(match.group(1)) * factor)


def heavy_processes_from_ps(
    text: str, patterns: Sequence[re.Pattern[str]], own_pid: int
) -> list[str]:
    """Like ``find_heavy_processes`` for ``ps -axww -o pid=,ppid=,command=`` output."""
    table: dict[int, tuple[int, str]] = {}
    for line in text.splitlines():
        parts = line.split(None, 2)
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            table[int(parts[0])] = (int(parts[1]), parts[2] if len(parts) == 3 else "")
    skip: set[int] = set()
    pid = own_pid
    while pid > 0 and pid not in skip:
        skip.add(pid)
        pid = table.get(pid, (0, ""))[0]
    return [
        f"{pid}: {command[:120]}"
        for pid, (_, command) in table.items()
        if pid not in skip and command and any(p.search(command) for p in patterns)
    ]


def _command_output(argv: Sequence[str]) -> str:
    return subprocess.run(
        list(argv), capture_output=True, text=True, check=True, timeout=30
    ).stdout


class LocalHost:
    """Read-only resource, service and permission probe of the local host."""

    def __init__(
        self,
        config: Config,
        proc: Path = Path("/proc"),
        system: str | None = None,
        run: Callable[[Sequence[str]], str] = _command_output,
    ) -> None:
        self.config = config
        self.proc = proc
        self.system = sys.platform if system is None else system
        self.run = run
        self.patterns = [re.compile(p) for p in config.heavy_process_patterns]

    def resources(self) -> ResourceSnapshot:
        if host_platform(self.system) == "macos":
            return self._macos_resources()
        meminfo: dict[str, int] = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, _, value = line.partition(":")
            meminfo[key] = int(value.split()[0])
        return ResourceSnapshot(
            mem_available_kib=meminfo.get("MemAvailable", 0),
            swap_free_kib=meminfo.get("SwapFree", 0),
            heavy_processes=find_heavy_processes(self.patterns, self.proc, os.getpid()),
            services={
                name: self._service_state(name)
                for name in self.config.watched_user_services
            },
        )

    def _macos_resources(self) -> ResourceSnapshot:
        try:
            memory = self.run(("vm_stat",))
            swap = self.run(("sysctl", "-n", "vm.swapusage"))
            processes = self.run(("ps", "-axww", "-o", "pid=,ppid=,command="))
        except (OSError, subprocess.SubprocessError) as error:
            raise GateStop(
                Code.ERROR, f"cannot read macOS resources: {error}"
            ) from error
        return ResourceSnapshot(
            mem_available_kib=parse_vm_stat(memory),
            swap_free_kib=parse_swapusage(swap),
            heavy_processes=heavy_processes_from_ps(
                processes, self.patterns, os.getpid()
            ),
            services={},
        )

    def uid(self) -> int:
        return os.getuid()

    def readable(self, path: str) -> bool:
        target = Path(path).expanduser()
        try:
            if target.is_dir():
                os.listdir(target)
            else:
                with target.open("rb") as handle:
                    handle.read(1)
        except OSError:
            return False
        return True

    @staticmethod
    def _service_state(name: str) -> str:
        completed = subprocess.run(
            ("systemctl", "--user", "is-active", name),
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.stdout.strip() or "unknown"


def check_resources(config: Config, snapshot: ResourceSnapshot) -> None:
    if snapshot.heavy_processes:
        raise GateStop(
            Code.RESOURCES,
            "another heavy check is running: "
            + "; ".join(snapshot.heavy_processes[:5]),
        )
    if snapshot.mem_available_kib < config.min_mem_available_mib * 1024:
        raise GateStop(
            Code.RESOURCES,
            f"MemAvailable {snapshot.mem_available_kib // 1024} MiB < "
            f"{config.min_mem_available_mib} MiB",
        )
    if snapshot.swap_free_kib < config.min_swap_free_mib * 1024:
        raise GateStop(
            Code.RESOURCES,
            f"SwapFree {snapshot.swap_free_kib // 1024} MiB < {config.min_swap_free_mib} MiB",
        )


@contextmanager
def exclusive_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a")
    try:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise GateStop(Code.RESOURCES, f"gate lock is held: {path}") from error
        yield
    finally:
        handle.close()


# --------------------------------------------------------------------------
# Step execution
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Invocation:
    name: str
    kind: str
    argv: list[str]
    env: dict[str, str]
    timeout_s: int


class StepRunner(Protocol):
    def run(self, invocation: Invocation, cwd: Path, log: Path) -> StepResult: ...


class ProcessStepRunner:
    """Runs one argument list without a shell, optionally in a systemd scope."""

    def __init__(self, systemd_scope: bool, scope_properties: Sequence[str]) -> None:
        self.systemd_scope = systemd_scope
        self.scope_properties = tuple(scope_properties)

    def run(self, invocation: Invocation, cwd: Path, log: Path) -> StepResult:
        argv = list(invocation.argv)
        if self.systemd_scope:
            props = [arg for prop in self.scope_properties for arg in ("-p", prop)]
            argv = ["systemd-run", "--user", "--scope", "--quiet", *props, "--", *argv]
        started = time.monotonic()
        peak: list[int] = [0]
        oom: list[bool] = [False]
        timed_out = False
        with log.open("w") as out:
            out.write(f"$ {' '.join(invocation.argv)}\n")
            out.flush()
            try:
                process = subprocess.Popen(
                    argv,
                    cwd=cwd,
                    env=invocation.env,
                    stdout=out,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
            except OSError as error:
                out.write(f"cannot start: {error}\n")
                return StepResult(
                    invocation.name,
                    invocation.kind,
                    list(invocation.argv),
                    "FAILED",
                    None,
                    0.0,
                    "",
                    None,
                    False,
                    False,
                )
            stop = threading.Event()
            watcher = threading.Thread(
                target=_watch_cgroup, args=(process.pid, stop, peak, oom), daemon=True
            )
            if self.systemd_scope:
                watcher.start()
            try:
                exit_code: int | None = process.wait(timeout=invocation.timeout_s)
            except subprocess.TimeoutExpired:
                timed_out = True
                _kill_group(process)
                exit_code = None
            stop.set()
            if self.systemd_scope:
                watcher.join(timeout=5)
        text = log.read_text(errors="replace")
        passed = exit_code == 0 and not timed_out and not oom[0]
        return StepResult(
            name=invocation.name,
            kind=invocation.kind,
            command=list(invocation.argv),
            state="PASSED" if passed else "FAILED",
            exit_code=exit_code,
            duration_s=round(time.monotonic() - started, 1),
            summary=summarize_output(text),
            peak_memory_bytes=peak[0] or None,
            oom_killed=oom[0],
            timed_out=timed_out,
        )


def _kill_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=30)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def cgroup_of(pid: int | str, proc: Path = Path("/proc")) -> str:
    """Unified-hierarchy cgroup path of a process (``0::<path>``)."""
    return (proc / str(pid) / "cgroup").read_text().strip().split("::", 1)[1]


def step_scope(relative: str, own: str) -> str | None:
    """The step's own ``systemd-run`` scope, never the gate's cgroup."""
    if relative == own or not Path(relative).name.startswith("run-"):
        return None
    return relative


def _watch_cgroup(
    pid: int, stop: threading.Event, peak: list[int], oom: list[bool]
) -> None:
    try:
        own = cgroup_of("self")
    except (OSError, IndexError):
        return
    while not stop.is_set():
        try:
            relative = step_scope(cgroup_of(pid), own)
            if relative is not None:
                base = Path("/sys/fs/cgroup") / relative.lstrip("/")
                peak[0] = max(peak[0], int((base / "memory.peak").read_text()))
                match = re.search(
                    r"oom_kill (\d+)", (base / "memory.events").read_text()
                )
                if match and int(match.group(1)) > 0:
                    oom[0] = True
        except (OSError, IndexError, ValueError):
            pass
        stop.wait(0.5)


def _describe_error(error: BaseException) -> str:
    if isinstance(error, subprocess.CalledProcessError):
        command = " ".join(str(part) for part in error.cmd)[:160]
        stderr = str(error.stderr or "").strip().splitlines()
        return f"command failed ({error.returncode}): {command}: {stderr[-1][:200] if stderr else ''}"
    return f"{type(error).__name__}: {error}"[:300]


# --------------------------------------------------------------------------
# Gate
# --------------------------------------------------------------------------


@dataclass
class RunOptions:
    mode: str  # check-only-pr | check-only-main | merge-ff
    repo_dir: Path
    pr: int | None = None
    main_sha: str | None = None
    expect_head: str | None = None
    confirm_own_task_pr: int | None = None
    comment: bool = False
    check_resources: bool = True
    keep_worktree: bool = False


def own_script_bytes() -> bytes:
    return Path(__file__).read_bytes()


class Gate:
    def __init__(
        self,
        config: Config,
        options: RunOptions,
        github: GitHub,
        runner: StepRunner,
        host: Host,
        tools: Callable[[], dict[str, str]],
        environ: Mapping[str, str] | None = None,
        script_bytes: Callable[[], bytes] = own_script_bytes,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        self.options = options
        self.github = github
        self.runner = runner
        self.host = host
        self.tools = tools
        self.environ = dict(os.environ if environ is None else environ)
        self.script_bytes = script_bytes
        self.sleep = sleep
        self.git = Git(options.repo_dir, config.remote)
        self.run_id = (
            dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
            + "-"
            + uuid.uuid4().hex[:6]
        )
        self.record = RunRecord(
            run_id=self.run_id,
            mode=options.mode,
            repository=config.slug,
            integration_ref=config.integration_ref,
            config_sha256=config.raw_sha256,
            started_at=utc_now(),
            pr=options.pr,
        )
        self.run_dir = config.state_dir / "runs" / self.run_id
        self.worktree: Path | None = None
        self.log_digest: str | None = None
        self.out: IO[str] = sys.stdout

    # -- entry -----------------------------------------------------------

    def execute(self) -> int:
        self.run_dir.mkdir(parents=True, exist_ok=False)
        self._say(f"run {self.run_id}, log {self.run_dir}")
        code = Code.PASS
        try:
            with exclusive_lock(self.config.state_dir / "gate.lock"):
                self._execute_locked()
        except GateStop as stop:
            code = self._stop(stop)
        except (subprocess.CalledProcessError, OSError) as error:
            code = self._stop(GateStop(Code.ERROR, _describe_error(error)))
        code = self._finalize_log(code)
        self._remove_worktree()
        return int(code)

    def _stop(self, stop: GateStop) -> Code:
        self._say(f"STOP {stop.code.name} ({int(stop.code)}): {stop.message}")
        if self.log_digest is None:
            self.record.result = "STOP"
            self.record.stop_code = stop.code.name
            self.record.stop_reason = stop.message
        else:
            # The sealed (possibly published) log stays untouched; the outcome
            # after sealing goes to completion.json.
            self._write_completion(
                {
                    "result": "STOP",
                    "stop_code": stop.code.name,
                    "stop_reason": stop.message,
                }
            )
        return stop.code

    def _execute_locked(self) -> None:
        if self.options.check_resources:
            before = self.host.resources()
            self.record.resources_before = asdict(before)
            check_resources(self.config, before)
        self.record.tools = self.tools()
        if self.options.mode == "check-only-main":
            self._prepare_main()
        else:
            self._prepare_pr()
        self._run_plan()
        if self.options.check_resources:
            self.record.resources_after = asdict(self.host.resources())
        if self.options.mode == "merge-ff":
            self.record.result = "GATE_PASS"
            self._merge()
        else:
            self.record.result = "PASS"
            self.record.finished_at = utc_now()
            self._seal_log()
            if self.options.comment and self.options.pr is not None:
                self._publish()

    # -- origin, authorization and isolation ------------------------------

    def _trusted_origin(self, pr: PullRequest) -> bool:
        return (
            not pr.is_cross_repository
            and pr.author in self.config.trusted_authors
            and (
                matches_any(pr.head_ref, self.config.check_head_patterns)
                or self._exception_for(pr) is not None
            )
        )

    def _exception_for(self, pr: PullRequest) -> OwnerException | None:
        for item in self.config.exceptions:
            if (
                item.pr == pr.number
                and item.head_ref == pr.head_ref
                and item.author == pr.author
                and not pr.is_cross_repository
            ):
                return item
        return None

    def _verify_isolation(self, pr: PullRequest) -> None:
        """Untrusted code runs only in a verified isolated check-only environment."""
        origin = f"author {pr.author!r}, branch {pr.head_ref!r}, fork {pr.is_cross_repository}"
        if self.config.untrusted_code == "refuse":
            raise GateStop(
                Code.ISOLATION_REQUIRED,
                f"untrusted origin ({origin}); no project code runs under this UID",
            )
        if self.options.mode == "merge-ff":
            raise GateStop(
                Code.NOT_AUTHORIZED, f"untrusted origin is never merged ({origin})"
            )
        problems: list[str] = []
        if self.host.uid() in self.config.forbidden_uids:
            problems.append(
                f"uid {self.host.uid()} is a forbidden (project/deploy) uid"
            )
        problems += [
            f"readable: {path}"
            for path in self.config.must_not_read
            if self.host.readable(path)
        ]
        leaked = sorted(name for name in self.environ if CREDENTIAL_ENV_RE.search(name))
        if leaked:
            problems.append("credential-like environment: " + ", ".join(leaked))
        if problems:
            raise GateStop(
                Code.ISOLATION_REQUIRED,
                "isolation not verified: " + "; ".join(problems[:5]),
            )
        self.record.isolation = f"verified isolated check-only environment ({origin})"

    def _authorize_merge(self, pr: PullRequest, handoff: Handoff, base: str) -> None:
        config = self.config
        if self.options.confirm_own_task_pr != pr.number:
            raise GateStop(
                Code.NOT_AUTHORIZED, "--confirm-own-task-pr must repeat the PR number"
            )
        if pr.is_draft:
            raise GateStop(Code.NOT_AUTHORIZED, "draft PRs are never merged")
        if pr.is_cross_repository or pr.author not in config.trusted_authors:
            raise GateStop(Code.NOT_AUTHORIZED, "not an own task PR (author or fork)")
        if matches_any(pr.head_ref, config.never_merge_heads):
            raise GateStop(
                Code.NOT_AUTHORIZED,
                f"branch {pr.head_ref} must not be merged by the gate",
            )
        exception = self._exception_for(pr)
        if exception is not None:
            self.record.authorization = f"project exception PR #{exception.pr} {exception.head_ref}: {exception.decision}"
        elif matches_any(pr.head_ref, config.merge_head_patterns):
            self.record.authorization = f"own task branch {pr.head_ref}"
        else:
            raise GateStop(
                Code.NOT_AUTHORIZED, f"branch {pr.head_ref} is no mergeable task branch"
            )
        status = (handoff.status or "").strip().upper()
        if not any(status.startswith(done.upper()) for done in config.done_statuses):
            raise GateStop(Code.NOT_AUTHORIZED, "handoff reports no done STATUS")
        if not handoff_matches(handoff, pr.head_oid):
            raise GateStop(
                Code.HEAD_MISMATCH,
                f"handoff COMMIT {handoff.commit} does not match PR head {pr.head_oid}",
            )
        if not blocker_is_none(handoff.blocker):
            raise GateStop(
                Code.NOT_AUTHORIZED, f"handoff reports a blocker: {handoff.blocker}"
            )
        if (
            config.require_merge_ready
            and (handoff.merge_ready or "").strip().lower() != "yes"
        ):
            raise GateStop(Code.NOT_AUTHORIZED, "handoff lacks MERGE_READY: yes")
        self._require_contract_on_base(base)

    def _require_contract_on_base(self, base: str) -> None:
        """merge-ff runs only with the gate script and config integrated on B."""
        try:
            script = run_text(
                ("git", "show", f"{base}:{self.config.gate_script}"),
                cwd=self.options.repo_dir,
            )
            config = run_text(
                ("git", "show", f"{base}:{self.config.gate_config}"),
                cwd=self.options.repo_dir,
            )
        except subprocess.CalledProcessError as error:
            raise GateStop(
                Code.NOT_AUTHORIZED,
                "gate contract is not integrated on B; merge-ff is locked",
            ) from error
        if hashlib.sha256(config.encode()).hexdigest() != self.config.raw_sha256:
            raise GateStop(
                Code.NOT_AUTHORIZED, "loaded gate config differs from the one on B"
            )
        if script.encode() != self.script_bytes():
            raise GateStop(
                Code.NOT_AUTHORIZED, "running gate script differs from the one on B"
            )

    # -- preparation -----------------------------------------------------

    def _prepare_pr(self) -> None:
        number = self.options.pr
        assert number is not None
        config = self.config
        pr = self.github.pull_request(number)
        self.record.pr_head_ref = pr.head_ref
        if pr.state != "OPEN":
            raise GateStop(Code.PRECONDITION, f"PR #{number} is not open ({pr.state})")
        if pr.base_ref != config.base_branch:
            raise GateStop(
                Code.PRECONDITION, f"PR base is {pr.base_ref}, not {config.base_branch}"
            )
        if not SHA_RE.match(pr.head_oid):
            raise GateStop(Code.PRECONDITION, "PR head is no full SHA")
        if (
            self.options.expect_head is not None
            and pr.head_oid != self.options.expect_head
        ):
            raise GateStop(
                Code.HEAD_MISMATCH,
                f"PR head {pr.head_oid}, expected {self.options.expect_head}",
            )
        handoff = parse_handoff(pr.body)
        self.record.handoff = asdict(handoff)
        self.record.handoff_matches_head = handoff_matches(handoff, pr.head_oid)

        refs = f"refs/merge-gate/{self.run_id}"
        self.git(
            "fetch",
            "--no-tags",
            "--quiet",
            config.remote,
            f"+{config.integration_ref}:{refs}/base",
            f"+refs/pull/{number}/head:{refs}/head",
        )
        base = self.git("rev-parse", f"{refs}/base")
        head = self.git("rev-parse", f"{refs}/head")
        if head != pr.head_oid:
            raise GateStop(
                Code.HEAD_MISMATCH, f"fetched head {head} != PR head {pr.head_oid}"
            )
        self.record.base = base
        self.record.head = head
        self.record.contract_on_base = self.git.ok(
            "cat-file", "-e", f"{base}:{config.gate_script}"
        ) and self.git.ok("cat-file", "-e", f"{base}:{config.gate_config}")

        trusted = self._trusted_origin(pr)
        if not trusted:
            self._verify_isolation(pr)
        if self.options.mode == "merge-ff":
            if not trusted:
                raise GateStop(Code.NOT_AUTHORIZED, "untrusted origin is never merged")
            self._authorize_merge(pr, handoff, base)

        paths = self._changed_paths(base, head)
        self.record.changed_paths = paths
        self.record.diff_sha256 = hashlib.sha256(
            run_text(
                ("git", "diff", "--no-renames", f"{base}...{head}"),
                cwd=self.options.repo_dir,
            ).encode()
        ).hexdigest()
        if self.options.mode == "merge-ff":
            contract = [path for path in paths if path in config.contract_paths]
            if contract:
                raise GateStop(
                    Code.NOT_AUTHORIZED,
                    "a PR that changes the gate contract cannot authorize itself: "
                    + ", ".join(contract),
                )
            blocked = excluded_paths(config, paths)
            if blocked:
                raise GateStop(
                    Code.EXCLUDED_PATHS,
                    "diff contains paths that need a separate owner order: "
                    + ", ".join(blocked[:10]),
                )

        self._build_merge(pr, base, head)
        assert self.record.merge_commit is not None
        merged_paths = self._changed_paths(base, self.record.merge_commit)
        self.record.classification = classify_paths(config, merged_paths)
        self.record.application = self._application_state(self.record.merge_commit)

    def _prepare_main(self) -> None:
        sha = self.options.main_sha
        assert sha is not None
        config = self.config
        if not SHA_RE.match(sha):
            raise GateStop(Code.USAGE, "--main needs a full 40-character SHA")
        remote = self.git.remote_sha(config.integration_ref)
        if remote != sha:
            raise GateStop(
                Code.BASE_MOVED,
                f"remote {config.integration_ref} is {remote}, not {sha}",
            )
        self.git(
            "fetch",
            "--no-tags",
            "--quiet",
            config.remote,
            f"+{config.integration_ref}:refs/merge-gate/{self.run_id}/main",
        )
        if self.git("rev-parse", f"refs/merge-gate/{self.run_id}/main") != sha:
            raise GateStop(
                Code.BASE_MOVED, "fetched integration ref differs from --main"
            )
        parents = self.git("rev-list", "--parents", "-n", "1", sha).split()[1:]
        base = parents[0] if parents else sha
        self.record.base = base
        self.record.head = sha
        self.record.merge_commit = sha
        self.record.tree = self.git("rev-parse", f"{sha}^{{tree}}")
        self.record.changed_paths = self._changed_paths(base, sha) if parents else []
        self.record.classification = "release"
        self.record.application = self._application_state(sha)
        self.worktree = self._add_worktree(sha)

    def _application_state(self, commit: str) -> str:
        markers = self.config.application_markers
        if not markers:
            return "not-configured"
        present = [m for m in markers if self.git.ok("cat-file", "-e", f"{commit}:{m}")]
        if len(present) == len(markers):
            return "present"
        if not present:
            return "absent"
        missing = sorted(set(markers) - set(present))
        raise GateStop(
            Code.PRECONDITION,
            f"application markers incomplete: present {present}, missing {missing}",
        )

    def _changed_paths(self, base: str, target: str) -> list[str]:
        raw = run_text(
            ("git", "diff", "--name-only", "--no-renames", "-z", f"{base}...{target}"),
            cwd=self.options.repo_dir,
        )
        return [path for path in raw.split("\0") if path]

    def _add_worktree(self, commit: str) -> Path:
        path = self.config.state_dir / "worktrees" / self.run_id
        path.parent.mkdir(parents=True, exist_ok=True)
        self.git("worktree", "add", "--quiet", "--detach", str(path), commit)
        return path

    def _build_merge(self, pr: PullRequest, base: str, head: str) -> None:
        self.worktree = self._add_worktree(base)
        tree_git = Git(self.worktree, self.config.remote)
        owner = self.config.slug.split("/", 1)[0]
        message = (
            f"Merge pull request #{pr.number} from {owner}/{pr.head_ref}\n\n{pr.title}\n\n"
            f"Gate-Run: {self.run_id}\nGate-Base: {base}\nGate-Head: {head}\n"
        )
        for ident in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
            if not tree_git.ok("var", ident):
                raise GateStop(
                    Code.PRECONDITION,
                    f"git identity missing ({ident}); configure user.name/user.email "
                    "for the gate checkout",
                )
        merged = subprocess.run(
            ("git", "merge", "--no-ff", "--no-edit", "-m", message, head),
            cwd=self.worktree,
            capture_output=True,
            text=True,
            check=False,
        )
        if merged.returncode != 0:
            unmerged = tree_git("ls-files", "--unmerged")
            tree_git.ok("merge", "--abort")
            if unmerged:
                raise GateStop(
                    Code.MERGE_TOPOLOGY, "merge conflict; integrate in the task branch"
                )
            detail = (merged.stderr or merged.stdout).strip().splitlines()
            raise GateStop(
                Code.ERROR,
                "git merge failed without a conflict: "
                + (detail[-1][:200] if detail else f"exit {merged.returncode}"),
            )
        merge = tree_git("rev-parse", "HEAD")
        self.record.merge_commit = merge
        self.record.tree = tree_git("rev-parse", "HEAD^{tree}")
        self._verify_topology(merge, base, head, self.record.tree)

    def _verify_topology(self, merge: str, base: str, head: str, tree: str) -> None:
        parents = self.git("rev-list", "--parents", "-n", "1", merge).split()[1:]
        if parents != [base, head]:
            raise GateStop(
                Code.MERGE_TOPOLOGY,
                f"parents of M are {parents}, expected {[base, head]}",
            )
        if self.git("rev-parse", f"{merge}^{{tree}}") != tree:
            raise GateStop(Code.MERGE_TOPOLOGY, "tree of M differs")

    # -- plan ------------------------------------------------------------

    def _values(self) -> dict[str, str]:
        assert self.worktree is not None
        return {
            "base": self.record.base or "",
            "target": self.record.merge_commit or "",
            "worktree": str(self.worktree),
            "run_id": re.sub(r"[^a-z0-9]", "_", self.run_id.lower()),
            "run_dir": str(self.run_dir),
        }

    def _invocation(self, spec: StepSpec, kind: str) -> Invocation:
        values = self._values()
        env = step_environment(self.config, self.environ)
        env.update({name: render(value, values) for name, value in self.config.env_set})
        env.update({name: render(value, values) for name, value in spec.env})
        return Invocation(
            name=spec.name,
            kind=kind,
            argv=[render(part, values) for part in spec.argv],
            env=env,
            timeout_s=spec.timeout_s,
        )

    def _run_plan(self) -> None:
        assert self.worktree is not None and self.record.classification is not None
        plan = self.record.classification
        selected = select_steps(
            self.config, plan, self.record.application or "not-configured"
        )
        to_run = [spec for spec, reason in selected if reason is None]
        if not to_run:
            raise GateStop(Code.GATE_FAILED, f"plan {plan!r} runs no step")
        steps_dir = self.run_dir / "steps"
        steps_dir.mkdir()
        index = 0
        completed = False
        try:
            for spec in self.config.setup:
                index += 1
                self._run_one(index, spec, "setup", steps_dir)
            for spec, reason in selected:
                if reason is not None:
                    self.record.steps.append(
                        asdict(
                            StepResult(
                                spec.name,
                                "step",
                                list(spec.argv),
                                reason,
                                None,
                                0.0,
                                "",
                                None,
                                False,
                                False,
                            )
                        )
                    )
                    continue
                index += 1
                self._run_one(index, spec, "step", steps_dir)
            completed = True
        finally:
            failures: list[str] = []
            for spec in self.config.teardown:
                index += 1
                try:
                    self._run_one(index, spec, "teardown", steps_dir)
                except GateStop as stop:
                    failures.append(stop.message)
            self._write_meta()
            # A failed teardown never hides the stop that is already in flight.
            if failures and completed:
                raise GateStop(
                    Code.GATE_FAILED, "teardown failed: " + "; ".join(failures)
                )
        ran = [
            s
            for s in self.record.steps
            if s["kind"] == "step" and s["state"] == "PASSED"
        ]
        if len(ran) != len(to_run):
            raise GateStop(Code.GATE_FAILED, "not every required step ran")

    def _run_one(self, index: int, spec: StepSpec, kind: str, steps_dir: Path) -> None:
        assert self.worktree is not None
        invocation = self._invocation(spec, kind)
        slug = re.sub(r"[^a-z0-9]+", "-", spec.name.lower()).strip("-")
        log = steps_dir / f"{index:02d}-{kind}-{slug}.log"
        self._say(f"[{index}] {kind}: {spec.name}")
        result = self.runner.run(invocation, self.worktree, log)
        self.record.steps.append(asdict(result))
        self._write_meta()
        if result.timed_out:
            raise GateStop(
                Code.GATE_FAILED, f"{spec.name}: timeout after {spec.timeout_s} s"
            )
        if result.oom_killed:
            raise GateStop(Code.GATE_FAILED, f"{spec.name}: memory limit (OOM)")
        if result.exit_code != 0 or result.state != "PASSED":
            raise GateStop(Code.GATE_FAILED, f"{spec.name}: exit {result.exit_code}")

    # -- merge -----------------------------------------------------------

    def _merge(self) -> None:
        number = self.options.pr
        config = self.config
        base, head, merge, tree = (
            self.record.base,
            self.record.head,
            self.record.merge_commit,
            self.record.tree,
        )
        assert number is not None and base and head and merge and tree
        temp_ref = f"{config.temp_ref_prefix}pr-{number}-{merge[:12]}"
        self.git("push", "--quiet", config.remote, f"{merge}:{temp_ref}")
        try:
            self.record.finished_at = utc_now()
            self._seal_log()
            self._publish()
            self._recheck_before_update(number, base, head, merge, tree)
            try:
                self.github.update_ref(
                    self.github.repository_id(), config.integration_ref, base, merge
                )
            except GateStop as stop:
                # A stale beforeOid comes back as a generic error; only the
                # actual remote ref tells what happened.
                remote = self.git.remote_sha(config.integration_ref)
                if remote == merge:
                    raise GateStop(
                        Code.POST_VERIFY,
                        f"updateRefs reported an error but the ref is at M: {stop.message}",
                    ) from stop
                raise GateStop(
                    Code.REF_UPDATE_REJECTED,
                    f"{stop.message} (remote ref unchanged at {remote})"
                    if remote == base
                    else f"{stop.message} (remote ref is now {remote})",
                ) from stop
            self._say(
                f"{config.integration_ref} {base} -> {merge} (updateRefs, force=false)"
            )
            self._verify_after_update(number, merge, tree)
        finally:
            if not self.git.ok("push", "--quiet", config.remote, "--delete", temp_ref):
                self._say(f"BLOCKER: temporary ref {temp_ref} could not be deleted")

    def _recheck_before_update(
        self, number: int, base: str, head: str, merge: str, tree: str
    ) -> None:
        pr = self.github.pull_request(number)
        if pr.state != "OPEN" or pr.is_draft or pr.base_ref != self.config.base_branch:
            raise GateStop(Code.PRECONDITION, "PR state changed before the merge")
        if pr.head_oid != head:
            raise GateStop(
                Code.HEAD_MISMATCH, f"PR head moved: {pr.head_oid} instead of {head}"
            )
        handoff = parse_handoff(pr.body)
        if asdict(handoff) != self.record.handoff:
            raise GateStop(Code.HEAD_MISMATCH, "handoff changed after the checks")
        remote = self.git.remote_sha(self.config.integration_ref)
        if remote != base:
            raise GateStop(
                Code.BASE_MOVED, f"remote ref is {remote}, checked base was {base}"
            )
        if self.log_digest is None or self._digest_now() != self.log_digest:
            raise GateStop(Code.LOG_INTEGRITY, "gate log differs from its checksum")
        self._verify_topology(merge, base, head, tree)

    def _verify_after_update(self, number: int, merge: str, tree: str) -> None:
        config = self.config
        remote = self.git.remote_sha(config.integration_ref)
        if remote != merge:
            raise GateStop(
                Code.POST_VERIFY, f"remote ref is {remote}, expected {merge}"
            )
        after = f"refs/merge-gate/{self.run_id}/after"
        self.git(
            "fetch",
            "--no-tags",
            "--quiet",
            config.remote,
            f"+{config.integration_ref}:{after}",
        )
        if self.git("rev-parse", f"{after}^{{tree}}") != tree:
            raise GateStop(
                Code.POST_VERIFY, "tree of the remote ref differs from the checked tree"
            )
        state = ""
        for _ in range(12):
            state = self.github.pull_request(number).state
            if state == "MERGED":
                break
            self.sleep(5)
        if state != "MERGED":
            raise GateStop(
                Code.POST_VERIFY,
                f"ref holds the checked commit, but PR #{number} is {state}",
            )
        self._write_completion(
            {"result": "MERGED", "ref_after": remote, "tree": tree, "pr_state": state}
        )

    def _write_completion(self, data: dict[str, str]) -> None:
        path = self.run_dir / "completion.json"
        payload = {
            "run_id": self.run_id,
            "log_digest": self.log_digest,
            **data,
            "at": utc_now(),
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        (self.run_dir / "completion.sha256").write_text(
            hashlib.sha256(path.read_bytes()).hexdigest() + "  completion.json\n"
        )

    # -- log -------------------------------------------------------------

    def _publish(self) -> None:
        assert self.options.pr is not None and self.log_digest is not None
        self.github.comment(
            self.options.pr, render_summary(self.record, self.log_digest)
        )

    def _write_meta(self) -> None:
        (self.run_dir / "meta.json").write_text(
            json.dumps(asdict(self.record), indent=2, ensure_ascii=False) + "\n"
        )

    def _sealed_files(self) -> list[Path]:
        skip = {"SHA256SUMS", "completion.json", "completion.sha256"}
        return [
            p
            for p in sorted(self.run_dir.rglob("*"))
            if p.is_file() and p.name not in skip
        ]

    def _seal_log(self) -> None:
        """Scan for secret patterns, write SHA256SUMS and remember its digest."""
        self._write_meta()
        (self.run_dir / "summary.md").write_text(render_summary(self.record, None))
        hits = [
            f"{path.name}: {pattern}"
            for path in self._sealed_files()
            for pattern in find_secret_patterns(
                self.config.secret_patterns, path.read_text(errors="replace")
            )
        ]
        if hits:
            raise GateStop(
                Code.LOG_INTEGRITY, "secret pattern in the log: " + "; ".join(hits[:5])
            )
        self.log_digest = self._digest_now(write=True)

    def _digest_now(self, write: bool = False) -> str:
        lines = [
            f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(self.run_dir)}"
            for path in self._sealed_files()
        ]
        content = "\n".join(lines) + "\n"
        if write:
            (self.run_dir / "SHA256SUMS").write_text(content)
        return hashlib.sha256(content.encode()).hexdigest()

    def _finalize_log(self, code: Code) -> Code:
        """Seal a log that stopped before sealing; never rewrite a sealed one."""
        if self.log_digest is None:
            self.record.finished_at = self.record.finished_at or utc_now()
            try:
                self._seal_log()
            except GateStop as stop:
                self.record.result = "STOP"
                self.record.stop_code = stop.code.name
                self.record.stop_reason = stop.message
                self._write_meta()
                self._say(f"STOP {stop.code.name}: {stop.message}")
                code = stop.code if code == Code.PASS else code
        for path in self.run_dir.rglob("*"):
            if path.is_file():
                path.chmod(stat.S_IRUSR | stat.S_IRGRP)
        self._say(
            f"result {self.record.result}; exit {int(code)}; checksum {self.log_digest}"
        )
        return code

    def _remove_worktree(self) -> None:
        if self.worktree is not None and not self.options.keep_worktree:
            self.git.ok("worktree", "remove", "--force", str(self.worktree))
            if self.worktree.exists():
                shutil.rmtree(self.worktree, ignore_errors=True)
            self.git.ok("worktree", "prune")
        for ref in self.git(
            "for-each-ref", "--format=%(refname)", f"refs/merge-gate/{self.run_id}"
        ).splitlines():
            self.git.ok("update-ref", "-d", ref)

    def _say(self, message: str) -> None:
        print(f"[merge-gate] {message}", file=self.out, flush=True)


# --------------------------------------------------------------------------
# Compare-and-swap probe on a temporary ref
# --------------------------------------------------------------------------


@dataclass
class ProbeCase:
    name: str
    before: str
    after: str
    expect_accept: bool
    expect_ref: str | None
    accepted: bool | None = None
    ref_after: str | None = None
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.accepted == self.expect_accept and self.ref_after == self.expect_ref


def probe_ref_cas(
    config: Config, git: Git, github: GitHub, ref: str
) -> list[ProbeCase]:
    """Exercise ``updateRefs`` on a fresh temporary ref; never the integration ref."""
    if not ref.startswith(config.probe_ref_prefix) or ref == config.integration_ref:
        raise GateStop(Code.USAGE, f"probe only on {config.probe_ref_prefix}*")
    if git.remote_ref(ref) is not None:
        raise GateStop(Code.PRECONDITION, f"probe ref {ref} already exists")
    tip = git.remote_sha(config.integration_ref)
    git("fetch", "--no-tags", "--quiet", config.remote, config.integration_ref)
    chain = git("rev-list", "--first-parent", "-n", "3", tip).split()
    if len(chain) < 3:
        raise GateStop(
            Code.PRECONDITION, "integration ref has too little history for the probe"
        )
    c2, c1, c0 = chain
    git("push", "--quiet", config.remote, f"{c0}:{ref}")
    cases = [
        ProbeCase("fast-forward with matching beforeOid", c0, c1, True, c1),
        # The ref moved to an ancestor of the target: a plain fast-forward push
        # would succeed, the compare-and-swap must not.
        ProbeCase("stale beforeOid, target would be a fast-forward", c0, c2, False, c1),
        ProbeCase(
            "matching beforeOid, no fast-forward (force=false)", c1, c0, False, c1
        ),
        ProbeCase("delete the probe ref", c1, ZERO_OID, True, None),
    ]
    repository_id = github.repository_id()
    try:
        for case in cases:
            try:
                github.update_ref(repository_id, ref, case.before, case.after)
                case.accepted = True
            except GateStop as stop:
                case.accepted = False
                case.detail = stop.message[:200]
            case.ref_after = git.remote_ref(ref)
    finally:
        if git.remote_ref(ref) is not None:
            git.ok("push", "--quiet", config.remote, "--delete", ref)
    return cases


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def tool_versions() -> dict[str, str]:
    versions: dict[str, str] = {"python": sys.version.split()[0]}
    for name, args in {"git": ("git", "--version"), "gh": ("gh", "--version")}.items():
        try:
            completed = subprocess.run(
                args, capture_output=True, text=True, check=False
            )
        except OSError:
            versions[name] = "unavailable"
            continue
        text = (completed.stdout or completed.stderr).strip().splitlines()
        versions[name] = text[0][:60] if text else "unavailable"
    return versions


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="devbox_merge_gate.py",
        description="Dev-box merge gate (DEVBOX_GATE_POLICY.md). No mode, no action.",
    )
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo-dir", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="mode")

    sub.add_parser("validate-config", help="validate the configuration only")

    check = sub.add_parser("check-only", help="check; never write the integration ref")
    target = check.add_mutually_exclusive_group(required=True)
    target.add_argument("--pr", type=int)
    target.add_argument("--main", dest="main_sha")
    check.add_argument("--expect-head")
    check.add_argument(
        "--comment", action="store_true", help="publish the redacted summary"
    )
    check.add_argument("--keep-worktree", action="store_true")

    merge = sub.add_parser(
        "merge-ff", help="check, then compare-and-swap the integration ref"
    )
    merge.add_argument("--pr", type=int, required=True)
    merge.add_argument("--confirm-own-task-pr", type=int, required=True)
    merge.add_argument("--expect-head")

    probe = sub.add_parser(
        "probe-ref-cas", help="check CAS semantics on a temporary ref"
    )
    probe.add_argument("--ref")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.mode is None:
        print(
            "mode missing: validate-config, check-only, merge-ff or probe-ref-cas",
            file=sys.stderr,
        )
        return int(Code.USAGE)
    try:
        config = load_config(args.config)
    except (ConfigError, OSError) as error:
        print(f"CONFIG: {error}", file=sys.stderr)
        return int(Code.CONFIG)
    if args.mode == "validate-config":
        print(
            f"config valid: {config.slug} {config.integration_ref} sha256 {config.raw_sha256}"
        )
        return int(Code.PASS)
    repo_dir = Path(
        run_text(("git", "rev-parse", "--show-toplevel"), cwd=args.repo_dir).strip()
    )
    github = GhCli(config.slug)
    if args.mode == "probe-ref-cas":
        ref = (
            args.ref
            or f"{config.probe_ref_prefix}{dt.datetime.now(dt.UTC):%Y%m%dT%H%M%SZ}"
        )
        try:
            cases = probe_ref_cas(config, Git(repo_dir, config.remote), github, ref)
        except GateStop as stop:
            print(f"STOP {stop.code.name}: {stop.message}", file=sys.stderr)
            return int(stop.code)
        for case in cases:
            print(json.dumps({**asdict(case), "ok": case.ok}, ensure_ascii=False))
        return int(
            Code.PASS if all(case.ok for case in cases) else Code.REF_UPDATE_REJECTED
        )

    if args.mode == "check-only":
        options = RunOptions(
            mode="check-only-main" if args.main_sha else "check-only-pr",
            repo_dir=repo_dir,
            pr=args.pr,
            main_sha=args.main_sha,
            expect_head=args.expect_head,
            comment=args.comment,
            keep_worktree=args.keep_worktree,
        )
    else:
        options = RunOptions(
            mode="merge-ff",
            repo_dir=repo_dir,
            pr=args.pr,
            expect_head=args.expect_head,
            confirm_own_task_pr=args.confirm_own_task_pr,
        )
    try:
        platform_preflight(config)
    except GateStop as stop:
        print(f"STOP {stop.code.name}: {stop.message}", file=sys.stderr)
        return int(stop.code)
    gate = Gate(
        config,
        options,
        github,
        ProcessStepRunner(config.systemd_scope, config.scope_properties),
        LocalHost(config),
        tool_versions,
    )
    return gate.execute()


if __name__ == "__main__":
    sys.exit(main())
