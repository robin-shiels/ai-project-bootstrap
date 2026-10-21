# Betriebssystem: Linux

Gilt auch innerhalb von WSL 2 unter Windows. Quellen: Quellenmatrix O3–O8. Beschrieben sind Ubuntu/Debian (apt) und Fedora (dnf); bei anderen Distributionen die Paketverwaltung mit `cat /etc/os-release` feststellen und die offizielle Anleitung verwenden.

Befehle mit `sudo` fragen nach dem Passwort des Nutzers. Das tippt er selbst ins Terminal, nie in den Chat.

## Schritt `start`

`uname -a`, `cat /etc/os-release`, `git --version`, `gh --version`, `gh auth status`.

## Schritt `github`

- **Git:** Ubuntu/Debian `sudo apt-get update && sudo apt-get install -y git`; Fedora `sudo dnf install -y git` (O3).
- **GitHub CLI:**
  - Ubuntu/Debian: offizielle Paketquelle laut https://github.com/cli/cli/blob/trunk/docs/install_linux.md (O5), Befehlsblock von dort unverändert.
  - Fedora: `sudo dnf install dnf5-plugins`, `sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo`, `sudo dnf install gh` (O5).
- **Anmelden:** `gh auth login` → GitHub.com → HTTPS → Browser. Ohne Browser zeigt `gh` einen Code für github.com/login/device. Danach `gh auth setup-git`. Arbeitet Git schon über SSH mit diesem Konto (`gh auth status` nennt „Git operations protocol: ssh“, `ssh -T git@github.com` begrüßt das Konto), ist das nicht nötig.

## Gate (nur bei Projektregel GATE)

- Python 3.12+: `python3 --version`. Ubuntu 24.04 bringt 3.12 mit, Ubuntu 22.04 nur 3.10 (O7); dann Upgrade über die Paketverwaltung oder eine aktuelle LTS-Version vorschlagen.
- Linux ist der Referenzweg des Merge-Gates (`DEVBOX_GATE_POLICY.md` §10). `systemd_scope = true` braucht einen laufenden systemd-Benutzerdienst (`systemctl --user is-system-running`).

## Paket entpacken (nur Offline-Weg)

Ohne `unzip`: `python3 -m zipfile -e <zip> <zielordner>`.
