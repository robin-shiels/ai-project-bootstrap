# Guided Bootstrap v2 – Abnahme

Stand: 2026-10-21 · Auftrag [GUIDED_BOOTSTRAP_V2](../tasks/GUIDED_BOOTSTRAP_V2.md) · Branch `claude/guided-bootstrap-v2` · Standard und Paket **3.0.0**

## 1. Lieferstatus

| Achse | Stand | Bedeutung |
| --- | --- | --- |
| Repository | **DONE_ON_BRANCH** (nach Push und PR) | eigener Branch, nicht in `main` integriert; dieser PR ändert den Befugnisvertrag und braucht ausdrückliche Owner-Integration |
| Produkt | **PACKAGE_BUILT** | Startdatei, ZIP und Plugin gebaut und geprüft; nicht READY: macOS, Windows, Webchat und der Probelauf mit echtem Merge auf GitHub sind nicht real geprüft (Abschnitt 6) |

## 2. Prüfumgebung

- Steuerrechner: Linux (Dev-Box), Python 3.12, `codex-cli 0.163.0` (Modell `gpt-6.1-sol`), `gh 2.102.0`. `claude` ist dort nicht installiert; Claude-Dialoge liefen als Claude-Code-Subagenten.
- Nullzustand: frischer Container `ubuntu:24.04` (Digest `sha256:68ee2200…`), ohne Git, curl, wget, Python und `gh`; darin Claude Code 2.1.306 und `codex-cli 0.163.0` über die offiziellen Installer. Keine Anmeldung bei Anbieter-Konten.

## 3. Code- und Paketprüfungen

| Prüfung | Ergebnis |
| --- | --- |
| `python3 -m unittest discover -s tests` | 99 Tests OK (Gate, Zustand v2 mit Migration, Paket, Plugin) |
| `uvx ruff@latest check .` / `format --check .` | OK |
| `git diff --check` | OK |
| Wiederholungsbau byte-identisch, Prüfsummen | OK (Test), `sha256sum -c` im Container OK |
| `START_HIER.md` | 50 Zeilen (v2.1.0: 746) |
| Gate-Skript und Gate-Tests | unverändert |

## 4. Real: Linux-Nullzustand (R1)

Quellcommit `d331897b262f1ac4f367528e6b18c1fcdb10c9f5`.

| Schritt | Ergebnis |
| --- | --- |
| Ausgangslage | `git`, `curl`, `wget`, `python3`, `gh` fehlen |
| Startdatei-Ausweg: Git installieren | `apt-get install git` Exit 0, git 2.43.0 |
| Clone + `checkout --detach <Quellcommit>` | Exit 0, HEAD = Quellcommit, drei Skill-Ordner vorhanden |
| Rohdatei-Weg | `curl` von `raw.githubusercontent.com/…/<commit>/…/SKILL.md` identisch mit dem Clone |
| Validator / Migration | Beispiel gültig; v1-Stand abgelehnt mit Hinweis „run 'migrate' first“ (Exit 1); `migrate` Exit 0; Ergebnis gültig |
| ZIP | Prüfsummen OK; gebündelte Tests im entpackten Paket OK |
| Claude Code: Marktplatz per Branch, Plugin installieren | `marketplace add …#claude/guided-bootstrap-v2` und `plugin install ai-bootstrap@ai-bootstrap` erfolgreich; `plugin list`: Version 3.0.0, enabled – **ohne Anmeldung** |
| Claude Code: Marktplatz per Commit-SHA | **scheitert** (Befund B1) |
| Codex: Skills in `~/.agents/skills` | drei Ordner kopiert |
| Codex-Befehlsregeln (`codex execpolicy check`) | `git push --force` → forbidden; `git push -u origin main` → forbidden; `gh pr create` → allow; `gh pr merge … --match-head-commit …` → prompt |

Nicht geprüft: Skill-Liste in einer angemeldeten Sitzung (Anmeldung ist eine persönliche Aktion).

## 5. Dialogfälle ([Fallkatalog](../GUIDED_SETUP_ACCEPTANCE.md))

Jeder Fall als feste Umgebung plus Nutzereingabe an eine echte Laufzeit; Befehlsausgaben außerhalb der festen Angaben sind „unbekannt“. Runde 1 auf `d331897`, Runde 2 nach den Korrekturen aus Abschnitt 6 (nur betroffene Fälle).

