# Anbieter: ChatGPT mit Codex

Quellen: `docs/research/GUIDED_BOOTSTRAP_V1_SOURCE_MATRIX.md` (C1–C15, S2, V4–V7, V10). Bedienwege ändern sich; richte dich nach dem, was der Nutzer tatsächlich sieht.

## Voraussetzung

Codex ist in ChatGPT Free, Go, Plus, Pro, Business, Edu und Enterprise enthalten; Free und Go nur für kleine Aufgaben (C1). Nenne keine Kontingent-Zahlen; maßgeblich ist die Nutzungsanzeige. Prüfe `codex --version` und `codex login status`, wenn `codex` im Suchpfad ist; sonst ist die laufende Sitzung in der App der Nachweis.

## Schritt `skills`

| Fähigkeit | Umsetzung |
| --- | --- |
| Brainstorming, Planung, Fehlersuche, Testen, Git-Isolation | Plugin **Superpowers** aus dem offiziellen Codex-Plugin-Marktplatz (S2) |
| Einrichtung, Projektstart, Arbeitsweise | Skills **ai-bootstrap** aus `robin-shiels/ai-project-bootstrap` als persönliche Skills (V4) |

1. **Prüfen:** `codex plugin list` (Zeile `superpowers`, „installed, enabled“) und `ls ~/.agents/skills` (Ordner `einrichtung`, `projekt-start`, `arbeitsweise`).
2. **Superpowers installieren (falls nötig):** `codex plugin add superpowers@<marktplatz>`; den Namen zeigt `codex plugin list`. Meldet die Liste „No marketplace plugins found.“, ist Codex nicht angemeldet. Alternativ der Nutzer: in der App „Plugins“ → „Superpowers“ → „+“.
3. **ai-bootstrap installieren (falls nötig):** Repository nach `~/.ai-bootstrap/repo` klonen (`git clone https://github.com/robin-shiels/ai-project-bootstrap.git ~/.ai-bootstrap/repo`, bei vorhandenem Ordner `git -C ~/.ai-bootstrap/repo pull --ff-only`), dann die drei Ordner aus `~/.ai-bootstrap/repo/plugins/ai-bootstrap/skills/` nach `~/.agents/skills/` kopieren (vorhandene gleichnamige Ordner vorher ansehen; ersetzen nur, wenn sie von ai-bootstrap stammen). Windows: `%USERPROFILE%\.agents\skills`.
4. **Wirksam:** neue Codex-Sitzung starten (V4, C10).
5. **Probeaufruf:** Deine Skill-Liste enthält `brainstorming` und `arbeitsweise`. Kannst du sie nicht einsehen, tippt der Nutzer `/skills`.

Superpowers stammt von Jesse Vincent (obra) und steht im offiziellen Codex-Marktplatz (S2, S3).

## Schritt `arbeitsweise`: Regeldatei

Persönliche Regeln: `~/.codex/AGENTS.md` (V6). Projektregeln gehören ins `AGENTS.md` des Projekts.

## Schritt `arbeitsweise`: Berechtigungsprofil

Erkläre kurz: Die **Sandbox** legt fest, wo Codex ohne Rückfrage schreiben darf und ob es ins Internet darf. Die **Freigaberegel** legt fest, wann es fragt. **Befehlsregeln** erlauben oder sperren einzelne Befehle (C6, V7).

```text
Frage 1 von 1: Wie selbstständig soll Codex arbeiten?

1. Vorsichtig – liest nur, fragt vor jeder Änderung
2. Standard – arbeitet im Projektordner selbst, Branch, Commit, Push, Pull Request und Merge nach Projektregel ohne Rückfrage, gefährliche Befehle gesperrt
3. Voller Zugriff – keine Schutzgrenze; nur für bewusst getrennte Umgebungen

Empfehlung: Standard, weil der Ablauf bis zum Merge flüssig läuft und Gefährliches trotzdem gesperrt bleibt.
Du kannst auch eine eigene Antwort schreiben.
```

