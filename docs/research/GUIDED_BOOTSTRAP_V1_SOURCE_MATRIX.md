# Guided Bootstrap v1 – Quellenmatrix und technische Entscheidungen

Stand: 2026-10-19 · Teilauftrag GBOOT-01 · Basis: main `11d642bcfd8de138da81ac11d7e5fedcc9c0028d`

Alle Quellen wurden am 2026-10-19 abgerufen. „Gelesen“ heißt: Seite tatsächlich abgerufen und gelesen. „Suchtreffer“ heißt: nur Zusammenfassung eines Suchergebnisses, nicht als belegt behandelt. Anbieterfunktionen ändern sich schnell; die Anleitungen verweisen deshalb auf diese Seiten und lassen Modellnamen, Preise und Kontingentzahlen bewusst weg.

Die `developers.openai.com/codex/*`-Adressen leiten am Prüftag dauerhaft (308) auf `learn.chatgpt.com/docs/...` um; zitiert sind die Ziele. `help.openai.com` war für automatischen Abruf gesperrt (403); Aussagen, die nur dort stehen, sind als UNBELEGT markiert.

## 1. Anbieter: ChatGPT mit Codex

| # | Belegte Aussage | Quelle | Status | Grenzen |
| --- | --- | --- | --- | --- |
| C1 | Codex ist in ChatGPT Free, Go, Plus, Pro, Business, Edu und Enterprise enthalten; Free und Go nur für kleine Aufgaben, lokale und Cloud-Nutzung teilen ein Kontingent, Wochenlimits möglich. | https://learn.chatgpt.com/docs/pricing | gelesen | Zahlen sind Schätzungen; maßgeblich ist die Nutzungsanzeige. |
| C2 | Desktop-App („ChatGPT desktop app“, Bereich Codex; früher „Codex app“) für macOS und Windows über https://chatgpt.com/download/; Linux als Vorschau (Ubuntu 24.04/26.04, Debian 13, Fedora 43/44, Arch). | https://learn.chatgpt.com/docs/app, https://learn.chatgpt.com/docs/linux/linux-app | gelesen | Mindestversion macOS nicht angegeben; Intel-Mac-Unterstützung der App UNBELEGT. |
| C3 | Windows: App aus dem Microsoft Store oder `winget install --id 9PLM9XGG6VKS -s msstore`; der Agent kann nativ unter Windows oder in WSL2 laufen (Umschaltung in den Einstellungen, danach Neustart); WSL1 ab Codex 0.115 nicht unterstützt. | https://learn.chatgpt.com/docs/windows/windows-app, https://learn.chatgpt.com/docs/windows/wsl | gelesen | – |
| C4 | CLI-Installation: macOS/Linux `curl -fsSL https://chatgpt.com/codex/install.sh \| sh`; Windows `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 \| iex"`; alternativ `npm install -g @openai/codex` oder `brew install --cask codex`. | https://learn.chatgpt.com/docs/codex/cli.md, https://github.com/openai/codex | gelesen | – |
| C5 | Anmeldung: `codex login` (oder erster Start) mit „Sign in with ChatGPT“ im Browser; ohne Browser `codex login --device-auth` (muss in den ChatGPT-Sicherheitseinstellungen erlaubt sein); `codex login status` endet mit 0, wenn Anmeldedaten vorhanden sind. | https://learn.chatgpt.com/docs/auth, https://learn.chatgpt.com/docs/cli/reference.md | gelesen | Standard-Speicherort der Anmeldedaten nicht angegeben. |
| C6 | Sandbox-Modi `read-only`, `workspace-write` (Standard für lokale Arbeit), `danger-full-access`; Freigaberegeln `on-request`, `never` (+ granular); `untrusted` ist entfernt; Netzwerk in `workspace-write` standardmäßig aus. App/IDE: „Ask for approval“ (empfohlener Start), „Approve for me“, „Full access“, „Custom“. CLI: `/permissions`. | https://learn.chatgpt.com/docs/sandboxing, https://learn.chatgpt.com/docs/permission-modes, https://learn.chatgpt.com/docs/agent-approvals-security.md | gelesen | Standardwert von `approval_policy` nicht ausdrücklich genannt. |
| C7 | Sandbox-Technik: macOS Seatbelt, Linux/WSL2 bubblewrap, Windows eigene Sandbox (MXC empfohlen; `elevated`; `unelevated` schwächer). | https://learn.chatgpt.com/docs/sandboxing, https://learn.chatgpt.com/docs/windows/windows-sandbox | gelesen | – |
| C8 | Konfiguration `~/.codex/config.toml`; Projektdatei `.codex/config.toml` nur für vertrauenswürdige Projekte. | https://learn.chatgpt.com/docs/config-file/config-basic | gelesen | – |
| C9 | `AGENTS.md` wird vom Repository-Wurzelverzeichnis bis zum aktuellen Ordner gelesen, nähere Dateien haben Vorrang, gemeinsame Obergrenze 32 KiB (Standard). | https://learn.chatgpt.com/docs/agent-configuration/agents-md | gelesen | – |
| C10 | Skills: Ordner mit `SKILL.md`; Orte `.agents/skills` (Projekt), `$HOME/.agents/skills` (persönlich); `/skills` listet. Plugins bündeln Skills; CLI `/plugins` sowie `codex plugin add\|list\|remove`; App: Bereich Plugins. Nach Installation neue Sitzung starten. | https://learn.chatgpt.com/docs/build-skills, https://learn.chatgpt.com/docs/plugins | gelesen | – |
| C11 | `codex exec` läuft nicht interaktiv, standardmäßig mit `read-only`-Sandbox; `codex --version` zeigt die Version. | https://learn.chatgpt.com/docs/non-interactive-mode | gelesen | – |
| C12 | Codex Cloud arbeitet mit verbundenen GitHub-Repositories und kann Pull Requests öffnen. | https://learn.chatgpt.com/docs/cloud | gelesen | Planabdeckung von Cloud nicht angegeben. |
| C13 | ChatGPT-Chat: Upload von Dokumenten, PDF, Bildern, Tabellen und Datenexporten. `.md` und `.zip` nicht ausdrücklich genannt. | https://learn.chatgpt.com/docs/use-chatgpt.md | gelesen | `.md`-Upload, ZIP-Lesen und Plangrenzen UNBELEGT. |
| C15 | Linux/WSL2: `bubblewrap` mit der Paketverwaltung installieren (`sudo apt install bubblewrap`); ohne `bwrap` im Suchpfad nutzt Codex einen mitgelieferten Helfer, der unprivilegierte Benutzer-Namensräume braucht. Ubuntu 24.04: zusätzlich Profil `bwrap-userns-restrict` aus `apparmor-profiles` installieren und mit `apparmor_parser -r` laden; Ubuntu 25.04 bringt es mit. | https://learn.chatgpt.com/docs/sandboxing | gelesen | Fehlertext `RTM_NEWADDR` nicht genannt; Zuordnung durch eigenen Befund (Abschnitt 6). |
| C14 | ChatGPT-GitHub-Verbindung über Einstellungen → GitHub, nur lesend. | https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt | Suchtreffer | UNBELEGT; Menübezeichnungen schwanken. |

