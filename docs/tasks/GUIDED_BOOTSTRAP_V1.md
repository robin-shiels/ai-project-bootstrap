# GUIDED_BOOTSTRAP_V1 — Claude-Auftragskette

> **For agentic workers:** Use superpowers:executing-plans, sofern verfügbar, um diese Kette schrittweise auszuführen. Gleichwertige verfügbare Fähigkeiten sind zulässig. Die Kette selbst verlangt keine Subagenten.

**Goal:** Aus dem vorhandenen Projekt-Bootstrap eine anfängerfreundliche, geführte und überprüfte Ersteinrichtung mit echter Startdatei und vollständigem ZIP fertigstellen.

**Architecture:** Gemeinsamer zustandsabhängiger Dialog und portabler Einrichtungsstand; Anbieterwege für ChatGPT/Codex und Claude/Claude Code; Betriebssystemwege für macOS, Windows und Linux. Der bestehende Projekt-Bootstrap bleibt der wiederverwendete Projektkern. Ein deterministischer Paketbau liefert einen eigenständig nutzbaren Einstieg.

**Tech Stack:** Markdown für KI-Anweisungen und Anleitungen; JSON für portablen Zustand und prüfbare Matrizen; vorhandenes Python 3.12+/Standardbibliothek für Paketbau und Tests. Zusätzliche Laufzeitabhängigkeiten nur bei belegtem Bedarf; keine zusätzliche Serverpflicht.

**Spec:** ../superpowers/specs/2026-10-19-guided-bootstrap-design.md
**Ist-Abgleich:** ../superpowers/specs/2026-10-19-guided-bootstrap-gap-audit.md

## Auftrag und Autorisierung

Dieser Auftrag wird durch den manuellen Startprompt in Claude gestartet. Er umfasst Recherche, Detailplanung, Umsetzung, Dokumentation, Paketbau und Abnahme aller unten genannten Teilaufträge. Nicht nach jeder Phase fragen, ob es weitergehen soll. Diese Kette ist ein zusammenhängender Auftrag; Teilaufträge sind keine separat zu startenden Empfehlungen.

Im eigenen isolierten Task-Branch darf Claude nach relevanten Prüfungen committen, diesen Branch pushen und den zugehörigen PR erstellen/aktualisieren. Zuerst Repository-Regeln und vorhandene Arbeit prüfen; andere Branches/Worktrees nicht verändern. PR #4 ist die vorgelagerte Planung und darf nicht stillschweigend als implementiert oder integriert behandelt werden.

Kein automatisches Merge, direkter main-Push, Force-Push, Release-Tag, öffentliches Release, Deployment, Kauf, Abowechsel, Kontenerstellung im Namen des Auftraggebers oder Änderung realer Kontoberechtigungen durch diesen Entwicklungsauftrag. Die spätere Einrichtungsdatei führt Nutzer im jeweiligen konkreten Kontext durch ihre eigenen Entscheidungen.

Gate-Portabilität darf innerhalb der unten festgelegten Sicherheitsinvarianten implementiert werden. PRs mit Gate-/Konfigurationsänderungen bleiben nach bestehendem Vertrag von Selbstmerge ausgeschlossen und benötigen Owner-Integration mit Gate-Nachweisen. Keine fehlende Plattformprüfung oder Berechtigung durch Lockerung des Gates umgehen.

Gewöhnliche technische Detailentscheidungen anhand vorhandener Regeln und offizieller Quellen selbst treffen und begründen. Nur echte neue Produkt-, Sicherheits-, Kosten- oder Befugnisentscheidungen vorlegen; in unserem Frageformat. Bei einem Blocker alle unabhängigen autorisierten Arbeiten fortsetzen und den konkreten Fortsetzungsschritt dauerhaft sichern.

## Verbindliche Nutzeranforderungen

