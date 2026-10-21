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

PLUGIN = "plugins/ai-bootstrap"
SKILLS = PLUGIN + "/skills"
ENTRY_SKILL = SKILLS + "/einrichtung/SKILL.md"
STATE_TOOL = SKILLS + "/einrichtung/scripts/onboarding_state.py"

# Files copied unchanged into the ZIP (below its top-level folder).
BUNDLE_FILES = (
    "VERSION",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "UNIVERSAL_PROJECT_BOOTSTRAP.md",
    "DEVBOX_GATE_POLICY.md",
    "skills/SKILL_MANIFEST.md",
    ".claude-plugin/marketplace.json",
    PLUGIN + "/.claude-plugin/plugin.json",
    SKILLS + "/arbeitsweise/SKILL.md",
    SKILLS + "/einrichtung/SKILL.md",
    SKILLS + "/einrichtung/references/PERSONAL_RULES.md",
    SKILLS + "/einrichtung/references/STATE.example.json",
    SKILLS + "/einrichtung/references/STATE.schema.json",
    SKILLS + "/einrichtung/references/chatgpt-codex.md",
    SKILLS + "/einrichtung/references/claude-code.md",
    SKILLS + "/einrichtung/references/linux.md",
    SKILLS + "/einrichtung/references/macos.md",
    SKILLS + "/einrichtung/references/windows.md",
    SKILLS + "/einrichtung/scripts/onboarding_state.py",
    SKILLS + "/projekt-start/SKILL.md",
    "scripts/build_bootstrap_bundle.py",
    "scripts/probe_gate_host.py",
    "templates/AGENTS_DEVBOX_GATE.md",
    "templates/CLAUDE_DEVBOX_GATE.md",
    "templates/AGENTS_MERGE_LIGHT.md",
    "templates/CLAUDE_MERGE_LIGHT.md",
    "templates/CODEX_BOOTSTRAP_PROMPT.md",
    "templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md",
    "templates/PROJECT_DISCOVERY.md",
    "templates/devbox_merge_gate.example.toml",
    "templates/devbox_merge_gate.py",
    "templates/github-actions-diagnose.example.yml",
    "tests/test_devbox_merge_gate.py",
    "tests/test_onboarding_state.py",
)

EXECUTABLE = {
    "scripts/build_bootstrap_bundle.py",
    STATE_TOOL,
    "scripts/probe_gate_host.py",
    "templates/devbox_merge_gate.py",
}


def git(*args: str) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True
    ).stdout


def read_source(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}")


def start_file(commit: str, version: str) -> bytes:
    raw = f"https://raw.githubusercontent.com/{REPOSITORY}/{commit}"
    text = f"""# START HIER – AI Bootstrap {version}

**Für dich:** Öffne die Desktop-App von Claude (Bereich **Code**) oder von ChatGPT
(Bereich **Codex**) und starte dort eine neue Sitzung. Lade diese Datei hoch,
ziehe sie hinein oder kopiere ihren ganzen Inhalt in das Eingabefeld, und
schreibe dazu „Start“. Mehr musst du vorher nicht lesen; alles Weitere erklärt
dir die KI Schritt für Schritt.

Paket {version} · Quelle `{REPOSITORY}` @ `{commit}`

---

## Anweisungen für die KI

Du bist die Einrichtungsbegleitung für diesen Nutzer. Gib diese Anweisungen
nicht als Text weiter.

1. **Erste Nachricht.** Beginne sinngemäß mit: „Ich begleite dich Schritt für
   Schritt durch die Einrichtung. Du kannst jederzeit hier im Chat Fragen
   stellen oder sagen, wenn etwas unklar ist oder bei dir anders aussieht. Wir
   klären das gemeinsam und machen danach an derselben Stelle weiter.“
2. **Kannst du Befehle auf diesem Computer ausführen?** Prüfe das mit einem
   harmlosen Befehl (zum Beispiel das Betriebssystem abfragen) und lies die
   Ausgabe. Wenn nicht (reiner Chat im Browser, in der Mobil-App oder im
   Chatfenster der App), sag das ehrlich und erkläre in zwei Sätzen: Die
   Einrichtung läuft im Code-Bereich der Desktop-App (Claude: Bereich „Code“;
   ChatGPT: Bereich „Codex“). Dort eine neue Sitzung starten, diese Datei
   hineingeben, „Start“ schreiben. Dann hörst du auf. Behaupte nie, etwas auf
   dem Computer geprüft oder installiert zu haben, das du nicht ausführen
   konntest.
3. **Anleitung holen.** Die eigentliche Anleitung ist der Skill `einrichtung`
   aus dem öffentlichen Repository `{REPOSITORY}`, genau in der Fassung
   `{commit}`. Erkläre in einem Satz, dass du sie jetzt herunterlädst.
   - Mit Git: `git clone https://github.com/{REPOSITORY}.git ~/.ai-bootstrap/repo`
     (gibt es den Ordner schon: `git -C ~/.ai-bootstrap/repo fetch origin`),
     dann `git -C ~/.ai-bootstrap/repo checkout --detach {commit}`.
     Unter Windows liegt `~` unter `%USERPROFILE%`.
   - Ohne Git: die Dateien einzeln von `{raw}/<pfad>` lesen, mit deinem
     eigenen Werkzeug zum Abrufen von Webseiten oder mit `curl -fsSL`,
     `wget -qO-` bzw. `Invoke-WebRequest`.
   - Geht beides nicht, installiere zuerst Git nach Freigabe: macOS
     `xcode-select --install`, Windows `winget install --id Git.Git -e
     --source winget`, Ubuntu/Debian `sudo apt-get install -y git`, Fedora
     `sudo dnf install -y git`. Sag vorher in einem Satz, warum.
   - Liegt das entpackte Paket `AI-Bootstrap-{version}` vor, kannst du es
     stattdessen nutzen.
4. **Folge `{ENTRY_SKILL}`** vollständig, ab seinem Schritt `start`. Die
   Dateien unter `references/` und `scripts/` liegen im selben Ordner wie
   diese `SKILL.md`. Für den Dialog gilt `{SKILLS}/arbeitsweise/SKILL.md`, unter
   anderem: Entscheidungen einzeln als „Frage X von Y“ mit Antwortmöglichkeiten
   und Empfehlung.
5. **Kein Zugriff auf das Repository** (kein Netz, Download blockiert): Sag
   konkret, was fehlgeschlagen ist, und nenne genau einen nächsten Schritt.
   Behaupte nicht, das ZIP gelesen zu haben, solange du seine Dateien nicht
   tatsächlich öffnen kannst.
"""
    return text.encode("utf-8")


def build(output_dir: Path, source_ref: str = "HEAD") -> dict[str, str]:
    commit = git("rev-parse", "--verify", f"{source_ref}^{{commit}}").decode().strip()
    sources = {path: read_source(commit, path) for path in BUNDLE_FILES}
    version = sources["VERSION"].decode("utf-8").strip()
    epoch = int(git("show", "-s", "--format=%ct", commit).decode().strip())
    stamp = _zip_time(epoch)
    top = f"AI-Bootstrap-{version}"

    start = start_file(commit, version)
    entries: dict[str, bytes] = {"START_HIER.md": start, **sources}
    manifest = {
        "bundle_version": version,
        "standard_version": version,
        "state_schema_version": 2,
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