## 2. Anbieter: Claude mit Claude Code

| # | Belegte Aussage | Quelle | Status | Grenzen |
| --- | --- | --- | --- | --- |
| A1 | Claude Code braucht Pro, Max, Team, Enterprise oder ein Console-(API-)Konto; der kostenlose Plan enthält Claude Code nicht. | https://code.claude.com/docs/en/setup | gelesen | – |
| A2 | Pro/Max: Sitzungs- (5 h) und Wochenlimit, gemeinsam mit Claude-Chat; `/status` zeigt den Verbrauch; ein gesetztes `ANTHROPIC_API_KEY` rechnet über die API ab. | https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan | gelesen | – |
| A3 | Team: Claude Code in jedem Sitz; Enterprise je nach Sitztyp. | https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan | gelesen | – |
| A4 | Systemvoraussetzungen: macOS 13+, Windows 10 1809+, Ubuntu 20.04+/Debian 10+/Alpine 3.19+, 4 GB RAM, x64 oder ARM64. | https://code.claude.com/docs/en/setup | gelesen | – |
| A5 | Installation: macOS/Linux/WSL `curl -fsSL https://claude.ai/install.sh \| bash`; Windows PowerShell `irm https://claude.ai/install.ps1 \| iex`; alternativ `brew install --cask claude-code`, `winget install Anthropic.ClaudeCode`. Nur die native Installation aktualisiert sich selbst. Git for Windows optional (Git Bash), sonst PowerShell-Werkzeug. | https://code.claude.com/docs/en/setup | gelesen | – |
| A6 | Desktop-App mit Code-Bereich für macOS und Windows (x64, ARM64), bezahltes Abo nötig, enthält Claude Code. | https://code.claude.com/docs/en/overview | gelesen | – |
| A7 | Desktop-App für Linux als Beta: Ubuntu 22.04+ oder Debian 12+, `sudo apt install claude-desktop` aus dem Anthropic-Paketquellen. | https://code.claude.com/docs/en/desktop-linux | gelesen | Beta. |
| A8 | Anmeldung beim ersten `claude`-Start im Browser; `/login`, `/logout`, `/status`. Prüfung: `claude --version`, `claude doctor`. | https://code.claude.com/docs/en/authentication, https://code.claude.com/docs/en/setup | gelesen | – |
| A9 | Berechtigungsmodi `default` (Anzeige „Manual“), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` (nur für isolierte Container/VMs). Ab v2.1.283 ist `auto` Startmodus im Terminal und in VS Code. Regeln `permissions.allow/ask/deny` in `settings.json`, Reihenfolge deny → ask → allow; durchgesetzt von Claude Code, nicht vom Modell. | https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/permissions | gelesen | Versionsabhängig. |
| A10 | Sandbox standardmäßig aus; `/sandbox` oder `sandbox.enabled: true`; isoliert Dateisystem und Netzwerk für Shell-Befehle; macOS Seatbelt; Linux/WSL2 brauchen `bubblewrap` und `socat`; natives Windows nicht unterstützt. | https://code.claude.com/docs/en/sandboxing | gelesen | Datei-Werkzeuge, MCP und Hooks laufen außerhalb. |
| A11 | `CLAUDE.md` (Projekt, Benutzer, `CLAUDE.local.md`); ab v2.1.277 liest Claude Code `AGENTS.md` direkt, wenn kein `CLAUDE.md` existiert; sonst `@AGENTS.md` im `CLAUDE.md` importieren (unter Windows Import statt Symlink). | https://code.claude.com/docs/en/memory | gelesen | – |
| A12 | Skills unter `~/.claude/skills/<name>/SKILL.md` bzw. `.claude/skills/`; `/skills` listet. Plugins: `/plugin install name@marketplace`, offizieller Marktplatz `claude-plugins-official`; Liste mit `claude plugin list` oder `/plugin`. | https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/discover-plugins | gelesen | – |
| A13 | claude.ai-Upload: PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX, Bilder; 20 Dateien je Chat. | https://support.claude.com/en/articles/8241126-upload-files-to-claude | gelesen | `.md` und `.zip` nicht genannt: UNBELEGT. |
| A14 | Code-Ausführung und Dateierstellung in claude.ai für alle Pläne, Standard an. | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude | gelesen | ZIP-Lesen UNBELEGT. |
| A15 | claude.ai-GitHub-Integration: „+“ → „Add from GitHub“; synchronisiert Dateien eines Branches, keine Commits/PRs. | https://support.claude.com/en/articles/10167454-use-the-github-integration | gelesen | Planabdeckung UNBELEGT. |
| A16 | Claude Code im Web (claude.ai/code) für Pro/Max/Team, braucht GitHub-Verbindung. | https://code.claude.com/docs/en/claude-code-on-the-web | gelesen | Läuft in der Cloud, nicht auf dem Nutzercomputer. |

## 3. Fähigkeiten: Superpowers

| # | Belegte Aussage | Quelle | Status |
| --- | --- | --- | --- |
| S1 | Claude Code: `/plugin install superpowers@claude-plugins-official` oder `/plugin marketplace add obra/superpowers-marketplace` und `/plugin install superpowers@superpowers-marketplace`. | https://github.com/obra/superpowers | gelesen |
| S2 | Codex App und CLI: über den offiziellen Codex-Plugin-Marktplatz; App „Plugins“ → „Superpowers“ (Coding) → „+“; CLI `/plugins`, „superpowers“ suchen, „Install Plugin“. | https://github.com/obra/superpowers | gelesen |
| S3 | Herausgeber Jesse Vincent (obra); Eintrag ohne „Anthropic verified“-Kennzeichen. | https://claude.com/plugins/superpowers | gelesen |

Eigene Beobachtung (Linux-Prüfrechner, 2026-10-19, `tool_check`): `codex plugin list` zeigt `superpowers@openai-curated-remote installed, enabled 6.4.2`; die laufende Claude-Code-Sitzung (Desktop, Code-Bereich) listet die Skills `superpowers:*`. Beides belegt Verfügbarkeit auf diesem Rechner, nicht auf anderen.

## 4. Betriebssysteme und Werkzeuge

| # | Belegte Aussage | Quelle | Status | Grenzen |
| --- | --- | --- | --- | --- |
| O1 | Git macOS: `xcode-select --install` (Apple liefert Git mit den Command Line Tools) oder `brew install git`. | https://git-scm.com/install/mac | gelesen | – |
| O2 | Git Windows: offizieller Git-for-Windows-Installer; `winget install --id Git.Git -e --source winget` (winget-Paket nicht vom Git-for-Windows-Projekt gepflegt). | https://git-scm.com/install/windows | gelesen | – |
| O3 | Git Linux: `sudo apt-get install git` (Debian/Ubuntu), `sudo dnf install git` (Fedora). | https://git-scm.com/install/linux | gelesen | – |
| O4 | Git-Identität `git config --global user.name`/`user.email`; GitHub-E-Mail privat halten und `ID+NAME@users.noreply.github.com` verwenden. | https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup, https://docs.github.com/en/account-and-profile/reference/email-addresses-reference | gelesen | – |
| O5 | GitHub CLI: `brew install gh`; `winget install --id GitHub.cli --source winget` (danach neues Terminalfenster); Debian/Ubuntu offizielle apt-Quelle; `gh auth login` (Browser), `gh auth status`, `gh auth setup-git`. | https://github.com/cli/cli/blob/trunk/docs/install_macos.md, …/install_windows.md, …/install_linux.md, https://cli.github.com/manual/gh_auth_login, https://cli.github.com/manual/gh_auth_setup-git | gelesen | – |
| O6 | GitHub-Konto: https://github.com/signup; Zwei-Faktor-Anmeldung ist für Code beitragende Konten Pflicht (Benachrichtigung, 45 Tage Frist). | https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github, https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-mandatory-two-factor-authentication | gelesen | Zeitpunkt für neue Konten UNBELEGT; wir empfehlen 2FA sofort. |
| O7 | Python Windows: Python install manager (python.org oder Microsoft Store); Python macOS: python.org-Installer; Ubuntu 24.04 hat Python 3.12. | https://docs.python.org/3/using/windows.html, https://docs.python.org/3/using/mac.html, https://ubuntu.com/developers/docs/reference/availability/python/ | gelesen | – |
| O8 | WSL2: `wsl --install` (Administrator-PowerShell, Neustart), Windows 10 2004+/Build 19041+ oder Windows 11, Standard Ubuntu, Prüfung `wsl -l -v`; systemd bei aktuellem Ubuntu Standard; Projekte im Linux-Dateisystem halten. | https://learn.microsoft.com/en-us/windows/wsl/install, https://learn.microsoft.com/en-us/windows/wsl/systemd, https://learn.microsoft.com/en-us/windows/wsl/filesystems | gelesen | – |
| O9 | `fcntl`, `os.getuid`, `os.killpg` und `start_new_session` nur unter Unix/POSIX. | https://docs.python.org/3/library/fcntl.html, https://docs.python.org/3/library/os.html, https://docs.python.org/3/library/subprocess.html | gelesen | – |
| O10 | macOS: `hw.memsize` (sysctl) und `vm_stat` liefern Speicherangaben. | https://developer.apple.com/library/archive/documentation/Performance/Conceptual/ManagingMemory/Articles/VMPages.html | gelesen (Archiv 2013) | Fehlen von `/proc` auf macOS nicht durch Apple-Quelle belegt; die Implementierung verlässt sich deshalb nicht darauf, sondern wählt den Weg nach `sys.platform`. |
| O11 | Homebrew: Installationsbefehl auf https://brew.sh/, unterstützt macOS 15+, Linux, WSL. | https://brew.sh/ | gelesen | – |

## 5a. Eigene Befunde auf dem Linux-Prüfrechner

Ubuntu 24.04.4, Kernel 6.8, codex-cli 0.163.0, am 2026-10-19 (`tool_check`):

- Ohne installiertes `bubblewrap` scheitert jeder Befehl in der Codex-Sandbox (`read-only` und `workspace-write`): `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; `codex sandbox -- true` endet mit Exit 1. `kernel.apparmor_restrict_unprivileged_userns = 1`; `unshare --user --net` scheitert ebenso. Das ist genau der in C15 beschriebene Fall. Die Abhilfe nach C15 wurde auf diesem Rechner **nicht** angewendet (Systemänderung am Owner-Rechner).

