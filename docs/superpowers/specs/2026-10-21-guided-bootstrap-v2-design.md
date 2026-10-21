# Guided Bootstrap v2 — Designentwurf

Stand: 2026-10-21
Status: Richtung im Chat vom Owner bestätigt; schriftlicher Entwurf zur Durchsicht. Keine Umsetzungsfreigabe.
Basis: main, 566f56c (Standard v2.1.0, Produktstand PACKAGE_BUILT)
Vorgänger: [Designentwurf v1](2026-10-19-guided-bootstrap-design.md)

## Ziel

Wer die Desktop-App von ChatGPT oder Claude und ein passendes Abo hat, gibt eine Startdatei in einen neuen Chat im Code-Bereich der App und wird von dort aus begleitet. Die Einrichtung hilft **nur** dabei, die essenziellen Dienste einzurichten und zu verknüpfen: GitHub, die für wichtig befundenen Skills und die Einstellungen der KI. Danach laufen die Abläufe bis Merge und Deploy flüssig, ohne dass der Nutzer noch viel einstellen muss.

Alles, was die KI selbst erledigen kann, erledigt sie. Sie erklärt dabei immer begleitend, was sie gerade tut und warum. Unsere Arbeitsweise (zum Beispiel „Frage X von Y“ mit Antwortmöglichkeiten und Empfehlung) gilt danach automatisch in jeder Sitzung.

## Warum ein zweiter Entwurf

Die v1-Einrichtung hat 18 Schritte und eine 746 Zeilen lange `START_HIER.md`. Sie geht vom Nullzustand aus (Agent installieren, vom Chat in die App umziehen, Stand von Hand sichern) und baut das lokale Merge-Gate früh ein. Das ist deutlich kleinteiliger als das Zielbild des Owners.

## Owner-Entscheidungen vom 2026-10-21

1. **Voraussetzung:** Desktop-App und Abo sind vorhanden. Gestartet wird im Code-Bereich (Codex bzw. Claude Code).
2. **Umfang:** nur Einrichtung und Verknüpfung der essenziellen Dienste, dazu die Erklärung, wie man ein Projekt in ChatGPT bzw. Claude anlegt, und eine kritische Server-Beratung.
3. **Windows:** nativ als Standard. WSL 2 nur, wenn ein Projekt das Merge-Gate übernimmt.
4. **Start im reinen Chat:** kurzer Hinweis, wie man in den Code-Bereich wechselt. Keine ausführliche Installationsführung.
5. **Arbeitsweise:** Berechtigungen, persönliche Regeln und das erste Projekt nach dem Projektstandard. Die Einstellungen werden erklärt und gemeinsam eingerichtet.
6. **Merge und Deploy „Leicht“** als Standard für neue Projekte (Abschnitt „Merge-/Deploy-Modell“). Zeigt sich ein Projekt als zu fehleranfällig, prüft die KI die strengeren Varianten gemeinsam mit dem Nutzer.
7. **Lieferform:** eigenes Plugin `ai-bootstrap` mit drei Skills, dazu kurze persönliche Regeln, die in jeder Sitzung geladen werden.

## Einstieg

`START_HIER.md` wird ein kurzer Starter (Ziel: unter 150 Zeilen). Er:

1. begrüßt und sagt, dass Fragen jederzeit im selben Chat möglich sind;
2. stellt fest, ob die KI Befehle auf dem Computer ausführen kann. Wenn nicht: ein kurzer Hinweis, wie man die Datei im Code-Bereich der App öffnet, dann Ende;
3. installiert das Plugin `ai-bootstrap` aus diesem öffentlichen Repository in einer festen Version (Claude: eigener Marktplatz aus dem Repository; Codex: Skill-Ordner, Weg wird in GB2-01 belegt);
4. übergibt an den Skill `einrichtung`.

Für den Fall, dass die Installation scheitert, trägt die Startdatei eine eingebettete Kurzfassung des Ablaufs. Das ZIP bleibt als Offline-Weg und enthält das Plugin.

## Ablauf (Skill `einrichtung`)

Steuerung wie in v1: prüfen → erfüllt? kurz bestätigen : erklären und selbst ausführen bzw. genau eine Nutzeraktion anleiten → erneut prüfen → Stand still sichern. Nur der aktuelle Schritt wird gezeigt.

