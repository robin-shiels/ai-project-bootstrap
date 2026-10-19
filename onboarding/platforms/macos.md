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
- Anmelden: `gh auth login` → GitHub.com → HTTPS → im Browser anmelden. Danach `gh auth setup-git`, damit Git die Anmeldung von `gh` nutzt (O5).
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
