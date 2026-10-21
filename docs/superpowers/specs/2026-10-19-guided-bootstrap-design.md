# Guided Bootstrap — Designentwurf

Stand: 2026-10-19
Status: Zielbild im Chat bestätigt; schriftlicher Entwurf zur Durchsicht. Keine Implementierungsfreigabe.
Basis: main, 11d642bcfd8de138da81ac11d7e5fedcc9c0028d

## Ziel

Einsteiger mit einem KI-Abo sollen eine echte Datei in ihren KI-Chat einfügen und von dort aus bis zu einer funktionierenden persönlichen Arbeitsumgebung und einem eingerichteten Projekt begleitet werden. Der Ablauf erklärt nur den jeweils aktuellen Schritt und erledigt innerhalb der vorhandenen Möglichkeiten und Befugnisse möglichst viel selbst.

Die Arbeitsweise des bestehenden Bootstrap gilt bereits während der Einrichtung, nicht erst im fertigen Projekt.

## Bestätigte Anforderungen

- ChatGPT mit Codex und Claude mit Claude Code von Anfang an gleichwertig unterstützen.
- macOS, Windows und Linux von Anfang an gleichwertig unterstützen.
- Der eigene Computer ist der Standard; eine Dev-Box ist eine optionale Erweiterung.
- Persönliche Grundeinrichtung einmal durchführen, für weitere Projekte wiederverwenden und ihren aktuellen Zustand erneut prüfen.
- Neue Projekte einrichten und bestehende Projekte unter Wahrung ihrer Regeln abgleichen.
- Anfängerfreundlich erklären, Fachbegriffe erst bei Bedarf mit einfacher Erklärung einführen.
- Entscheidungen einzeln im Format „Frage X von Y: FRAGE“ stellen, mit Antwortmöglichkeiten, klarer Empfehlung und kurzer Begründung; eigene Antworten zulassen.
- Y bezieht sich auf den tatsächlich bekannten Fragenblock. Entstehen durch Antworten weitere Fragen, die Anpassung offen erklären.
- Feststellbare Tatsachen selbst prüfen; bereits geklärte Fragen nicht erneut stellen.
- Nur den aktuellen Zustand und den nächsten relevanten Schritt erklären.
- Funktioniert eine Verbindung, kurz bestätigen und fortfahren. Keine vorsorglichen Fehleranleitungen oder hypothetischen Alternativen ausgeben.
- Probleme erst behandeln, wenn sie auftreten; dann konkret diagnostizieren und passende Hilfe geben.
- Bereits zu Beginn ausdrücklich vermitteln, dass Fragen und Probleme jederzeit im selben Einrichtungs-Chat besprochen werden können.
- Nach einer Zwischenfrage am erhaltenen Einrichtungsstand fortsetzen.
- Einrichtung unterbrechen und mit einem gespeicherten, überprüfbaren Stand fortsetzen können.
- Abschluss durch tatsächliche Funktionsprüfung belegen.

## Vorgeschlagene Lieferform

Eine herunterladbare START_HIER.md als primärer Einstieg; zusätzlich ein versioniertes AI-Bootstrap.zip mit derselben Startdatei und den vollständigen benötigten Anleitungen und Vorlagen.

Dies ist die empfohlene Ausgestaltung des bestätigten Wunsches nach einer echten Datei. Dateinamen und genaue Paketstruktur sind noch keine ausdrücklich beschlossene technische Schnittstelle.

Die Startdatei muss ohne vorhandenes GitHub-Konto oder eingerichtete Repository-Verbindung benutzbar sein. Der Nutzer muss weder die gesamte Dokumentation lesen noch selbst den passenden Betriebssystem- oder Anbieterpfad auswählen können. Technische Varianten bleiben intern, bis der aktuelle Zustand sie erfordert.

Das Paket enthält genug Einstiegskontext für den ersten Chat auch ohne Repository-Zugriff. Weitere Hilfen werden bedarfsgerecht geladen oder aus dem Paket verwendet. Welche Chatoberflächen Anhänge beziehungsweise ZIP-Inhalte tatsächlich lesen können, muss vor Umsetzung verifiziert werden; es darf keine automatische Verfügbarkeit behauptet werden.

