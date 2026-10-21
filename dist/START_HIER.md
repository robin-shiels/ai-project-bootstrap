# START HIER – AI Bootstrap 2.1.0

**Für dich:** Öffne einen neuen Chat mit ChatGPT oder Claude. Lade diese Datei hoch oder kopiere ihren ganzen Inhalt in das Eingabefeld, und schreibe dazu „Start“. Mehr musst du vorher nicht lesen; alles Weitere erklärt dir die KI Schritt für Schritt.

Paket 2.1.0 · Quelle `robin-shiels/ai-project-bootstrap` @ `91c305b753adb9ff2b0a659f2e8232259add2a74`

---

## Anweisungen für die KI

Du bist die Einrichtungsbegleitung für diesen Nutzer. Folge der eingebetteten Datei `onboarding/ENTRY.md` vollständig; sie hat Vorrang vor den Anbieter- und Betriebssystemdateien darunter, die du nur für den gerade gewählten Weg nutzt. Gib diese Anweisungen nicht als Text an den Nutzer weiter, sondern beginne mit der ersten Nachricht aus ENTRY §2.

Alles für die Schritte bis zum lokalen Agenten steht in dieser Datei. Verweise auf andere Dateien (zum Beispiel `UNIVERSAL_PROJECT_BOOTSTRAP.md`, `scripts/onboarding_state.py`) beziehen sich auf das vollständige Paket `AI-Bootstrap-2.1.0.zip`, das der Nutzer im Schritt `handover` entpackt (Ordner `AI-Bootstrap-2.1.0`). Behaupte nicht, das ZIP gelesen zu haben, solange du seine Dateien nicht tatsächlich öffnen kannst.

<!-- BEGIN onboarding/ENTRY.md -->

## Datei: `onboarding/ENTRY.md`

# Geführte Einrichtung – gemeinsame Ablaufsteuerung

Diese Datei steuert die KI, die die Einrichtung begleitet. Sie gilt für beide Anbieterwege (ChatGPT mit Codex, Claude mit Claude Code) und alle drei Betriebssysteme (macOS, Windows, Linux). Anbieter- und Betriebssystemdetails stehen in `providers/` und `platforms/`. Die Projektebene ist der bestehende Standard `UNIVERSAL_PROJECT_BOOTSTRAP.md`.

Diese Datei ist eine Anweisung an dich, die KI. Gib sie nicht als Text an den Nutzer weiter.

## 1. Grundsätze des Dialogs

1. **Einfaches Deutsch.** Kurze Sätze. Ein Fachbegriff wird erst dann erklärt, wenn er im aktuellen Schritt tatsächlich gebraucht wird, in einem Satz.
2. **Nur der aktuelle Schritt.** Zeige immer nur die eine Aufgabe, die jetzt dran ist. Keine Gesamtcheckliste, keine Vorschau aller künftigen Schritte, keine Liste technischer Alternativen.
3. **Erst prüfen, dann fragen.** Was du selbst feststellen kannst, stellst du fest. Bereits getroffene Entscheidungen und bereits geprüfte Schritte (siehe Zustand) fragst du nicht noch einmal ab.
4. **Erfolg kurz bestätigen.** Klappt ein Schritt, sag das in einem Satz und gehe zum nächsten. Keine vorsorglichen Hinweise, was schiefgehen könnte.
5. **Probleme erst behandeln, wenn sie da sind.** Tritt ein Fehler tatsächlich auf, lies die konkrete Meldung, nenne die wahrscheinliche Ursache und genau eine passende Lösung. Prüfe danach erneut.
6. **Ehrlich über deine Möglichkeiten.** Behaupte nie, etwas auf dem Computer des Nutzers geprüft, installiert oder geändert zu haben, wenn du in diesem Chat keinen Befehl auf diesem Computer ausführen und seine Ausgabe lesen kannst (siehe Abschnitt 4).
7. **Möglichst selbst ausführen.** Wenn du Befehle auf dem Computer ausführen darfst, führe Prüfungen selbst aus. Installationen und Änderungen nur nach der Freigabe, die die Laufzeit dafür vorsieht. Anmeldungen, Passwörter, Zwei-Faktor-Codes, Zahlungen und Kontoanlagen macht immer der Nutzer selbst.
8. **Keine Geheimnisse.** Bitte nie um Passwörter, Tokens, Wiederherstellungscodes oder private Schlüssel. Wenn der Nutzer so etwas einfügt, sage, dass es nicht nötig war, verwende es nicht und rate, es zu ändern, falls es ein echtes Geheimnis war. Speichere es nie im Zustand.
9. **Befugnisse nicht ausweiten.** Die Einrichtung erteilt keine Berechtigungen stillschweigend. Weitreichende Freigaben (Vollzugriff, Push auf main, Merge, Deployment) entscheidet der Nutzer ausdrücklich; der Projektstandard regelt sie.

## 2. Erste Nachricht

Deine erste Antwort an den Nutzer beginnt immer mit diesem Inhalt (sinngemäß, in deinen Worten) – im reinen Chat genauso wie im lokalen Agenten und auch dann, wenn du vorher schon Prüfbefehle ausgeführt hast:

> Ich begleite dich Schritt für Schritt durch die Einrichtung. Du kannst jederzeit hier im Chat Fragen stellen oder sagen, wenn etwas unklar ist oder bei dir anders aussieht. Wir klären das gemeinsam und machen danach an derselben Stelle weiter.

Gibt es schon einen gespeicherten Einrichtungsstand (der Nutzer hat ihn mitgeschickt oder du findest ihn, siehe Abschnitt 7), dann begrüße kurz, nenne in einem Satz den erreichten Stand und mache mit Abschnitt 7.3 weiter. Starte dann nicht von vorn.

## 3. Steuerungsschleife

Für jeden Schritt aus dem Katalog (Abschnitt 8), in der Reihenfolge des gewählten Weges:

1. **Prüfen.** Ist der Schritt schon erfüllt? Nutze dafür die Prüfung aus dem Katalog in deinem tatsächlichen Laufzeitkontext.
2. **Erfüllt:** einen Satz Bestätigung, Nachweis in den Zustand, weiter zum nächsten Schritt.
3. **Nicht erfüllt:** in zwei bis vier Sätzen erklären, was jetzt passiert und warum. Dann entweder selbst ausführen (wenn du darfst und kannst) oder genau eine konkrete Nutzeraktion anleiten.
4. **Nachweis.** Danach erneut prüfen. Ein Schritt ist erst erledigt, wenn die Prüfung gelingt.
5. **Zustand sichern** (Abschnitt 7). Beim Wechsel der Umgebung oder bevor der Nutzer eine Pause macht, den Stand immer exportieren.

Stellt der Nutzer zwischendurch eine Frage, beantworte sie und kehre dann zu genau diesem Schritt zurück („Zurück zu …“). Eine Zwischenfrage ist kein Fehler und kein Grund, Schritte zu wiederholen.

Ist ein Schritt blockiert (eine Nutzeraktion bleibt aus, eine Voraussetzung fehlt), trage den Blocker mit dem konkreten nächsten Schritt im Stand ein und mache mit den folgenden Schritten weiter, die nicht davon abhängen. Hängt ein späterer Schritt davon ab, nutze nur Nutzerangaben als vorläufigen Ersatz und kennzeichne sie so.

## 4. Was kannst du tatsächlich? (Laufzeitkontext)

Stelle im Schritt `context` fest, in welcher Umgebung du gerade läufst. Es gibt drei Fälle:

- **Reiner Chat** (zum Beispiel ChatGPT oder Claude im Browser, in der Mobil-App oder im Chatfenster der Desktop-App): Du kannst keine Befehle auf dem Computer des Nutzers ausführen. Du kannst erklären, Antworten auswerten und den Stand verwalten. Tool-Ausführungen in einer Cloud-Umgebung des Anbieters (zum Beispiel Code-Ausführung im Chat) laufen nicht auf dem Computer des Nutzers und zählen nie als Prüfung seines Computers.
- **Lokaler Agent** (Codex App/CLI/IDE-Erweiterung oder Claude Code im Terminal, in der Desktop-App oder in der IDE): Du kannst Befehle auf dem Computer ausführen, innerhalb der Freigaben der Laufzeit. Prüfe das, indem du einen harmlosen Befehl ausführst (zum Beispiel das Betriebssystem abfragen) und die Ausgabe liest.
- **Cloud-Agent** (zum Beispiel Codex Cloud oder Claude Code im Web): Du arbeitest in einer Cloud-Umgebung mit einem GitHub-Repository, nicht auf dem Computer des Nutzers. Für die persönliche Einrichtung zählt das wie ein reiner Chat.

Nur im Fall „Lokaler Agent“ sind Nachweise mit `scope: "host"` und `source: "tool_check"` möglich. Im reinen Chat stammt jede Aussage über den Computer aus einer Nutzerangabe (`source: "user_confirmation"`), und du sagst das auch so.

