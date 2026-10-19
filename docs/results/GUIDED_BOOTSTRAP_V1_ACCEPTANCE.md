# Guided Bootstrap v1 – Abnahme und Lieferstatus

Datum: 2026-10-19 · Prüfer: Claude Code (Opus 5.5) im Auftrag `docs/tasks/GUIDED_BOOTSTRAP_V1.md` (e29b3f2) · Basis: main `11d642bcfd8de138da81ac11d7e5fedcc9c0028d` · Branch `claude/guided-bootstrap-v1`

Paketversion 2.1.0. Die Artefakt-Quelle (Commit, aus dem die Dateien gebaut wurden) und die Prüfsummen stehen in Abschnitt 6.

## 1. Lieferstatus

| Achse | Status | Begründung |
| --- | --- | --- |
| Repository | DONE_ON_BRANCH (nach Push, Nachweis in Abschnitt 6) | auf eigenem Branch committet und gepusht; nicht in main integriert |
| Produkt | **PACKAGE_BUILT** | `START_HIER.md` und ZIP gebaut, deterministisch, Paket- und Dialogtests bestanden. Beide Linux-Wege wurden zusätzlich vom Nullzustand in einer frischen Ubuntu-24.04-VM durchlaufen; der Codex-Sandbox-Befund F5 und seine Abhilfe sind dort real belegt. **Nicht READY**: die vier macOS-/Windows-Wege sind nicht real geprüft (keine Geräte, in einer VM auf der Dev-Box nicht machbar, Abschnitt 4b), die Webchats (ChatGPT, claude.ai) mit Datei-Upload sind nicht real geprüft, und die Konto-Anmeldungen (Claude, ChatGPT/Codex, GitHub) sowie die Plugin-Installation im Nullzustand sind persönliche Aktionen, die nicht ausgeführt wurden. |

Die Aussage „alle sechs Wege einsatzbereit“ wird **nicht** getroffen.

## 2. Prüfarten

- **Code/Struktur:** Unit-Tests (Gate, Zustand, Paket), Ruff.
- **Simulation:** Gate mit simulierten macOS- und Windows-Hostantworten. Kein Plattformnachweis.
- **Dialog:** `START_HIER.md` als Anweisung an eine echte KI-Laufzeit mit geskriptetem Nutzerverlauf. Für reine Chats wurde der Rahmen „kein Computerzugriff“ vorgegeben (Claude-Modell als Claude-Code-Subagent, GPT-Modell über `codex exec`). Das prüft die Anweisungen, nicht die Webchat-Oberfläche und nicht den Datei-Upload.
- **VM-Nullzustand:** frische Ubuntu-24.04.5-VM (offizielles Cloud-Image, Prüfsumme verifiziert) unter QEMU/KVM auf der Dev-Box, 2 vCPU, 2 GB RAM. Die KI läuft als lokaler Agent auf dem Steuerrechner (Claude-Modell als Subagent bzw. `codex exec`) und führt jeden Befehl per SSH in der VM aus; Nutzerantworten kommen aus einem festen Skript. Anmeldungen bei Anbieter-Konten wurden nicht durchgeführt (persönliche Aktion); die laufende Agenten-Sitzung gilt per Testvorgabe als angemeldeter lokaler Agent.
- **Real:** tatsächliche Ausführung auf dem Linux-Prüfrechner (Ubuntu 24.04.4 LTS, Kernel 6.8, x86_64) durch Claude Code 2.1.299 (Desktop-App-Sitzung) bzw. codex-cli 0.163.0. Ausgangszustand: **kein sauberer Rechner**, sondern ein vorhandener Entwicklungsrechner mit Git 2.43.0, gh 2.102.0 (angemeldet, SSH), Python 3.12.3, Codex angemeldet und Superpowers 6.4.2 aktiv; ohne globale Git-Identität und ohne `bubblewrap`. Testgrenzen: keine globalen Änderungen, keine Installation, Stand nur im Testordner.

## 3. Code-, Struktur- und Paketprüfungen

