# Guided Bootstrap v1 – Deckungsnachweis

Jede Zeile des Ist-Abgleichs (`docs/superpowers/specs/2026-10-19-guided-bootstrap-gap-audit.md`) und jedes Abnahmeziel des Designentwurfs ist einem Teilauftrag, einem Umsetzungspfad und einem Nachweis zugeordnet. Der Nachweis nennt die tatsächliche Prüfart: **Struktur** (Datei-/Texttest), **Code** (Unit-Test), **Simulation** (simulierte Host-Antworten), **Dialog** (Startanweisungen mit einer echten KI-Laufzeit und geskriptetem Nutzer), **Real** (reale Ausführung auf dem genannten System). Dateiexistenz allein ist kein Nachweis.

Stand: siehe `GUIDED_BOOTSTRAP_V1_STATUS.json`; Ergebnisse im Detail: `GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md`.

## Audit-Zeilen

| ID | Anforderung (Audit) | Teilauftrag | Umsetzungspfad | Nachweis | Stand |
| --- | --- | --- | --- | --- | --- |
| A01 | Neue und bestehende Projekte abgleichen | 05 | `onboarding/ENTRY.md` §9 bindet `UNIVERSAL_PROJECT_BOOTSTRAP.md` unverändert ein | geplant | offen |
| A02 | Projektziele und Arbeitsregeln festhalten | 05 | ENTRY §9 → `templates/PROJECT_DISCOVERY.md` | geplant | offen |
| A03 | Dauerhafte Aufträge, Ergebnisse, Übergaben | 05 | Standard unverändert; Einrichtung verweist darauf | geplant | offen |
| A04 | Bestehendes prüfen, keine unnötigen Rückfragen | 02–03 | ENTRY §1.3, §3, §7.3; Prüfung je Schritt | geplant | offen |
| A05 | Arbeitsweise ab erster Einrichtungsnachricht | 02, 05 | `START_HIER.md` mit eingebetteter Steuerung | geplant | offen |
| A06 | Frage X von Y, Optionen, Empfehlung | 02 | ENTRY §5–6 | geplant | offen |
| A07 | Anfängerfreundlich, nur situationsbezogen | 02 | ENTRY §1 | geplant | offen |
| A08 | Fragen im selben Chat, Fortsetzung | 02 | ENTRY §2, §3 | geplant | offen |
| A09 | GitHub-Konto und Verbindungen | 03 | Schritte `github_account`, `github_cli`, `chat_github` | geplant | offen |
| A10 | Lokaler Computer und Ausführungsumgebung | 03 | `onboarding/platforms/*.md`, Schritte `local_agent`, `git`, `python`, `wsl` | geplant | offen |
| A11 | ChatGPT/Codex und Claude gleichwertig | 01, 03 | `onboarding/providers/*.md`, Quellenmatrix E2 | geplant | offen |
| A12 | macOS, Windows, Linux gleichwertig | 01, 03, 04 | Plattformdateien, Gate-Plattformweg (Quellenmatrix E1) | geplant | offen |
| A13 | Eigener Computer Standard, Dev-Box optional | 03 | ENTRY §12, `onboarding/OPTIONAL_DEVBOX.md` | geplant | offen |
| A14 | Skills installieren und Aktivität prüfen | 01, 03 | Schritt `skills`, Manifest-Zuordnung | geplant | offen |
| A15 | Berechtigungen und Sandbox | 01, 03 | Quellenmatrix E6, Schritt `permissions` | geplant | offen |
| A16 | Portabler Stand und Wiederaufnahme | 02 | `STATE.schema.json`, `scripts/onboarding_state.py`, ENTRY §7 | geplant | offen |
| A17 | Startdatei und vollständiges ZIP | 05 | `scripts/build_bootstrap_bundle.py` | geplant | offen |
| A18 | Funktionsnachweis der Einrichtung | 06 | `GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md` | geplant | offen |

## Abnahmeziele des Designentwurfs (je Kombination)

| ID | Abnahmeziel | Teilauftrag | Prüffall | Nachweis | Stand |
| --- | --- | --- | --- | --- | --- |
| Z01 | Einstieg ohne GitHub-Zugriff | 05, 06 | D1 | geplant | offen |
| Z02 | Nur fehlende Schritte, vorhandene erkannt | 02, 06 | D2 | geplant | offen |
| Z03 | Frage X von Y mit Optionen und Empfehlung | 02, 06 | D1, D3, D4 | geplant | offen |
| Z04 | Keine hypothetischen Fehlerhinweise bei Erfolg | 02, 06 | D2 | geplant | offen |
| Z05 | Zwischenfrage, danach korrekt fortgesetzt | 02, 06 | D5 | geplant | offen |
| Z06 | Auftretendes Problem konkret behandelt | 02, 06 | D6 | geplant | offen |
| Z07 | Unterbrechung/Wiederaufnahme, veränderlicher Zustand neu geprüft | 02, 06 | D7 | geplant | offen |
| Z08 | Werkzeuge, Zugriffe, Fähigkeiten tatsächlich geprüft | 03, 06 | Plattformzeilen | geplant | offen |
| Z09 | Projekt-Probelauf mit Datei-, Prüf- und Git-Schritten | 06 | P1 | geplant | offen |
| Z10 | Abschluss nennt nur Belegtes und Blocker | 06, 07 | D9 | geplant | offen |