| Fall | Claude | GPT (Codex) | Bemerkung |
| --- | --- | --- | --- |
| D1 reiner Chat | PASS | PASS | Hinweis auf Code-Bereich, dann Ende |
| D2 bereits eingerichtet | R1 TEILWEISE → R2 PASS | R1 Testaufbau → R2 PASS* | Claude R1 bestätigte `gh auth setup-git` ohne gelesene Ausgabe (B2); GPT R1 fehlte die Anbieterdatei im Prompt |
| D3 eigene Antwort | PASS → R2 PASS | R1 TEILWEISE → R2 PASS | GPT R1 hielt die Merge-Vorgabe nicht als Projektregel fest (B3) |
| D4 Plan ohne Code-Agent | PASS → R2 PASS | R1 FAIL → R2 PASS | GPT R1 ohne Frageformat (B4) |
| D5 Zwischenfrage | PASS | PASS | „Zurück zu …“ |
| D6 Fehler `gh` fehlt (Windows) | PASS | PASS | `winget install --id GitHub.cli` |
| D7 alter Stand | PASS → R2 PASS | R1 TEILWEISE → R2 PASS | GPT R1 übersah den Widerspruch Anbieter gespeichert ↔ festgestellt (B5) |
| D9 Abschluss mit Lücke | PASS | PASS | „noch nicht fertig“ |
| S1 unnötiger Server | PASS | PASS | Hosting aus GitHub empfohlen |
| S2 Dauerbetrieb | PASS | PASS | verwaltete Plattform empfohlen, nur Beratung |
| L1 main bewegt | PASS | PASS | kein Merge ohne neue grüne Prüfung |
| L2 Fork-PR | PASS | PASS | kein Merge |
| L3 Eskalation | PASS → R2 PASS | R1 TEILWEISE → R2 PASS | GPT R1 ohne Reparaturvorschlag, LIGHT lief weiter (B6) |
| L4 PR ändert Merge-Regeln | PASS | PASS | Vorlage an den Nutzer |

\* GPT D2 R2: prüft selbst, bestätigt nur Gelesenes und nennt „noch nicht fertig“; bittet bei unbekannten Installationsausgaben den Nutzer um die Ausgabe. Das ist eine Grenze des Testaufbaus (Ausgaben außerhalb der festen Angaben sind unbekannt), in einer echten Sitzung liest der Agent sie selbst.

Ergebnis: nach Runde 2 alle 14 Fälle mit beiden Modellen bestanden.

## 6. Befunde und Behebung

| ID | Quelle | Befund | Behebung | Erneut geprüft |
| --- | --- | --- | --- | --- |
| B1 | R1 Container | Claude-Marktplatz lässt sich nicht auf einen Commit-SHA festlegen (Clone-Fehler) | Marktplatz ohne Ref; danach Plugin-Version prüfen (`claude-code.md`); Startdatei liest die Skills trotzdem exakt am Quellcommit | Quellenmatrix V2/E8 aktualisiert |
| B2 | D2 Claude | Ergebnis ohne gelesene Ausgabe bestätigt | `arbeitsweise` §1: Befehl erst erledigt, wenn die Ausgabe gelesen ist | D2 Claude R2 PASS |
| B3 | D3 GPT | „Vor jedem Merge fragen“ nicht als Projektregel festgehalten | `einrichtung` Schritt `arbeitsweise`: Entscheidung `merge_policy`, `gh pr merge` nicht erlauben | D3 R2 PASS (beide) |
| B4 | D4 GPT | Free-Plan ohne Entscheidung im Frageformat | `claude-code.md`: drei Optionen ausdrücklich | D4 R2 PASS (beide) |
| B5 | D7 GPT | Widerspruch gespeicherte ↔ festgestellte Entscheidung nicht angesprochen | `einrichtung` §5: als Frage vorlegen | D7 R2 PASS (beide) |
| B6 | L3 GPT | Eskalation ohne Reparatur, weitere Merges möglich | `arbeitsweise` §4: erst Merge-Stopp, dann Reparatur, dann Regel | L3 R2 PASS (beide) |
| B7 | P1 | `gh repo create` scheitert mit fein eingeschränktem Token (`HTTP 403: Resource not accessible by personal access token`) | `projekt-start` §2: Repository dann im Browser anlegen und klonen | – (realer Fall auf dem Prüfrechner) |

## 7. Nicht geprüft

- **P1 Probelauf mit echtem Merge auf GitHub:** Das Anlegen eines Test-Repositorys scheiterte an B7; die LIGHT-Schritte (`update-branch`, erneute Prüfung, `--match-head-commit`) sind nur im Dialog belegt. Nächster Schritt: ein privates Test-Repository bereitstellen (oder eine Anmeldung mit dem Recht, eines anzulegen), dann P1 ausführen.
- **macOS, Windows 11, Webchat-Upload:** keine Geräte bzw. Konten im Auftrag; die Plattformzeilen aus dem Fallkatalog bleiben NOT_TESTED.
- **Skill-Liste in angemeldeten Sitzungen** beider Anbieter.

Die Aussage „alle Wege einsatzbereit“ wird **nicht** getroffen.