| Prüfung | Befehl | Ergebnis |
| --- | --- | --- |
| Ausgangslage Gate | `python3 -m unittest discover -s tests` auf main 11d642b | 38 Tests OK, Exit 0 |
| Gesamte Suite | `python3 -m unittest discover -s tests` | 81 Tests OK, Exit 0 (38 Gate-Bestand + 10 Gate-Portabilität + 15 Zustand + 18 Paket/Host-Probe) |
| Lint/Format | `uvx ruff@latest check templates tests scripts`, `uvx ruff@latest format --check …` (Ruff 0.17.1) | All checks passed; formatiert |
| Wiederholungsbau | zweimal `python3 scripts/build_bootstrap_bundle.py --output-dir …` vom selben Commit, `cmp` | byte-identisch |
| Prüfsummen | `sha256sum -c SHA256SUMS` | OK für beide Dateien |
| ZIP aus Paket nutzbar | Test: ZIP entpacken, `python3 -I scripts/onboarding_state.py validate onboarding/STATE.example.json` | Exit 0 |
| Gate-Hostprobe real Linux | `python3 scripts/probe_gate_host.py` | platform linux, preflight ok, MemAvailable 3999 MiB, SwapFree 2273 MiB, Exit 0 |
| Gate real Linux, Beispielkonfiguration | `python3 templates/devbox_merge_gate.py --config templates/devbox_merge_gate.example.toml validate-config` | config valid, Exit 0 |
| Gate macOS | Unit-Tests mit simuliertem `vm_stat`/`sysctl`/`ps` | bestanden – **Simulation** |
| Gate natives Windows | Unit-Test: `main()` mit `sys.platform = "win32"` | `STOP PRECONDITION … WSL 2`, Exit 10, kein Zustandsordner angelegt – **Simulation** |
| Reales GitHub-Gate | – | nicht ausgeführt (kein Projekt mit integriertem Gate im Auftrag; kein Merge erlaubt) |

## 4. Dialogfälle (onboarding/ACCEPTANCE.md)

| Fall | Laufzeit | Paket | Ergebnis | Kernbeleg |
| --- | --- | --- | --- | --- |
| D1 nackter Start | Claude-Modell, Rahmen claude.ai | 3d0fb4c | PASS | Begleitungs-Hinweis, „kann auf deinem Computer nichts ausführen“, „Frage 1 von 2“ mit Optionen und Empfehlung |
| D1 nackter Start | GPT-Modell via `codex exec`, Rahmen ChatGPT-Webchat | 4473012 | PASS | dieselben Merkmale |
| D2 bereits eingerichtet | Claude Code, **real** | 3d0fb4c | PASS (Befunde F1, F2 behoben) | 13 Befehle real; Weg ohne Frage aus Sitzung + Befehl belegt; stoppt an Zustimmung zum Speicherort |
| D2 bereits eingerichtet | Codex, **real** | 4473012 → 497e399 | TEILWEISE → PASS (Befund F4, Wiederholung 4a) | Weg aus Sitzung belegt, keine Frage zu Feststellbarem; Begrüßungshinweis fehlte |
| D3 eigene Antwort | Claude-Modell, Rahmen chatgpt.com | 3d0fb4c → b97466b | FAIL → PASS | Runde 1 nannte ChromeOS-Linux „reicht“; nach Regel „nicht geprüft“ korrekt |
| D4 neue Unterfrage | Claude-Modell, Rahmen claude.ai | 3d0fb4c → b97466b | FAIL → PASS | Runde 2: „Durch deine Antwort kommt eine Frage dazu: Frage 2 von 3“, kein Kauf |
| D5 Zwischenfrage | Claude-Modell, Rahmen chatgpt.com | 3d0fb4c | PASS | Terminal kurz erklärt, „Zurück zur GitHub CLI“ |
| D6 tatsächlicher Fehler | Claude-Modell | 3d0fb4c | PASS | `command not found: gh` → konkrete Ursache, ein Lösungsweg (Homebrew prüfen) |
| D7 Wiederaufnahme | Claude Code, **real** | 3d0fb4c | PASS (Befund F3 behoben) | Stand validiert, Entscheidungen übernommen, Nachweise vom „anderen Laptop“ ersetzt, git_identity real offen |
| D7 Wiederaufnahme | Codex, **real** | 4473012 | PASS | neu geprüft, neue Nachweise mit eigenem Kontext gespeichert und erneut validiert |
| D8 kein Hostzugriff | Claude-Modell, Rahmen Mobil-App | 3d0fb4c | PASS | „Das kann ich von hier aus leider nicht prüfen“ |
| D9 Abschluss mit Lücke | Claude-Modell, lokaler Agent ohne Werkzeuge | 3d0fb4c → b97466b | TEILWEISE → PASS | Runde 2: „Noch nicht fertig“, Blocker im Stand gesichert, ein nächster Schritt |
| P1 Probelauf | Claude Code, **real**, lokales Test-Remote | 4473012 | PASS | Commit `807414e434471070a214a73774a181d642d81bd0` = Remote-SHA; main unverändert; Branch-Frage gestellt |
| P1 Probelauf | Codex, **real**, lokales Test-Remote | 4473012 | PASS | Commit `7e5453c921921922fcbee1b0465124b59de55bc4` = Remote-SHA; main unverändert; Branch-Frage gestellt |

