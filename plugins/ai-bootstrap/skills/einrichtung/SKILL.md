---
name: einrichtung
description: Geführte persönliche Einrichtung des AI Bootstrap – GitHub verbinden, wichtige Skills installieren, Arbeitsweise und KI-Einstellungen gemeinsam einrichten, erstes Projekt und Probelauf bis zum Merge. Verwenden, wenn der Nutzer START_HIER.md geschickt hat, "Einrichtung", "Start" oder "Einrichtung fortsetzen" sagt oder einen gespeicherten Einrichtungsstand (stand.json) mitbringt.
---

# Geführte Einrichtung

Du begleitest den Nutzer durch die Einrichtung seiner persönlichen Arbeitsumgebung. Voraussetzung: Die Desktop-App von ChatGPT (Bereich Codex) oder Claude (Bereich Code) und ein passendes Abo sind vorhanden, und du läufst als lokaler Agent auf seinem Computer.

Es geht **nur** um die Einrichtung und Verknüpfung der essenziellen Dienste: GitHub, die wichtigen Skills, die Einstellungen der KI und das erste Projekt. Alles, was du selbst tun kannst, tust du. Du erklärst dabei immer begleitend, was du tust und warum.

Für den Dialog gilt der Skill `arbeitsweise` (Frageformat, Erklären, erst prüfen dann fragen). Lade ihn jetzt, falls er nicht schon geladen ist; ist er nicht verfügbar, gelten seine Regeln trotzdem sinngemäß, wie unten zusammengefasst.

Anbieterdetails stehen in `references/claude-code.md` bzw. `references/chatgpt-codex.md`, Betriebssystemdetails in `references/macos.md`, `references/windows.md`, `references/linux.md`. Lies nur die Datei, die du für den aktuellen Schritt brauchst.

## 1. Erste Nachricht

Deine erste Antwort beginnt immer sinngemäß mit:

> Ich begleite dich Schritt für Schritt durch die Einrichtung. Du kannst jederzeit hier im Chat Fragen stellen oder sagen, wenn etwas unklar ist oder bei dir anders aussieht. Wir klären das gemeinsam und machen danach an derselben Stelle weiter.

Danach ein Satz, was die Einrichtung umfasst: „Wir verbinden GitHub, installieren die wichtigen Skills, richten deine Arbeitsweise und die Einstellungen ein und probieren alles an deinem ersten Projekt aus.“ Keine weitere Gesamtliste.

Gibt es einen gespeicherten Stand (Abschnitt 5), begrüße kurz, nenne in einem Satz den erreichten Stand und mache dort weiter.

## 2. Steuerung

Für jeden Schritt aus Abschnitt 3, in dieser Reihenfolge:

1. **Prüfen**, ob er schon erfüllt ist. Selbst, mit Befehlen.
2. **Erfüllt:** ein Satz Bestätigung, weiter.
3. **Nicht erfüllt:** in zwei bis vier Sätzen erklären, was jetzt passiert und warum. Dann selbst ausführen, oder genau eine Nutzeraktion anleiten, wenn es eine Anmeldung, eine Kontoanlage oder ein Slash-Befehl ist.
4. **Erneut prüfen.** Erst dann ist der Schritt erledigt.
5. **Stand sichern** (Abschnitt 5), still.

Ist ein Schritt blockiert, trage den Blocker mit dem nächsten konkreten Schritt im Stand ein und mache mit allem weiter, was nicht davon abhängt.

Slash-Befehle der eigenen Oberfläche (`/plugin`, `/skills`, `/permissions`, `/status`) kannst du nicht selbst ausführen. Nutze die Kommandozeilenbefehle aus der Anbieterdatei, oder bitte den Nutzer, den Befehl einzutippen und dir das Ergebnis zu sagen.

## 3. Schritte

### `start`

Stelle still fest: Anbieter (Claude Code oder Codex), Betriebssystem, ob `git` und `gh` vorhanden sind, ob `gh` angemeldet ist. Befehle: siehe Betriebssystemdatei. Frage nichts davon ab. Sage in einem Satz, was du gefunden hast, nur wenn etwas fehlt.

Läufst du nicht als lokaler Agent (du kannst keinen Befehl auf dem Computer ausführen), sag das ehrlich und erkläre in zwei Sätzen, wie der Nutzer diese Einrichtung im Code-Bereich der Desktop-App startet. Mehr nicht.

### `github`

Erkläre in zwei bis drei Sätzen, was GitHub ist und warum wir es brauchen, zum Beispiel:

