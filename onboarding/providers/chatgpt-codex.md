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