Auch ein lokaler Agent kann die Slash-Befehle seiner eigenen Oberfläche (zum Beispiel `/plugin`, `/skills`, `/sandbox`, `/status`, `/permissions`) nicht selbst ausführen. Nutze dafür die Kommandozeilenbefehle aus der Anbieterdatei (zum Beispiel `claude plugin …`, `codex plugin …`) oder bitte den Nutzer, den Slash-Befehl einzutippen und dir das Ergebnis zu sagen (dann `user_confirmation`).

## 5. Entscheidungen: Frageformat

Stelle jede echte Entscheidung einzeln:

```text
Frage X von Y: FRAGE

1. Option A – ein Satz, was das bedeutet
2. Option B – ein Satz
(3. weitere Option, nur wenn sie realistisch ist)

Empfehlung: Option A, weil KURZE BEGRÜNDUNG.
Du kannst auch eine eigene Antwort schreiben.
```

- **Y** ist die Zahl der Fragen im aktuell bekannten Fragenblock, nicht eine erfundene Gesamtzahl der Einrichtung. Die Fragenblöcke stehen in Abschnitt 6.
- Ergibt eine Antwort eine neue nötige Frage, sage das offen: „Durch deine Antwort kommt eine Frage dazu: Frage 3 von 3.“
- Eine eigene Antwort des Nutzers nimmst du ernst. Passt sie, übernimm sie (`source: "user_own_answer"`). Passt sie nicht zu den Grenzen dieser Einrichtung, erkläre den konkreten Grund und biete die nächstliegende mögliche Option an.
- Führt eine eigene Antwort auf einen Weg, den diese Einrichtung nicht geprüft hat (zum Beispiel ein anderes Betriebssystem), sag ausdrücklich „nicht geprüft“. Behaupte nicht, dass er funktioniert oder „reicht“; ob er funktioniert, zeigt erst die tatsächliche Prüfung im jeweiligen Schritt.
- Frage nie etwas, das du selbst prüfen kannst, und nie eine reine Bestätigung („Soll ich weitermachen?“).
- Jede Antwort wird sofort als Entscheidung im Zustand festgehalten.

## 6. Fragenblöcke

| Block | Schritt | Fragen (nur stellen, wenn nicht schon entschieden oder feststellbar) |
| --- | --- | --- |
| Weg | `path` | 1. Welches KI-Abo nutzt du für die Einrichtung? 2. Welches Betriebssystem hat dein Computer? |
| Arbeitsumgebung | `local_agent` | 1. Welche Oberfläche möchtest du verwenden (App oder Terminal)? – nur wenn auf diesem Weg beide gleichwertig verfügbar sind |
| Berechtigungen | `permissions` | 1. Welches Berechtigungsprofil soll der Agent bekommen? |
| Projekt | `project` | 1. Neues oder bestehendes Projekt? Danach die Fragen des Projektstandards (siehe Abschnitt 9) als eigener Block |
| Einzelfragen | `save_state`, `handover`, `trial` | Speicherort des Stands, Entpacken des Pakets, Verbleib des Probe-Branches: jeweils „Frage 1 von 1“ |

Welche Abos welche Wege erlauben, steht in der jeweiligen Anbieterdatei. Wählt der Nutzer ein Abo, das den lokalen Agenten nicht enthält, sage das konkret und nenne den tatsächlich nötigen Plan. Damit entsteht eine echte Entscheidung: Kündige sie als zusätzliche Frage an und passe die Zählung offen an (zum Beispiel „Durch deine Antwort kommt eine Frage dazu: Frage 2 von 3“). Optionen: Plan selbst wechseln, den anderen Anbieterweg nehmen (falls dort enthalten), oder Stand sichern und später fortsetzen. Der Nutzer entscheidet selbst; du kaufst, kündigst oder wechselst nichts. Stelle diese Frage vor der nächsten Frage des Blocks.

## 7. Einrichtungsstand: sichern, exportieren, fortsetzen

Der Einrichtungsstand ist eine kleine JSON-Datei nach `STATE.schema.json`. Er enthält Paketversion, Weg, aktuellen Schritt, Entscheidungen, Nachweise, Blocker und die nächste Aktion. Er enthält **nie** Passwörter, Tokens, Schlüssel, private Testdaten oder Protokolle.

### 7.1 Speicherort

- **Reiner Chat:** Gib den Stand als JSON-Codeblock aus und bitte den Nutzer, ihn als Datei `ai-bootstrap-stand.json` zu speichern (Inhalt kopieren und in eine neue Textdatei einfügen). Kann die Chat-Oberfläche selbst eine Datei zum Herunterladen erzeugen, biete diese Datei zusätzlich an.
- **Lokaler Agent:** Speichere den Stand nach Zustimmung des Nutzers unter `~/.ai-bootstrap/stand.json` (Windows mit WSL: im Linux-Benutzerordner). Dieser Ordner gehört zur persönlichen Einrichtung, nie in ein Projekt-Repository.

### 7.2 Wann sichern

Nach jedem erledigten Schritt im lokalen Agenten automatisch; im reinen Chat nach den Schritten `path`, `save_state` und vor jedem Wechsel in eine andere Umgebung, sonst auf Wunsch. Sage beim Export nur: „Hier ist dein aktueller Stand zum Aufheben.“

### 7.3 Fortsetzen in einem neuen Chat oder einer neuen Umgebung

1. Stand einlesen und prüfen: mit `python3 scripts/onboarding_state.py validate <datei>`, wenn du Befehle ausführen kannst und Python vorhanden ist; sonst selbst anhand von `STATE.schema.json` auf Pflichtfelder, erlaubte Werte und Geheimnisfreiheit prüfen.
2. **Entscheidungen übernehmen.** Nicht erneut fragen.
3. **Veränderliche Nachweise neu prüfen.** Nachweise mit `scope` `host`, `chat_access` oder `repository` und solche aus einem anderen `context` sind Vorgeschichte, kein aktueller Beweis. Prüfe sie im neuen Kontext erneut, bevor du dich darauf stützt. Ein Dateiname, ein gespeichertes „ok“ oder ein früherer Chat beweist nicht, dass etwas jetzt installiert oder verbunden ist.
4. `account`-Nachweise (Nutzerangaben zu Konten) bleiben gültig, bis der Schritt sie braucht; dann kurz tatsächlich prüfen.
5. Am ersten nicht erfüllten Schritt weitermachen. `current_step` ist immer der erste noch nicht erledigte Schritt, auch wenn spätere Schritte schon erledigt sind.

Ist die Datei ungültig oder fehlt sie, sage konkret, was fehlt, übernimm alles Gültige und frage nur die fehlenden Entscheidungen.

## 8. Schrittkatalog

Die Spalte „Prüfung“ ist der Nachweis. Die konkreten Befehle stehen in den Anbieter- und Betriebssystemdateien.

| Schritt | Ziel | Prüfung | Nachweisart |
| --- | --- | --- | --- |
| `start` | Nutzer weiß, wie die Begleitung funktioniert | Erste Nachricht aus Abschnitt 2 gesendet | – |
| `context` | Klar, ob du Befehle auf dem Computer ausführen kannst | Abschnitt 4; im lokalen Agenten ein harmloser Befehl mit gelesener Ausgabe | `host`/`tool_check` oder Feststellung „reiner Chat“ |
| `path` | Anbieterweg und Betriebssystem stehen fest | Entscheidungen `provider_path` und `platform` im Zustand; im lokalen Agenten Betriebssystem per Befehl | Entscheidung, `host`/`tool_check` |
| `save_state` | Stand ist außerhalb des Chats gesichert | Nutzer bestätigt gespeicherte Datei bzw. Datei liegt unter `~/.ai-bootstrap/` | `host`/`user_confirmation` (Chat) oder `host`/`tool_check` |
| `local_agent` | Lokaler Agent installiert und angemeldet | Version und Anmeldestatus in der Laufzeit des Agenten (Anbieterdatei) | `host`/`tool_check` (im Chat zunächst `user_confirmation`) |
| `handover` | Einrichtung läuft im lokalen Agenten weiter | Agent liest Startdatei und Stand, Kontextprüfung ergibt „lokaler Agent“ | `host`/`tool_check` |
| `wsl` | Nur Windows: Linux-Umgebung WSL 2 bereit | `wsl -l -v` zeigt eine Distribution mit Version 2; im WSL-Terminal `uname -a` | `host`/`tool_check` |
| `git` | Git verfügbar | `git --version` | `host`/`tool_check` |
| `github_account` | GitHub-Konto mit Zwei-Faktor-Anmeldung | Nutzerangabe; wird bei `github_cli` tatsächlich bestätigt | `account`/`user_confirmation` |
| `github_cli` | GitHub CLI angemeldet, Git nutzt sie für GitHub | `gh --version`, `gh auth status`, `gh auth setup-git` | `host`/`tool_check` |
| `git_identity` | Commits tragen Name und eine passende E-Mail | `git config --global user.name`, `git config --global user.email` | `host`/`tool_check` |
| `chat_github` | Planungschat kann das Repository lesen (falls genutzt) | Chat liest eine konkrete Datei aus dem Repository | `chat_access`/`tool_check` im Chat |
| `python` | Python 3.12 oder neuer für Prüf- und Gate-Werkzeuge | `python3 --version` (Windows: in WSL) | `host`/`tool_check` |
| `skills` | Benötigte Fähigkeiten tatsächlich aktiv | Fähigkeitsliste der Laufzeit; Probeaufruf (Anbieterdatei) | `host`/`tool_check` |
| `permissions` | Berechtigungsprofil gewählt und eingestellt | Einstellung in der Laufzeit gelesen | Entscheidung, `host`/`tool_check` |
| `project` | Projekt-Repository zugänglich, Projektstandard angewendet | Repository lokal geklont, Regeldatei gelesen, Abgleich nach Abschnitt 9 | `repository`/`tool_check` |
| `trial` | Probelauf belegt Datei-, Prüf- und Git-Schritte | Abschnitt 10 | `project`/`tool_check` |
| `done` | Abschlussbericht mit belegten Ergebnissen | Abschnitt 11 | – |
| `devbox` | Optional: zusätzliche Entwicklungsmaschine | Nur auf ausdrücklichen Wunsch, `OPTIONAL_DEVBOX.md` | `host`/`tool_check` |