- Beide KI-Wege und alle drei Betriebssysteme gleichwertig ab der ersten fertigen Version.
- Eigener Computer als Standard; Dev-Box nur optional.
- Einmalige persönliche Grundeinrichtung, danach Wiederverwendung und projektbezogener Abgleich.
- Einfaches Deutsch, kleine aktuelle Schritte, Fachbegriffe bei ihrem ersten tatsächlichen Bedarf erklären.
- Einstieg erklärt ausdrücklich: Fragen und Probleme können jederzeit im selben Chat geklärt werden; anschließend wird an derselben Stelle fortgesetzt.
- Entscheidungen einzeln: „Frage X von Y: FRAGE“, Antwortmöglichkeiten, Empfehlung und kurze Begründung; eigene Antworten zulassen.
- X/Y gilt für einen bekannten Fragenblock, keine erfundene Gesamtzahl. Änderungen des Blocks nachvollziehbar machen.
- Vorhandenes selbst prüfen, soweit tatsächlich zugänglich; bekannte Entscheidungen nicht wiederholen.
- Nur den aktuellen Stand behandeln. Bei Erfolg kurz bestätigen und weitergehen. Keine prophylaktischen Fehleranleitungen, hypothetischen Probleme oder Liste aller technischen Alternativen ausgeben.
- Ein eingetretenes Problem konkret diagnostizieren; passende Lösung anleiten.
- Möglichst selbst ausführen, aber tatsächliche Werkzeug-, Host- und Befugnisgrenzen beachten.
- Fortschritt vor GitHub-Einrichtung und nach Chatwechsel exportierbar und überprüfbar erhalten.
- Echte herunterladbare START_HIER.md plus vollständiges versioniertes ZIP. Eine Beschreibung dieser Dateien ersetzt die Dateien nicht.
- Kein falsches „fertig“: Funktionsnachweis und verbleibende Lücken benennen.
- Bestehende Projektregeln, durable Aufträge/Ergebnisse, Prüfungen, Übergaben und Gate-Vertrag semantisch bewahren.

## Basis und Inventur

Planung basiert auf main 11d642bcfd8de138da81ac11d7e5fedcc9c0028d und Planungsbranch docs/guided-bootstrap-design. Vor Start aktuellen main, PR #4, Regeln, offene PRs und Abhängigkeiten neu prüfen. Die Spezifikation und den Audit vom Planungsbranch lesen, falls noch nicht auf main. Eigene Umsetzung auf aktuellem main in separatem Branch aufbauen; Planungsunterlagen gezielt übernehmen, ohne fremde Änderungen zu überschreiben.

Auf der geprüften Basis: Standard v2.0.0, Changelog mit Gate-Patch v2.0.1; 38 Gate-Tests auf Linux/Python 3.12 bestanden. Das ist Ausgangsevidenz, keine aktuelle Prüfung und kein plattformübergreifender Installationsnachweis.

## Vorgesehene Dateien und Verantwortlichkeiten

- START_HIER.md: erzeugter, eigenständig hochladbarer Einstieg mit eingebetteten nötigen Anweisungen; keine bestehende GitHub-Verbindung zum Start verlangen.
- onboarding/ENTRY.md: bearbeitbare gemeinsame Start- und Dialogsteuerung.
- onboarding/STATE.schema.json und onboarding/STATE.example.json: versioniertes Zustandsformat und synthetisches Beispiel.
- onboarding/providers/chatgpt-codex.md und onboarding/providers/claude-code.md: gleichwertige Anbieterwege mit aktuellen Quellen.
- onboarding/platforms/macos.md, windows.md, linux.md: nachgewiesene Installations-/Prüfschritte je Betriebssystem.
- onboarding/OPTIONAL_DEVBOX.md: erst bei tatsächlichem Bedarf verwendeter Erweiterungsweg.
- onboarding/ACCEPTANCE.md: prüfbare gemeinsame Abnahmefälle.
- scripts/build_bootstrap_bundle.py: reproduzierbarer Dateibau ohne Netzwerkzugriff.
- tests/test_bootstrap_bundle.py: Paket-, Referenz-, Konsistenz- und Zustandsprüfungen.
- docs/research/GUIDED_BOOTSTRAP_V1_SOURCE_MATRIX.md: datierte offizielle Quellen, unterstützte Oberflächen, Plattformwege und technische Entscheidungen.
- docs/results/GUIDED_BOOTSTRAP_V1_STATUS.json: aktueller Fortschritt der Kette und Fortsetzungsposition.
- docs/results/GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md: Nachweise, Einschränkungen und abschließender Lieferstatus.
- docs/results/GUIDED_BOOTSTRAP_V1_COVERAGE.md: jede Audit-Zeile und jedes Abnahmeziel mit Umsetzungspfad und Nachweis.
- Bestehende README, Standard, Manifest, Codex-Prompt und Discovery-Vorlage: widerspruchsfrei integrieren, keinen konkurrierenden Regelkern erzeugen.
- Gate-Skript und Tests: nur für den belegten plattformgerechten Weg ändern; Verantwortung und Schnittstellen bei Bedarf gezielt aufteilen.