Rein strukturelle Texttests (Schrittkatalog = Schema, eingebettete Dateien vollständig, Einstieg ohne GitHub) sind zusätzlich in `tests/` und gelten nicht als Dialognachweis.

## 4b. VM-Nullzustand (Ubuntu 24.04.5, frisch)

Ausgangszustand jeder VM: Git 2.43.0 und Python 3.12.3 vorhanden; `gh`, `unzip`, `bubblewrap`, `socat`, `claude`, `codex` fehlen; `kernel.apparmor_restrict_unprivileged_userns = 1`. Paket in der VM über den öffentlichen Branch-Link geladen bzw. kopiert, `sha256sum -c` OK.

| Prüfung | Ergebnis |
| --- | --- |
| Claude Code installieren: `curl -fsSL https://claude.ai/install.sh \| bash` | Exit 0, `2.1.303 (Claude Code)`, im PATH einer Login-Shell; `claude doctor`: „No installation issues found“, „Not signed in“ |
| Codex installieren: `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | Exit 0, `codex-cli 0.163.0`; `codex login status`: „Not logged in“, Exit 1 |
| F5 im Nullzustand | `codex sandbox -- true` → `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, Exit 1 |
| F5 Abhilfe 1: `sudo apt install bubblewrap` | weiterhin Exit 1 |
| F5 Abhilfe 2: AppArmor-Profil `bwrap-userns-restrict` | `codex sandbox -- true` Exit 0; read-only: Schreiben in `/tmp` und `$HOME` gesperrt, Netzwerk gesperrt; `workspace-write`: Schreiben im Projekt ok, außerhalb gesperrt; systemweite Sperre bleibt `1` |
| Claude-Sandbox-Grundlage | `bwrap --ro-bind / / --unshare-user --unshare-net true`: vor dem Profil Exit 1, danach Exit 0 (Claude Codes eigenes `/sandbox` ohne Anmeldung nicht aufrufbar) |
| Plugin-Befehle | `claude plugin install <plugin>@<marktplatz>` und `codex plugin add <plugin>@<marktplatz>` existieren (Hilfe gelesen); `codex plugin list` ohne Anmeldung: „No marketplace plugins found.“ |
| Gate aus entpacktem ZIP (kein Git-Repository) | zuerst 63 Tests, 1 Fehler (Befund F6); nach Korrektur 63 Tests OK; `probe_gate_host.py` Exit 0; Validator Exit 0 |
| **Lauf A** Claude-Weg (Claude-Modell, Paket 9494504) | bis Abschluss „teilweise eingerichtet“: Stand nach Zustimmung gesichert, Paket per `python3 -m zipfile` entpackt, `gh` aus offizieller Quelle installiert, Git-Identität gesetzt, Profil Standard geschrieben, `bubblewrap`/`socat` installiert, Projektregeln (`AGENTS.md` + `CLAUDE.md` mit `@AGENTS.md`) auf `setup/projektstandard-20261019`, Probelauf `c4632ec` = Remote, main unverändert; Blocker: GitHub-Anmeldung, Skills, Sandbox (AppArmor). 11 Anleitungslücken (V1–V11), behoben in 08d44e7 |
| **Lauf B** Codex-Weg (`codex exec`, Paket 08d44e7) | bis Abschluss „teilweise eingerichtet“, 114 VM-Aufrufe: Codex CLI installiert, Anmeldung als Blocker, „die unabhängigen Schritte gehen weiter“, `gh` installiert, Git-Identität, Profil Standard, **F5 vom Agenten selbst nach Anleitung behoben** (`codex sandbox -- true` Exit 0), Standard-B-Hinweis und zwei Projektfragen, Regeln auf eigenem Branch, Probelauf-Branch ohne main-Verfolgung, Commit `822e53e96787fa89d8f44d07d0cca054d555c90f` = Remote; Endstand gültig. Eine Lücke (leere Plugin-Liste ohne Anmeldung), behoben in d91d87f |
| **Lauf A2** Claude-Weg, Bestätigung (Paket d91d87f) | bis Abschluss „teilweise eingerichtet“ mit einem Blocker (GitHub-Anmeldung): Korrekturen aus Lauf A wirksam – Agent installiert `bubblewrap`/`socat`, erkennt die AppArmor-Sperre und wendet die Abhilfe selbst an (bwrap-Probe Exit 1 → 0, Sperre bleibt `1`), arbeitet nach dem Blocker weiter, legt Branches mit `--no-track` an; Regeln `72ca075` und Probelauf `a502766` jeweils = Remote, main unverändert; Endstand gültig. Skill-„Nachweis“ testbedingt **nicht gewertet** (Skill-Liste stammte aus der Steuerumgebung). Restlücken (Nachweisart `/status`, Einzelfragen-Zählung, `current_step` bei Teil-Einrichtung, unbekannte Version, Regel-Branch nach main, Einstellungen ab neuer Sitzung) behoben in 678c15a; danach 63 gebündelte Tests im entpackten Endpaket in der VM OK |