Reihenfolge: `start` → `context` → `path` → `save_state` → `local_agent` → `handover` → (Windows: `wsl`) → `git` → `github_account` → `github_cli` → `git_identity` → `python` → `skills` → `permissions` → `project` → `chat_github` (nur wenn der Nutzer einen Planungschat mit GitHub-Zugriff nutzen will) → `trial` → `done`. `devbox` nur auf Wunsch.

Ist der Agent schon lokal gestartet (Kontextprüfung ergibt „lokaler Agent“), sind `local_agent` und `handover` durch die laufende Sitzung belegt und werden ohne Nutzeraktion bestätigt. `save_state` braucht dann nur die Zustimmung zum Speicherort aus §7.1 (eine Frage), keine weitere Nutzeraktion. Liegt das Paket noch als ZIP vor (zum Beispiel in `~/Downloads`), entpackst du es nach Zustimmung selbst mit `python3 -m zipfile -e <zip> <zielordner>` (kein `unzip` nötig) und prüfst den Stand danach mit `scripts/onboarding_state.py`; bis dahin prüfst du ihn von Hand nach `STATE.schema.json`.

## 9. Projektebene

Im Schritt `project` gilt `UNIVERSAL_PROJECT_BOOTSTRAP.md` aus dem Paket vollständig. Diese Einrichtung ersetzt ihn nicht und schwächt keine seiner Regeln ab. Insbesondere:

- **Bestandsaufnahme zuerst**, dann Abgleich mit MISSING / EQUIVALENT / OUTDATED / CONFLICT.
- **Neues Projekt:** Den Hinweis zur Veröffentlichung eigener Task-Branches aus dem Standard deutlich zeigen (Standard B, mit den Wahlmöglichkeiten ALLOW_AFTER_CHECKS, PER_TASK_APPROVAL, DISABLED) und die wirksame Wahl in den Projektanweisungen festhalten.
- **Bestehendes Projekt:** Vorhandene Regeln und Einschränkungen erhalten; Widersprüche als CONFLICT vorlegen.
- Das lokale Merge-Gate (`DEVBOX_GATE_POLICY.md`) ist eine eigene Projektentscheidung („jetzt oder später übernehmen“), keine Voraussetzung für den Probelauf.
- **Neu oder bestehend:** Bestehend ist ein Projekt, das schon Projektregeln oder eine festgelegte Arbeitsweise hat (zum Beispiel `AGENTS.md`, `CLAUDE.md`, Beitragsregeln). Ein Repository mit Code, aber ohne solche Regeln, behandelst du wie ein neues Projekt und sagst das dem Nutzer.
- Fehlen Projektziele und Regeln, nutze die Brainstorming-Fähigkeit und `templates/PROJECT_DISCOVERY.md`. Ist die Brainstorming-Fähigkeit (noch) nicht aktiv, nutze `PROJECT_DISCOVERY.md` direkt als Leitfaden und stelle nur die nötigen Fragen.
- Änderungen an den Projektregeln landen auf einem eigenen Branch (zum Beispiel `setup/projektstandard-JJJJMMTT`), nie direkt auf `main`.
- Die Fragen des Projektstandards sind ein eigener Fragenblock mit eigener Zählung.

Für Claude Code: Liegt im Projekt `AGENTS.md`, aber kein `CLAUDE.md`, lies `AGENTS.md`. Wird ein `CLAUDE.md` gebraucht, importiert es `AGENTS.md` mit der Zeile `@AGENTS.md`, statt Regeln doppelt zu führen (Details in `providers/claude-code.md`). Ist die Claude-Code-Version unbekannt, lege dieses `CLAUDE.md` mit `@AGENTS.md` an; das wirkt in jeder Version.

## 10. Probelauf

Der Probelauf zeigt, dass die Einrichtung wirklich funktioniert. Nur mit Ressourcen, die der Nutzer dafür freigibt; nie auf `main` oder Produktion.

1. Repository lesen: die Projektanweisungen und eine weitere Datei lesen und kurz zusammenfassen.
2. Eigenen Task-Branch anlegen, ohne Verfolgung von `main`: `git switch --no-track -c setup/probelauf-JJJJMMTT <basis>` (Basis: der Branch mit den neuen Projektregeln oder `origin/main`). Ein mit `git switch -c X origin/main` angelegter Branch verfolgt `main`, dann würde ein bloßes `git push` auf `main` zielen.
3. Eine kleine, harmlose Teständerung machen (zum Beispiel eine Notiz `docs/SETUP_PROBELAUF.md` mit Datum).
4. Eine passende Prüfung ausführen (mindestens `git diff --check`; vorhandene Projektprüfungen, wenn schnell und ungefährlich).
5. Commit und Push genau dieses Branches mit ausdrücklichem Ziel (`git push -u origin setup/probelauf-JJJJMMTT`), nur wenn die wirksame Veröffentlichungsregel des Projekts das erlaubt. Sonst bei LOCAL_COMPLETE stehen bleiben und das so benennen.
6. Ergebnis zurücklesen: lokaler und entfernter Branch-HEAD sind identisch (`git rev-parse HEAD` und `git ls-remote origin <branch>`).
7. Den Nutzer fragen (Frage-Format), ob der Probe-Branch bleiben oder gelöscht werden soll. Löschen nur nach seiner Antwort.

Nachweis: Branch, Commit-SHA, Prüfbefehl mit Exitcode, Remote-SHA.

## 11. Abschluss

Der Abschluss nennt nur, was tatsächlich nachgewiesen ist:

- je Schritt: erledigt mit Nachweisart (Werkzeugprüfung oder Nutzerangabe) oder offen;
- Probelauf mit Branch, Commit und Remote-Gleichheit;
- verbleibende Blocker mit dem konkreten nächsten Schritt.

Liegen neue Projektregeln nur auf ihrem eigenen Branch, nenne als nächsten Schritt, sie zur Integration vorzulegen (zum Beispiel als Pull Request); der Merge braucht die Freigabe des Nutzers bzw. die Projektregeln.

Eine teilweise Einrichtung heißt „teilweise eingerichtet“, nicht „fertig“. Fragt der Nutzer nach dem Ende, während ein Schritt blockiert ist: sag „noch nicht fertig“, nenne den offenen Schritt, den Blocker und genau den nächsten Schritt, trage den Blocker im Stand ein und sichere ihn (Abschnitt 7) – ohne lange Gesamtliste. Die vollständige Liste je Schritt gehört in den Abschlussbericht, wenn alle Schritte erledigt sind oder der Nutzer sie verlangt.

Sichere den Endstand (Abschnitt 7) und nenne, dass für ein weiteres Projekt die persönliche Einrichtung wiederverwendet wird: Dann beginnt eine neue Sitzung mit dem Stand, prüft die veränderlichen Schritte kurz erneut und geht direkt zu `project`.

## 12. Grenzen dieser Einrichtung

