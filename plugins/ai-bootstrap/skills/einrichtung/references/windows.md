# Betriebssystem: Windows

Quellen: Quellenmatrix O2, O5, O8, V9, V10. Standard ist **nativ unter Windows**, so wie die Desktop-App läuft. WSL 2 brauchst du nur, wenn ein Projekt die Merge-Regel GATE wählt.

## Schritt `start`

In PowerShell: `[System.Environment]::OSVersion.Version`, `git --version`, `gh --version`, `gh auth status`, `winget --version`. Claude Code nutzt für sein Bash-Werkzeug Git Bash aus Git for Windows; ohne Git for Windows arbeitet es mit PowerShell (V9).

## Schritt `github`

- **Git for Windows:** `winget install --id Git.Git -e --source winget` (O2). Danach ein neues Terminal bzw. eine neue Sitzung, damit `git` im Suchpfad ist. Findet Claude Code Git Bash danach nicht, die Umgebungsvariable `CLAUDE_CODE_GIT_BASH_PATH` auf `C:\Program Files\Git\bin\bash.exe` setzen (V9).
- **GitHub CLI:** `winget install --id GitHub.cli -e --source winget` (O5), dann neues Terminal.
- **Anmelden:** `gh auth login` → GitHub.com → HTTPS → Browser, danach `gh auth setup-git`.
- Fehlt `winget`: Der Nutzer installiert „App Installer“ aus dem Microsoft Store; alternativ die Installer von https://git-scm.com/download/win und https://cli.github.com/.

## Hinweise

- Pfade mit Leerzeichen in Anführungszeichen setzen.
- Der Einrichtungsstand liegt unter `%USERPROFILE%\.ai-bootstrap\stand.json`, persönliche Skills für Codex unter `%USERPROFILE%\.agents\skills`.
- Claude Code hat unter nativem Windows keine Sandbox (V9). Codex hat eine eigene Windows-Sandbox (V10).

## Gate (nur bei Projektregel GATE)

Das Merge-Gate läuft nur in WSL 2, dort wie unter Linux (`DEVBOX_GATE_POLICY.md` §10); unter nativem Windows stoppt es mit `PRECONDITION`.

1. Prüfen: `wsl -l -v` zeigt eine Distribution mit `VERSION 2`.
2. Fehlt WSL: in einer **Administrator**-PowerShell `wsl --install`, dann Windows neu starten (O8). Voraussetzung: Windows 10 ab 2004 (Build 19041) oder Windows 11. Nach dem Neustart wählt der Nutzer in Ubuntu einen Linux-Benutzernamen und ein Passwort selbst.
3. In WSL gilt `linux.md` (Git, GitHub CLI, Python). Projekte für das Gate liegen im Linux-Dateisystem (`/home/<name>/…`), nicht unter `/mnt/c/…`.