Die Dateistruktur ist ein konkreter Startpunkt. Technisch nötige Anpassungen vor Umsetzung im Detailplan dokumentieren; Zuständigkeiten und Abnahmedeckung erhalten.

## Review Focus

1. Reiner Web-/Mobilchat hat keinen Zugriff auf den Computer: keine Host-Prüfung oder Installation behaupten.
2. ZIP oder externe Referenz ist im gewählten Chat nicht lesbar: Einzelstartdatei muss trotzdem den echten ersten Schritt tragen.
3. Nach Konto-/Chatwechsel ist eine alte Berechtigung ungültig: Zustand bewahren, Zugriff neu prüfen.
4. Windows/macOS weichen vom Linux-Gate ab: keine Sicherheitsprüfung überspringen und keine bloße Simulation als Plattformnachweis ausgeben.
5. Erfolgreiche Verbindung oder Zwischenfrage: keinen Fehlertext ausgeben beziehungsweise keinen Neustart der Einrichtung auslösen.

---

## GBOOT-01 — Quellen, unterstützte Wege und vollständige Deckung

**Abhängigkeit:** keine. **Lieferung:** belastbare technische Grundlage und Ausführungsplan.

- [ ] Repository/Branch/Regeln inventarisieren und Basis-SHAs dokumentieren.
- [ ] Alle 18 Audit-Zeilen und zehn Abnahmeziele als Einträge in COVERAGE.md anlegen; jedem die folgenden Teilaufträge und späteren Nachweise zuordnen.
- [ ] Mit aktuellen offiziellen Quellen die Voraussetzungen beider KI-Wege und aller OS prüfen: Konto/Abo, unterstützte Oberflächen, Dateiupload, GitHub-Verbindung, lokale Werkzeuge, Hostzugriff, Skills, Sandbox/Berechtigungen.
- [ ] Fähigkeiten des bestehenden Manifests konkreten verfügbaren Implementierungen zuordnen. Superpowers und seine Installationswege prüfen; benötigte Fähigkeiten begründet auswählen. Kein identisches Produkt auf beiden Wegen erzwingen, falls tatsächliche Verfügbarkeit abweicht.
- [ ] Den Begriff „Two-Sandbox“ auflösen, ohne einen universellen Modus zu erfinden. Profile anhand realer Funktionen und unserer gewünschten Arbeitsweise beschreiben.
- [ ] Lokalen Gate-Weg für Windows/macOS/Linux festlegen. Native Anpassung oder lokale Kompatibilitätsumgebung anhand Sicherheit, Anfängeraufwand und offizieller Unterstützung auswählen. Eine Kompatibilitätsschicht darf keinen separaten Server voraussetzen.
- [ ] SOURCE_MATRIX.md mit Quellen-URL, Datum, belegter Aussage, Anbieter/OS, Grenzen und gewähltem Weg schreiben.
- [ ] Internen Detailplan mit konkreten Dateien, Prüfungen und Schnittstellen vervollständigen; echte unresolved Owner-Entscheidungen klären, sonst direkt fortfahren.

**Abnahme:** Jede der sechs Kombinationen besitzt einen begründeten vollständigen Standardweg oder einen konkret belegten Blocker. Keine Scheingleichwertigkeit durch Weglassen wesentlicher Fähigkeiten.

## GBOOT-02 — Gemeinsamer Dialog und wiederaufnehmbarer Zustand

**Abhängigkeit:** 01. **Lieferung:** direkt verwendbare gemeinsame KI-Anweisungen und portabler Einrichtungsstand.

**Zustandsvertrag:** schema_version, bundle_version, provider_path, platform, current_step, decisions, verifications, blockers, next_action. Unbekannte Werte ausdrücklich als unbekannt behandeln. Verifications tragen Schritt-ID, Zeitpunkt, Geltungsbereich und Quelle des Nachweises; unterscheiden z. B. tatsächliche Werkzeugprüfung und Nutzerbestätigung. Keine Tokens, Passwörter, Schlüssel, private Testdaten oder vertraulichen Protokolle im portablen Zustand.