`~/.codex/config.toml` (vorhandene Einträge behalten):

| Profil | Einstellung |
| --- | --- |
| Vorsichtig | `sandbox_mode = "read-only"`, `approval_policy = "on-request"` |
| **Standard** | `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"` |
| Voller Zugriff | `sandbox_mode = "danger-full-access"`, `approval_policy = "never"` |

Befehlsregeln für Standard in `~/.codex/rules/ai-bootstrap.rules` (V7; experimentell, wirksam nach Neustart):

```starlark
# ai-bootstrap v3.0.0: Ablauf bis Merge ohne Rückfrage, Gefährliches gesperrt.
prefix_rule(pattern=["git", "push", "-u", "origin"], decision="allow", justification="eigenen Task-Branch veröffentlichen")
prefix_rule(pattern=["gh", "pr", "create"], decision="allow", justification="Pull Request anlegen")
prefix_rule(pattern=["gh", "pr", "view"], decision="allow", justification="Pull Request lesen")
prefix_rule(pattern=["gh", "pr", "update-branch"], decision="allow", justification="Branch auf aktuellen main bringen")
prefix_rule(pattern=["gh", "pr", "merge"], decision="prompt", justification="nur mit --match-head-commit nach Projektregel")
prefix_rule(pattern=["git", "push", "--force"], decision="forbidden", justification="kein Force-Push")
prefix_rule(pattern=["git", "push", "-f"], decision="forbidden", justification="kein Force-Push")
prefix_rule(pattern=["git", "push", "origin", "main"], decision="forbidden", justification="nie direkt auf main")
prefix_rule(pattern=["git", "push", "origin", "HEAD:main"], decision="forbidden", justification="nie direkt auf main")
prefix_rule(pattern=["git", "push", "-u", "origin", "main"], decision="forbidden", justification="nie direkt auf main")
prefix_rule(pattern=["gh", "pr", "merge", "--admin"], decision="forbidden", justification="kein Admin-Merge")
```

- `gh pr merge` steht auf „prompt“, weil Präfixregeln die Bedingung `--match-head-commit` nicht prüfen können. Unter LIGHT bestätigt der Nutzer diese Rückfrage der Laufzeit; die inhaltlichen Bedingungen prüfst du vorher selbst (Skill `arbeitsweise` §4).
- Prüfen: `codex execpolicy check --rules ~/.codex/rules/ai-bootstrap.rules -- git push --force` muss „forbidden“ melden, `-- gh pr create` „allow“.
- Deploy-Befehle werden im Projekt erlaubt (`<repo>/.codex/rules/`, nur in vertrauenswürdigen Projekten wirksam), sobald dort ein Deploy-Ziel festgelegt ist.
- `untrusted` nicht verwenden; diese Freigaberegel ist entfernt (C6).
- **Linux und WSL2:** Die Sandbox braucht `bubblewrap` (C15). `command -v bwrap`; fehlt es: `sudo apt install bubblewrap`. Prüfen: `codex sandbox -- true` endet mit Exit 0. Unter Ubuntu 24.04 bei `bwrap: … Operation not permitted`: `sudo apt install apparmor-profiles apparmor-utils`, `sudo install -m 0644 /usr/share/apparmor/extra-profiles/bwrap-userns-restrict /etc/apparmor.d/bwrap-userns-restrict`, `sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict`, dann erneut prüfen. Keine systemweite Abschaltung; „Voller Zugriff“ ist keine Lösung für einen Sandbox-Fehler.
- **Windows nativ:** Codex hat dort eine eigene Sandbox (V10). Fragt Codex beim ersten Start nach deren Einrichtung, folgt der Nutzer dem Dialog.
- Prüfung: Datei lesen bzw. der Nutzer tippt `/permissions`; den wirksamen Wert nennen.

## Projekt in der App

Siehe Skill `projekt-start` §3 (V12).
