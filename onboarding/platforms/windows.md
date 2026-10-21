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
