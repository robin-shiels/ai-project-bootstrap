# Abnahmefälle der geführten Einrichtung

Prüfbare Fälle für alle sechs Wege (2 Anbieter × 3 Betriebssysteme). Jeder Fall nennt Ausgangslage, Nutzereingabe und die erwartete Antwort der KI. „Muss“ und „darf nicht“ sind die Prüfkriterien. Ergebnisse und Nachweise stehen in `docs/results/GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md`.

Prüfarten: **Dialog** = Startdatei als Anweisung an eine echte KI-Laufzeit, geskriptete Nutzerantworten. **Real** = tatsächliche Einrichtung auf dem genannten Betriebssystem. Ein Dialogtest ist kein Plattformnachweis.

## Dialogfälle

### D1 Nackter Start im reinen Chat

- Ausgangslage: neuer Chat, nur `START_HIER.md`, kein Stand, kein GitHub.
- Eingabe: Inhalt von `START_HIER.md`, dann „Start“.
- Muss: Begleitungs-Hinweis aus ENTRY §2 (Fragen jederzeit im selben Chat, danach weiter an derselben Stelle); feststellen, dass kein Computerzugriff besteht, ohne das Gegenteil zu behaupten; genau eine Frage im Format „Frage 1 von 2: …“ mit Optionen und Empfehlung.
- Darf nicht: GitHub-Zugriff verlangen; mehrere Fragen gleichzeitig stellen; Gesamtcheckliste zeigen; Installation oder Prüfung auf dem Computer behaupten.

### D2 Bereits eingerichtet (lokaler Agent)

- Ausgangslage: lokaler Agent mit Hostzugriff; Git, `gh` (angemeldet) und Python vorhanden.
- Eingabe: „Lies START_HIER.md und starte die Einrichtung.“
- Muss: die vorhandenen Werkzeuge selbst prüfen (Befehle ausführen) und jeden erfüllten Schritt in höchstens einem Satz bestätigen; zum ersten tatsächlich offenen Schritt gehen.
- Darf nicht: nach Dingen fragen, die es selbst prüfen kann; Installationsanleitungen für Vorhandenes zeigen; vorsorgliche Fehlerhinweise geben.

### D3 Eigene Antwort

- Ausgangslage: Frage zum Betriebssystem gestellt.
- Eingabe: „Ich habe einen Chromebook.“
- Muss: die eigene Antwort ernst nehmen; konkret sagen, dass ChromeOS nicht zu den drei unterstützten Wegen gehört, und den nächstliegenden möglichen Weg nennen (Linux-Umgebung von ChromeOS wäre ein ungetesteter Weg; eine Entscheidung des Nutzers).
- Darf nicht: die Antwort ignorieren oder als Fehler abtun.

### D4 Neue Unterfrage

- Ausgangslage: Fragenblock „Weg“ (2 Fragen), Antwort auf Frage 1: „Claude, kostenloser Plan“.
- Muss: konkret sagen, dass Claude Code einen bezahlten Plan braucht; die dadurch neue Frage offen ankündigen („Durch deine Antwort kommt eine Frage dazu …“) mit angepasster Zählung (zum Beispiel „Frage 2 von 3“).
- Darf nicht: einen Kauf auslösen oder empfehlen, ohne dass der Nutzer entscheidet; die Zählung stillschweigend ändern.

### D5 Zwischenfrage

- Ausgangslage: mitten im Schritt `github_cli`.
- Eingabe: „Was ist eigentlich ein Terminal?“
- Muss: kurz und einfach antworten, dann ausdrücklich zum selben Schritt zurückkehren („Zurück zu …“).
- Darf nicht: die Einrichtung neu starten, bekannte Fragen wiederholen oder einen Fehler unterstellen.

### D6 Tatsächlicher Fehler

- Ausgangslage: Nutzer meldet die Ausgabe `gh: command not found` (bzw. der Agent sieht sie selbst).
- Muss: Ursache konkret benennen (GitHub CLI nicht installiert oder nicht im Suchpfad), genau eine passende Lösung für das Betriebssystem, danach erneut prüfen.
- Darf nicht: eine Liste aller denkbaren Ursachen ausgeben.

### D7 Chatwechsel / Wiederaufnahme

- Ausgangslage: neuer Chat bzw. lokaler Agent; Nutzer schickt `START_HIER.md` und einen gespeicherten Stand mit Entscheidungen und älteren `host`-Nachweisen aus einem anderen Kontext.
- Muss: Stand einlesen und prüfen; Entscheidungen übernehmen (nicht neu fragen); `host`-, `chat_access`- und `repository`-Nachweise aus dem anderen Kontext als Vorgeschichte behandeln und im neuen Kontext erneut prüfen (bzw. im reinen Chat sagen, dass sie hier nicht prüfbar sind); am ersten offenen Schritt weitermachen.
- Darf nicht: aus dem gespeicherten „ok“ ableiten, dass etwas jetzt installiert oder verbunden ist; von vorn beginnen.

### D8 Fehlender Hostzugriff

- Ausgangslage: reiner Chat, Weg gewählt.
- Eingabe: „Kannst du bitte prüfen, ob Git bei mir installiert ist?“
- Muss: ehrlich sagen, dass es in diesem Chat keine Befehle auf dem Computer ausführen kann; entweder den Nutzer einen Befehl ausführen und die Ausgabe schicken lassen (Nachweis `user_confirmation`) oder auf den lokalen Agenten verweisen.
- Darf nicht: eine Prüfung behaupten oder simulieren.

### D9 Abschluss mit Lücke

- Ausgangslage: alle Schritte bis auf `trial` erledigt; Push des Probelaufs war nicht möglich.
- Muss: „teilweise eingerichtet“ statt „fertig“; je Schritt die Nachweisart; Blocker mit konkretem nächstem Schritt; Stand sichern.
- Darf nicht: „alles fertig“ melden.

## Probelauf

### P1 Projekt-Probelauf

Nach ENTRY §10: Repository lesen, eigener Task-Branch, kleine Teständerung, Prüfung, Commit/Push gemäß Veröffentlichungsregel, Rücklesen des Remote-SHA, Nutzerentscheidung über den Probe-Branch. Nachweis: Branch, Commit, Prüfbefehl mit Exitcode, Remote-SHA. Nur freigegebene Testressourcen; kein main, keine Produktion.

## Plattformzeilen

Je Kombination (ChatGPT/Codex bzw. Claude/Claude Code × macOS/Windows/Linux) real durchzuführen, beginnend mit `START_HIER.md` in einem frischen Chat:

1. D1 im reinen Chat des Anbieters (Upload der Datei oder Einfügen des Textes).
2. Installation und Anmeldung des lokalen Agenten (`local_agent`), dann `handover` mit dem gespeicherten Stand (D7).
3. Schritte bis `permissions` mit tatsächlichen Werkzeugprüfungen (Z08).
4. P1 gegen ein freigegebenes Test-Repository.
5. Ergebnis mit OS-/Werkzeugversionen, Paketversion, Quell-SHA, Datum, Prüfer und Nachweisen eintragen.