> GitHub ist ein Online-Speicher für Projekte. Jede Änderung wird dort mit Datum und Beschreibung festgehalten, sodass nichts verloren geht und man jederzeit zurück kann. Ich arbeite dort auf eigenen Zweigen und lege dir Änderungen als Antrag vor; so bleibt der Hauptstand immer sauber.

Dann, jeweils nur wenn nötig:

1. **Git installieren** (Betriebssystemdatei). Nach Freigabe der Laufzeit selbst.
2. **GitHub-Konto:** Frage nur, ob eines existiert. Wenn nicht, legt der Nutzer es selbst unter https://github.com/signup an. Empfiehl die Zwei-Faktor-Anmeldung und in den Einstellungen unter „Emails“ die Option „Keep my email addresses private“.
3. **GitHub CLI installieren** (Betriebssystemdatei) und **anmelden:** `gh auth login` (GitHub.com → HTTPS → Browser). Die Anmeldung im Browser macht der Nutzer. Danach `gh auth setup-git`, außer Git arbeitet bereits über SSH mit diesem Konto.
4. **Name und E-Mail für Commits:** `git config --global user.name` und `user.email` prüfen. Fehlt etwas, frage nach dem Namen, den der Nutzer zeigen möchte, und setze als E-Mail die private GitHub-Adresse `ID+NUTZERNAME@users.noreply.github.com` (aus `gh api user --jq '.id, .login'`). Bestehende Werte nicht überschreiben.

Nachweis: `gh auth status` zeigt das Konto, beide Git-Werte sind gesetzt.

### `skills`

Erkläre in einem Satz: „Skills sind Anleitungen, mit denen ich bestimmte Arbeiten immer gleich gut mache, zum Beispiel planen, Fehler suchen oder testen.“

Installiere und prüfe nach der Anbieterdatei:

- **Superpowers** (Planung, Brainstorming, Fehlersuche, Testen, Git-Isolation);
- **ai-bootstrap** (dieser Skill, `projekt-start`, `arbeitsweise`), falls noch nicht dauerhaft installiert.

Vorhandene gleichwertige Skills behalten, nichts doppelt installieren. Nachweis ist die tatsächliche Skill-Liste in einer neuen Sitzung, nicht der Installationsbefehl. Muss dafür eine neue Sitzung gestartet werden, sichere vorher den Stand und sage genau, was der Nutzer in der neuen Sitzung schreibt („Einrichtung fortsetzen“).

### `arbeitsweise`

Zwei Teile, jeweils mit kurzer Erklärung:

1. **Persönliche Regeln.** Erkläre: „Damit ich in jeder Sitzung so arbeite wie jetzt – Fragen mit Empfehlung, alles begleitend erklärt –, schreibe ich das kurz in deine persönliche Regeldatei.“ Ergänze den Block aus `references/PERSONAL_RULES.md` in `~/.claude/CLAUDE.md` (Claude Code) bzw. `~/.codex/AGENTS.md` (Codex). Vorhandene Inhalte bleiben, ein vorhandener Block mit denselben Markierungen wird ersetzt, nicht verdoppelt.
2. **Einstellungen der KI.** Lies die vorhandenen Einstellungen vor, erkläre in einfachen Worten, was die wichtigen bedeuten, und stelle eine Frage zum Berechtigungsprofil (Anbieterdatei). Empfehlung „Standard“: Du arbeitest im Projekt selbstständig, Branch, Commit, Push, Pull Request und Merge nach der Projektregel laufen ohne Rückfrage, gefährliche Befehle (Force-Push, Push auf `main`, Admin-Merge) sind technisch gesperrt. Setze das Profil nach der Antwort, behalte alle anderen Einträge, und nenne, ab wann es gilt (meist ab der nächsten Sitzung).

   Sagt der Nutzer dabei etwas zu Merge oder Deploy (zum Beispiel „vor jedem Merge fragen“), ist das keine Profileinstellung, sondern die Merge-Regel seiner Projekte. Erkläre das in einem Satz, halte sie als Entscheidung `merge_policy` im Stand fest (hier PER_CHANGE_APPROVAL) und nimm `gh pr merge` nicht in die Liste der Befehle ohne Rückfrage auf. Im Schritt `projekt` gilt sie dann als Vorgabe.

### `projekt`

Lade den Skill `projekt-start` und folge ihm: Projekt in der App anlegen und mit GitHub verbinden, Repository anlegen oder übernehmen, Projektstandard mit Merge-/Deploy-Regel, bei Bedarf Server-Beratung. Ergebnis: Die neuen Projektregeln liegen auf einem eigenen Branch, mit Pull Request.

### `probelauf`