| # | Schritt | Inhalt | Wer macht was |
|---|---|---|---|
| 1 | `start` | Begrüßung; im Hintergrund Betriebssystem, App, Git und GitHub CLI feststellen | KI |
| 2 | `github` | In zwei bis drei Sätzen erklären, was GitHub ist und warum wir es brauchen (Sicherung, Versionen, Zusammenarbeit mit der KI). Konto mit Zwei-Faktor-Anmeldung, GitHub CLI anmelden, Git für GitHub einrichten, Name und E-Mail für Commits. Fehlt Git oder GitHub CLI, installiert die KI es nach Freigabe. | Konto anlegen und anmelden: Nutzer. Alles andere: KI |
| 3 | `skills` | Superpowers und `ai-bootstrap` installieren, mit Probeaufruf prüfen. Vorhandene gleichwertige Skills behalten. | KI; Slash-Befehle tippt der Nutzer, wo die KI sie nicht ausführen kann |
| 4 | `arbeitsweise` | Persönliche Regeln (Abschnitt „Arbeitsweise“) und Einstellungen der KI gemeinsam einrichten (Abschnitt „Einstellungen“), jeweils mit Erklärung. | KI schlägt vor und setzt um; Nutzer entscheidet das Profil (eine Frage) |
| 5 | `projekt` | Skill `projekt-start`: erklären, wie man ein Projekt in ChatGPT bzw. Claude anlegt und mit dem GitHub-Repository verbindet; Repository anlegen oder vorhandenes übernehmen; Projektstandard anwenden; Server-Beratung, nur wenn das Projekt danach klingt. | gemeinsam |
| 6 | `probelauf` | Eine kleine echte Änderung: eigener Branch, Prüfung, Push, Pull Request, Merge nach „Leicht“, Ergebnis zurücklesen. Damit ist der ganze Ablauf einmal real gelaufen. | KI, Nutzer schaut zu |
| 7 | `fertig` | Kurzer Abschluss: was eingerichtet ist, was offen ist, wie man das nächste Projekt startet | KI |

**Entfällt gegenüber v1:** `context` und `path` (stecken in `start`), `local_agent` und `handover` (App ist vorhanden), `save_state` als eigener Schritt (die KI sichert still unter `~/.ai-bootstrap/`), `git`, `github_account`, `github_cli`, `git_identity` (stecken in `github`), `chat_github` (Teil von `projekt`).

**Optional, nur auf Wunsch oder Projektentscheidung:** `python` und `wsl` (nur für das Merge-Gate), Merge-Gate, Dev-Box/Server.

## Skills (Plugin `ai-bootstrap`)

| Skill | Wann er greift | Inhalt |
|---|---|---|
| `einrichtung` | Startdatei, „Einrichtung fortsetzen“, Wiederaufnahme eines gespeicherten Stands | Ablauf oben, Zustand, Wiederaufnahme |
| `projekt-start` | neues Projekt anlegen, bestehendes Projekt übernehmen, Frage nach Server/Dev-Box | Projekt in ChatGPT/Claude anlegen und verbinden, Projektstandard, Server-Beratung |
| `arbeitsweise` | jede Entscheidung, Planung, Umsetzung bis Merge und Deploy | Frageformat, begleitendes Erklären, erst prüfen dann fragen, Merge-/Deploy-Modell, Eskalationsregel |

Skills greifen nur, wenn ihr Thema passt. Was **immer** gelten soll, steht deshalb zusätzlich kurz in der persönlichen Regeldatei (`~/.claude/CLAUDE.md` bzw. `~/.codex/AGENTS.md`). Die Datei verweist für Details auf den Skill `arbeitsweise`. Vorhandene Einträge des Nutzers bleiben erhalten; die KI ergänzt einen klar markierten Block.

Superpowers bleibt die Grundlage für Brainstorming, Planung, Fehlersuche, Testen und Git-Isolation. `ai-bootstrap` ergänzt nur, was dort fehlt, und dupliziert nichts.

Aufbau im Repository (Vorschlag, Details in GB2-01/03):