Frische Ubuntu-24.04.5-VM (QEMU/KVM auf dem Prüfrechner, Cloud-Image, Kernel 6.8.0-147, 2026-10-19, `tool_check`): Ohne `bubblewrap` derselbe Fehler; nur `sudo apt install bubblewrap` (0.9.0) reicht **nicht** (weiter Exit 1); erst mit dem Profil `bwrap-userns-restrict` aus `apparmor-profiles` (`apparmor_parser -r`) endet `codex sandbox -- true` mit Exit 0. Danach blockiert die Sandbox Schreiben außerhalb des Arbeitsbereichs und das Netzwerk weiterhin, und `kernel.apparmor_restrict_unprivileged_userns` bleibt `1`. Dasselbe Profil macht `bwrap --ro-bind / / --unshare-user --unshare-net true` (Grundlage der Claude-Code-Sandbox) von Exit 1 zu Exit 0; Claude Codes eigenes `/sandbox` wurde in der VM nicht aufgerufen (keine Anmeldung). `claude plugin install <plugin>@<marktplatz>` und `codex plugin add <plugin>@<marktplatz>` existieren als Kommandozeilenbefehle (Hilfe gelesen).

## 5. Technische Entscheidungen

### E1 Sechs Standardwege

| Weg | Lokaler Agent (Standard) | Gate-Weg | Bekannte Abweichung |
| --- | --- | --- | --- |
| ChatGPT/Codex × macOS | ChatGPT-Desktop-App (Codex) oder Codex CLI | nativ (macOS-Adapter) | App-Mindestversion unbelegt |
| ChatGPT/Codex × Windows | ChatGPT-Desktop-App mit Agent in WSL2, alternativ Codex CLI in WSL2 | WSL2 (unveränderter Linux-Weg) | – |
| ChatGPT/Codex × Linux | Codex CLI (App nur Vorschau) | nativ (Referenz) | App Vorschau |
| Claude/Claude Code × macOS | Claude-Desktop-App (Code) oder Claude Code CLI | nativ (macOS-Adapter) | – |
| Claude/Claude Code × Windows | Claude Code CLI in WSL2 | WSL2 | Desktop-App startet Claude Code nativ unter Windows, dort ohne Sandbox (A10) und ohne Gate |
| Claude/Claude Code × Linux | Claude Code CLI (Desktop-App Beta) | nativ (Referenz) | Desktop-App Beta |