Der Probelauf zeigt, dass der ganze Ablauf funktioniert. Er nutzt den echten Pull Request mit den Projektregeln aus `projekt`.

1. Erkläre in zwei Sätzen, was jetzt passiert: prüfen, Branch auf den aktuellen Stand bringen, übernehmen.
2. Prüfungen ausführen (mindestens `git diff --check`, dazu vorhandene schnelle Projektprüfungen).
3. Weil dieser PR die Merge-Regeln des Projekts festlegt, fragst du **einmal** ausdrücklich: „Frage 1 von 1: Sollen die neuen Projektregeln jetzt übernommen werden?“ mit Empfehlung. Künftige eigene PRs laufen danach nach der festgelegten Regel ohne diese Frage.
4. Nach Zustimmung genau die LIGHT-Schritte aus `arbeitsweise` §4: Branch enthält aktuellen `main`, Prüfungen grün auf diesem Commit, `gh pr merge <N> --squash --match-head-commit <sha>`.
5. Zurücklesen: `git fetch origin`, `main` enthält den Commit, `gh pr view <N> --json state` meldet `MERGED`.
6. Erkläre in zwei Sätzen, was gerade passiert ist und dass es künftig genau so läuft.

Gibt es keine Regeländerung (das Projekt war schon passend eingerichtet), nimm eine kleine, nützliche Änderung, die der Nutzer bestätigt, zum Beispiel einen Abschnitt „So arbeiten wir“ in der README. Ist die Projektregel nicht LIGHT, endet der Probelauf beim Pull Request und du erklärst, wie es unter der gewählten Regel weitergeht.

Nachweis: PR-Nummer, geprüfter Commit, Prüfbefehl mit Ergebnis, Merge-Commit auf `main`.

### `fertig`

Kurzer Abschluss, nur Belegtes:

- was eingerichtet ist (GitHub, Skills, Regeln, Profil, Projekt), jeweils mit Nachweisart;
- was offen ist, mit dem nächsten konkreten Schritt;
- wie der Nutzer das nächste Projekt startet: neue Sitzung, „Neues Projekt anlegen“ (Skill `projekt-start`).

Teilweise eingerichtet heißt „noch nicht fertig“, nie „fertig“.

### `gate` (optional)

Nur wenn ein Projekt die Merge-Regel GATE wählt. Dann zusätzlich Python 3.12+ und unter Windows WSL 2 (Betriebssystemdatei, Abschnitt „Gate“), Einführung nach `DEVBOX_GATE_POLICY.md` und `templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md` aus dem Repository `robin-shiels/ai-project-bootstrap`.

## 4. Grenzen

- Kein Konto anlegen, nichts kaufen, kein Abo wechseln.
- Keine Passwörter, Tokens oder Schlüssel erfragen oder speichern.
- Kein Push auf `main`, kein Force-Push; Merge nur wie im Probelauf beschrieben.
- Keine Sicherheitsfunktion abschalten, um einen Schritt grün zu machen. Fehlt etwas, ist das ein benannter Blocker.
- Kein Server, keine Dev-Box einrichten. Dazu gibt es nur Beratung (`projekt-start`).

## 5. Einrichtungsstand

Der Stand ist eine kleine, geheimnisfreie JSON-Datei nach `references/STATE.schema.json` (Beispiel: `references/STATE.example.json`). Speicherort: `~/.ai-bootstrap/stand.json` (Windows: `%USERPROFILE%\.ai-bootstrap\stand.json`). Sage beim ersten Speichern einmal in einem Satz, dass du dort den Stand ablegst, damit es nach einer Pause weitergeht.

- **Sichern** nach jedem erledigten Schritt, still.
- **Prüfen:** `python3 scripts/onboarding_state.py validate <datei>` aus dem Ordner dieses Skills, wenn Python vorhanden ist; sonst selbst anhand des Schemas (Pflichtfelder, erlaubte Werte, keine Geheimnisse).
- **Alter Stand (Version 1):** zuerst `python3 scripts/onboarding_state.py migrate <alt> <neu>`, ohne Python von Hand nach der Zuordnung im Skript.
- **Fortsetzen:** Entscheidungen übernehmen, nicht neu fragen. Widerspricht eine gespeicherte Entscheidung dem, was du jetzt feststellst (zum Beispiel ist `provider_path` „claude-code“, du läufst aber als Codex), sag das und lege es im Frageformat vor, statt still eins von beiden anzunehmen. Nachweise über Computer, Konten-Zugriff und Repositories aus einer früheren Sitzung sind Vorgeschichte und werden kurz neu geprüft. `current_step` ist der erste noch nicht erledigte Schritt.
