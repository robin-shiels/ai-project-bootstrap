---
name: projekt-start
description: Neues Projekt anlegen oder bestehendes übernehmen – erklärt, wie man ein Projekt in ChatGPT oder Claude anlegt und mit GitHub verbindet, legt das Repository an, wendet den Projektstandard mit Merge-/Deploy-Regel (LIGHT als Standard) an und berät kritisch, ob ein Server oder eine Dev-Box wirklich nötig ist. Verwenden bei "neues Projekt", "Projekt anlegen", "Projekt übernehmen", "brauche ich einen Server", während der Einrichtung im Schritt projekt.
---

# Projekt anlegen oder übernehmen

Es gilt der Skill `arbeitsweise` (Frageformat, begleitendes Erklären). Die Projektebene regelt `UNIVERSAL_PROJECT_BOOTSTRAP.md` aus `robin-shiels/ai-project-bootstrap`; diese Anleitung ersetzt ihn nicht. Lies ihn bei Bedarf direkt aus dem öffentlichen Repository (`gh api repos/robin-shiels/ai-project-bootstrap/contents/UNIVERSAL_PROJECT_BOOTSTRAP.md --jq .content | base64 -d`) oder aus dem entpackten Paket. Die unten genannten Vorlagen (`templates/…`) und `DEVBOX_GATE_POLICY.md` liest du genauso.

## 1. Neu oder bestehend?

Prüfe zuerst selbst, ob der aktuelle Ordner schon ein Repository ist und ob es Projektregeln gibt (`AGENTS.md`, `CLAUDE.md`, Beitragsregeln). Frage nur, was du nicht feststellen kannst:

```text
Frage 1 von 1: Wollen wir ein neues Projekt anlegen oder ein bestehendes übernehmen?

1. Neues Projekt – ich lege ein privates Repository auf GitHub an
2. Bestehendes Projekt – du nennst mir das Repository oder den Ordner

Empfehlung: …, weil …
Du kannst auch eine eigene Antwort schreiben.
```

Ein Repository mit Code, aber ohne Regeln, behandelst du wie ein neues Projekt und sagst das.

## 2. Repository

- **Neu:** Frage nach einem kurzen Namen und einem Satz, worum es geht. Lege es nach Zustimmung an: `gh repo create <name> --private --clone` (Empfehlung privat, weil ein öffentliches Repository für alle lesbar ist). Wechsle in den Ordner. Meldet `gh` dabei `HTTP 403: Resource not accessible by personal access token`, darf die vorhandene Anmeldung keine Repositories anlegen. Dann legt der Nutzer es selbst unter https://github.com/new an (privat, ohne weitere Dateien), und du klonst es mit `gh repo clone <konto>/<name>`.
- **Bestehend:** klonen, falls nötig (`gh repo clone <owner>/<name>`), und die vorhandenen Regeln lesen.

## 3. Projekt in der App anlegen und verbinden

Erkläre in zwei Sätzen, warum: „In der App gibt es ‚Projekte‘. Das sind Ordner für Chats, Dateien und Anweisungen zu einem Vorhaben. Wenn du das GitHub-Repository dort verbindest, kann ich auch im normalen Chat den aktuellen Code lesen, zum Beispiel zum Planen.“

Leite dann genau den Weg an, den der Nutzer sieht. Bedienwege können sich ändern; richte dich nach dem, was er dir beschreibt.

- **Claude:** links „Projects“ → „+ New Project“, Name und Beschreibung. Im Projekt unter Projektwissen „+“ → „GitHub“, Repository suchen oder Adresse einfügen, Dateien wählen; „Sync“ holt später den neuesten Stand. Der Free-Plan erlaubt höchstens fünf Projekte.
- **ChatGPT:** in der Seitenleiste „Projekte“ → neues Projekt anlegen. GitHub wird einmal pro Konto unter Einstellungen → Plugins (früher Apps) → GitHub verbunden und dann im Chat genutzt. Wie das an ein einzelnes Projekt gebunden wird, ist nicht belegt; sag das ehrlich, wenn der Nutzer fragt.

Nachweis: Der Nutzer stellt im Projekt-Chat eine Frage zu einer Datei (zum Beispiel „Was steht in der README?“) und bekommt den richtigen Inhalt. Die Projektanweisungen der App sind optional. Die verbindlichen Regeln stehen im Repository, nicht in der App.

## 4. Projektstandard anwenden

Nach `UNIVERSAL_PROJECT_BOOTSTRAP.md`: Bestandsaufnahme, dann Abgleich (MISSING / EQUIVALENT / OUTDATED / CONFLICT). Fehlen Ziele und Regeln, nutze Superpowers-Brainstorming und `templates/PROJECT_DISCOVERY.md` und frage nur, was nötig ist.

