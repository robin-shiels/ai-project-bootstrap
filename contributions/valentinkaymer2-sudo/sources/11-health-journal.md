# S11: Quellenmaterial

Auszüge aus dem eigenen Projekt-Skill. Setup, Client, Verbindung und Beispiele ausgelassen. API-Felder dienen hier der Beurteilung eines projektspezifischen Ablaufs; ohne Serververtrag nicht ausführbar.

```markdown
## Reichweite und Auslöser

Nutze ausschließlich den aktiven, tatsächlich zugänglichen Chat oder Inhalte, die der Nutzer ausdrücklich bereitstellt. Suche keine Gesprächsarchive, Browserprofile oder fremde Plattformen ab. Dieser Skill ist kein Hintergrunddienst. Telegram verarbeitet ein separater dauerhafter Worker; Recaps erzeugt ein Scheduler.

Eindeutig relevant: „Heute nicht gefrühstückt“, „Ich habe heute Reis gegessen“, „Ich habe heute Kniebeschwerden“, ausdrücklich durchgeführtes Training, tatsächliche Einnahme oder persönliche Rückmeldung zum Wochenrecap. Nicht relevant: „Wie entsteht Muskelkater?“, ein Rezept, ein Zitat, ein Freund mit Schmerzen oder „Morgen will ich trainieren“. Negation ist kein positiver Befund. Ein ausdrücklich berichtetes ausgelassenes Frühstück ist dagegen ein zulässiger Nutzerbericht.

Bei einer anderen Hauptaufgabe nicht ständig unterbrechen. Einen relevanten eindeutigen Nutzerbericht knapp erfassen und zur Hauptaufgabe zurückkehren; bei unklarer Relevanz eine unaufdringliche „Ins Tagebuch“-Option anbieten. Keine Vermutung zu Alkohol, Urlaub, Diagnose, Unteressen oder Trainingserfolg ergänzen. Flug ist nicht Urlaub. Fehlend ist unbekannt.

## Ablauf

1. Prüfe, dass es eine persönliche tatsächliche Aussage oder explizit zu übernehmender Inhalt ist. Übertrage nur die notwendige Passage, nicht den ganzen Chat.
2. Ermittle die ursprüngliche Aussagezeit mit Offset und persönliche Zeitzone. „Gestern“ bezieht sich darauf, nicht auf eine spätere Verarbeitung. Ist der ursprüngliche Zeitpunkt unbekannt, keine Tageszuordnung erfinden; um Datum bitten oder als zeitlich unbekannte ausdrückliche Notiz speichern.
3. Vergib eine stabile `source_id` für dieselbe Chat-Aussage (z. B. aktuelle zugängliche Nachrichten-ID). Bei Retry dieselbe ID verwenden. `provenance` enthält nur eine notwendige verfügbare Referenz, keine erfundene Chat-URL.
4. Rufe `submit` mit JSON über stdin auf. `mode=unspecified` für Extraktion; `mode=note` ausschließlich für bewusst als Notiz abgelegten Inhalt. `today_meal` nur bei ausdrücklicher Nutzerwahl. Keine Foto-/Körperdaten mit diesem Textwerkzeug übertragen.
5. Frage bei Bedarf den zurückgegebenen Eingang mit `get EVENT_ID` ab. Verarbeitung ist asynchron. Ein angenommener Eingang ist noch kein bestätigter Tagebucheintrag. Bewahre Erkenntnisart (Bericht/Messwert/Schätzung/Vermutung) getrennt vom Workflow.
6. Rückfragen nur über die konkrete serverseitige `question_id` beantworten. Bei mehreren offenen Vorgängen niemals das letzte „Ja“ zuordnen. Biete Stimmt, Ändern, Überspringen, Nicht speichern, Rückgängig an. Keine Antwort bedeutet keine Bestätigung. Serverpräferenzen für Pause, Ruhezeiten und höchstens eine gebündelte proaktive Nachfrage/Tag respektieren; direkte notwendige Fragen und Wochenreview bleiben getrennt.
7. Abschluss knapp mit gespeichertem Eingangsstatus/ID oder konkreter Einrichtungsgrenze. Ein bestätigter Schätzwert bleibt Schätzung. Ein geplanter Schritt bleibt geplant.
```