Begründung Windows: Das Gate braucht POSIX-Funktionen (O9), Claude Code hat nativ unter Windows keine Sandbox (A10), Codex unterstützt WSL2 offiziell (C3). WSL2 ist eine offizielle Microsoft-Funktion ohne separaten Server (O8). Ein nativer Windows-Port des Gates müsste Sperren, Prozessgruppen, UID-Isolation und Speicherprüfung neu bauen und wäre auf diesem Prüfrechner nicht prüfbar; das wäre mehr Risiko für weniger Nutzen.

Begründung macOS: macOS ist POSIX; `fcntl`, `getuid`, `killpg` und neue Sitzungen sind vorhanden (O9). Es fehlen nur `/proc`-Zugriffe und systemd. Ein kleiner Adapter (Speicher über `sysctl`/`vm_stat`, Prozesse über `ps`) ist sicherer und für Anfänger einfacher als eine Linux-VM. systemd-Ressourcenscopes sind schon heute optional (`systemd_scope = false`); auf macOS wird `true` abgelehnt statt still ignoriert.

### E2 Gleichwertigkeit

Gleichwertig heißt: gleiche Abnahmeziele, gleicher Schrittkatalog, gleiche Sicherheitsgrenzen. Nicht gleich sind Abo-Voraussetzungen (Claude Code braucht einen bezahlten Plan, A1; Codex ist ab Free enthalten, C1) und Oberflächen. Die Abweichung wird im Schritt `path` konkret genannt, nicht verschwiegen.