**Windows und macOS in einer VM:** nicht durchgeführt. macOS darf laut Apple-Lizenz nur auf Apple-Hardware virtualisiert werden. Eine Windows-11-VM braucht mindestens 4 GB RAM, die Dev-Box (selbst eine KVM-VM mit 7,9 GB) hatte rund 4 GB frei, und WSL 2 in dieser VM wäre eine dritte Virtualisierungsebene. Diese vier Wege bleiben NOT_TESTED.

## 5. Befunde und Behebung

| ID | Quelle | Befund | Behebung | Erneut geprüft |
| --- | --- | --- | --- | --- |
| R1 | Commit dieses Auftrags | globale Git-Identität auf dem Prüfrechner fehlt | nicht geändert (Owner-Umgebung); Commits mit der im Repository üblichen Identität pro Befehl | – (realer Fall für Schritt `git_identity`, von D7 korrekt erkannt) |
| F-D3 | D3 | ungeprüfter Weg als funktionierend dargestellt | ENTRY §5 „nicht geprüft“ | D3 PASS |
| F-D4 | D4 | entstandene Entscheidung nur als Prosa | ENTRY §6 angekündigte Zusatzfrage | D4 PASS |
| F-D9 | D9 | Stand mit Blocker nicht gesichert; Kriterium zu breit | ENTRY §11, Kriterium präzisiert | D9 PASS |
| F1 | D2 Claude | Widerspruch §8/§7.1 zu `save_state` | ENTRY §8 | nach Korrektur nicht erneut real gelaufen |
| F2 | D2 Claude | Desktop-App-Sitzung ohne CLI hatte keinen Nachweis | claude-code.md | nicht erneut gelaufen |
| F3 | D7 Claude | `gh auth setup-git` pauschal verlangt trotz funktionierendem SSH | linux.md, macos.md | nicht erneut gelaufen |
| F6 | VM: Gate-Tests im entpackten ZIP | `main()` löste das Repository vor der Plattformprüfung auf; natives Windows außerhalb eines Repositories hätte mit Traceback statt `STOP PRECONDITION` geendet; Test hing vom Arbeitsordner ab | Preflight vor Repository-Auflösung; Test mit Nicht-Repo-`--repo-dir` (9494504) | 63 gebündelte Tests OK in der VM |
| V1–V11 | VM-Lauf A | u. a.: Agent kann eigene Slash-Befehle nicht ausführen; Claude-Sandbox unter Ubuntu 24.04 ohne konkrete Abhilfe; `git switch -c X origin/main` verfolgt main; Weiterarbeit nach Blocker ungeregelt; neu/bestehend nicht abgegrenzt; `unzip` fehlt; Entpacken bei laufendem Agenten | ENTRY §3, §4, §8, §9, §10; claude-code.md; chatgpt-codex.md; linux.md; windows.md (08d44e7) | VM-Lauf B bestätigt Weiterarbeit und Branch ohne Verfolgung; Lauf A2 |
| VB1 | VM-Lauf B | leere Codex-Plugin-Liste ohne Anmeldung ohne Hinweis | chatgpt-codex.md (d91d87f) | – |
| **F5** | **D1/D2/D7 Codex Runde 1** | **Codex-Sandbox (`read-only`, `workspace-write`) scheitert auf Ubuntu 24.04: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; `codex sandbox -- true` Exit 1; `kernel.apparmor_restrict_unprivileged_userns = 1`, kein `bubblewrap` installiert** | chatgpt-codex.md: `bubblewrap` als Teil von `permissions` auf Linux/WSL2, Prüfung `codex sandbox -- true`, AppArmor-Profil `bwrap-userns-restrict` laut OpenAI (Quelle C15); keine systemweite Abschaltung | **in frischer VM real belegt** (Abschnitt 4b; Lauf B wendet die Abhilfe selbst an). Auf dem Owner-Rechner nicht angewendet; Codex-Läufe dort deshalb mit der vorhandenen Nutzerkonfiguration `danger-full-access` in Testordnern |
| F4 | D2 Codex | Begrüßungshinweis fehlte im lokalen Agenten | ENTRY §2 „erste Antwort immer“ | siehe Abschnitt 4a |