```
.claude-plugin/marketplace.json        Marktplatz „ai-bootstrap“ aus diesem Repository
plugins/ai-bootstrap/
  .claude-plugin/plugin.json
  skills/einrichtung/SKILL.md
  skills/projekt-start/SKILL.md
  skills/arbeitsweise/SKILL.md
templates/PERSONAL_RULES.md            Block für die persönliche Regeldatei
```

Das `SKILL.md`-Format ist bei beiden Anbietern gleich (A12, C10). Codex liest persönliche Skills aus `~/.agents/skills`; ob Codex auch einen eigenen Plugin-Marktplatz aus einem Repository installieren kann, wird in GB2-01 belegt.

## Arbeitsweise (immer aktiv)

- Einfaches Deutsch, kurze Sätze; Fachbegriffe beim ersten Bedarf in einem Satz erklären.
- Begleitend erklären: vor jeder Aktion ein Satz, was jetzt passiert und warum; danach ein Satz zum Ergebnis.
- Erst prüfen, dann fragen. Nichts fragen, was die KI selbst feststellen kann; nichts erneut fragen, was schon entschieden ist.
- Entscheidungen einzeln im Format:
  ```text
  Frage X von Y: FRAGE
  1. Option – ein Satz
  2. Option – ein Satz
  Empfehlung: Option N, weil …
  Du kannst auch eine eigene Antwort schreiben.
  ```
- Selbst ausführen, was die KI darf und kann. Anmeldungen, Passwörter, Zwei-Faktor-Codes, Zahlungen und Kontoanlagen macht immer der Nutzer.
- Probleme erst behandeln, wenn sie auftreten; dann konkrete Ursache und genau eine Lösung.

## Einstellungen der KI

Die KI erklärt jede Einstellung in einem Satz und richtet sie gemeinsam mit dem Nutzer ein. Ziel ist, dass der Ablauf bis Merge und Deploy ohne weitere Rückfragen läuft, aber gefährliche Befehle technisch gesperrt bleiben.

- **Berechtigungsprofil** (eine Frage, Empfehlung „Standard“):
  - Claude Code: `defaultMode` ausdrücklich setzen (`acceptEdits` für „Standard“, `auto` für „Selbstständig“), Sandbox an, wo unterstützt (nicht auf nativem Windows, A10).
  - Codex: Freigabe- und Sandbox-Modus passend dazu (Werte belegt GB2-01).
- **Erlaubt ohne Rückfrage:** Branch anlegen, Commit, Push des eigenen Task-Branches, Pull Request anlegen, Merge des eigenen Pull Requests über `gh pr merge` mit den Bedingungen aus dem Merge-Modell.
- **Weiter technisch gesperrt:** Force-Push, direkter Push auf `main`, Löschen fremder Branches, `bypassPermissions`.
- **Deploy:** wird nicht in der persönlichen Einrichtung freigeschaltet, sondern im Schritt `projekt`, sobald das Projekt ein Deploy-Ziel hat. Dort wird der Befehl als erlaubter Befehl eingetragen.

Bestehende Einstellungen liest die KI zuerst vor, spricht nur Abweichungen an und erhält alle anderen Einträge.

## Merge-/Deploy-Modell „Leicht“

Gilt als Standard für neue Projekte, die über die Einrichtung entstehen.

**Merge.** Die KI merged einen Pull Request selbst, wenn alle Bedingungen erfüllt sind:

1. Es ist ihr eigener Task-PR in diesem Projekt (kein fremder PR, kein Fork).
2. Die Projektprüfungen sind lokal grün gelaufen.
3. Direkt vor dem Merge ist der Branch auf dem aktuellen `main`. Hat sich `main` seit der Prüfung geändert, holt die KI den neuen Stand, prüft erneut und merged erst dann.
4. Der Merge bindet sich an den geprüften Commit (`gh pr merge --match-head-commit <sha>`), damit nichts Ungeprüftes mitgeht.
5. Es ist keine Entscheidung offen und nichts im PR verlangt ausdrücklich eine Freigabe.

Punkt 3 und 4 fangen den Hauptnachteil gegenüber dem Gate (Änderung von `main` zwischen Prüfung und Merge) weitgehend ab, ohne Python oder WSL.

