# Guided Bootstrap v1 – Abnahme und Lieferstatus

Datum: 2026-10-19 · Prüfer: Claude Code (Opus 5.5) im Auftrag `docs/tasks/GUIDED_BOOTSTRAP_V1.md` (e29b3f2) · Basis: main `11d642bcfd8de138da81ac11d7e5fedcc9c0028d` · Branch `claude/guided-bootstrap-v1`

Paketversion 2.1.0. Die Artefakt-Quelle (Commit, aus dem die Dateien gebaut wurden) und die Prüfsummen stehen in Abschnitt 6.

## 1. Lieferstatus

| Achse | Status | Begründung |
| --- | --- | --- |
| Repository | DONE_ON_BRANCH (nach Push, Nachweis in Abschnitt 6) | auf eigenem Branch committet und gepusht; nicht in main integriert |
| Produkt | **PACKAGE_BUILT** | `START_HIER.md` und ZIP gebaut, deterministisch, Paket- und Dialogtests bestanden; zwei Linux-Wege real teilweise geprüft. **Nicht READY**: vier von sechs Wegen (macOS, Windows) sind nicht real geprüft, die reinen Webchats (ChatGPT, claude.ai) mit Datei-Upload sind nicht real geprüft, und auf dem Linux-Prüfrechner funktioniert die Codex-Sandbox (empfohlenes Profil) erst nach einer Systemänderung, deren Wirkung hier nicht belegt ist. |

Die Aussage „alle sechs Wege einsatzbereit“ wird **nicht** getroffen.

## 2. Prüfarten

- **Code/Struktur:** Unit-Tests (Gate, Zustand, Paket), Ruff.
- **Simulation:** Gate mit simulierten macOS- und Windows-Hostantworten. Kein Plattformnachweis.
- **Dialog:** `START_HIER.md` als Anweisung an eine echte KI-Laufzeit mit geskriptetem Nutzerverlauf. Für reine Chats wurde der Rahmen „kein Computerzugriff“ vorgegeben (Claude-Modell als Claude-Code-Subagent, GPT-Modell über `codex exec`). Das prüft die Anweisungen, nicht die Webchat-Oberfläche und nicht den Datei-Upload.
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
| **F5** | **D1/D2/D7 Codex Runde 1** | **Codex-Sandbox (`read-only`, `workspace-write`) scheitert auf Ubuntu 24.04: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; `codex sandbox -- true` Exit 1; `kernel.apparmor_restrict_unprivileged_userns = 1`, kein `bubblewrap` installiert** | chatgpt-codex.md: `bubblewrap` als Teil von `permissions` auf Linux/WSL2, Prüfung `codex sandbox -- true`, AppArmor-Profil `bwrap-userns-restrict` laut OpenAI (Quelle C15); keine systemweite Abschaltung | **nicht belegt**: Abhilfe braucht `sudo` auf dem Owner-Rechner. Weitere Codex-Läufe deshalb mit der vorhandenen Nutzerkonfiguration `danger-full-access` in Testordnern |
| F4 | D2 Codex | Begrüßungshinweis fehlte im lokalen Agenten | ENTRY §2 „erste Antwort immer“ | siehe Abschnitt 4a |

### 4a. Wiederholung nach F4

Codex D2 erneut, **real**, Paket aus `497e399` (ENTRY-§2-Korrektur): erste Antwort beginnt mit „Ich begleite dich Schritt für Schritt … Du kannst jederzeit hier im Chat Fragen stellen … machen danach an derselben Stelle weiter.“, bestätigt lokalen Codex-Agenten und Ubuntu 24.04.4 per Befehl, kein Stand gefunden, „Frage 1 von 1“ zur Speicherung mit Empfehlung. **PASS.** F1–F3 wurden nicht erneut real durchlaufen; ihre Korrekturen sind Textpräzisierungen ohne Auswirkung auf die übrigen Fälle.

## 6. Artefakte und Downloadweg

- Quellstand (Artefakt-Quelle): `a13e0737f09b962edb5e643bc43df4fa2aac933d`. Gebaut mit `python3 scripts/build_bootstrap_bundle.py --output-dir dist --source-ref a13e0737f09b962edb5e643bc43df4fa2aac933d`; ein zweiter Bau in einen anderen Ordner war byte-identisch (`cmp`), `sha256sum -c SHA256SUMS` OK, Manifest nennt denselben Commit und 31 Dateien, die `START_HIER.md` im ZIP ist identisch mit der einzelnen Datei.
- `START_HIER.md` – SHA-256 `6eab59b4a35d48355180518ebf0d12e1399ca43ee4da70c46a73e67a05015853`, 54 028 Byte.
- `AI-Bootstrap-2.1.0.zip` – SHA-256 `da3816a93dfb554e1e4b0bcc977401f1efa441eddb045119ce682b1785c14e6b`, 383 326 Byte.
- Downloadweg (Task-Branch, öffentliches Repository, kein Release): `https://github.com/robin-shiels/ai-project-bootstrap/raw/claude/guided-bootstrap-v1/dist/START_HIER.md` und `…/dist/AI-Bootstrap-2.1.0.zip`, Prüfsummen in `…/dist/SHA256SUMS`. Die Dateien liegen im Commit nach der Artefakt-Quelle; dieser ändert nur `dist/` und `docs/results/`, nicht den Paketinhalt (`git diff --stat a13e073..HEAD`).
- Eine öffentliche Release-Veröffentlichung ist nicht Teil dieses Auftrags.