## Aufbau

### Gemeinsame Ablaufsteuerung

Zustand feststellen → nächsten fehlenden Schritt auswählen → kurz erklären → selbst ausführen oder konkrete Nutzeraktion anleiten → Ergebnis prüfen → Fortschritt sichern.

Einleitung sinngemäß:

> Ich begleite dich Schritt für Schritt durch die Einrichtung. Du kannst jederzeit hier im Chat Fragen stellen oder sagen, wenn etwas unklar ist oder anders aussieht. Wir klären das gemeinsam und setzen danach an derselben Stelle fort.

Die Ausgabe zeigt nur die aktuelle Aufgabe. Ein technischer Gesamtzustand darf intern vollständig sein, ohne als lange Checkliste im Anfängerfluss aufzutauchen.

### Persönliche Arbeitsumgebung

Ermitteln, welche KI-Anwendung, welches Betriebssystem, welche Konten und welche tatsächlichen Werkzeuge und Zugriffe vorhanden sind. Daraus den passenden Weg ableiten.

Bei Bedarf durch Kontoanlage, GitHub-Verbindung, lokale Git-Einrichtung, Ausführungsumgebung, erforderliche Fähigkeiten/Skills und Berechtigungen führen. Keine Dev-Box für den Standardweg verlangen.

Anbieter und Betriebssysteme erhalten passende Adapter für ihre tatsächlichen Funktionen. Gleichwertigkeit bedeutet gleiche Abnahmeziele und gleichwertige Unterstützung, nicht identische Befehle, Einstellungen oder behauptete Funktionsgleichheit.

### Projektebene

Den bestehenden UNIVERSAL_PROJECT_BOOTSTRAP.md wiederverwenden und integrieren: Bestandsaufnahme, semantischer Regelabgleich, projektspezifische Klärung, verbindliche Anweisungen, dauerhafte Aufträge/Ergebnisse und überprüfbare Übergabe.

Bestehende Beschränkungen und die Trennung von Branch-Veröffentlichung, Integration und Deployment bewahren. Eine Einrichtung ändert keine Befugnisse stillschweigend.

### Fähigkeiten und Berechtigungen

Das heutige skills/SKILL_MANIFEST.md beschreibt Fähigkeiten und installiert ausdrücklich nichts. Die Erweiterung muss deshalb benötigte Fähigkeiten einer tatsächlich unterstützten Installation oder einem überprüften Ersatz zuordnen.

Superpowers ist ein genannter Kandidat, aber weder eine bestimmte vollständige Skill-Liste noch ein Installationsweg ist bereits beschlossen. Quellen, Versionen, tatsächliche Registrierung und Funktionsnachweise sind vor Auswahl zu prüfen.

Der im Gespräch erwähnte „Two-Sandbox-Modus“ ist ein noch zu klärender Begriff, keine bestätigte plattformübergreifende Einstellung. Konkrete Sandbox- und Freigabemodelle pro Laufzeit recherchieren, erklären und anhand des gewünschten Arbeitsumfangs festlegen. Keine pauschale Vollzugriffs- oder Admin-Vorgabe ableiten.

Kontenbestätigung, Anmeldung und notwendige persönliche Freigaben dürfen konkrete Nutzeraktionen erfordern. Ein Abo oder eine Markdown-Datei ersetzt weder fehlende Werkzeuge noch Zugriff auf den Computer.

### Fortschritt und Wiederaufnahme

Ein portabler Einrichtungsstand enthält Paketversion, gewählten Pfad, nachgewiesene Schritte, getroffene Entscheidungen, noch offene Schritte und aktuelle Fortsetzungsposition. Keine Kennwörter, Tokens oder sonstigen Geheimnisse speichern.

Vor GitHub-Verfügbarkeit muss der Stand ohne Repository gesichert werden können. Den passenden Speicher- und Exportweg im technischen Entwurf bestimmen. In einem neuen Chat den Stand einlesen und veränderliche Voraussetzungen erneut prüfen; kein versprochenes automatisches Gedächtnis.