### 4a. Wiederholung nach F4

Codex D2 erneut, **real**, Paket aus `497e399` (ENTRY-§2-Korrektur): erste Antwort beginnt mit „Ich begleite dich Schritt für Schritt … Du kannst jederzeit hier im Chat Fragen stellen … machen danach an derselben Stelle weiter.“, bestätigt lokalen Codex-Agenten und Ubuntu 24.04.4 per Befehl, kein Stand gefunden, „Frage 1 von 1“ zur Speicherung mit Empfehlung. **PASS.** F1–F3 wurden nicht erneut real durchlaufen; ihre Korrekturen sind Textpräzisierungen ohne Auswirkung auf die übrigen Fälle.

## 6. Artefakte und Downloadweg

- Quellstand (Artefakt-Quelle): `678c15addaacaa4e5b45149eb8ccdb842f065ca8`. Gebaut mit `python3 scripts/build_bootstrap_bundle.py --output-dir dist --source-ref 678c15addaacaa4e5b45149eb8ccdb842f065ca8`; ein zweiter Bau in einen anderen Ordner war byte-identisch (`cmp`), `sha256sum -c SHA256SUMS` OK, Manifest nennt denselben Commit und 31 Dateien, die `START_HIER.md` im ZIP ist identisch mit der einzelnen Datei.
- `START_HIER.md` – SHA-256 `c0875a8e07a4f8f600f13326ccb04c7ab35427593bb5a64595b3643ded7721f9`, 58 552 Byte.
- `AI-Bootstrap-2.1.0.zip` – SHA-256 `e7d028cffdc7a94abbedc375bc65baa1f87ccef8ef3df452192f848796dbbb96`, 392 769 Byte.
- Downloadweg (Task-Branch, öffentliches Repository, kein Release): `https://github.com/robin-shiels/ai-project-bootstrap/raw/claude/guided-bootstrap-v1/dist/START_HIER.md` und `…/dist/AI-Bootstrap-2.1.0.zip`, Prüfsummen in `…/dist/SHA256SUMS`. Die Dateien liegen im Commit nach der Artefakt-Quelle; dieser ändert nur `dist/` und `docs/`, nicht den Paketinhalt (`git diff --stat 678c15a..HEAD`). Zusätzlich wurde das Endpaket in der frischen VM entpackt: 63 gebündelte Tests OK, Hostprobe Exit 0.
- Eine öffentliche Release-Veröffentlichung ist nicht Teil dieses Auftrags.

## 7. Readiness-Matrix

