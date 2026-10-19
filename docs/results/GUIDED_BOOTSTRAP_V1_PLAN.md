# Guided Bootstrap v1 – Detailplan

Stand: 2026-10-19 · GBOOT-01 · Auftrag `docs/tasks/GUIDED_BOOTSTRAP_V1.md` (e29b3f2)

## Inventur

- main = `11d642bcfd8de138da81ac11d7e5fedcc9c0028d` (unverändert seit der Planung; geprüft per `git fetch` am 2026-10-19).
- Planungsbranch `docs/guided-bootstrap-design` = `e29b3f21eb877f9f1215d29a4bff5d6dfbac6174`, offener Draft-PR #4. Übernommen wurden nur Designentwurf, Ist-Abgleich und Auftragsdatei (unverändert). PR #4 gilt weiter als Planung, nicht als Implementierung.
- Weitere offene PRs: keine. Andere Branches/Worktrees (`claude/devbox-gate-*`, `codex/*`, `research/*`) werden nicht berührt.
- Regeln: `UNIVERSAL_PROJECT_BOOTSTRAP.md`, `DEVBOX_GATE_POLICY.md`, `skills/SKILL_MANIFEST.md`; das Repository hat kein `AGENTS.md`/`CLAUDE.md`. Eigene Branch-Veröffentlichung ist durch den Auftrag erlaubt; Merge, main-Push, Tag, Release nicht.
- Ausgangsprüfung: `python3 -m unittest discover -s tests` → 38 Tests OK, Exit 0, Linux/Python 3.12.3.
- Arbeitsbranch: `claude/guided-bootstrap-v1` von main.

## Abweichungen von der vorgeschlagenen Dateistruktur

| Ergänzung | Grund |
| --- | --- |
| `VERSION` | eine einzige Versionsquelle für Standard, Paket und Zustandsbeispiel (GBOOT-05) |
| `scripts/onboarding_state.py`, `tests/test_onboarding_state.py` | tatsächliche Zustandsprüfung getrennt vom JSON-Schema-Dokument (GBOOT-02) |
| `docs/results/GUIDED_BOOTSTRAP_V1_PLAN.md` | dieser Detailplan |
| Schritt `wsl` im Katalog | Windows-Weg braucht WSL 2 vor Git/Python (Quellenmatrix E1) |

## Schnittstellen

- Zustand: `onboarding/STATE.schema.json` (Format) + `scripts/onboarding_state.py validate <datei>` (Prüfung, Exit 0/1/2).
- Schrittkatalog: Tabelle in `onboarding/ENTRY.md` §8; Test erzwingt Gleichheit mit dem Schema-Enum.
- Paketbau: `python3 scripts/build_bootstrap_bundle.py --output-dir <dir>` → `START_HIER.md`, `AI-Bootstrap-<version>.zip`, `SHA256SUMS`; Manifest `BUNDLE_MANIFEST.json` im ZIP mit Version, vollständigem Quellcommit und Dateiliste. Kein Netzwerk; deterministische Zeitstempel und Reihenfolge; verweigert Bau aus unsauberem Arbeitsbaum außer mit `--allow-dirty` (dann Manifest-Feld `source_dirty: true`).
- Gate: `platform_preflight()` und macOS-Adapter in `templates/devbox_merge_gate.py`; keine neuen Stoppcodes, keine Änderung an Merge-/Isolations-/CAS-Logik.

## Prüfungen

| Ebene | Prüfung |
| --- | --- |
| Code | `python3 -m unittest discover -s tests`; `uvx ruff check` und `ruff format --check` wie bei v2.0.1 |
| Struktur | Pakettests: Pflichtdateien, interne Links, keine privaten Daten, keine Pfadtraversierung, Prüfsummen, Wiederholungsbau byte-identisch |
| Dialog | `START_HIER.md` als Anweisung an echte KI-Laufzeiten (Claude-Code-Subagent, `codex exec`) mit geskripteten Nutzerantworten; Fälle D1–D9 aus `onboarding/ACCEPTANCE.md` |
| Real | Linux-Prüfrechner: Host-Prüfungen, Gate-Preflight und Ressourcenprobe, Probelauf gegen ein lokales Test-Remote |
| Nicht möglich hier | macOS, Windows, reiner ChatGPT-/Claude-Webchat mit Datei-Upload: als NOT_TESTED mit reproduzierbarer Anleitung |

## Owner-Entscheidungen

Bei Planung keine offene Owner-Entscheidung: Gate-Weg, Skill-Auswahl, Version und Profilaufbau sind technische Entscheidungen mit Begründung in der Quellenmatrix (E1–E7). Reale Prüfungen auf macOS/Windows und in den Webchats brauchen Geräte bzw. Konten des Owners und werden am Ende als konkrete Owner-Aktion vorgelegt.