**Deploy.** Hat ein Projekt ein Deploy-Ziel, stehen Ziel und Befehl in den Projektregeln. Nach einem Merge deployed die KI dann selbst und prüft das Ergebnis (zum Beispiel, ob die Seite antwortet). Für eine Produktion mit echten Nutzerdaten fragt sie **einmal pro Projekt** ausdrücklich, ob automatisches Deploy dort gelten soll.

**Eskalation.** Die KI beobachtet Anzeichen, dass „Leicht“ für ein Projekt nicht reicht: `main` ist nach einem Merge kaputt, ein Deploy muss zurückgerollt werden, derselbe Fehler kommt wieder, oder mehrere Aufgaben laufen parallel. Dann spricht sie das an und prüft mit dem Nutzer im Frageformat die strengeren Varianten (Merge-Gate, Freigabe pro Merge oder Deploy). Sie stellt nicht still selbst um.

**Bestehende Projekte.** Strengere vorhandene Regeln bleiben, insbesondere ein integriertes Merge-Gate. Ein Widerspruch wird als CONFLICT vorgelegt, nie still überschrieben.

**Verhältnis zum Standard.** Bisher gilt: Merge nur über das Gate oder eine eigene Freigabe, Deploy folgt nie aus dem Standard. „Leicht“ ändert das für neue Projekte und muss deshalb sichtbar in Standard, Manifest, Gate-Richtlinie und CHANGELOG stehen. Weil sich damit der Befugnisvertrag ändert, schlägt dieser Entwurf **Version 3.0.0** vor (statt 2.2.0); für bestehende Projekte ändert sich nichts, solange sie nicht ausdrücklich wechseln.

## Projekt anlegen (Skill `projekt-start`)

1. **Erklären, was ein Projekt in der App ist:** In ChatGPT und Claude gibt es „Projekte“ als Ordner für Chats, Dateien und Anweisungen. Die KI zeigt, wie man eines anlegt und mit dem GitHub-Repository verbindet, damit Planungschats den Code lesen können. Bedienwege und Grenzen belegt GB2-01.
2. **Repository:** neu anlegen (privat als Empfehlung) oder vorhandenes übernehmen.
3. **Projektstandard:** `UNIVERSAL_PROJECT_BOOTSTRAP.md` gilt unverändert, also Bestandsaufnahme, Abgleich, Regeln auf eigenem Branch. Neu: Das Merge-/Deploy-Modell wird hier festgehalten.
4. **Server-Beratung:** nur, wenn das Projekt danach fragt (dauerhaft laufende Dienste, Zeitpläne, eigene Datenbank, Webseite mit Backend). Die KI fragt zuerst kritisch, ob ein Server wirklich nötig ist, und nennt die einfachere Alternative (eigener Rechner, Hosting-Dienst, Cloud-Agent). Sie berät nur und richtet keinen Server ein.

## Zustand

Der Einrichtungsstand bleibt eine kleine, geheimnisfreie JSON-Datei. Das Schema bekommt Version 2 mit den neuen Schritten. Ein v1-Stand wird beim Einlesen umgeschrieben: erledigte v1-Schritte zählen für den passenden v2-Schritt, veränderliche Nachweise werden wie bisher neu geprüft.

## Abnahme

- Paket- und Strukturtests (Plugin, Skills, Marktplatz-Datei, Startdatei, Zustand v2 mit Migration).
- Dialogfälle D1–D9 auf den neuen Ablauf angepasst, plus neue Fälle: Server-Beratung rät von unnötigem Server ab; Probelauf mit Merge nach „Leicht“; `main` ändert sich vor dem Merge; Eskalation nach kaputtem `main`.
- Linux real vom Nullzustand in einer VM für beide Anbieter, einschließlich echter Plugin-Installation aus dem Repository.
- macOS, Windows und Webchat bleiben NOT_TESTED, bis jemand sie auf echten Geräten durchläuft. Dafür entsteht eine einfache Testanleitung für Nicht-Techniker.

## Nicht Bestandteil

- Server oder Dev-Box einrichten (nur Beratung).
- Bestehende Projekte umstellen (deine Gate-Projekte bleiben, wie sie sind).
- Konten anlegen, Abos kaufen oder wechseln im Namen des Nutzers.
- Hosted CI wieder einschalten.