- [ ] Schema und synthetisches Beispiel vor Implementierung mit Tests pinnen: Pflichtfelder, unbekannte Werte, ungültige Typen, unterstützte Version, keine geheimen Werte in Beispieldateien. JSON-Schema-Dokument und tatsächliche Validierung auseinanderhalten.
- [ ] ENTRY.md um den vollständigen Steuerungsablauf ergänzen: prüfen → nächsten fehlenden Schritt erklären → ausführen/anleiten → Nachweis → Zustand sichern.
- [ ] Dialogfälle in ACCEPTANCE.md mit konkreten erwarteten Antworten festlegen: nackter Start; bereits verbunden; eigene Antwort; neue Unterfrage; Zwischenfrage; tatsächlicher Fehler; Chatwechsel; fehlender Hostzugriff.
- [ ] Vor GitHub-Verfügbarkeit einen tatsächlich nutzbaren Export-/Wiederaufnahmepfad implementieren. Nach Chatwechsel Variablen wie Zugriff und Installationsstand erneut prüfen, Entscheidungen erhalten.
- [ ] Keine binäre „installiert“-Behauptung aus einem gespeicherten Dateinamen ableiten; Fähigkeit muss im jeweiligen Laufzeitkontext belegt sein.
- [ ] Dialogfälle anhand der tatsächlichen Startanweisungen prüfen; rein strukturelle Texttests zusätzlich kennzeichnen.

**Abnahme:** Kein Routine-Neustart nach Zwischenfragen; keine Wiederholung bekannter Entscheidungen; keine hypothetischen Fehlerhilfen bei Erfolg; keine erfundene Hostkontrolle.

## GBOOT-03 — Zwei vollständige Anbieterwege und drei Plattformwege

**Abhängigkeit:** 01–02. **Lieferung:** ausführbare/anleitbare End-to-End-Einrichtung ab fehlender persönlicher Umgebung.

- [ ] Beide Anbieterdateien und drei OS-Dateien aus den geprüften Quellen umsetzen; jede Entscheidung und Aktion an den gemeinsamen Schritt-/Zustandsvertrag anbinden.
- [ ] GitHub-Konto, benötigte Verbindungen, lokale Git-Identität und Authentifizierung, tatsächliche Ausführungsumgebung und benötigte Werkzeuge einrichten beziehungsweise gezielt anleiten und prüfen.
- [ ] Chat-/Repository-Zugriff, lokales Git und Ausführung auf dem Nutzercomputer ausdrücklich getrennt nachweisen.
- [ ] Skill-Auswahl, Installation/Registrierung und Funktionsprüfung umsetzen; schon verfügbare gleichwertige Fähigkeiten erhalten.
- [ ] Berechtigungs-/Sandboxprofile verständlich im aktuellen Schritt erklären. Wesentliche Freigabeentscheidungen durch den Nutzer treffen lassen; keine globale Admin-/Vollzugriffsvorgabe aus dem Ziel „Autonomie“ ableiten.
- [ ] Optionalen Dev-Box-Weg ergänzen, aber im lokalen Standardablauf nur bei Bedarf zeigen.
- [ ] Für jede Kombination konkrete Checks mit erwarteter Wirkung und Nachweis dokumentieren; schon vorhandene Umgebung muss Schritte überspringen können.
- [ ] Anbieter-/OS-Anweisungen auf Schlüsselbegriffe, Zustandsreferenzen, Quellen und vollständige Pfadkombinationen prüfen.

**Abnahme:** Vollständigkeit beider Wege auf allen drei OS nachgewiesen; kein bloßer CLAUDE.md-Verweis als Ersatz für Claude-Ersteinrichtung.

## GBOOT-04 — Lokales Gate auf allen unterstützten Wegen

**Abhängigkeit:** 01 und relevante Teile aus 03. **Lieferung:** lokaler Prüfgate-Weg pro OS unter unverändertem Sicherheitsvertrag.

- [ ] Regressionsfälle für den in 01 gewählten Weg vor Codeänderung festlegen und ausführen.
- [ ] Linux-/POSIX-Annahmen konkret behandeln: fcntl, /proc/meminfo, Prozess-/UID-Prüfung, Prozessgruppen, systemd und Ressourcenlimits.
- [ ] Minimal nötige plattformbezogene Implementierung oder vollständige lokale Kompatibilitätsanleitung erstellen; bestehende Linux-Referenz nicht pauschal umschreiben.
- [ ] Ressourcen-, Isolations-, Timeout-, Log- und CAS-Prüfungen erhalten. Fehlende Schutzfunktion führt zu benanntem Blocker, nicht stiller Deaktivierung.
- [ ] Vorhandene 38 Gate-Tests erneut ausführen, neue Portabilitätsfälle hinzufügen und auf jedem unterstützten tatsächlichen Ausführungsweg prüfen.
- [ ] Gate-Vertragsänderungen, falls technisch unvermeidbar, vor Umsetzung zur konkreten Owner-Entscheidung vorlegen. Keine automatische Selbstintegration.
- [ ] Im Handoff Codeprüfung, Simulation, reale Betriebssystemprüfung und reales GitHub-Gate jeweils getrennt nachweisen.