### E3 Start ohne Repository und ohne ZIP-Lesbarkeit

`.md`-Upload und ZIP-Lesen sind für beide Chats nicht belegt (C13, A13, A14). Deshalb: `START_HIER.md` ist reiner Text, enthält alle Anweisungen bis zum lokalen Agenten und funktioniert auch durch Einfügen des Textes. Das ZIP wird erst im lokalen Agenten gebraucht, der es nach dem Entpacken direkt von der Festplatte liest.

### E4 Zustand vor GitHub

Der Stand ist eine JSON-Datei (`onboarding/STATE.schema.json`). Im reinen Chat als Codeblock zum Speichern, im lokalen Agenten unter `~/.ai-bootstrap/stand.json`. Prüfung mit `scripts/onboarding_state.py` (Standardbibliothek). Kein Anbieter-Gedächtnis wird vorausgesetzt.

### E5 Fähigkeiten

Superpowers ist auf beiden Wegen über den jeweils offiziellen Plugin-Weg verfügbar (S1, S2) und deckt die Manifest-Fähigkeiten Brainstorming, Planung, systematische Fehlersuche, Test/Verifikation, Git-Isolation und Abschluss ab. Ausgewählt, weil es auf beiden Wegen dieselbe Fähigkeitsgruppe liefert. Recherche/Audit und Repository-Anweisungen kommen aus den eingebauten Funktionen (Websuche, `AGENTS.md`/`CLAUDE.md`). Vorhandene gleichwertige Fähigkeiten bleiben erhalten (Manifest-Regel EQUIVALENT); nichts wird nur zur Vollständigkeit installiert. Die Zuordnung steht in `skills/SKILL_MANIFEST.md`.