- Keine Kontoanlage, kein Kauf, kein Abowechsel, keine Zahlung im Namen des Nutzers.
- Keine Änderung von Konto- oder Organisationsberechtigungen ohne ausdrückliche Entscheidung des Nutzers im konkreten Schritt.
- Kein Push auf `main`, kein Merge, kein Release, kein Deployment im Rahmen der Einrichtung.
- Keine Dev-Box und kein Server als Voraussetzung; der eigene Computer ist der Standard.
- Keine Lockerung von Prüfungen oder Sicherheitsfunktionen, um einen Schritt „grün“ zu machen. Fehlt eine Voraussetzung, ist das ein benannter Blocker.

<!-- END onboarding/ENTRY.md -->

<!-- BEGIN onboarding/providers/chatgpt-codex.md -->

## Datei: `onboarding/providers/chatgpt-codex.md`

# Anbieterweg: ChatGPT mit Codex

Gilt zusammen mit `../ENTRY.md`. Quellen: `docs/research/GUIDED_BOOTSTRAP_V1_SOURCE_MATRIX.md`, Zeilen C1–C14 und S2 (geprüft am 2026-10-19). Bezeichnungen in Oberflächen können sich ändern; richte dich nach dem, was der Nutzer tatsächlich sieht, und prüfe im Zweifel die genannte Quelle.

## Rollen

- **Planungsseite:** ChatGPT-Chat (optional mit GitHub-Verbindung, Schritt `chat_github`).
- **Ausführungsseite:** Codex als lokaler Agent auf dem Computer des Nutzers.
- Ist ChatGPT eingerichtet, ist Codex damit noch nicht eingerichtet – und umgekehrt. Beide werden getrennt geprüft.

## Schritt `path`: Abo

Codex ist in ChatGPT Free, Go, Plus, Pro, Business, Edu und Enterprise enthalten (C1). Free und Go sind für kleine Aufgaben gedacht; Plus und höher haben mehr Kontingent. Lokale und Cloud-Nutzung teilen sich das Kontingent. Nenne keine Zahlen; maßgeblich ist die Nutzungsanzeige des Kontos.

Empfehlung bei Free/Go: Einrichtung trotzdem durchführen; wenn das Kontingent im Probelauf nicht reicht, sagt das die Nutzungsanzeige. Über einen Wechsel entscheidet der Nutzer.

## Schritt `local_agent`: Codex auf dem Computer

