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

## Speicherort des Einrichtungsstands

`~/.ai-bootstrap/stand.json` (`mkdir -p ~/.ai-bootstrap`).