## 7. Readiness-Matrix

| Weg | OS/Tools | Ausgangszustand | Konto/Verbindung | Skills | Berechtigungen | Gate | Probelauf | Ergebnis | Nachweis | Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGPT/Codex × macOS | – | – | – | – | – | Simulation | – | **NOT_TESTED** | – | kein Mac im Zugriff; Owner-Test nach `onboarding/ACCEPTANCE.md` |
| ChatGPT/Codex × Windows | – | – | – | – | – | Simulation (nativer Stopp); WSL-Weg = Linux-Code, in WSL nicht gelaufen | – | **NOT_TESTED** | – | kein Windows-Rechner im Zugriff |
| ChatGPT/Codex × Linux | Ubuntu 24.04.4; codex-cli 0.163.0; git 2.43.0; gh 2.102.0; Python 3.12.3 | vorbereiteter Entwicklungsrechner, kein sauberer Zustand | Codex angemeldet (ChatGPT), gh angemeldet, SSH zu GitHub ok | Superpowers 6.4.2 `installed, enabled` | **Sandbox defekt (F5)**, Tests mit vorhandenem Vollzugriff | Hostprobe + Preflight real ok; Gate-Tests real | P1 PASS (lokales Test-Remote) | **TEILWEISE** | Abschnitte 3–5 | F5 unbelegt behoben; ChatGPT-Webchat mit Upload nicht real geprüft; GitHub-Push im Probelauf nicht über diesen Weg |
| Claude/Claude Code × macOS | – | – | – | – | – | Simulation | – | **NOT_TESTED** | – | kein Mac im Zugriff |
| Claude/Claude Code × Windows | – | – | – | – | – | Simulation | – | **NOT_TESTED** | – | kein Windows-Rechner im Zugriff |
| Claude/Claude Code × Linux | Ubuntu 24.04.4; Claude Code 2.1.299 (Desktop-App, Linux-Beta); git 2.43.0; gh 2.102.0; Python 3.12.3 | vorbereiteter Entwicklungsrechner | gh angemeldet, SSH ok; Push dieses Task-Branches zu GitHub aus dieser Laufzeit (Abschnitt 6) | `superpowers:*` in der Sitzung gelistet | `/sandbox` und Profil-Einstellung nicht geprüft (keine Änderung an `~/.claude`) | wie oben | P1 PASS (lokales Test-Remote) | **TEILWEISE** | Abschnitte 3–5 | claude.ai-Webchat mit Upload nicht real geprüft; CLI-Installation nicht geprüft (Desktop-Sitzung); Sandbox-Profil nicht geprüft |

## 8. Reproduzierbare offene Schritte (Owner)

Für jede Zeile mit NOT_TESTED/TEILWEISE, auf dem jeweiligen Rechner und mit dem eigenen Konto:

1. `START_HIER.md` und `AI-Bootstrap-2.1.0.zip` herunterladen (Abschnitt 6), `SHA256SUMS` prüfen (`sha256sum -c SHA256SUMS`, macOS `shasum -a 256 -c SHA256SUMS`, Windows PowerShell `Get-FileHash`).
2. Neuer Chat beim Anbieter, `START_HIER.md` hochladen oder einfügen, „Start“ (D1). Upload und Einfügen getrennt notieren.
3. Der Einrichtung bis `permissions` folgen; jeden Schritt mit Werkzeugprüfung bestätigen lassen (Z08).
4. Gate-Weg: im entpackten Paket `python3 -m unittest discover -s tests` und `python3 scripts/probe_gate_host.py` (Windows: in WSL; zusätzlich nativ `py scripts\probe_gate_host.py`, erwartet Exit 10 mit Hinweis auf WSL 2).
5. Probelauf P1 gegen ein eigenes, freigegebenes Test-Repository auf GitHub.
6. Ergebnisse (OS-/Werkzeugversionen, Paket-SHA, Datum, Nachweise) in Abschnitt 7 eintragen.

Linux-Prüfrechner zusätzlich: die F5-Abhilfe (`sudo apt install bubblewrap`, ggf. AppArmor-Profil) ausführen und `codex sandbox -- true` erneut prüfen.
