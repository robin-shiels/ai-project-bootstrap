# Extraktion und Vergleich der eigenen Workflow-Quellen

**Datum:** 30.09.2026
**Beitrag:** `valentinkaymer2-sudo`
**Baseline:** `robin-shiels/ai-project-bootstrap`, Bootstrap v1.1.0, `main@217b4b3ccd75557f707a627df87c2495e36cd35c`
**Eigener Branch:** `contributions/valentinkaymer2-sudo-workflow-sources`
**Status:** Quellenextraktion und Vorschläge zur Beurteilung; keine Standardübernahme.

## 1. Auftrag und tatsächlich untersuchte Umgebung

Der aktuelle direkte Nutzerauftrag umfasst die Extraktion unserer eigenen Regeln und Skills, ihre öffentliche Bereinigung, Vergleich mit vorhandenen Repository-Inhalten sowie Commit/Veröffentlichung nur auf dem eigenen Branch. Er autorisiert keine Änderung bestehender Bootstrap-Regeln, keinen Merge, Release oder Deployment und keine automatische Installation von Vorschlägen.

Ein neuer lokaler Checkout wurde geklont, `main` gefetcht und per Fast-forward synchronisiert. Die GitHub-Verbindung weist den Handle `valentinkaymer2-sudo` und Schreibrecht auf dem Repository aus. Der eigene Branch wurde am oben genannten Basiskommit lokal und remote angelegt. In der untersuchten `main`-Dateiliste existieren keine repository-eigenen `AGENTS.md` oder `CONTRIBUTING.md`, keine Runtime und keine `SKILL.md`-Pakete. README, Standard, Manifest, Vorlagen und passende Forschungs-/Ergebnisabschnitte wurden gelesen. Die geltenden Sitzungs- und Nutzeranweisungen bleiben maßgeblich.