Zwei Regeln werden bei einem **neuen** Projekt immer festgehalten. Bei beiden zeigst du den Hinweis aus dem Standard deutlich und bietest die Wahl im Frageformat an:

1. **Veröffentlichung eigener Branches:** ALLOW_AFTER_CHECKS (Standard), PER_TASK_APPROVAL, DISABLED.
2. **Merge und Deploy:** LIGHT (Standard), GATE, PER_CHANGE_APPROVAL. Erkläre LIGHT in drei Sätzen: „Ich übernehme meine eigenen Änderungen selbst in den Hauptstand, wenn alle Prüfungen grün sind. Vorher hole ich den neuesten Stand und prüfe erneut. Wenn das Projekt eine Veröffentlichung hat, veröffentliche ich danach selbst und prüfe, ob alles läuft.“ Hat das Projekt ein Deploy-Ziel, frage nach Ziel und Befehl, soweit du sie nicht im Repository findest. Dient die Produktion echten Nutzerdaten, frage einmal, ob dort automatisch deployed werden darf.

Bei einem **bestehenden** Projekt bleiben vorhandene strengere Regeln, insbesondere ein integriertes Merge-Gate. Ein Widerspruch wird als CONFLICT vorgelegt, nie still überschrieben.

Schreibe die Regeln in die maßgebliche Regeldatei, normalerweise `AGENTS.md`, mit den Textbausteinen `templates/AGENTS_MERGE_LIGHT.md` bzw. `templates/AGENTS_DEVBOX_GATE.md`. Für Claude Code: Gibt es nur `AGENTS.md`, reicht das. Braucht es ein `CLAUDE.md`, importiert es `AGENTS.md` mit der Zeile `@AGENTS.md`.

Die Änderungen kommen auf einen eigenen Branch, zum Beispiel `setup/projektstandard-JJJJMMTT`, angelegt mit `git switch --no-track -c <branch> origin/main`. Dann Commit, Push genau dieses Branches, Pull Request. Gemerged wird im Probelauf der Einrichtung bzw. nach ausdrücklicher Zustimmung, weil dieser PR die Befugnisregeln festlegt.

## 5. Server oder Dev-Box? Kritisch beraten

Nur ansprechen, wenn das Projekt danach klingt (etwas soll dauerhaft laufen, nach Zeitplan arbeiten, eine eigene Datenbank haben, eine Webseite mit eigenem Backend) oder der Nutzer fragt. Du berätst nur und richtest nichts ein.

1. **Zuerst kritisch fragen, ob es wirklich nötig ist.** Ein eigener Server kostet Geld und Zeit: Updates, Sicherheit, Sicherungen, Überwachung. Für die meisten Vorhaben reicht etwas Einfacheres.
2. **Die einfachere Alternative nennen**, passend zum Vorhaben:
   - nur entwickeln und prüfen → der eigene Computer;
   - statische Webseite → ein Hosting-Dienst mit kostenlosem Einstieg, der direkt aus GitHub veröffentlicht;
   - Web-App mit Datenbank → eine verwaltete Plattform, bei der Server, Updates und Sicherungen der Anbieter übernimmt;
   - Aufgaben nach Zeitplan oder ohne laufenden Laptop → geplante Aufgaben beim Anbieter (Cloud-Agent, Routinen) oder eine verwaltete Plattform.
3. **Ein eigener Server oder eine Dev-Box ist sinnvoll**, wenn mehrere dieser Punkte zutreffen: Es soll rund um die Uhr selbst Betriebenes laufen; es braucht besondere Software oder Hardware; Prüfungen oder das Merge-Gate sollen laufen, während der Laptop aus ist; fremder Code soll strikt getrennt geprüft werden; die Kosten einer verwalteten Plattform wären deutlich höher.
4. **Ergebnis als Empfehlung** im Frageformat, mit realistischen Optionen und einer Empfehlung. Die Wahl von Anbieter, Kosten und Zugang trifft der Nutzer. Du mietest, kaufst oder registrierst nichts.
5. Entscheidet sich der Nutzer für einen Server, halte die Entscheidung in den Projektregeln fest. Für die Einrichtung gilt: private Schlüssel bleiben auf seinem Gerät; auf einer Maschine mit Zugriff auf Projekte, Deployments oder Konten läuft kein fremder Code (`DEVBOX_GATE_POLICY.md` §5).

## 6. Abschluss

Nenne kurz: Repository, App-Projekt verbunden (ja/nein, Nachweis), wirksame Regeln (Veröffentlichung, Merge/Deploy, Deploy-Ziel), Branch und PR mit den Regeln, Server-Empfehlung falls besprochen.