**Abnahme:** Kein Pfad wird als einsatzbereit markiert, wenn sein verbindliches Gate dort nicht funktioniert oder wesentliche Prüfungen fehlen.

## GBOOT-05 — Projektkern integrieren und versionierte Downloaddateien bauen

**Abhängigkeit:** 02–04. **Lieferung:** START_HIER.md und vollständiges ZIP als echte nutzbare Artefakte.

**Bauschnittstelle:** python3 scripts/build_bootstrap_bundle.py --output-dir <dir>.
**Erzeugnisse:** START_HIER.md, AI-Bootstrap-<version>.zip, SHA256SUMS und ein Manifest im ZIP mit Standard-/Paketversion, vollständigem Quellcommit und enthaltenen Dateien. Identische Quellen und Bauparameter müssen byte-identische Artefakte ergeben.

- [ ] Pakettests vor Bauimplementierung anlegen: alle Pflichtdateien enthalten, keine fehlenden internen Referenzen, keine privaten Daten/Arbeitsstände, keine Pfadtraversierung, Prüfsummen korrekt, deterministischer Wiederholungsbau.
- [ ] Alle nötigen Einstiegskomponenten in die einzelne Startdatei einbetten. Sie darf den ersten Schritt nicht von einem bereits verbundenen Repository oder ungeprüfter automatischer ZIP-Lesbarkeit abhängig machen.
- [ ] Vollständiges ZIP mit genau derselben Startdatei, benötigten Anleitungen, Standard und Vorlagen bauen. Keine Netzwerkabfrage beim Paketbau.
- [ ] Versionsquelle vereinheitlichen und Migration gemäß tatsächlichem Änderungsumfang dokumentieren; bestehende v2.0.0/v2.0.1-Darstellung konsistent auflösen.
- [ ] README/Standard/Manifest/Übergabevorlagen abgleichen: persönliche Einrichtung vor Projektkern, Claude und Codex gleichwertig, neue Projekte und bestehende Projekte erhalten ihre Regeln.
- [ ] Nach abgeschlossenen Quellcommits aus sauberem Quellstand bauen; Manifest-SHA muss exakt den verwendeten Quellstand benennen. Generierte Dateien/Prüfsummen nicht in einen Selbstreferenz-Zyklus zwingen.
- [ ] Beide Artefakte mit konkretem Download-/Dateipfad bereitstellen. Ein lokaler Build ohne zugängliche Dateien genügt nicht. Falls die Umgebung Anhänge nicht unterstützt, auf dem Task-Branch einen dokumentierten tatsächlichen Downloadweg vorbereiten; öffentliche Release-Veröffentlichung separat behandeln.

**Abnahme:** Einzeldatei und ZIP existieren tatsächlich, stimmen miteinander überein und starten vom vorgesehenen Nullzustand.

## GBOOT-06 — End-to-End-Abnahme und Nachbesserung

**Abhängigkeit:** 05. **Lieferung:** ehrliche Readiness-Matrix und geschlossene Befunde.

Sechs Zeilen: ChatGPT/Codex × macOS/Windows/Linux und Claude/Claude Code × macOS/Windows/Linux.
Pro Zeile mindestens: genaue OS-/Toolversionen, Ausgangszustand, Paketversion/Quell-SHA, Datum, Prüfer, Konto-/Verbindungsweg, Skills, Berechtigungen, Gate, Probelauf, Ergebnis, Nachweisreferenz und Blocker.

- [ ] Paket-/Regressionsprüfungen und gemeinsame Dialogfälle vollständig durchführen.
- [ ] Pro Kombination einen tatsächlich verfügbaren sauberen oder dokumentiert vorbereiteten lokalen Testweg vom Einfügen der Startdatei bis zum Projekt-Probelauf prüfen.
- [ ] Probelauf umfasst: Repository lesen, isolierte Teständerung, relevante Prüfung, vereinbarten Commit-/Push-Ablauf und Rücklesen des exakten Ergebnisses. Nur freigegebene Testressourcen verwenden; kein main-/Produktionszugriff.
- [ ] Erfolgsweg, tatsächlich auftretender Fehler, Zwischenfrage und Wiederaufnahme prüfen. Bei fehlender realer Störung einen kontrollierten Testfall als solchen kennzeichnen.
- [ ] Gefundene Fehler im autorisierten Umfang beheben und betroffene Nachweise erneut durchführen.
- [ ] Alle 18 Audit-Zeilen und zehn Design-Abnahmeziele auf tatsächlich erstellte Dateien und Nachweise zurückführen; kein leeres „done“ aus Dateiexistenz.
- [ ] Fehlende Geräte/Konten als NOT_TESTED oder BLOCKED dokumentieren; reproduzierbare noch auszuführende Schritte liefern. Benutzer nur für tatsächlich notwendige Aktionen einbeziehen, keine erfundenen Plattformnachweise.