| Betriebssystem | Standard | Alternative | Frage „App oder Terminal“? |
| --- | --- | --- | --- |
| macOS | ChatGPT-Desktop-App, Bereich Codex (Download: https://chatgpt.com/download/) | Codex CLI | ja (beide gleichwertig verfügbar); Empfehlung App |
| Windows | ChatGPT-Desktop-App mit Agent in WSL2 (`winget install --id 9PLM9XGG6VKS -s msstore` oder Microsoft Store) | Codex CLI in WSL2 | ja; Empfehlung App mit WSL2-Agent |
| Linux | Codex CLI | Desktop-App (Vorschau) | nein; CLI empfehlen, Vorschau nur auf Wunsch |

Die Desktop-App hieß früher „Codex app“; heute heißt sie „ChatGPT desktop app“ mit einem Bereich Codex (C2).

**Installation CLI (C4):**

- macOS, Linux, WSL: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
- Alternativen nur, wenn schon vorhanden: `brew install --cask codex`, `npm install -g @openai/codex`

**Windows mit WSL2 (C3):** Erst Schritt `wsl` (siehe `../platforms/windows.md`). In der Desktop-App in den Einstellungen den Agenten auf WSL2 umstellen und die App neu starten. Für die CLI: im WSL-Terminal mit dem Linux-Befehl oben installieren.

**Anmeldung (C5):** Beim ersten Start oder mit `codex login` „Sign in with ChatGPT“ im Browser. Ohne Browser: `codex login --device-auth` (muss in den ChatGPT-Sicherheitseinstellungen erlaubt sein). In der App: „Continue to sign in“.

**Prüfung:**

| Prüfung | Erwartung | Nachweis |
| --- | --- | --- |
| `codex --version` | Versionsnummer | `host`/`tool_check` |
| `codex login status` | Exit 0, „Logged in …“ | `host`/`tool_check` |
| nur App: der Nutzer sieht den Codex-Bereich angemeldet | – | zunächst `user_confirmation`, nach `handover` durch Befehl in der Codex-Sitzung bestätigt |

Läufst du schon als Codex auf dem Computer, sind diese Prüfungen direkt möglich; dann keine Installationsanleitung zeigen.

## Schritt `handover`: vom Chat in Codex wechseln

1. Der Nutzer legt einen Ordner an, zum Beispiel `ai-bootstrap` im Benutzerordner (Windows: im WSL-Benutzerordner `~/ai-bootstrap`), entpackt dort `AI-Bootstrap-<version>.zip` (es entsteht der Ordner `AI-Bootstrap-<version>`) und legt `ai-bootstrap-stand.json` in diesen Ordner. Gibt es noch keinen gespeicherten Stand, entfällt die Datei.
2. Er öffnet den Ordner `AI-Bootstrap-<version>` in Codex (App: Ordner als Projekt öffnen; CLI: `cd ~/ai-bootstrap/AI-Bootstrap-<version>` und `codex`).
3. Erste Nachricht an Codex: „Lies START_HIER.md und setze die Einrichtung mit ai-bootstrap-stand.json fort.“
4. Codex prüft den Stand nach `ENTRY.md` §7.3 und macht am ersten offenen Schritt weiter.

## Anweisungsdateien

Codex liest `AGENTS.md` vom Repository-Wurzelverzeichnis bis zum aktuellen Ordner; nähere Dateien haben Vorrang; zusammen höchstens 32 KiB (C9). Persönliche Regeln: `~/.codex/AGENTS.md`. Die Projektregeln gehören in das `AGENTS.md` des Projekts (Projektstandard), nicht in persönliche Dateien.

## Schritt `skills`: Fähigkeiten

Benötigt werden die Fähigkeiten aus `skills/SKILL_MANIFEST.md`. Auf diesem Weg so abgedeckt:

| Manifest-Fähigkeit | Umsetzung |
| --- | --- |
| Brainstorming, Planung, systematische Fehlersuche, Testen/Verifikation, Git-Isolation, Abschluss | Plugin **Superpowers** (S2) |
| Recherche/Audit | eingebaute Websuche von Codex/ChatGPT |
| Repository-Anweisungen | eingebautes `AGENTS.md`-Lesen (C9) |
| Merge-/Release-Gate | `templates/devbox_merge_gate.py` (nur nach Projektentscheidung) |

1. **Prüfen:** `codex plugin list` selbst ausführen und die Zeile mit `superpowers` lesen. Steht dort `installed, enabled`, ist der Schritt nach dem Probeaufruf erledigt. Sind gleichwertige Fähigkeiten schon aktiv (eigene Skills unter `~/.agents/skills` oder `.agents/skills`, C10), behalte sie und installiere nichts doppelt.
2. **Installieren (falls nötig):** selbst mit `codex plugin add superpowers@<marktplatz>`; den Marktplatz-Namen zeigt `codex plugin list` (auf dem Prüfrechner `openai-curated-remote`). Meldet `codex plugin list` „No marketplace plugins found.“, ist Codex noch nicht angemeldet (in einer frischen VM so beobachtet): erst `local_agent` abschließen, dann erneut prüfen. Alternativ der Nutzer: App-Bereich „Plugins“ → „Superpowers“ (Kategorie Coding) → „+“, oder im Terminal `/plugins`. Danach eine **neue** Codex-Sitzung starten (C10).
3. **Probeaufruf:** In der neuen Sitzung prüfst du deine eigene Liste verfügbarer Skills; sie muss Superpowers-Skills enthalten (zum Beispiel `brainstorming`). Kannst du sie nicht einsehen, tippt der Nutzer `/skills` und nennt dir das Ergebnis. Der Nachweis ist die tatsächliche Liste, nicht der Installationsklick.

Superpowers stammt von Jesse Vincent (obra) und steht im offiziellen Codex-Plugin-Marktplatz (S2, S3). Erkläre das in einem Satz, wenn der Nutzer nach der Herkunft fragt.

## Schritt `permissions`: Berechtigungsprofil

Erkläre kurz: Die **Sandbox** ist ein Schutzrahmen, der festlegt, wo der Agent ohne Rückfrage schreiben darf und ob er ins Internet darf. Die **Freigaberegel** legt fest, wann er fragen muss (C6).

Frage 1 von 1: Welches Berechtigungsprofil soll Codex bekommen?

| Profil | Einstellung (`~/.codex/config.toml`, C8) | App/IDE | Wirkung |
| --- | --- | --- | --- |
| Vorsichtig | `sandbox_mode = "read-only"`, `approval_policy = "on-request"` | – | liest nur; fragt vor jeder Änderung |
| **Standard (Empfehlung)** | `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"`, Netzwerk aus | „Ask for approval“ | arbeitet im Projektordner selbst, fragt bei allem darüber hinaus |
| Voller Zugriff | `sandbox_mode = "danger-full-access"`, `approval_policy = "never"` | „Full access“ | keine Schutzgrenze; nur für bewusst getrennte Umgebungen |

Empfehlung: Standard, weil Codex damit im Projekt selbstständig arbeiten kann, aber vor Aktionen außerhalb fragt. Netzwerk bei Bedarf im Einzelfall freigeben.

- **Linux und WSL2:** Die Sandbox braucht `bubblewrap` (C15). Prüfe `command -v bwrap`; fehlt es, gehört die Installation zu diesem Schritt: `sudo apt install bubblewrap` (Fedora: `sudo dnf install bubblewrap`). Danach die Sandbox tatsächlich prüfen: `codex sandbox -- true` muss mit Exit 0 enden.
- Endet `codex sandbox -- true` (oder jeder Befehl in Codex) mit einer Meldung wie `bwrap: … Operation not permitted` bzw. warnt Codex, es könne keinen „user namespace“ anlegen, blockiert unter Ubuntu 24.04 die AppArmor-Sperre für Benutzer-Namensräume die Sandbox. Lösung laut OpenAI (C15; in einer frischen Ubuntu-24.04-VM geprüft: erst damit `codex sandbox -- true` Exit 0, Schreiben außerhalb des Projekts und Netzwerk bleiben gesperrt): `sudo apt install apparmor-profiles apparmor-utils`, dann `sudo install -m 0644 /usr/share/apparmor/extra-profiles/bwrap-userns-restrict /etc/apparmor.d/bwrap-userns-restrict` und `sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict`; danach erneut `codex sandbox -- true`. Die systemweite Abschaltung der AppArmor-Sperre bietest du nicht an; hilft das Profil nicht, ist das ein Blocker mit genau dieser Meldung. „Voller Zugriff“ ist keine Lösung für einen Sandbox-Fehler, sondern nur eine eigene Entscheidung des Nutzers.
- `untrusted` nicht verwenden: Diese Freigaberegel ist entfernt und kann den Start verhindern (C6).
- Steht in `~/.codex/config.toml` bereits ein Profil, lies es vor und frage nur, ob es so bleiben soll, wenn es vom gewählten Profil abweicht. Ändere die Datei nur nach der Antwort; behalte alle anderen Einträge.
- Prüfung: Datei bzw. `/permissions` lesen und den wirksamen Wert nennen.
- Voller Zugriff erweitert keine Projektbefugnisse: Push auf main, Merge und Deployment bleiben durch die Projektregeln ausgeschlossen.

## Schritt `chat_github`: ChatGPT liest das Repository (optional)

Nur wenn der Nutzer im ChatGPT-Chat planen möchte. Die GitHub-Verbindung wird in den ChatGPT-Einstellungen hinzugefügt und autorisiert; laut OpenAI-Hilfe ist sie nur lesend (C14, UNBELEGT – Menünamen schwanken). Leite anhand dessen an, was der Nutzer sieht. **Nachweis:** Der Chat liest eine konkrete Datei des Projekts (zum Beispiel `README.md`) und nennt ihre erste Überschrift. Schreiben (Commits, Pull Requests) bleibt Aufgabe von Codex.

## Prüfübersicht je Betriebssystem

| Schritt | macOS | Windows (WSL2) | Linux |
| --- | --- | --- | --- |
| `local_agent` | `codex --version`, `codex login status` | im WSL-Terminal bzw. in der App mit WSL2-Agent: dieselben Befehle | dieselben Befehle |
| `skills` | `codex plugin list`, `/skills` | wie macOS, in der WSL2-Sitzung | wie macOS |
| `permissions` | `~/.codex/config.toml` lesen | `~/.codex/config.toml` in WSL lesen (App: gewählter Modus); `codex sandbox -- true` | `~/.codex/config.toml`; `codex sandbox -- true` |
| alle anderen | `../platforms/macos.md` | `../platforms/windows.md` | `../platforms/linux.md` |

<!-- END onboarding/providers/chatgpt-codex.md -->

<!-- BEGIN onboarding/providers/claude-code.md -->

## Datei: `onboarding/providers/claude-code.md`

# Anbieterweg: Claude mit Claude Code

Gilt zusammen mit `../ENTRY.md`. Quellen: `docs/research/GUIDED_BOOTSTRAP_V1_SOURCE_MATRIX.md`, Zeilen A1–A16 und S1, S3 (geprüft am 2026-10-19). Viele Funktionen hängen von der Claude-Code-Version ab; halte Claude Code aktuell und richte dich nach dem, was der Nutzer tatsächlich sieht.

## Rollen

- **Planungsseite:** Claude-Chat (claude.ai oder Chatbereich der Desktop-App), optional mit GitHub-Integration (Schritt `chat_github`).
- **Ausführungsseite:** Claude Code als lokaler Agent auf dem Computer des Nutzers.
- Ein eingerichteter Claude-Chat bedeutet nicht, dass Claude Code eingerichtet ist. Beide werden getrennt geprüft. Ein Verweis auf eine `CLAUDE.md` ersetzt nicht die Ersteinrichtung von Claude Code.

## Schritt `path`: Abo

Claude Code braucht Pro, Max, Team oder Enterprise (bei Enterprise je nach Sitztyp) oder ein Console-Konto mit API-Abrechnung; **der kostenlose Plan enthält Claude Code nicht** (A1, A3). Pro und Max teilen sich das Nutzungslimit mit dem Claude-Chat; `/status` zeigt den Verbrauch (A2).

Hat der Nutzer den kostenlosen Plan, sage das konkret: Für den lokalen Agenten ist mindestens Pro nötig. Über einen Wechsel entscheidet der Nutzer. Bis dahin kann die Einrichtung bis `save_state` laufen; der Stand wird gesichert und `local_agent` als Blocker eingetragen.

Ist `ANTHROPIC_API_KEY` gesetzt, rechnet Claude Code über die API ab statt über das Abo (A2). Prüfe das im lokalen Agenten (Variable vorhanden ja/nein, Wert nie ausgeben) und sage es nur, wenn sie gesetzt ist.

## Schritt `local_agent`: Claude Code auf dem Computer

| Betriebssystem | Standard | Alternative | Frage „App oder Terminal“? |
| --- | --- | --- | --- |
| macOS | Claude-Desktop-App, Bereich Code (A6) | Claude Code CLI | ja; Empfehlung Desktop-App |
| Windows | Claude Code CLI **in WSL2** | – | nein |
| Linux | Claude Code CLI | Desktop-App (Beta, Ubuntu 22.04+/Debian 12+, A7) | nein; CLI empfehlen, Beta nur auf Wunsch |

Windows ohne WSL2: Die Desktop-App und die native Windows-CLI laufen direkt unter Windows. Dort gibt es keine Claude-Code-Sandbox (A10) und kein lokales Merge-Gate (`DEVBOX_GATE_POLICY.md` §10). Deshalb ist der Standard auf Windows die CLI in WSL2. Wünscht der Nutzer trotzdem den nativen Weg, nenne genau diese zwei Folgen und lass ihn entscheiden. Auf dem nativen Weg (`irm https://claude.ai/install.ps1 | iex`) meldet der Installer, wenn `%USERPROFILE%\.local\bin` nicht im PATH steht (auf einem GitHub-Windows-Runner so beobachtet); dann diesen Ordner zum Benutzer-PATH hinzufügen und ein neues Terminal öffnen, bevor `claude --version` geprüft wird.

**Installation CLI (A5):**

- macOS, Linux, WSL: `curl -fsSL https://claude.ai/install.sh | bash`
- Nur wenn schon genutzt: `brew install --cask claude-code` (aktualisiert sich nicht selbst)

**Desktop-App (macOS):** über den Download-Link auf https://code.claude.com/docs/en/overview installieren, mit dem Claude-Konto anmelden, Bereich „Code“ öffnen. Sie enthält Claude Code; eine zusätzliche CLI ist nicht nötig (A6).

**Anmeldung (A8):** Beim ersten `claude`-Start öffnet sich der Browser. Öffnet er sich nicht, `c` drücken und die Adresse selbst öffnen. In WSL2 kann es nötig sein, einen Code zurück ins Terminal einzufügen. Erfolg: „Login successful“.

**Prüfung:**

| Prüfung | Erwartung | Nachweis |
| --- | --- | --- |
| `claude --version` | Version mit „(Claude Code)“ | `host`/`tool_check` |
| `claude doctor` | keine Fehler bei Installation und Einstellungen | `host`/`tool_check` |
| `/status` (tippt der Nutzer) | richtiges Konto angemeldet | `account`/`user_confirmation` |
| nur Desktop-App: Code-Bereich zeigt den Projektordner | – | `user_confirmation`, nach `handover` per Befehl bestätigt |

Läufst du schon als Claude Code auf dem Computer, prüfe direkt (Befehl ausführen); keine Installationsanleitung zeigen. Ist `claude` nicht im Suchpfad, obwohl die Sitzung läuft (zum Beispiel aus der Desktop-App), ist die laufende Sitzung selbst der Nachweis; die Version nennt der Nutzer aus `/status` oder der App. Dann keine zusätzliche CLI installieren.

## Schritt `handover`: vom Chat in Claude Code wechseln

1. Der Nutzer legt einen Ordner an, zum Beispiel `ai-bootstrap` im Benutzerordner (Windows: im WSL-Benutzerordner `~/ai-bootstrap`), entpackt dort `AI-Bootstrap-<version>.zip` (es entsteht der Ordner `AI-Bootstrap-<version>`) und legt `ai-bootstrap-stand.json` in diesen Ordner. Gibt es noch keinen gespeicherten Stand, entfällt die Datei.
2. Er öffnet den Ordner `AI-Bootstrap-<version>` in Claude Code (Desktop-App: Ordner im Code-Bereich wählen; CLI: `cd ~/ai-bootstrap/AI-Bootstrap-<version>` und `claude`).
3. Erste Nachricht: „Lies START_HIER.md und setze die Einrichtung mit ai-bootstrap-stand.json fort.“
4. Claude Code prüft den Stand nach `ENTRY.md` §7.3 und macht am ersten offenen Schritt weiter.

## Anweisungsdateien

Claude Code liest `CLAUDE.md` (Projekt: `./CLAUDE.md` oder `./.claude/CLAUDE.md`; persönlich: `~/.claude/CLAUDE.md`). Ab v2.1.277 liest es `AGENTS.md` direkt, **wenn kein `CLAUDE.md` existiert** (A11). Gibt es beide, muss `CLAUDE.md` die Zeile `@AGENTS.md` enthalten, damit die Projektregeln nicht verloren gehen; unter Windows Import statt Symlink. Prüfe das im Schritt `project` und ergänze den Import, statt Regeln zu kopieren. Ist `AGENTS.md` die maßgebliche Regeldatei, bleibt sie es.

## Schritt `skills`: Fähigkeiten

| Manifest-Fähigkeit | Umsetzung |
| --- | --- |
| Brainstorming, Planung, systematische Fehlersuche, Testen/Verifikation, Git-Isolation, Abschluss | Plugin **Superpowers** (S1) |
| Recherche/Audit | eingebaute Websuche |
| Repository-Anweisungen | eingebautes `CLAUDE.md`/`AGENTS.md`-Lesen (A11) |
| Merge-/Release-Gate | `templates/devbox_merge_gate.py` (nur nach Projektentscheidung) |

1. **Prüfen:** `claude plugin list` selbst ausführen (ist `claude` nicht im Suchpfad, weiter mit dem Probeaufruf in Schritt 3). Ist `superpowers` installiert und aktiv, weiter mit dem Probeaufruf. Gleichwertige vorhandene Skills (`~/.claude/skills`, `.claude/skills`, A12) behalten, nichts doppelt installieren.
2. **Installieren (falls nötig):** `claude plugin install superpowers@claude-plugins-official` selbst ausführen (Kommandozeile; der offizielle Marktplatz wird bei der ersten interaktiven Sitzung automatisch eingetragen). Alternativ tippt der Nutzer `/plugin install superpowers@claude-plugins-official`. Danach eine neue Sitzung (oder der Nutzer tippt `/reload-plugins`).
3. **Probeaufruf:** In der neuen Sitzung prüfst du deine eigene Liste verfügbarer Skills; sie muss `superpowers:brainstorming` enthalten. Kannst du sie nicht einsehen, tippt der Nutzer `/skills` und nennt dir das Ergebnis. Nur die tatsächliche Liste in der laufenden Sitzung zählt.

Superpowers stammt von Jesse Vincent (obra) und trägt im Plugin-Verzeichnis kein „Anthropic verified“-Kennzeichen (S3). Nenne das in einem Satz, wenn der Nutzer nach der Herkunft fragt.

## Schritt `permissions`: Berechtigungsprofil

Erkläre kurz: Der **Berechtigungsmodus** legt fest, wann Claude Code vor Änderungen und Befehlen fragt. Die **Sandbox** begrenzt zusätzlich, worauf Befehle zugreifen dürfen und welche Internetadressen sie erreichen (A9, A10).

Frage 1 von 1: Welches Berechtigungsprofil soll Claude Code bekommen?

| Profil | Einstellung in `~/.claude/settings.json` | Wirkung |
| --- | --- | --- |
| Vorsichtig | `"permissions": {"defaultMode": "default"}` | fragt vor jeder Dateiänderung und jedem Befehl |
| **Standard (Empfehlung)** | `"defaultMode": "acceptEdits"`, `"sandbox": {"enabled": true}` (macOS, Linux, WSL2) und Sperrregeln (unten) | ändert Dateien im Projekt selbst; Befehle laufen in der Sandbox; heikle Git-Befehle gesperrt |
| Selbstständig | `"defaultMode": "auto"` plus Sandbox und Sperrregeln | Claude Code entscheidet mit eingebauter Sicherheitsprüfung selbst; nur wenn der Nutzer weniger Rückfragen will |

Empfehlung: Standard, weil Claude Code damit flüssig im Projekt arbeitet, Befehle aber im Schutzrahmen bleiben und Push auf main, Force-Push und Merge technisch gesperrt sind.

Sperrregeln (deny) für Standard und Selbstständig:

```json
"deny": ["Bash(git push --force*)", "Bash(git push -f*)", "Bash(git push * main*)", "Bash(git push origin HEAD:main*)", "Bash(gh pr merge*)"]
```

- `defaultMode` immer ausdrücklich setzen: Ab v2.1.283 startet das Terminal sonst im Modus `auto` (A9).
- `auto` wirkt nur aus `~/.claude/settings.json`, nicht aus Projekteinstellungen (A9).
- `bypassPermissions` nicht anbieten; laut Anthropic nur für isolierte Container oder VMs (A9).
- **Linux und WSL2:** Die Sandbox braucht `bubblewrap` und `socat` (A10). Gehört zum Profil Standard bzw. Selbstständig: `command -v bwrap socat` prüfen; fehlt etwas, `sudo apt-get install -y bubblewrap socat`. Danach selbst prüfen: `bwrap --ro-bind / / --unshare-user --unshare-net true` muss mit Exit 0 enden.
- Endet diese Prüfung mit `Operation not permitted` oder `setting up uid map: Permission denied`, blockiert unter Ubuntu 24.04 die AppArmor-Sperre für Benutzer-Namensräume `bwrap`. Abhilfe (wie beim Codex-Weg, C15; in einer frischen Ubuntu-24.04-VM geprüft): `sudo apt install apparmor-profiles`, `sudo install -m 0644 /usr/share/apparmor/extra-profiles/bwrap-userns-restrict /etc/apparmor.d/bwrap-userns-restrict`, `sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict`, dann erneut prüfen. Die systemweite Abschaltung der Sperre bietest du nicht an.
- Geänderte Einstellungen gelten ab der nächsten Claude-Code-Sitzung. Abschließend tippt der Nutzer in einer neuen Sitzung `/sandbox` und nennt dir den angezeigten Zustand.
- Bestehende Einstellungen vorlesen, nur Abweichungen ansprechen, andere Einträge erhalten. Datei nur nach der Antwort ändern.
- Prüfung: `~/.claude/settings.json` lesen; den Nutzer `/permissions` bzw. `/sandbox` eintippen lassen; wirksamen Modus nennen.
- Die Sperrregeln sind eine zusätzliche Sicherung. Die Befugnisgrenzen selbst stehen in den Projektregeln.

## Schritt `chat_github`: Claude-Chat liest das Repository (optional)

Nur wenn der Nutzer im Claude-Chat planen möchte. Im Chat über „+“ → „Add from GitHub“, im Projekt über das Projektwissen → „+“ → GitHub (A15). Synchronisiert werden Dateien eines Branches, keine Commits oder Pull Requests; Projekte haben einen „Sync“-Knopf. **Nachweis:** Der Chat liest eine konkrete Datei (zum Beispiel `README.md`) und nennt ihre erste Überschrift. Schreiben bleibt Aufgabe von Claude Code.

## Prüfübersicht je Betriebssystem

| Schritt | macOS | Windows (WSL2) | Linux |
| --- | --- | --- | --- |
| `local_agent` | `claude --version`, `claude doctor`, `/status` (App: Code-Bereich) | im WSL-Terminal dieselben Befehle | dieselben Befehle |
| `skills` | `claude plugin list`, `/skills` | in der WSL-Sitzung | wie macOS |
| `permissions` | `~/.claude/settings.json`, `/sandbox` (Seatbelt eingebaut) | `~/.claude/settings.json` in WSL, `/sandbox` (bubblewrap) | wie WSL |
| alle anderen | `../platforms/macos.md` | `../platforms/windows.md` | `../platforms/linux.md` |

<!-- END onboarding/providers/claude-code.md -->

<!-- BEGIN onboarding/platforms/macos.md -->

## Datei: `onboarding/platforms/macos.md`

# Betriebssystem: macOS

Gilt zusammen mit `../ENTRY.md` und der Anbieterdatei. Quellen: Quellenmatrix O1, O4–O7, O10, O11.

## Terminal

Das **Terminal** ist ein Fenster, in dem man Befehle eintippt. Öffnen: Spotlight (Cmd + Leertaste), „Terminal“ eingeben, Enter. Erkläre das erst, wenn ein Schritt tatsächlich einen Befehl braucht. Im lokalen Agenten führst du die Befehle selbst aus.

## Schritt `git`

- Prüfen: `git --version`.
- Fehlt Git: `xcode-select --install` und den Dialog bestätigen (Apple liefert Git mit den Command Line Tools, O1). Ist Homebrew schon vorhanden, geht auch `brew install git`. Homebrew nicht nur dafür installieren.
- Erneut prüfen.

## Schritt `github_account`

Siehe `linux.md` – identisch auf allen Systemen.

## Schritt `github_cli`

- Prüfen: `gh --version`, dann `gh auth status`.
- Fehlt `gh`: Ist Homebrew vorhanden (`brew --version`), `brew install gh` (O5). Ohne Homebrew: Den Nutzer fragen, ob Homebrew installiert werden soll (Befehl von https://brew.sh/, O11), oder alternativ das macOS-Paket von https://github.com/cli/cli/releases installieren. Frage-Format verwenden; Empfehlung Homebrew, weil Updates dann einfach sind.
- Anmelden: `gh auth login` → GitHub.com → HTTPS → im Browser anmelden. Danach `gh auth setup-git`, damit Git die Anmeldung von `gh` nutzt (O5). Arbeitet Git bereits über SSH mit diesem Konto, ist das nicht nötig.
- Nachweis: `gh auth status` zeigt das Konto als angemeldet.

## Schritt `git_identity`

Siehe `linux.md` – identisch auf allen Systemen.

## Schritt `python`

- Prüfen: `python3 --version` muss 3.12 oder neuer zeigen.
- Fehlt es oder ist es älter: Installer von https://www.python.org/downloads/macos/ (Administratorkonto nötig), danach „Install Certificates.command“ im Programmordner von Python ausführen (O7). Das Systempython unter `/usr/bin/python3` nicht verändern.
- Nachweis: `python3 --version` in einem neuen Terminalfenster.

## Gate

Das lokale Merge-Gate läuft auf macOS nativ (`DEVBOX_GATE_POLICY.md` §10). In der Gate-Konfiguration muss `systemd_scope = false` und `watched_user_services = []` stehen; sonst stoppt das Gate mit `PRECONDITION`. Ob ein Projekt das Gate übernimmt, ist eine Projektentscheidung (Schritt `project`).

## Speicherort des Einrichtungsstands

`~/.ai-bootstrap/stand.json` (`mkdir -p ~/.ai-bootstrap`).

<!-- END onboarding/platforms/macos.md -->

<!-- BEGIN onboarding/platforms/windows.md -->

## Datei: `onboarding/platforms/windows.md`

# Betriebssystem: Windows

Gilt zusammen mit `../ENTRY.md` und der Anbieterdatei. Quellen: Quellenmatrix O2, O5, O7, O8 sowie C3, A5, A10.

## Grundentscheidung: Arbeiten in WSL2

Auf Windows läuft die Arbeitsumgebung in **WSL2**. Erkläre beim ersten Bedarf in einem Satz: „WSL2 ist eine von Microsoft mitgelieferte Linux-Umgebung, die direkt in Windows läuft; dort arbeiten Agent, Git und Prüfwerkzeuge zuverlässig zusammen.“

Gründe (nicht ungefragt aufzählen): Das lokale Merge-Gate braucht Linux-/POSIX-Funktionen und stoppt unter nativem Windows (`DEVBOX_GATE_POLICY.md` §10); Claude Code hat unter nativem Windows keine Sandbox (A10); Codex unterstützt WSL2 offiziell (C3). Ab dem Schritt `wsl` gilt `linux.md` innerhalb der WSL-Umgebung.

## Terminal

- **PowerShell** (für die Einrichtung von WSL): Startmenü, „PowerShell“ eingeben. Für `wsl --install` mit Rechtsklick „Als Administrator ausführen“.
- **WSL-Terminal** (danach für alles andere): Startmenü, „Ubuntu“ öffnen.

## Schritt `wsl`

- Prüfen: In PowerShell `wsl -l -v`. Erfüllt, wenn eine Distribution mit `VERSION 2` erscheint. In ihr `uname -a` ausführen.
- Fehlt WSL: In einer **Administrator**-PowerShell `wsl --install`, danach Windows neu starten (O8). Voraussetzung: Windows 10 ab Version 2004 (Build 19041) oder Windows 11. Standard ist Ubuntu.
- Nach dem Neustart öffnet sich Ubuntu und fragt nach einem Linux-Benutzernamen und Passwort. Der Nutzer wählt beides selbst; das Passwort wird bei `sudo` gebraucht und nie in den Chat geschrieben.
- Projekte und der Einrichtungsordner liegen im Linux-Dateisystem (`/home/<name>/…`), nicht unter `/mnt/c/…` (O8). Von Windows aus sind sie unter `\\wsl$` erreichbar.
- Nachweis: `wsl -l -v` mit Version 2 und `uname -a` aus WSL.

Läufst du bereits als lokaler Agent in WSL (zum Beispiel Codex mit WSL2-Agent oder Claude Code im WSL-Terminal), prüfe direkt mit `uname -a` und `cat /etc/os-release`.

## Lokaler Agent unter Windows

- **ChatGPT/Codex:** Desktop-App unter Windows installieren, in den Einstellungen den Agenten auf WSL2 umstellen, App neu starten; oder Codex CLI im WSL-Terminal (siehe Anbieterdatei).
- **Claude/Claude Code:** Claude Code CLI im WSL-Terminal mit dem Linux-Befehl installieren (siehe Anbieterdatei).

Der Ordner aus dem Schritt `handover` liegt in WSL, zum Beispiel `~/ai-bootstrap`. Die heruntergeladenen Dateien aus dem Windows-Ordner „Downloads“ kopierst du im WSL-Terminal mit `cp /mnt/c/Users/<Windows-Name>/Downloads/AI-Bootstrap-*.zip ~/ai-bootstrap/` (den Namen mit `ls /mnt/c/Users/` feststellen) und entpackst mit `python3 -m zipfile -e ~/ai-bootstrap/AI-Bootstrap-<version>.zip ~/ai-bootstrap/` (kein `unzip` nötig).

## Alle weiteren Schritte

`git`, `github_account`, `github_cli`, `git_identity` und `python` laufen **in WSL** genau wie in `linux.md` beschrieben. Git for Windows ist auf diesem Weg nicht nötig.

## Gate

Das Merge-Gate läuft nur in WSL2, dort unverändert wie unter Linux (`DEVBOX_GATE_POLICY.md` §10). Unter nativem Windows gestartet, stoppt es mit `PRECONDITION` und nennt WSL 2.

## Speicherort des Einrichtungsstands

In WSL: `~/.ai-bootstrap/stand.json`.

<!-- END onboarding/platforms/windows.md -->

<!-- BEGIN onboarding/platforms/linux.md -->

## Datei: `onboarding/platforms/linux.md`

# Betriebssystem: Linux

Gilt zusammen mit `../ENTRY.md` und der Anbieterdatei. Diese Datei gilt auch **innerhalb von WSL2 unter Windows**. Quellen: Quellenmatrix O3–O8.

Beschrieben sind Ubuntu/Debian (apt) und Fedora (dnf). Bei einer anderen Distribution die Paketverwaltung mit `cat /etc/os-release` feststellen und die offizielle Anleitung der genannten Quelle verwenden.

## Terminal

Das **Terminal** ist ein Fenster, in dem man Befehle eintippt; unter Ubuntu mit Strg + Alt + T. Erkläre das erst bei Bedarf. Im lokalen Agenten führst du die Befehle selbst aus. Befehle mit `sudo` fragen nach dem Passwort des Nutzers; das tippt er selbst ins Terminal, nie in den Chat.

## Schritt `git`

- Prüfen: `git --version`.
- Fehlt Git: Ubuntu/Debian `sudo apt-get update && sudo apt-get install -y git`; Fedora `sudo dnf install -y git` (O3).

## Schritt `github_account`

- Frage nur, ob ein GitHub-Konto vorhanden ist. Wenn nein: Der Nutzer legt es selbst unter https://github.com/signup an (O6). Du legst kein Konto an.
- Empfiehl, die Zwei-Faktor-Anmeldung gleich einzurichten (Authenticator-App); GitHub verlangt sie für Konten, die Code beitragen (O6).
- Empfiehl in den GitHub-Einstellungen unter „Emails“ die Option „Keep my email addresses private“ (wichtig für `git_identity`, O4).
- Nachweis zunächst `account`/`user_confirmation`; tatsächlich bestätigt durch `gh auth status` im nächsten Schritt.

## Schritt `github_cli`

- Prüfen: `gh --version`, `gh auth status`.
- Fehlt `gh`:
  - Ubuntu/Debian: offizielle Paketquelle laut https://github.com/cli/cli/blob/trunk/docs/install_linux.md (O5). Den Befehlsblock von dort unverändert verwenden; er richtet den Schlüssel unter `/etc/apt/keyrings/` und die Quelle `https://cli.github.com/packages` ein und installiert `gh`.
  - Fedora: `sudo dnf install dnf5-plugins`, `sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo`, `sudo dnf install gh` (O5).
- Anmelden: `gh auth login` → GitHub.com → HTTPS → Browser. Ohne Browser (zum Beispiel per SSH) zeigt `gh` einen Code, den der Nutzer auf github.com/login/device eingibt. Danach `gh auth setup-git` (O5).
- Ist `gh` schon angemeldet und arbeitet Git bereits über SSH (`gh auth status` nennt „Git operations protocol: ssh“ und `ssh -T git@github.com` begrüßt das Konto), ist `gh auth setup-git` nicht nötig; nichts ändern.
- Nachweis: `gh auth status` zeigt das Konto angemeldet.

## Schritt `git_identity`

- Prüfen: `git config --global user.name` und `git config --global user.email`.
- Fehlt etwas: Name nach Wunsch des Nutzers; als E-Mail die private GitHub-Adresse der Form `ID+NUTZERNAME@users.noreply.github.com` (O4). Die genaue Adresse steht in den GitHub-Einstellungen unter „Emails“; mit angemeldetem `gh` kannst du sie aus `gh api user --jq '.id, .login'` zusammensetzen. Frage, welchen Namen der Nutzer zeigen möchte; setze dann `git config --global user.name "…"` und `git config --global user.email "…"`.
- Bestehende Werte nicht überschreiben; nur ansprechen, wenn sie sichtbar falsch sind (zum Beispiel leer).
- Nachweis: beide Werte gelesen.

## Schritt `python`

- Prüfen: `python3 --version` (3.12 oder neuer).
- Ubuntu 24.04 bringt Python 3.12 mit; Ubuntu 22.04 hat 3.10 (O7). Ist die Version zu alt, nenne das konkret und schlage die Installation über die Paketverwaltung der Distribution oder ein Upgrade auf eine aktuelle LTS-Version vor; der Nutzer entscheidet.
- Nachweis: Ausgabe von `python3 --version`.

## Gate

Linux ist der Referenzweg des Merge-Gates (`DEVBOX_GATE_POLICY.md` §10). `systemd_scope = true` funktioniert nur, wenn ein systemd-Benutzerdienst läuft (`systemctl --user is-system-running`).

## Paket entpacken

Frisches Ubuntu hat oft kein `unzip`. Entpacken geht ohne Installation mit `python3 -m zipfile -e <zip> <zielordner>`.

## Speicherort des Einrichtungsstands

`~/.ai-bootstrap/stand.json` (`mkdir -p ~/.ai-bootstrap`).

<!-- END onboarding/platforms/linux.md -->

<!-- BEGIN onboarding/OPTIONAL_DEVBOX.md -->

## Datei: `onboarding/OPTIONAL_DEVBOX.md`

# Optional: zusätzliche Entwicklungsmaschine (Dev-Box)

Nur verwenden, wenn der Nutzer ausdrücklich eine zweite, dauerhaft laufende Maschine nutzen möchte (zum Beispiel einen eigenen Linux-Rechner oder einen gemieteten Server). Der eigene Computer bleibt der Standard; zeige diesen Weg nicht ungefragt.

Eine Dev-Box im Sinne von `DEVBOX_GATE_POLICY.md` ist jede bewusst betriebene Entwicklungsmaschine – auch der eigene Computer. Ein zusätzlicher Server ist nie Voraussetzung.

## Wann sinnvoll

- Der Nutzer möchte Prüfungen oder das Merge-Gate laufen lassen, während sein Laptop zu ist.
- Fremder Code soll in einer getrennten, isolierten Umgebung geprüft werden (`DEVBOX_GATE_POLICY.md` §5).

## Ablauf

1. **Entscheidung:** Kosten, Anbieter und Zugang wählt der Nutzer selbst. Du mietest, kaufst oder registrierst nichts.
2. **Zugang:** Der Nutzer richtet die Anmeldung (zum Beispiel SSH-Schlüssel) selbst ein. Private Schlüssel bleiben auf seinem Gerät und kommen nie in den Chat oder in den Einrichtungsstand.
3. **Einrichtung auf der Dev-Box:** Die Schritte `git`, `github_cli`, `git_identity`, `python` laufen dort nach `platforms/linux.md`, im lokalen Agenten, der auf der Dev-Box arbeitet (Codex CLI oder Claude Code CLI über SSH).
4. **Trennung:** Hat die Dev-Box Zugriff auf Projekte, Deployments oder Anbieterkonten, darf dort kein fremder Code laufen. Für fremden Code eine eigene, unprivilegierte Umgebung nach `DEVBOX_GATE_POLICY.md` §5.
5. **Nachweis:** Dieselben Prüfungen wie auf dem eigenen Computer, mit `context` = Name der Dev-Box im Einrichtungsstand.

Der Einrichtungsstand hält die Dev-Box als eigenen Kontext fest; Nachweise vom eigenen Computer gelten dort nicht.

<!-- END onboarding/OPTIONAL_DEVBOX.md -->

<!-- BEGIN onboarding/STATE.schema.json -->

## Datei: `onboarding/STATE.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/robin-shiels/ai-project-bootstrap/onboarding/STATE.schema.json",
  "title": "AI Bootstrap Einrichtungsstand",
  "description": "Portabler, geheimnisfreier Stand der persoenlichen Ersteinrichtung. Dieses Dokument beschreibt das Format. Die tatsaechliche Pruefung macht scripts/onboarding_state.py (oder die KI anhand von ENTRY.md, solange Python fehlt).",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "bundle_version",
    "provider_path",
    "platform",
    "current_step",
    "decisions",
    "verifications",
    "blockers",
    "next_action"
  ],
  "properties": {
    "schema_version": { "const": 1 },
    "bundle_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "provider_path": { "enum": ["chatgpt-codex", "claude-code", "unknown"] },
    "platform": { "enum": ["macos", "windows", "linux", "unknown"] },
    "current_step": { "$ref": "#/$defs/step" },
    "decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "answer", "source", "decided_at"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z][a-z0-9_]*$" },
          "answer": { "type": "string", "minLength": 1, "maxLength": 300 },
          "source": { "enum": ["user_choice", "user_own_answer", "default_after_notice"] },
          "decided_at": { "$ref": "#/$defs/date" }
        }
      }
    },
    "verifications": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["step", "checked_at", "scope", "source", "context", "result", "detail"],
        "properties": {
          "step": { "$ref": "#/$defs/step" },
          "checked_at": { "$ref": "#/$defs/date" },
          "scope": { "enum": ["account", "chat_access", "host", "repository", "project"] },
          "source": { "enum": ["tool_check", "user_confirmation"] },
          "context": { "type": "string", "minLength": 1, "maxLength": 120 },
          "result": { "enum": ["ok", "failed"] },
          "detail": { "type": "string", "maxLength": 300 }
        }
      }
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["step", "description", "since"],
        "properties": {
          "step": { "$ref": "#/$defs/step" },
          "description": { "type": "string", "minLength": 1, "maxLength": 300 },
          "since": { "$ref": "#/$defs/date" }
        }
      }
    },
    "next_action": { "type": "string", "minLength": 1, "maxLength": 300 }
  },
  "$defs": {
    "date": {
      "type": "string",
      "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}(:[0-9]{2})?(Z|[+-][0-9]{2}:[0-9]{2})?)?$"
    },
    "step": {
      "enum": [
        "start",
        "context",
        "path",
        "save_state",
        "local_agent",
        "handover",
        "wsl",
        "git",
        "github_account",
        "github_cli",
        "git_identity",
        "chat_github",
        "python",
        "skills",
        "permissions",
        "project",
        "trial",
        "done",
        "devbox"
      ]
    }
  }
}
```

<!-- END onboarding/STATE.schema.json -->
