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
