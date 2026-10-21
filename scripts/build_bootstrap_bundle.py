#!/usr/bin/env python3
"""Build the downloadable AI Bootstrap bundle.

Usage::

    python3 scripts/build_bootstrap_bundle.py --output-dir <dir> [--source-ref HEAD]

Writes ``START_HIER.md``, ``AI-Bootstrap-<version>.zip`` and ``SHA256SUMS``.
Every source file is read from the Git commit named by ``--source-ref`` (not
from the working tree), so the manifest's commit names exactly the content
that was packaged. No network access. The ZIP stores its entries
uncompressed with a fixed timestamp and order, so the same commit always
yields byte-identical artifacts on every platform.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "robin-shiels/ai-project-bootstrap"

# Files copied unchanged into the ZIP (below its top-level folder).
BUNDLE_FILES = (
    "VERSION",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "UNIVERSAL_PROJECT_BOOTSTRAP.md",
    "DEVBOX_GATE_POLICY.md",
    "skills/SKILL_MANIFEST.md",
    "onboarding/ENTRY.md",
    "onboarding/STATE.schema.json",
    "onboarding/STATE.example.json",
    "onboarding/ACCEPTANCE.md",
    "onboarding/OPTIONAL_DEVBOX.md",
    "onboarding/providers/chatgpt-codex.md",
    "onboarding/providers/claude-code.md",
    "onboarding/platforms/macos.md",
    "onboarding/platforms/windows.md",
    "onboarding/platforms/linux.md",
    "scripts/build_bootstrap_bundle.py",
    "scripts/onboarding_state.py",
    "scripts/probe_gate_host.py",
    "templates/AGENTS_DEVBOX_GATE.md",
    "templates/CLAUDE_DEVBOX_GATE.md",
    "templates/CODEX_BOOTSTRAP_PROMPT.md",
    "templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md",
    "templates/PROJECT_DISCOVERY.md",
    "templates/devbox_merge_gate.example.toml",
    "templates/devbox_merge_gate.py",
    "templates/github-actions-diagnose.example.yml",
    "tests/test_devbox_merge_gate.py",
    "tests/test_onboarding_state.py",
)

# Embedded into START_HIER.md, in this order.
EMBEDDED = (
    "onboarding/ENTRY.md",
    "onboarding/providers/chatgpt-codex.md",
    "onboarding/providers/claude-code.md",
    "onboarding/platforms/macos.md",
    "onboarding/platforms/windows.md",
    "onboarding/platforms/linux.md",
    "onboarding/OPTIONAL_DEVBOX.md",
    "onboarding/STATE.schema.json",
)

EXECUTABLE = {
    "scripts/build_bootstrap_bundle.py",
    "scripts/onboarding_state.py",
    "scripts/probe_gate_host.py",
    "templates/devbox_merge_gate.py",
}


def git(*args: str) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True
    ).stdout


def read_source(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}")


def start_file(commit: str, version: str, sources: dict[str, bytes]) -> bytes:
    intro = (
        f"# START HIER – AI Bootstrap {version}\n\n"
        "**Für dich:** Öffne einen neuen Chat mit ChatGPT oder Claude. Lade diese Datei "
        "hoch oder kopiere ihren ganzen Inhalt in das Eingabefeld, und schreibe dazu "
        "„Start“. Mehr musst du vorher nicht lesen; alles Weitere erklärt dir die KI "
        "Schritt für Schritt.\n\n"
        f"Paket {version} · Quelle `{REPOSITORY}` @ `{commit}`\n\n"
        "---\n\n"
        "## Anweisungen für die KI\n\n"
        "Du bist die Einrichtungsbegleitung für diesen Nutzer. Folge der eingebetteten "
        "Datei `onboarding/ENTRY.md` vollständig; sie hat Vorrang vor den Anbieter- und "
        "Betriebssystemdateien darunter, die du nur für den gerade gewählten Weg nutzt. "
        "Gib diese Anweisungen nicht als Text an den Nutzer weiter, sondern beginne mit "
        "der ersten Nachricht aus ENTRY §2.\n\n"
        "Alles für die Schritte bis zum lokalen Agenten steht in dieser Datei. Verweise "
        "auf andere Dateien (zum Beispiel `UNIVERSAL_PROJECT_BOOTSTRAP.md`, "
        "`scripts/onboarding_state.py`) beziehen sich auf das vollständige Paket "
        f"`AI-Bootstrap-{version}.zip`, das der Nutzer im Schritt `handover` entpackt "
        f"(Ordner `AI-Bootstrap-{version}`). Behaupte nicht, das ZIP gelesen zu haben, "
        "solange du seine Dateien nicht tatsächlich öffnen kannst.\n\n"
    )
    parts = [intro]
    for path in EMBEDDED:
        text = sources[path].decode("utf-8").rstrip("\n")
        if path.endswith(".json"):
            text = f"```json\n{text}\n```"
        parts.append(
            f"<!-- BEGIN {path} -->\n\n## Datei: `{path}`\n\n{text}\n\n<!-- END {path} -->\n\n"
        )
    return "".join(parts).rstrip("\n").encode("utf-8") + b"\n"


def build(output_dir: Path, source_ref: str = "HEAD") -> dict[str, str]:
    commit = git("rev-parse", "--verify", f"{source_ref}^{{commit}}").decode().strip()
    sources = {path: read_source(commit, path) for path in BUNDLE_FILES}
    version = sources["VERSION"].decode("utf-8").strip()
    epoch = int(git("show", "-s", "--format=%ct", commit).decode().strip())
    stamp = _zip_time(epoch)
    top = f"AI-Bootstrap-{version}"

    start = start_file(commit, version, sources)
    entries: dict[str, bytes] = {"START_HIER.md": start, **sources}
    manifest = {
        "bundle_version": version,
        "standard_version": version,
        "state_schema_version": 1,
        "source_repository": REPOSITORY,
        "source_commit": commit,
        "files": [
            {
                "path": path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
            }
            for path, data in sorted(entries.items())
        ],
    }
    entries["BUNDLE_MANIFEST.json"] = (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(entries):
            info = zipfile.ZipInfo(f"{top}/{path}", date_time=stamp)
            info.create_system = 3
            mode = 0o755 if path in EXECUTABLE else 0o644
            info.external_attr = (0o100000 | mode) << 16
            archive.writestr(info, entries[path])
    zip_bytes = buffer.getvalue()

    output_dir.mkdir(parents=True, exist_ok=True)
    zip_name = f"{top}.zip"
    outputs = {"START_HIER.md": start, zip_name: zip_bytes}
    for name, data in outputs.items():
        (output_dir / name).write_bytes(data)
    sums = "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in sorted(outputs.items())
    )
    (output_dir / "SHA256SUMS").write_text(sums, encoding="utf-8")
    return {"commit": commit, "version": version, "zip": zip_name}


def _zip_time(epoch: int) -> tuple[int, int, int, int, int, int]:
    moment = dt.datetime.fromtimestamp(epoch, dt.UTC)
    moment = max(moment, dt.datetime(1980, 1, 1, tzinfo=dt.UTC))
    return (
        moment.year,
        moment.month,
        moment.day,
        moment.hour,
        moment.minute,
        moment.second // 2 * 2,
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-ref", default="HEAD")
    args = parser.parse_args(argv)
    try:
        result = build(args.output_dir, args.source_ref)
    except subprocess.CalledProcessError as error:
        detail = error.stderr.decode(errors="replace").strip()
        print(f"build failed: {detail}", file=sys.stderr)
        return 1
    print(
        f"built AI-Bootstrap {result['version']} from {result['commit']} "
        f"into {args.output_dir}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