### E6 „Two-Sandbox“

Kein universeller Modus. Aufgelöst als zwei getrennte Grenzen:

1. **Agent-Sandbox**: begrenzt, was der KI-Agent selbst auf dem Computer darf (Codex: Sandbox-Modus + Freigaberegel, C6/C7; Claude Code: Berechtigungsmodus, Regeln und `/sandbox`, A9/A10).
2. **Gate-Isolation**: getrennte Umgebung für Prüfungen fremden Codes (`DEVBOX_GATE_POLICY.md` Abschnitt 5).

Daraus drei verständliche Agent-Profile (Vorsichtig, Standard, Erweitert) je Anbieter in den Anbieterdateien. Empfohlen: Standard. Vollzugriff nur auf ausdrückliche Nutzerentscheidung; `bypassPermissions` wird nicht angeboten (A9).

### E7 Version

Neue, kompatible Funktion: Standard und Paket werden **v2.1.0**. Eine Versionsquelle: Datei `VERSION`. v2.0.1 bleibt die Gate-Korrektur im Changelog; die Standarddateien nannten bisher v2.0.0 und werden auf v2.1.0 angehoben.

## v2-Ergänzung (GB2-01, 2026-10-21)

Abgerufen am 2026-10-21 für [GUIDED_BOOTSTRAP_V2](../tasks/GUIDED_BOOTSTRAP_V2.md). Lokal geprüft mit `codex-cli 0.163.0` und `gh 2.102.0`; `claude` war auf dem Prüfrechner nicht im Suchpfad, Claude-Aussagen sind deshalb nur aus der Dokumentation belegt.