**Abnahme:** Keine offenen wesentlichen Funktions-/Sicherheitsfehler. Die globale Aussage „alle sechs Wege einsatzbereit“ erfordert reale Nachweise aller sechs Wege. Ein Paket kann gebaut sein, während die Gesamtfreigabe noch blockiert ist.

## GBOOT-07 — Finale Prüfung, Übergabe und Lieferstatus

**Abhängigkeit:** 06. **Lieferung:** überprüfbare Dateien, Ergebnisbericht und veröffentlichter eigener Task-Branch.

- [ ] Aktuellen main auf Änderungen und Überschneidungen prüfen, eigene Änderungen abgleichen, betroffene Checks erneut ausführen.
- [ ] Finalen Diff auf Scope, Geheimnisse, persönliche Angaben, fremde Änderungen und Dokumentationswidersprüche prüfen. Das Repository ist öffentlich.
- [ ] Vollständige Ergebnisse einschließlich Quellen, Tests, Exitcodes, Plattformmatrix, Fehlern und Blockern in ACCEPTANCE.md und STATUS.json sichern.
- [ ] Quellstand, Pakete und SHA256SUMS abgleichen; mit neuen Änderungen ungültig gewordene Builds/Nachweise erneuern.
- [ ] Eigenen Branch committen/pushen, exakten Remote-HEAD und sauberen eigenen Worktree belegen; PR erstellen oder aktualisieren.
- [ ] Finale Übersicht liefern: was funktioniert, was fehlt, konkrete Downloads, Quellcommit, Prüfungen, noch nötige Owner-Aktionen, tatsächlicher Integrationszustand.

**Zwei unabhängige Statusachsen:**
- Repository: LOCAL_COMPLETE / DONE_ON_BRANCH / INTEGRATED gemäß bestehendem Standard.
- Produkt: PACKAGE_BUILT / READY_FOR_ACCEPTANCE / READY / BLOCKED.

READY heißt: Dateien zugänglich, alle sechs Wege tatsächlich geprüft, alle wesentlichen Befunde geschlossen. DONE_ON_BRANCH allein bedeutet weder READY noch in main integriert. Eine finale Freigabe/Veröffentlichung darf nicht durch einen Abschlussbericht vorgetäuscht werden.

## Fortschritts- und Fortsetzungsvertrag

STATUS.json führt pro Teilauftrag: id, state (pending/running/done/blocked), dependencies, result_files, validation, blockers. Dazu source_base, branch, last_commit und next_action. Nach sinnvoll abgeschlossenen Abschnitten aktualisieren, insbesondere vor Chatwechsel oder Blocker. Keine künstlichen Zwischenstopps für Routinefortsetzung.

Wenn die Kontextlänge oder Umgebung einen weiteren Claude-Chat erfordert, einen kurzen Fortsetzungsprompt mit exaktem Repository, Branch, Commit, Auftragsdatei und aktuellem STATUS.json liefern. Keine wesentlichen Ergebnisse ausschließlich im Chat halten.

## Selbstprüfung dieses Auftrags

Alle Bereiche des Ist-Abgleichs sind zugeordnet: Projektkern/Regeln/Übergaben → 05; Inventur und Arbeitsweise → 02–03; Frageform und situationsbezogener Dialog → 02; Konten/lokale Umgebung/Skills/Sandbox/Dev-Box → 01 und 03; Gleichwertigkeit und Gate → 03–04; Zustand/Wiederaufnahme → 02; Lieferdateien → 05; reale Funktionsnachweise → 06; dauerhafte Übergabe → 07.

Nicht Bestandteil: unbegrenzte Automationsplattform, verpflichtender Server, Produktionsintegration, fremde Projekte re-bootstrapen oder kostenpflichtige Zusatzdienste anschaffen.
