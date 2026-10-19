# Guided Bootstrap v1 – Deckungsnachweis

Jede Zeile des Ist-Abgleichs (`docs/superpowers/specs/2026-10-19-guided-bootstrap-gap-audit.md`) und jedes Abnahmeziel des Designentwurfs ist einem Teilauftrag, einem Umsetzungspfad und einem Nachweis zugeordnet. Der Nachweis nennt die tatsächliche Prüfart: **Struktur** (Datei-/Texttest), **Code** (Unit-Test), **Simulation** (simulierte Host-Antworten), **Dialog** (Startanweisungen mit einer echten KI-Laufzeit und geskriptetem Nutzer), **Real** (reale Ausführung auf dem genannten System). Dateiexistenz allein ist kein Nachweis.

Stand: siehe `GUIDED_BOOTSTRAP_V1_STATUS.json`; Ergebnisse im Detail: `GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md`.

## Audit-Zeilen

| ID | Anforderung (Audit) | Teilauftrag | Umsetzungspfad | Nachweis | Stand |
| --- | --- | --- | --- | --- | --- |
| A01 | Neue und bestehende Projekte abgleichen | 05 | `onboarding/ENTRY.md` §9 bindet `UNIVERSAL_PROJECT_BOOTSTRAP.md` unverändert ein | Struktur: Paket enthält Standard unverändert verlinkt; Dialog: P1 liest AGENTS.md | umgesetzt; real nur Testprojekt |
| A02 | Projektziele und Arbeitsregeln festhalten | 05 | ENTRY §9 → `templates/PROJECT_DISCOVERY.md` | Struktur: ENTRY §9 → Discovery im Paket | umgesetzt; nicht im Dialog geprüft |
| A03 | Dauerhafte Aufträge, Ergebnisse, Übergaben | 05 | Standard unverändert; Einrichtung verweist darauf | Struktur: Standard unverändert; dieser Auftrag selbst mit STATUS/ACCEPTANCE | umgesetzt |
| A04 | Bestehendes prüfen, keine unnötigen Rückfragen | 02–03 | ENTRY §1.3, §3, §7.3; Prüfung je Schritt | Real: D2/D7 (Claude, Codex) prüfen selbst, fragen nichts Feststellbares | umgesetzt, Linux real |
| A05 | Arbeitsweise ab erster Einrichtungsnachricht | 02, 05 | `START_HIER.md` mit eingebetteter Steuerung | Struktur: START_HIER-Tests; Dialog: D1 (beide Modelle) | umgesetzt |
| A06 | Frage X von Y, Optionen, Empfehlung | 02 | ENTRY §5–6 | Dialog: D1, D3, D4 (nach Korrektur), D2, D7, P1 | umgesetzt |
| A07 | Anfängerfreundlich, nur situationsbezogen | 02 | ENTRY §1 | Dialog: D5, D6, D8 | umgesetzt |
| A08 | Fragen im selben Chat, Fortsetzung | 02 | ENTRY §2, §3 | Dialog: D1, D5; F4 nach Korrektur siehe ACCEPTANCE 4a | umgesetzt |
| A09 | GitHub-Konto und Verbindungen | 03 | Schritte `github_account`, `github_cli`, `chat_github` | Real Linux: gh angemeldet/SSH erkannt (D2, D7); Konto-Neuanlage und Chat-GitHub nicht real geprüft | teilweise belegt |
| A10 | Lokaler Computer und Ausführungsumgebung | 03 | `onboarding/platforms/*.md`, Schritte `local_agent`, `git`, `python`, `wsl` | Real Linux: git/gh/python geprüft; macOS/Windows nicht real | teilweise belegt |
| A11 | ChatGPT/Codex und Claude gleichwertig | 01, 03 | `onboarding/providers/*.md`, Quellenmatrix E2 | Quellenmatrix E2; Dialog und Real auf Linux für beide Anbieter | umgesetzt; Real nur Linux |
| A12 | macOS, Windows, Linux gleichwertig | 01, 03, 04 | Plattformdateien, Gate-Plattformweg (Quellenmatrix E1) | Code + Simulation (Gate); Real nur Linux | teilweise belegt |
| A13 | Eigener Computer Standard, Dev-Box optional | 03 | ENTRY §12, `onboarding/OPTIONAL_DEVBOX.md` | Struktur: ENTRY §12, OPTIONAL_DEVBOX | umgesetzt |
| A14 | Skills installieren und Aktivität prüfen | 01, 03 | Schritt `skills`, Manifest-Zuordnung | Real: Superpowers 6.4.2 in Codex aktiv; superpowers:* in Claude-Code-Sitzung; Installation von Null nicht geprüft | teilweise belegt |
| A15 | Berechtigungen und Sandbox | 01, 03 | Quellenmatrix E6, Schritt `permissions` | Real: F5 Codex-Sandbox-Befund; Claude-Profil nicht real eingestellt | teilweise belegt, F5 offen |
| A16 | Portabler Stand und Wiederaufnahme | 02 | `STATE.schema.json`, `scripts/onboarding_state.py`, ENTRY §7 | Code: 15 Zustandstests; Real: D7 beide Anbieter | umgesetzt |
| A17 | Startdatei und vollständiges ZIP | 05 | `scripts/build_bootstrap_bundle.py` | Code: 16 Pakettests; Real: Build byte-identisch, Prüfsummen OK | umgesetzt |
| A18 | Funktionsnachweis der Einrichtung | 06 | `GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md` | ACCEPTANCE §7: 2 von 6 Wegen teilweise real, 4 NOT_TESTED | nicht erfüllt (BLOCKED auf Owner-Geräte) |

## Abnahmeziele des Designentwurfs (je Kombination)

| ID | Abnahmeziel | Teilauftrag | Prüffall | Nachweis | Stand |
| --- | --- | --- | --- | --- | --- |
| Z01 | Einstieg ohne GitHub-Zugriff | 05, 06 | D1 | Dialog D1 beide Modelle; Struktur-Test Einstieg ohne GitHub | Dialog belegt; Upload real offen |
| Z02 | Nur fehlende Schritte, vorhandene erkannt | 02, 06 | D2 | Real D2/D7 Linux | Linux belegt |
| Z03 | Frage X von Y mit Optionen und Empfehlung | 02, 06 | D1, D3, D4 | Dialog D1/D3/D4; Real D2/D7/P1 | belegt |
| Z04 | Keine hypothetischen Fehlerhinweise bei Erfolg | 02, 06 | D2 | Dialog D5/D6; Real D2/D7 | belegt |
| Z05 | Zwischenfrage, danach korrekt fortgesetzt | 02, 06 | D5 | Dialog D5 | belegt |
| Z06 | Auftretendes Problem konkret behandelt | 02, 06 | D6 | Dialog D6; Real F5 (Codex meldete Sandbox-Fehler ehrlich) | belegt |
| Z07 | Unterbrechung/Wiederaufnahme, veränderlicher Zustand neu geprüft | 02, 06 | D7 | Real D7 Claude und Codex | Linux belegt |
| Z08 | Werkzeuge, Zugriffe, Fähigkeiten tatsächlich geprüft | 03, 06 | Plattformzeilen | Real Linux (Abschnitt 3, D2/D7); macOS/Windows offen | teilweise |
| Z09 | Projekt-Probelauf mit Datei-, Prüf- und Git-Schritten | 06 | P1 | Real P1 Claude und Codex gegen lokales Test-Remote | Linux belegt; GitHub-Remote offen |
| Z10 | Abschluss nennt nur Belegtes und Blocker | 06, 07 | D9 | Dialog D9 (nach Korrektur) | belegt |