| Weg | OS/Tools | Ausgangszustand | Konto/Verbindung | Skills | Berechtigungen | Gate | Probelauf | Ergebnis | Nachweis | Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT/Codex × macOS | – | – | – | – | – | Simulation | – | **NOT_TESTED** | – | kein Mac; VM lizenzrechtlich nicht zulässig |
| ChatGPT/Codex × Windows | – | – | – | – | – | Simulation (nativer Stopp); WSL-Weg = Linux-Code, in WSL nicht gelaufen | – | **NOT_TESTED** | – | kein Windows-Rechner; Windows-VM mit WSL 2 auf der Dev-Box nicht machbar (RAM, dritte Virtualisierungsebene) |
| ChatGPT/Codex × Linux | (a) Prüfrechner Ubuntu 24.04.4, codex-cli 0.163.0; (b) frische VM Ubuntu 24.04.5, codex-cli 0.163.0, gh 2.102.0, bubblewrap 0.9.0 | (a) eingerichteter Rechner; (b) **Nullzustand** | (a) Codex und gh angemeldet; (b) Anmeldungen nicht durchgeführt (persönliche Aktion) | (a) Superpowers 6.4.2 aktiv; (b) ohne Anmeldung nicht installierbar | (a) Sandbox defekt (F5, nicht geändert); (b) Standardprofil, Sandbox nach Abhilfe Exit 0 | (a) Hostprobe real; (b) 63 gebündelte Tests + Hostprobe real | (a) P1 PASS; (b) Lauf B PASS (lokales Test-Remote) | **TEILWEISE** | Abschnitte 3–5, 4b | Konto-Anmeldungen und Plugin-Installation im Nullzustand nicht durchgeführt; ChatGPT-Webchat mit Upload nicht real geprüft; Push zu GitHub im Probelauf nicht geprüft |
| Claude/Claude Code × macOS | – | – | – | – | – | Simulation | – | **NOT_TESTED** | – | kein Mac; VM lizenzrechtlich nicht zulässig |
| Claude/Claude Code × Windows | – | – | – | – | – | Simulation | – | **NOT_TESTED** | – | kein Windows-Rechner; Windows-VM mit WSL 2 auf der Dev-Box nicht machbar |
| Claude/Claude Code × Linux | (a) Prüfrechner Ubuntu 24.04.4, Claude Code 2.1.299 (Desktop-App); (b) frische VM Ubuntu 24.04.5, Claude Code 2.1.303 (installiert), gh 2.102.0 | (a) eingerichteter Rechner; (b) **Nullzustand** | (a) gh angemeldet, Push dieses Task-Branches zu GitHub aus dieser Laufzeit; (b) Anmeldungen nicht durchgeführt | (a) `superpowers:*` in der Sitzung; (b) nicht prüfbar ohne Anmeldung | (b) Standardprofil geschrieben, `bwrap`-Grundlage nach AppArmor-Abhilfe Exit 0; `/sandbox` selbst nicht aufgerufen | wie oben | (a) P1 PASS; (b) Lauf A/A2 (lokales Test-Remote) | **TEILWEISE** | Abschnitte 3–5, 4b | Konto-Anmeldungen, Plugin-Installation und `/sandbox` im Nullzustand nicht durchgeführt; claude.ai-Webchat mit Upload nicht real geprüft |

## 8. Reproduzierbare offene Schritte

Der Owner hat am 2026-10-19 entschieden, selbst keine Tests durchzuführen. Die folgenden Schritte bleiben als Anleitung für jede spätere reale Abnahme, auf dem jeweiligen Rechner und mit dem eigenen Konto:

1. `START_HIER.md` und `AI-Bootstrap-2.1.0.zip` herunterladen (Abschnitt 6), `SHA256SUMS` prüfen (`sha256sum -c SHA256SUMS`, macOS `shasum -a 256 -c SHA256SUMS`, Windows PowerShell `Get-FileHash`).
2. Neuer Chat beim Anbieter, `START_HIER.md` hochladen oder einfügen, „Start“ (D1). Upload und Einfügen getrennt notieren.
3. Der Einrichtung bis `permissions` folgen; jeden Schritt mit Werkzeugprüfung bestätigen lassen (Z08).
4. Gate-Weg: im entpackten Paket `python3 -m unittest discover -s tests` und `python3 scripts/probe_gate_host.py` (Windows: in WSL; zusätzlich nativ `py scripts\probe_gate_host.py`, erwartet Exit 10 mit Hinweis auf WSL 2).
5. Probelauf P1 gegen ein eigenes, freigegebenes Test-Repository auf GitHub.
6. Ergebnisse (OS-/Werkzeugversionen, Paket-SHA, Datum, Nachweise) in Abschnitt 7 eintragen.

Die F5-Abhilfe ist in einer frischen VM belegt; auf dem eingerichteten Prüfrechner wurde sie bewusst nicht angewendet.
