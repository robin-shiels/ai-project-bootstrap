# Anbieter: Claude mit Claude Code

Quellen: `docs/research/GUIDED_BOOTSTRAP_V1_SOURCE_MATRIX.md` (A1–A16, S1, S3, V1–V3, V8, V9). Bedienwege ändern sich; richte dich nach dem, was der Nutzer tatsächlich sieht.

## Voraussetzung

Claude Code braucht Pro, Max, Team oder Enterprise (oder ein Console-Konto mit API-Abrechnung); der kostenlose Plan enthält es nicht (A1, A3). Hat der Nutzer nur den kostenlosen Plan, sag das konkret. Über einen Wechsel entscheidet er selbst. Ist `ANTHROPIC_API_KEY` gesetzt, rechnet Claude Code über die API ab (A2); prüfe nur, ob die Variable gesetzt ist, gib den Wert nie aus, und erwähne es nur, wenn sie gesetzt ist.

Läufst du in der Desktop-App (Bereich Code), ist `claude` oft nicht im Suchpfad. Die laufende Sitzung ist dann der Nachweis; installiere keine zusätzliche Kommandozeile nur dafür. Plugin-Befehle tippt in diesem Fall der Nutzer als Slash-Befehl.

## Schritt `skills`

| Fähigkeit | Umsetzung |
| --- | --- |
| Brainstorming, Planung, Fehlersuche, Testen, Git-Isolation | Plugin **Superpowers** (S1) |
| Einrichtung, Projektstart, Arbeitsweise | Plugin **ai-bootstrap** aus `robin-shiels/ai-project-bootstrap` (V1, V2) |

1. **Prüfen:** `claude plugin list` (wenn `claude` verfügbar), sonst deine eigene Skill-Liste. Gesucht: `superpowers` und `ai-bootstrap`.
2. **Installieren (falls nötig):**
   - `claude plugin install superpowers@claude-plugins-official`
   - `claude plugin marketplace add robin-shiels/ai-project-bootstrap` und `claude plugin install ai-bootstrap@ai-bootstrap`
   - Ohne `claude` im Suchpfad tippt der Nutzer: `/plugin install superpowers@claude-plugins-official`, `/plugin marketplace add robin-shiels/ai-project-bootstrap`, `/plugin install ai-bootstrap@ai-bootstrap`.
3. **Wirksam** ab der nächsten Sitzung oder nach `/reload-plugins` (tippt der Nutzer).
4. **Probeaufruf:** Deine Skill-Liste enthält `superpowers:brainstorming` und `ai-bootstrap:arbeitsweise`. Kannst du sie nicht einsehen, tippt der Nutzer `/skills` und nennt das Ergebnis.

Superpowers stammt von Jesse Vincent (obra) und trägt kein „Anthropic verified“-Kennzeichen (S3). ai-bootstrap stammt aus diesem öffentlichen Repository. Nenne das in einem Satz, wenn der Nutzer nach der Herkunft fragt.

## Schritt `arbeitsweise`: Regeldatei

Persönliche Regeln: `~/.claude/CLAUDE.md` (A11). Projektregeln gehören ins Projekt, nicht hierher.

## Schritt `arbeitsweise`: Berechtigungsprofil

Erkläre kurz: Der **Berechtigungsmodus** legt fest, wann Claude Code vor Änderungen und Befehlen fragt. **Erlaubt- und Sperrregeln** legen fest, welche Befehle ohne Rückfrage laufen und welche nie. Die **Sandbox** begrenzt zusätzlich, worauf Befehle zugreifen dürfen (A9, A10).

```text
Frage 1 von 1: Wie selbstständig soll Claude Code arbeiten?

1. Vorsichtig – fragt vor jeder Dateiänderung und jedem Befehl
2. Standard – ändert Dateien im Projekt selbst, Branch, Commit, Push, Pull Request und Merge nach Projektregel ohne Rückfrage, gefährliche Befehle gesperrt
3. Selbstständig – wie Standard, entscheidet zusätzlich selbst mit eingebauter Sicherheitsprüfung über weitere Befehle

Empfehlung: Standard, weil der Ablauf bis zum Merge flüssig läuft und Gefährliches trotzdem gesperrt bleibt.
Du kannst auch eine eigene Antwort schreiben.
```

Einstellungen in `~/.claude/settings.json` (vorhandene Einträge behalten, nur diese Schlüssel setzen bzw. Listen ergänzen):

| Profil | `permissions.defaultMode` | Sandbox |
| --- | --- | --- |
| Vorsichtig | `"default"` | wie vorhanden |
| **Standard** | `"acceptEdits"` | `"sandbox": {"enabled": true}` auf macOS, Linux, WSL2 |
| Selbstständig | `"auto"` | wie Standard |

Erlaubt (Standard und Selbstständig), damit der Ablauf ohne Rückfrage läuft:

```json
"allow": [
  "Bash(git status*)", "Bash(git diff*)", "Bash(git log*)", "Bash(git fetch*)",
  "Bash(git switch*)", "Bash(git add*)", "Bash(git commit*)", "Bash(git merge-base*)",
  "Bash(git push -u origin *)", "Bash(gh pr create *)", "Bash(gh pr view *)",
  "Bash(gh pr update-branch *)", "Bash(gh pr merge * --match-head-commit *)"
]
```

Gesperrt (alle Profile), gilt immer vor „erlaubt“ (V8):

```json
"deny": [
  "Bash(git push --force*)", "Bash(git push -f*)", "Bash(git push * --force*)",
  "Bash(git push * main*)", "Bash(git push origin HEAD:main*)",
  "Bash(gh pr merge * --admin*)"
]
```

- Deploy-Befehle werden nicht hier, sondern im Projekt erlaubt (`.claude/settings.json` des Projekts), sobald dort ein Deploy-Ziel festgelegt ist.
- `defaultMode` immer ausdrücklich setzen; ohne Angabe startet das Terminal ab v2.1.283 im Modus `auto` (A9). `auto` wirkt nur aus `~/.claude/settings.json`.
- `bypassPermissions` nicht anbieten (A9).
- **Windows nativ:** Die Sandbox gibt es dort nicht (V9). Sag das in einem Satz; Erlaubt- und Sperrregeln gelten trotzdem.
- **Linux und WSL2:** Die Sandbox braucht `bubblewrap` und `socat` (A10). `command -v bwrap socat`; fehlt etwas: `sudo apt-get install -y bubblewrap socat`. Prüfen: `bwrap --ro-bind / / --unshare-user --unshare-net true` endet mit Exit 0. Endet er unter Ubuntu 24.04 mit `Operation not permitted` oder `setting up uid map: Permission denied`: `sudo apt install apparmor-profiles`, `sudo install -m 0644 /usr/share/apparmor/extra-profiles/bwrap-userns-restrict /etc/apparmor.d/bwrap-userns-restrict`, `sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict`, dann erneut prüfen. Die systemweite Abschaltung der Sperre bietest du nicht an.
- Fragt die Sandbox beim ersten Zugriff auf `github.com` nach, erlaubt der Nutzer das einmal.
- Wirksam ab der nächsten Sitzung. Prüfung: Datei lesen; der Nutzer tippt in einer neuen Sitzung `/permissions` (und, wo vorhanden, `/sandbox`) und nennt den Zustand.

## Projekt in der App

Siehe Skill `projekt-start` §3 (V11).