Zusätzlich wurde der veröffentlichte [Vergleichsrahmen V1](https://github.com/robin-shiels/ai-project-bootstrap/blob/c918dfb24faba6cc3f8c5406b3c3150b01c72d58/research/CONTRIBUTION_COMPARISON_FRAMEWORK_V1.md) gelesen. Er liegt auf `research/contribution-comparison-preparation`, nicht auf der untersuchten `main`. Er dient als Vergleichshilfe und erteilt keine Handlungsberechtigung. Dessen verlinkte private Auditquellen und Pilotpakete wurden für diesen Beitrag nicht erneut geprüft.

## 2. Quellenklassen und Praxisnachweise

[SOURCE_OVERVIEW.md](SOURCE_OVERVIEW.md) und [sources.json](sources.json) enthalten je Quelle Herkunft, Stand, Zweck, Regeln, Grenzen und ein konkretes **synthetisches** Anwendungsbeispiel mit Gegenfall.

| Klasse | Zahl | Aussagegrenze |
| --- | ---: | --- |
| Eigene Skillanweisungen | 10 | Geschriebene Vorgaben und aktueller Katalog; meist keine fachliche Ausführung in diesem Audit. |
| Mit Codex bereitgestellte Skillanweisungen | 3 | Lokal gelesen; fremde Originaltexte/-ressourcen nicht veröffentlicht. |
| Eigenes Hilfsskript | 1 | Unveränderter exportierter Quelltext und künstliche Funktionsprobe. |
| Workflow-, Projekt- und Betriebsdokumente | 10 | Aktuelle Texte bzw. genannte Abschnitte; historische Testberichte bleiben zugeschriebene Berichte. |
| Aktiver Gesprächskontext | 1 | Sichtbarer Auftrag und einzelne Toolschritte; keine Archiv- oder Vollzugriffsaussage. |

Die 25 Quellen sind keine 25 unabhängigen Evaluierungen. Sie stammen aus derselben Nutzerumgebung und überschneiden sich semantisch. Die zehn eigenen Skills sind im aktuellen Katalog sichtbar; dadurch werden Fähigkeiten weder in anderen Chats noch bei anderen Personen installiert. Es wird kein Nutzen in Prozent, gesparte Laufzeit oder Kostenbetrag behauptet.

| Evidenz-ID | Tatsächlich beobachtet | Grenze |
| --- | --- | --- |
| E01 | Im aktuellen Auftrag: relevante Akten/Skillanweisungen gelesen, Repository direkt geklont und synchronisiert, GitHub-Identität/Schreibrecht geprüft, eigener Branch am Basiskommit angelegt. | Belegt diesen Ablauf, keine Langzeitwirkung und keine fremden Projekte. |
| E02 | Die erfassten Skillquellen existieren und sind im aktuellen Sitzungskatalog verfügbar. | Verfügbarkeit ist keine erfolgreiche Ausführung, frische Installation oder funktionierende externe Integration. |
| E03 | Im zugänglichen Modellwahl-Follow-up: Lernschleife gelesen, kleine globale Regel ergänzt, Änderung zurückgelesen und dem Nutzer erklärt. | Kein automatischer Modellwechsel, Vergleichsbenchmark oder Einsparnachweis. |
| E04 | Das eigene unveränderte Excel-Hilfsskript an einer synthetischen Mappe auf Formelerkennung, Cachefehler, Scanlimit und unveränderte Eingabedatei geprüft; tatsächliche Ergebnisse in [VALIDATION.md](VALIDATION.md). | Keine Neuberechnung und keine Zusage zur Erhaltung komplexer Office-Funktionen. |

Die Quellen zur Skillinstallation berichten frühere Erstellung; die Betriebsakte berichtet frühere Tests. Diese Rückblicke werden nicht zu unabhängiger Direktbeobachtung aufgewertet. Die veröffentlichten Artefakte sind an den Beitragscommit gebunden; private Originale sind für externe Leser nicht unabhängig zugänglich.

## 3. Verhaltenskandidaten und Baseline-Abgleich

Die Klassifikation beschreibt die Abdeckung durch die **unveränderte v1.1.0-Baseline**, keine Adoption. `MISSING` bedeutet nur, dass kein gleich konkretes Verhalten im untersuchten Standard steht; es begründet keine Pflicht zur Ergänzung. `OUTDATED` wurde nicht vergeben: aktuelle Dateizeitstempel allein belegen keine bessere Praxis. Dispositionen sind Empfehlungen. Die [maschinenlesbaren Kandidaten](candidates.json) erfassen Auslöser, Handlung, Ergebnis, Autoritätsgrenze, Fehlerfall, Belege und Aufwand.

| ID / Verhalten | Quellen | Baseline / Klassifikation | Mehrwert und Reichweite | Belege / Aufwand | Empfehlung |
| --- | --- | --- | --- | --- | --- |
| C01 Quellen, Zugriff und tatsächlichen Stand unterscheiden | S01, S02, S18, S22–S25 | [Inventar](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#inventory-first), [Manifest](../../skills/SKILL_MANIFEST.md) / EQUIVALENT | Belegt den bestehenden Ansatz anhand getrennter Chats, Dateien, Tools und Logins. | E01/E02; geringer zusätzlicher Aufwand. | Baseline behalten, Beispiele anbieten. |
| C02 Bereits autorisierte Arbeit fortführen; Folgeempfehlung separat behandeln | S01, S13, S17, S22 | [Autorität](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#authority-and-owner-boundary), [Empfehlung](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#recommendation-only-exception) / EQUIVALENT | Vermeidet wiederholte Routinefreigaben und automatische neue Aufgaben. | E01; keine neue Grundregel nötig. | Baseline behalten. |
| C03 Knappe offene Themen plus maßgebliche Detailakte | S01, S09, S18, S19 | [Aktueller Stand](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#current-work-overview) / MISSING für sitzungsübergreifenden persönlichen Index | Hilft bei mehreren Projekten über getrennte Sitzungen; sparsame Auslöser und Nachfassgrenzen erforderlich. | E01 belegt Einstieg, nicht langfristige Erinnerungswirkung; moderater Pflegeaufwand. | Optional anbieten. |
| C04 Skill-Lernschleife aus realen wiederkehrenden Abläufen | S01, S03, S24 | [Skillpflege](../../skills/SKILL_MANIFEST.md#skill-authoring--maintenance--optional-until-needed) / MISSING für konkreten Lern-/Duplikatcheck | Ergänzt Auslöser, Gegenfall und transparente dauerhafte Änderung. | E03, nur ein Fall; geringer Aufwand pro geeignetem Anlass. | Optional adaptieren. |
| C05 Schmale Skillauslöser und sinnvolle Gegenfälle | S04, S09, S11, S16, S24 | [Skills](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#skills) / EQUIVALENT | Beispiele trennen neue Funktion/Debugging, Wissen/persönlichen Bericht und Bedienung/Sicherheitsreview. | Quelltext/Katalog; Qualität nicht automatisch bewiesen. | Beispiele anbieten, keinen zusätzlichen Router erzwingen. |
| C06 Modellberatung bei deutlicher Fehlpassung | S01, S17, S22, S23 | [Manifest](../../skills/SKILL_MANIFEST.md) / MISSING für Empfehlung | Kann Qualität, Zeit und Nutzungskosten berücksichtigen; Hauptmodell wird im T3-Thread gewählt. | E03 belegt Regeländerung; Nutzen ungemessen, Verfügbarkeit kontobezogen. | Optional anbieten; keine automatische Abwertung. |
| C07 Reproduzieren, Ursache prüfen, ursprüngliche Fehlerprobe wiederholen | S04 | [Debugging](../../skills/SKILL_MANIFEST.md#systematic-debugging--required-when-diagnosing-failures) / EQUIVALENT | Konkreter kleiner Skill statt Pflichtprozess für jede Änderung. | Quelltext/Katalog; keine frische Fehlerbehebung im Audit. | Baseline behalten, eigenes Quellenbeispiel anbieten. |
| C08 Quelle, Build, Veröffentlichung und sichtbaren Live-Stand trennen | S05, S10, S20 | [Lebenszyklus](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#completion-and-lifecycle) / EQUIVALENT | Praktischer Website-/Betriebsfall des bestehenden Lebenszyklus. | Quelltext und zugeschriebene Betriebsberichte. | Baseline behalten, optionale Live-Prüfanleitung. |
| C09 Formeltext, Cache und echte Neuberechnung unterscheiden | S06, S07 | [Verifikation](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#execution-and-verification) / MISSING für Tabellen | Verhindert die Behauptung berechneter Ergebnisse nach reinem Dateischreiben. | E04 nur für Inspector; Officeengine-Abhängigkeit. | Optional für Tabellenarbeit. |
| C10 OCR und Textprüfung am sichtbaren Seitenbild absichern | S08 | [Verifikation](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#execution-and-verification) / MISSING für PDFs | Reduziert stille Fehler bei Scans und visuell fehlerhaften Exporten. | Quelltext/Katalog; OCR-/Renderwerkzeuge erforderlich. | Optional für Dokumentarbeit. |
| C11 Erkenntnisart getrennt vom Bearbeitungsstatus erhalten | S10–S12, S15, S20 | [Provenienz](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#inventory-first) / MISSING für konkrete Datensemantik | Eine bestätigte Schätzung bleibt Schätzung; angekommen bedeutet nicht verarbeitet. | Vorgaben; domänenspezifische Umsetzung nicht erneut geprüft. | Adaptieren als optionales Datenprofil. |
| C12 Frische Messung, Wiederverwendung und abhängige Quellen unterscheiden | S12–S14 | [Research](../../skills/SKILL_MANIFEST.md#research--audit--required-capability) / MISSING für Datenerhebungszählung | Verhindert künstlich erhöhte Evidenz aus alten Daten oder Quellenkopien. | Gelesene Methode; reale Erhebungen nicht nachgeprüft. | Optional für datenbasierte Recherche. |
| C13 Unvollständiges Ranking mit Abdeckung und eigenem Evidenzgrad | S15 | [Discovery](../../templates/PROJECT_DISCOVERY.md) / MISSING für Bewertungslogik | Macht Unsicherheit sichtbar; konkrete Gewichte bleiben im Projekt. | Schriftliches Modell; Rechenimplementierung nicht geprüft. | Optionales Bewertungsmuster, vor Nutzung testen. |
| C14 Wiederherstellung isoliert prüfen und Produktionsfreigabe separat halten | S10, S20 | [Verifikation](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#execution-and-verification), [Lebenszyklus](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#completion-and-lifecycle) / MISSING für Restoreablauf | Konkrete Sicherungs-/Rückrollgrenze für datenhaltende Systeme. | Historischer Bericht, kein frischer Restore; Aufwand projektabhängig. | Optionales Betriebsprofil. |
| C15 Asynchronen Eingang, Retry und konkrete Rückfragezuordnung absichern | S11 | [Automationgrenze](../../README.md#relationship-to-automationsoftware-factories) / MISSING für diesen API-Workflow | Übertragbare Fehlermuster bei Dubletten und unklaren Antworten. | Vorgabe; Server/API/Client fehlen im öffentlichen Paket. | Projektspezifisch behalten, Muster optional beschreiben. |
| C16 Fremde Skills als Lieferkette und Inhalte als Daten prüfen | S13, S16, S17 | [Autorität](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#authority-and-owner-boundary) / MISSING für Lieferkettenprüfung | Konkrete Prüfung referenzierter Skripte/Rechte statt Vertrauen in einen Prompt. | Texte wurden vor Export gelesen; kein technischer Angriffstest. | Optional adaptieren; Policy ist kein Sandboxnachweis. |
| C17 Browserprofil und Toolverfügbarkeit pro Laufzeit prüfen | S01, S18, S21 | [Skills](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#skills) / EQUIVALENT für Verfügbarkeitsgrenze | Praktischer Beleg: gemeinsame Dateien übertragen keinen Login. | Quelle und früherer Bericht; Browser in diesem Audit nicht getestet. | Betriebsdetails projektspezifisch behalten. |
| C18 Portabilität, alte lokale Vorgaben und Plattformkonflikte auflösen | S01, S06, S08, S14, S17, S18, S20, S21 | [Reconciliation](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#inventory-first) / CONFLICT bei unveränderter globaler Übernahme | Deckt alte Modelle/Zugänge, relative Projektpfade und behauptete Werkzeugverfügbarkeit auf. | Direkter Textvergleich; Live-Lösung fehlt. | Übernahme zurückstellen, betroffene Regeln erst konkret abgleichen. |

## 4. Konkrete Unterschiede, Gegenfälle und vorgeschlagene Anpassungen

### C03–C04: Gedächtnisablage und Skill-Lernschleife

Der Bootstrap bietet dauerhafte Git-Aufträge und Ergebnisse. Unser zusätzlicher Index adressiert auch persönliche mehrstufige Angelegenheiten ohne eigenes Repository. Das ist ein optionales persönliches Profil, kein Ersatz für Git-Aufträge. Der Gegenfall ist die allgemeine Wissensfrage: weder neuer Vorgang noch Nachfasspflicht. Ablagepfad, Hinweisfrequenz und Scheduler sind getrennte Entscheidungen.

Vorschlag C04: Nach einem wiederkehrenden, nicht offensichtlichen Ablauf oder einer wesentlichen Nutzerkorrektur prüfen, ob ein vorhandener Skill gezielt verbessert werden kann. Auslöser, Nutzen und Gegenfall nennen; gewöhnliche Projektfakten in der Projektakte belassen. Dauerhafte Änderungen sichtbar erklären. E03 ist ein tatsächlicher Fall, aber kein Beleg einer autonomen kontinuierlichen Selbstoptimierung.

### C06: Modellberatung und tatsächliche Steuerung

Der lokale Ansatz empfiehlt ein passendes Modell/Reasoning nur bei erkennbarer deutlicher Fehlpassung. Er behandelt Routineaufgaben ohne zusätzlichen Modelldialog. Er bietet keine globale automatische Umschaltung oder Kontingentgarantie. Konkrete aktuell verfügbare Optionen und aktive Threadauswahl müssen bekannt sein. Explizite Nutzerwahl bleibt maßgeblich. Unteragenten werden nur verwendet, wenn sie für den Auftrag ausdrücklich vorgesehen sind; ein verfügbarer Spawnmechanismus reicht nicht.

Vorschlag: Dieses Verhalten optional als Beratung anbieten. Feste Modellnamen nicht dauerhaft in einen allgemeinen Standard schreiben. Ohne verfügbare Thread-/Kontoinformationen die Grenze nennen. Der frühere Regeländerungsfall zeigt die Umsetzung der Beratungsvorgabe, keine erzielte Einsparung.

### C09–C10: Formatbezogene Verifikation

Das allgemeine Verifikationsgebot beschreibt noch nicht den Unterschied zwischen Excel-Formeltext und berechnetem Cache oder PDF-Textebene und Seitenbild. Die beiden kleinen Profile nennen hier konkrete typische Fehlannahmen. Gegenfälle: komplexe Makromappe ohne Erhaltungstest; OCR mit plausibel aussehendem falschem Betrag.

Das beigefügte eigene Inspector-Skript liest Struktur, Formeln und Cachefehler. Es gibt eine Begrenzung des Scans aus und berechnet nichts. E04 prüft diesen engen Zweck. Officeengine, Dateityp und OCR-Abhängigkeiten müssen auf dem Zielrechner geprüft werden. Die in Originalskills geschriebenen lokalen Verfügbarkeitsaussagen dürfen nicht unverändert als allgemeine Tatsache übernommen werden.

### C11–C13: Datenprovenienz und wirtschaftliche Evidenz

Ein Workflowstatus und die Erkenntnisart sind unabhängig: Eine vom Nutzer bestätigte Schätzung bleibt eine Schätzung. Suchvolumen, beobachtete Werbung, Angebotspreis und bezahlter Verkauf beantworten verschiedene Fragen. Eine Wiederverwendung erhöht nicht die Anzahl frischer Erhebungen. Quellen desselben Ursprungs und nahe Varianten liefern keine unabhängigen Marktbestätigungen.

Das Bewertungsmuster zeigt zusätzlich Datenabdeckung und Evidenzgrad. Die unbekannt/0-Semantik, konkreten Gewichte und Statusschwellen sind projektgebunden. Gegenfall: Ein universelles Pflichtschema würde fremde Domänen falsch modellieren. Vorschlag: optionale Forschungs-/Datenprofile mit klarer Parametrisierung; zunächst Rechenbeispiel und bestehende Zielregeln prüfen.

### C14–C17: Betrieb, API und Browser

Die privaten Projekte liefern konkrete Muster für isolierte Restoreziele, deaktivierte externe Adapter, idempotente Eingänge und gezielte Rückfragen. Sie bleiben abhängig von ihren Serververträgen und Betriebsrechten. Eine Eingangsannahme bestätigt noch keine abgeschlossene Verarbeitung. Ein pauschales „Ja“ darf nicht einer beliebigen offenen Frage zugeordnet werden.

Browserprofile und Laufzeiten haben eigene Logins und Werkzeuge. Ein persistentes Volume ist kein unabhängiges Backup. Fremde Inhalte und Skills verleihen keine Berechtigung; technische Grenzen müssen gesondert geprüft werden. Diese Quellen beschreiben benötigte Kontrollen, aber dieser Audit beweist weder Isolation noch erfolgreiche Abwehr von Prompt-Injection.

### C18: Nachgewiesene Textkonflikte und unbekannter Live-Stand

| Fall | Beobachteter Unterschied | Praktische Konsequenz / derzeitige Behandlung |
| --- | --- | --- |
| S17/S18 Modellnotizen | Frühe feste Modellwahl und spätere datierte Änderungen stehen neben abweichender Zusammenfassung in der Übergabeakte. | Textzeitpunkt und spezifische Entscheidung prüfen; aktuelle Konfiguration nicht aus einem beliebigen Absatz ableiten. Live-Hermes-Modell hier ungeprüft. |
| S14 Recherchepriorität | Ältere fokussierte Priorisierung steht neben späterer ausdrücklich geänderter branchenoffener Suchstrategie. | Spätere geltende Präzisierung berücksichtigen; Gewichte separat erhalten. Keine öffentliche Kopie der bevorzugten Geschäftsprojekte. |
| S17/S18 Zugangsnotizen | Ältere Zugangszusagen stehen neben später gemeldeten Ausfällen/Umstellungen. | Frische Zugriffsevidenz erforderlich; pauschale Kalender-/Browserfähigkeit nicht versprechen. |
| S06/S08 Werkzeugverfügbarkeit | Die Originaltexte nennen auf dem Herkunftsrechner installierte Programme und feste Pythonpfade. | Für einen portablen Skill erst Abhängigkeiten prüfen/parametrisieren; ein exportierter Text installiert nichts. |
| S01 gegenüber beliebiger Agenten-/Bootstrapvorgabe | Lokale Regel erlaubt Unteragenten nur bei ausdrücklicher Aufgabenbestimmung; ein generisches Parallelrezept könnte weiter gehen. | Höher priorisierte und aktuelle lokale Grenze erhalten; keine automatische Delegation aus dem Beitrag. |
| S20 historische Startanleitung gegenüber aktuellem Betrieb | Eine alte Entwicklungsanleitung steht neben ausdrücklich ausgeschlossenen Neustart-/Produktionspfaden. | Aktuellen Dienst-/Datenbankstand vor Aktionen prüfen; keine alten Befehle aus der Quellensammlung ausführen. |

Diese Konflikte wurden dokumentiert, nicht durch globale Übernahme oder operative Änderungen gelöst. Dateimtime, hoher Score, neue Dokumentfassung und generische Skillanweisung ersetzen keine Autoritätsprüfung.

## 5. Was wir aus diesem Repository sinnvoll nutzen könnten

Die nachstehenden Vorschläge betreffen unsere eigene spätere Nutzung. Sie wurden hier nicht installiert oder global aktiviert. Das Manifest beschreibt gewünschte Fähigkeiten, keine herunterladbare Skillinstallation.

| Inhalt | Konkreter Nutzen für uns | Aufwand / Anwendungsgrenze |
| --- | --- | --- |
| [Dauerhafte Arbeitsaufträge](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#durable-git-work-orders) und [Codex-Übergabe](../../templates/CODEX_BOOTSTRAP_PROMPT.md) | Für größere Programmierprojekte vollständigen Auftrag/Ergebnis in der Projektablage halten und einen kurzen Startprompt mit exakter Referenz weitergeben. | Niedrig bis moderat; bestehende Projektakten und konkrete Freigaben einbeziehen. Kein Pflichtbootstrap für jede kleine Dateiänderung. |
| [MISSING/EQUIVALENT/OUTDATED/CONFLICT](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#inventory-first) | Skills von Freunden vor Übernahme auf tatsächliche neue Wirkung und Widersprüche prüfen; vergleichbare vorhandene Fähigkeiten erhalten. | Gering bei kleinen Skills; Skripte/Referenzen erhöhen Prüfaufwand. |
| [Projekt-Discovery](../../templates/PROJECT_DISCOVERY.md) | Neue Ideen in Ziel, Nutzer, Daten, Akzeptanz, Kosten und Grenzen konkretisieren. | Nur offene echte Entscheidungen erfragen, nicht die gesamte Checkliste mechanisch abarbeiten. |
| [Lebenszyklus und Verifikationsvertrag](../../UNIVERSAL_PROJECT_BOOTSTRAP.md#completion-and-lifecycle) | Ergänzt unsere Websiteprüfung um exakte branchbezogene Veröffentlichung und klaren Unterschied zu Integration. | Überwiegend bereits ähnlich; projektspezifische Gates erhalten. |
| [Vergleichsrahmen V1](https://github.com/robin-shiels/ai-project-bootstrap/blob/c918dfb24faba6cc3f8c5406b3c3150b01c72d58/research/CONTRIBUTION_COMPARISON_FRAMEWORK_V1.md) | Gemeinsamer Austausch mit Herkunft, Gegenfall, Nutzen, Aufwand und tatsächlichen Praxisbelegen. | Derzeit nur Forschungsbranch, keine geltende main-Regel. |

Für uns wäre zuerst der strukturierte Skillvergleich hilfreich. Für umfangreiche neue Codeaufgaben sind der dauerhafte Auftrag und die kurze Übergabe der stärkste zusätzliche Workflow. Eine vollständige globale Übernahme des Bootstrap würde vorherige Projektregeln, Publikationsrechte und Plattformgrenzen konkret abgleichen müssen.

## 6. Fehlende Quellen und Beurteilungsgrenzen

- Native ChatGPT-Projektanweisungen und nicht bereitgestellte ChatGPT-Planungschats: nicht zugänglich; keine Inhalte oder Konfiguration rekonstruiert.
- Frühere Gespräche nach dieser aktiven Sitzung und private Archive: nicht durchsucht. Ein Gesprächsrückblick ist kein Originaltoolprotokoll.
- Tatsächliche Nutzung von Skills auf anderen Rechnern, bei Freunden, in CI oder Hermes: nicht frisch geprüft.
- Vollständige health-journal-Verbindung, Client, Serververtrag und personenbezogene Eingänge: nicht exportiert und für diesen Audit nicht ausgeführt. Der Auszug ist kein funktionsfähiges Integrationspaket.
- Live-Produktionsstand, Office-Neuberechnung, OCR-Arbeit, echte Geräteanmeldung und heutige Marktkennzahlen: keine frische Funktionsprüfung im Austauschauftrag; schriftliche Anforderungen nicht als Beleg ausgeben.
- Langzeitzuverlässigkeit, Kosteneinsparung und unabhängige Evaluation: offen. Die Quellen sind korreliert und teilweise jung.
- Private Originale und exakte private Betriebsparameter sind für öffentliche Reviewer nicht einsehbar. Dafür liefern die bereinigten öffentlichen Artefakte klare Transformationshinweise und prüfbare Git-/Dateifingerprints.

## 7. Ergebnis, Prüfungen und nächste Beurteilungsgrenze

25 Quellen wurden in 18 Verhaltenskandidaten verdichtet: sechs EQUIVALENT, elf MISSING für die jeweilige konkrete optionale Ausgestaltung und ein CONFLICT bei unveränderter Übernahme. Null OUTDATED-Einstufungen und keine als allgemeiner Standard adoptierte Regel. Die einzelnen Empfehlungen bleiben bedingt und evidenzbezogen.

Die tatsächlichen Inhalts-, Quellen-, Link-, Format-, Privatsphäre-, Scope- und Skriptprüfungen stehen in [VALIDATION.md](VALIDATION.md). Commit und genaue remote SHA werden im abschließenden Handoff angegeben, damit kein selbstreferenzieller Hash in diesen Bericht eingetragen wird. Erst nach geprüfter Veröffentlichung und sauberem eigenen Checkout ist dieser Beitrag DONE_ON_BRANCH; das besagt nichts über Integration oder Deployment.

Die nächste sachliche Grenze ist die Beurteilung dieses Quellenbeitrags durch die Beteiligten. Ein späterer Skillimport oder eine Standardänderung wäre ein eigener Auftrag mit Quellen-, Rechte-, Abhängigkeits- und Konfliktprüfung.