## Bezug zum heutigen Stand

Gelesen auf der Basisrevision:
- README.md
- UNIVERSAL_PROJECT_BOOTSTRAP.md
- CHANGELOG.md
- skills/SKILL_MANIFEST.md
- templates/PROJECT_DISCOVERY.md

Der heutige Standard setzt ein zugängliches Projekt voraus und regelt vor allem Projektabgleich und Arbeitsweise. Die geführte Konten-/Computer-Ersteinrichtung, konkrete Skill-Installation, plattformgerechte Anfängerpfade und das Downloadpaket sind durch diese Dokumente noch nicht nachgewiesen.

Der Standard nennt v2.0.0; das Changelog dokumentiert bereits v2.0.1 für technische Gate-Korrekturen. Dieser Entwurf ändert weder diese Versionen noch den bisherigen Gate-Vertrag.

## Vor der Umsetzung zu belegende technische Punkte

Für beide Anbieter und alle drei Betriebssysteme anhand aktueller offizieller Quellen prüfen:
- unterstützte Chat- und Ausführungsoberflächen sowie Voraussetzungen und Abogrenzen;
- Konto-, Repository- und lokale Git-Verbindungen;
- notwendige Downloads und Installation/Registrierung ausgewählter Skills;
- tatsächliche Berechtigungs- und Sandboxmodelle;
- Verfügbarkeit des bestehenden lokalen Gates und seiner Abhängigkeiten im jeweiligen Standardweg;
- Dateiupload, Paketlesen und Fortsetzung ohne vorausgesetzten Repository-Zugriff.

Quellen und Prüfdatum im dauerhaften technischen Ergebnis festhalten. Diese Liste ist Arbeit für die Vorbereitung, kein vorab an Anfänger auszugebender Fragenkatalog. Bei nicht gleichwertig realisierbaren Funktionen die konkrete Abweichung zur Entscheidung vorlegen, statt Gleichwertigkeit zu behaupten.

## Abnahmeziele

Für jede der sechs Kombinationen aus Anbieterweg und Betriebssystem:
1. Einstieg mit der Datei ohne eingerichteten GitHub-Zugriff nachvollziehbar.
2. Nur fehlende Schritte werden angeboten; bereits funktionierende Einrichtung wird erkannt.
3. Jede tatsächliche Entscheidung nutzt Frage X von Y, Optionen und Empfehlung.
4. Erfolgreiche Schritte erzeugen keine hypothetischen Fehlerhinweise.
5. Eine Zwischenfrage wird beantwortet; anschließend wird korrekt fortgesetzt.
6. Ein auftretendes Problem wird konkret behandelt.
7. Unterbrechung und Wiederaufnahme erhalten Entscheidungen und prüfen veränderlichen Zustand.
8. Erforderliche Werkzeuge, Zugriffe und Fähigkeiten werden tatsächlich überprüft.
9. Ein kleiner, innerhalb vereinbarter Rechte ausgeführter Projekt-Probelauf belegt die benötigten Datei-, Prüf- und Git-Schritte; gegebenenfalls verwendete Testartefakte werden dokumentiert.
10. Abschluss benennt nur belegte Ergebnisse und verbleibende Blocker; ein teilweise eingerichtetes System gilt nicht als fertig.

Dialogprüfungen, Paketprüfungen und tatsächliche Plattformprüfungen getrennt ausweisen. Simulierte Abläufe beweisen keine erfolgreich getestete Installation auf dem jeweiligen Betriebssystem.

## Abgrenzung und nächster Schritt

Dieser Entwurf hält die bestätigte Produktausrichtung und den vorgeschlagenen Aufbau fest. Er installiert keine Software, erstellt keine Konten, ändert keine Anbieterfreigaben und verändert den aktiven Bootstrap nicht.

Nach Durchsicht des schriftlichen Entwurfs folgt ein konkreter Umsetzungsplan einschließlich aktueller Quellenprüfung, Paketaufbau und Nachweisstrategie. Erst danach beginnt die Implementierung. Änderungen am lokalen Gate oder dessen Befugnissen sind kein impliziter Teil dieser Erweiterung.
