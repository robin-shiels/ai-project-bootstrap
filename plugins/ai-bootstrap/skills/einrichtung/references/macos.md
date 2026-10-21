# Betriebssystem: macOS

Quellen: Quellenmatrix O1, O5, O7, O11.

## Schritt `start`

`sw_vers`, `git --version`, `gh --version`, `gh auth status`. Fehlt Git, erscheint beim ersten `git`-Aufruf ein Apple-Dialog; das ist kein Fehler.

## Schritt `github`

- **Git:** `xcode-select --install` und den Dialog bestätigen (Command Line Tools, O1). Ist Homebrew schon vorhanden, geht auch `brew install git`. Homebrew nicht nur dafür installieren.
- **GitHub CLI:** Ist Homebrew vorhanden (`brew --version`): `brew install gh` (O5). Ohne Homebrew eine Frage im Frageformat: Homebrew installieren (Befehl von https://brew.sh/, O11; Empfehlung, weil Updates dann einfach sind) oder das macOS-Paket von https://github.com/cli/cli/releases.
- **Anmelden:** `gh auth login` → GitHub.com → HTTPS → Browser, danach `gh auth setup-git` (außer Git arbeitet schon über SSH mit diesem Konto).

## Gate (nur bei Projektregel GATE)

- Python 3.12+: `python3 --version`. Sonst Installer von https://www.python.org/downloads/macos/, danach „Install Certificates.command“ ausführen (O7). Das Systempython nicht verändern.
- Das Merge-Gate läuft auf macOS nativ; in der Gate-Konfiguration `systemd_scope = false` und `watched_user_services = []` (`DEVBOX_GATE_POLICY.md` §10).