| # | Belegte Aussage | Quelle | Status | Grenzen |
| --- | --- | --- | --- | --- |
| V1 | Claude-Marktplatz: `<repo>/.claude-plugin/marketplace.json` mit `name`, `owner.name`, `plugins[]` (je `name`, `source`); Plugin im selben Repository mit relativer Quelle `./plugins/<name>`; `plugin.json` unter `<plugin>/.claude-plugin/` (nur `name` Pflicht); Skills unter `<plugin>/skills/<name>/SKILL.md`. | https://code.claude.com/docs/en/plugins/marketplace-reference, https://code.claude.com/docs/en/plugins-reference | gelesen | – |
| V2 | `claude plugin marketplace add owner/repo` (Ref mit `owner/repo#ref` oder `@ref`), `--scope user` Standard; `claude plugin install name@marketplace`; wirksam ab nächster Sitzung oder nach `/reload-plugins`. | https://code.claude.com/docs/en/plugins/cli-reference | gelesen; real geprüft 2026-10-21 (frisches Ubuntu 24.04, Claude Code 2.1.306, ohne Anmeldung) | Branch-Ref funktioniert; **Commit-SHA als Ref scheitert** („Please make sure you have the correct access rights…“) |
| V3 | `SKILL.md`: `name` (Standard: Ordnername) und `description` empfohlen; claude.ai-Upload erlaubt nur `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. | https://code.claude.com/docs/en/skills | gelesen | – |
| V4 | Codex-Skills: persönlich `$HOME/.agents/skills`, Projekt `.agents/skills`; `SKILL.md` mit `name` und `description` Pflicht (gleiches Format); neue Skills werden erkannt, sonst Neustart. | https://learn.chatgpt.com/docs/build-skills | gelesen | – |
| V5 | Codex-Plugin-Marktplätze aus Git: `codex plugin marketplace add owner/repo[@ref]` mit `--ref`; Marktplatzdatei `.agents/plugins/marketplace.json` (Einträge mit `policy` und `category`); `.claude-plugin/marketplace.json` wird „legacy-compatible“ gelesen. | https://developers.openai.com/plugins/build/plugins; lokal `codex plugin marketplace add --help` | gelesen, lokal geprüft (CLI) | Werte für `policy` und Lesen eines reinen Claude-Marktplatzes durch die CLI UNBELEGT → Skill-Ordner-Weg gewählt |
| V6 | Persönliche Codex-Anweisungen: `~/.codex/AGENTS.md` (bzw. `$CODEX_HOME/AGENTS.md`). | https://learn.chatgpt.com/docs/agent-configuration/agents-md | gelesen | – |
| V7 | Codex-Befehlsregeln: Starlark-Dateien `~/.codex/rules/*.rules`, `prefix_rule(pattern=[...], decision="forbidden"\|"prompt"\|"allow")`, strengste Regel gewinnt; Test mit `codex execpolicy check`; experimentell, Neustart nötig. | https://learn.chatgpt.com/docs/agent-configuration/rules | gelesen | experimentell |
| V8 | Claude-Berechtigungsregeln: `Bash(gh pr merge *)` gleich `Bash(gh pr merge:*)`; Reihenfolge deny → ask → allow, allow hebt deny nie auf. | https://code.claude.com/docs/en/permissions | gelesen | – |
| V9 | Claude Code nativ unter Windows: Windows 10 1809+; Git for Windows empfohlen (Git Bash für das Bash-Werkzeug, sonst PowerShell); Sandbox auf nativem Windows nicht unterstützt (nur macOS, Linux, WSL2). | https://code.claude.com/docs/en/setup, https://code.claude.com/docs/en/sandboxing | gelesen | – |
| V10 | Codex nativ unter Windows (CLI, IDE, Desktop-App) mit eigener Windows-Sandbox (MXC empfohlen). | https://learn.chatgpt.com/docs/windows/windows-sandbox | gelesen | – |
| V11 | Claude-Projekte: „Projects“ → „+ New Project“; alle Pläne (Free bis 5 Projekte); GitHub im Projektwissen über „+“ → „GitHub“, „Sync“ zum Aktualisieren. | https://support.claude.com/en/articles/9519177, https://support.claude.com/en/articles/10167454 | gelesen | Planabdeckung der GitHub-Anbindung teils UNBELEGT |
| V12 | ChatGPT-Projekte auf allen Plänen; GitHub wird pro Konto unter Einstellungen → Plugins (früher Apps) → GitHub verbunden und live gelesen. | https://help.openai.com/en/articles/10169521, https://help.openai.com/en/articles/11145903 | Suchtreffer (403) | genaue Bedienwege und Bindung an ein Projekt UNBELEGT |
| V13 | `gh pr merge --match-head-commit <sha>`: Merge nur, wenn der PR-Kopf diesem Commit entspricht (GraphQL `expectedHeadOid`); nicht interaktiv ist `--merge`/`--squash`/`--rebase` Pflicht; ein veralteter Branch wird nur abgelehnt, wenn eine Schutzregel „up to date“ verlangt. `gh pr update-branch [--rebase]` holt die Basis in den PR-Branch. | https://cli.github.com/manual/gh_pr_merge, https://cli.github.com/manual/gh_pr_update-branch; lokal `--help` | gelesen, lokal geprüft | Ablehnung bei veraltetem Branch ohne Schutzregel nicht getestet → „Leicht“ prüft das selbst |

### E8 Entscheidungen v2

- **Claude:** eigener Marktplatz aus diesem Repository (V1, V2), ohne Ref (Hauptzweig); danach die Plugin-Version prüfen, weil ein Commit-SHA als Ref nicht funktioniert. Die Startdatei selbst liest die Skills exakt am Quellcommit (Clone + Checkout bzw. Rohdatei-Adresse).
- **Codex:** Repository nach `~/.ai-bootstrap/repo` klonen und die drei Skill-Ordner nach `~/.agents/skills/` kopieren (V4). Der Codex-Plugin-Marktplatz (V5) wird erst genutzt, wenn sein Format belegt ist.
- **Persönliche Regeln:** `~/.claude/CLAUDE.md` bzw. `~/.codex/AGENTS.md` (A11, V6) mit markiertem Block.
- **Sperren:** Claude `permissions.deny` (V8); Codex `prefix_rule(..., decision="forbidden")` (V7).
- **Windows:** nativ (V9, V10). Claude Code hat dort keine Sandbox; das wird im Profil offen gesagt, Sperrregeln gelten trotzdem.
- **„Leicht“-Merge:** Prüfung „Branch enthält aktuellen main“ selbst ausführen (`git merge-base --is-ancestor origin/main HEAD`), bei Bedarf `gh pr update-branch`, dann `gh pr merge --match-head-commit` (V13).
