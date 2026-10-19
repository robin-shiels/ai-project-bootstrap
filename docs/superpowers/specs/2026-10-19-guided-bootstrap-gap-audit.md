# Guided Bootstrap — Ist-Abgleich

Datum: 2026-10-19
Prüfobjekt: ai-project-bootstrap, main = 11d642bcfd8de138da81ac11d7e5fedcc9c0028d
Zielbild: docs/superpowers/specs/2026-10-19-guided-bootstrap-design.md, Commit 68183c4cfa6107e5eb0b848bd8d91307c80d3c02
Art: Repository-Audit, keine Implementierung.

## Ergebnis

Die Arbeitsregeln für bereits zugängliche Projekte sind weitgehend als Standard und Vorlagen vorhanden. Ein technischer Baustein, das lokale Merge-/Release-Gate, ist implementiert und durch lokal erneut ausgeführte Tests belegt. Die geführte persönliche Ersteinrichtung ab einem KI-Abo, der adaptive Anfänger-Dialog und das dafür gedachte Downloadpaket fehlen im geprüften main.

Der Designentwurf auf PR #4 beschreibt diese Anforderungen, implementiert sie jedoch nicht. Ein Gesamtprozentsatz wäre irreführend: Ein dokumentierter Vertrag ist nicht dieselbe Art Fortschritt wie eine tatsächlich funktionierende Installation.

## Anforderungsmatrix

„Vorhanden als Regel“ beschreibt einen formulierten und integrierten Vertrag, keinen Nachweis, dass jeder KI-Chat ihn zuverlässig ausführt. „Fehlt“ bezieht sich auf den vollständigen Repository-Baum der Basisrevision, nicht auf erfolglose Codesuche.

| Ziel | Stand auf main | Vorhandenes und konkrete Lücke |
| --- | --- | --- |
| Neue und bestehende Projekte abgleichen | Vorhanden als Regel | UNIVERSAL_PROJECT_BOOTSTRAP.md: Inventur, vier Klassifikationen, Abgleich und erneute Anwendung. Voraussetzung ist ein zugängliches Projekt. |
| Projektziele und Arbeitsregeln festhalten | Vorhanden als Regel | Standard und PROJECT_DISCOVERY.md erfassen Ziele, Architektur, Daten, Qualität und Befugnisse. Keine Anfänger-Ersteinrichtung davor. |
| Dauerhafte Aufträge, Ergebnisse und geprüfte Übergaben | Vorhanden als Regel | Standard, Manifest und CODEX_BOOTSTRAP_PROMPT.md. Keine unabhängige Ende-zu-Ende-Prüfung des gesamten geführten Ablaufs. |
| Bestehendes prüfen und unnötige Rückfragen vermeiden | Teilweise | Regelabgleich, Erhalt gleichwertiger Fähigkeiten und nur echte Entscheidungen sind geregelt. Konto-/Computer-Inventur mit schrittweisem Einrichtungszustand fehlt. |
| Arbeitsweise ab der ersten Einrichtungsnachricht | Teilweise | Universelle Regeln existieren; ein eigenständiger Einstieg vor Repository-Zugriff fehlt. |
| Frage X von Y, Optionen und Empfehlung | Fehlt | Im neuen Design dokumentiert, im aktiven Standard kein entsprechender durchgehender Dialogvertrag und keine Dialogprüfungen. |
| Anfängerfreundliche, ausschließlich situationsbezogene Erklärungen | Fehlt | Kein geführter Dialog, der nur den aktuellen Schritt und erst tatsächlich aufgetretene Fehler erklärt. |
| Fragen im selben Chat und anschließende Fortsetzung | Fehlt | Kein ausdrücklicher Einstiegshinweis und kein definierter Fortsetzungsablauf. |
| GitHub-Konto und Verbindungen einrichten | Fehlt | README beginnt mit dem zugänglich zu machenden Repository; kein Weg ab fehlendem Konto, keine geführte Anmeldung/Verbindungsprüfung. |
| Lokalen Computer und Ausführungsumgebung einrichten | Fehlt | Gate-Rollout setzt lokale Werkzeuge und Laufzeiten voraus. Keine Anfängerinstallation für die drei Betriebssysteme. |
| ChatGPT/Codex und Claude/Claude Code gleichwertig | Teilweise | Codex-Übergabe ausführlich; CLAUDE_DEVBOX_GATE.md ist ein kurzer Gate-Verweis. Kein gleichwertiger vollständiger Claude-Einrichtungsweg. |
| macOS, Windows und Linux gleichwertig | Fehlt | Keine Anbieter-/OS-Einrichtungswege. Gate-Implementierung enthält konkrete Linux-/POSIX-Abhängigkeiten, siehe unten. |
| Eigener Computer als Standard, Dev-Box optional | Teilweise | Gate-Policy versteht „dev box“ allgemein als bewusst betriebene Entwicklungsmaschine; ein zusätzlicher Server ist damit nicht zwingend. Konkreter lokaler Anfängerweg und optionale Servererweiterung fehlen. |
| Erforderliche Skills installieren und Aktivität prüfen | Teilweise | Manifest definiert erforderliche Fähigkeiten und verlangt tatsächliche Verfügbarkeit. Es installiert ausdrücklich nichts; verbindliche Skill-Auswahl und geprüfte Installationswege fehlen. |
| Berechtigungen und Sandbox einrichten | Teilweise | Befugnisse, Einschränkungen und Gate-Isolation sind beschrieben. Anbieterbezogene geführte Einstellungen fehlen; „Two-Sandbox“ ist kein belegter universeller Modus. |
| Portabler Einrichtungsstand und Wiederaufnahme | Fehlt | Git-basierte Arbeitsstände und Handoffs existieren, aber kein persönlicher Einrichtungsstand vor GitHub, kein Export-/Importformat und kein Fortsetzungstest. |
| Startdatei und vollständiges versioniertes ZIP | Fehlt | Kein START_HIER.md, kein Paketerzeuger oder entsprechendes Lieferpaket im Baum; die Releases-API lieferte eine leere Liste. Der automatische GitHub-Quellarchivdownload ist kein kuratiertes Einrichtungspaket. |
| Funktionsnachweis der fertigen Einrichtung | Teilweise | Gate-Tests und allgemeine Abschlussregeln vorhanden; kein Einrichtungs-Probelauf oder Nachweis für die sechs Anbieter-/OS-Kombinationen. |

## Technischer Befund: Gate-Portabilität

Quelle: templates/devbox_merge_gate.py auf der Basisrevision.

- Zeile 38: import fcntl.
- LocalHost.resources(), ab Zeile 1027: liest /proc/meminfo direkt.
- Prozess-/Vorfahrenprüfung nutzt /proc.
- UID-Prüfung nutzt os.getuid().
- Prozessabbruch nutzt os.killpg().
- Optionale Ressourcenbegrenzung nutzt systemd-run; Dienstabfragen systemctl.
- Beispielkonfiguration setzt systemd_scope = true.

Damit ist die vorhandene Referenz kein belegter nativer Windows-/macOS-Weg. systemd_scope auszuschalten beseitigt insbesondere den direkten /proc/meminfo-Zugriff nicht. Für die neue Gleichwertigkeit braucht es einen belegten, bedienbaren Weg pro Betriebssystem oder eine geprüfte gemeinsame Ausführungsumgebung. Die konkrete Lösung ist noch nicht beschlossen.

Die vorhandene Gate-Isolation für fremden Code ist zudem kein vollständiger Einrichtungsweg für die Sandbox eines KI-Entwicklungsagenten.

## Ausgeführte Verifikation

Umgebung: Linux, Python 3.12.14.

Aus dem fixierten Commit wurden Gate-Skript, Tests, TOML-Beispiel und Diagnose-Workflow lokal bereitgestellt. Die Git-Blob-Hashes wurden nach dem Lauf gegen den Repository-Baum geprüft:

| Datei | Verifizierter Git-Blob |
| --- | --- |
| templates/devbox_merge_gate.py | dd95f7bc00c82af33842b76bc9309f941a8dc660 |
| tests/test_devbox_merge_gate.py | 52d9a6e95d8a1bfb58396dfe124e38756f06a318 |
| templates/devbox_merge_gate.example.toml | fe00895823d31c7241babaefd2920e4ac5abba10 |
| templates/github-actions-diagnose.example.yml | 046d3095087b219be6ad35f31f8565a1844da718 |

Befehl: python3 -m unittest discover -s tests -q
Ergebnis: 38 Tests, OK, Exit 0, 8,384 Sekunden.

Transparenz: Ein erster Lauf hatte einen Fehler, weil die lokale Dateibereitstellung jeweils eine zusätzliche Leerzeile angefügt hatte und der interne git diff --check diese beanstandete. Nach Korrektur ausschließlich der lokalen Kopien und Nachweis der exakten Blob-Identität bestand die vollständige Suite. Keine Änderung am Repository-Code.

Die Tests verwenden temporäre Git-Repositories und gefälschte GitHub-/Host-Schnittstellen. Sie beweisen weder eine reale Kontoanlage noch eine tatsächliche GitHub-Integration oder eine erfolgreiche macOS-/Windows-Installation. Es fand kein realer Merge und kein Release-/Deployment-Gate-Lauf statt.

## Quellenumfang und Grenzen

Gelesen: README.md, UNIVERSAL_PROJECT_BOOTSTRAP.md, CHANGELOG.md, skills/SKILL_MANIFEST.md, templates/PROJECT_DISCOVERY.md sowie Gate-Policy, Codex-Prompt, Rollout-Checkliste, AGENTS-/CLAUDE-Gate-Vorlagen, TOML-Beispiel, Diagnose-Workflow, Gate-Skript und Tests. Der vollständige nicht abgeschnittene main-Baum, main-Ref, PR #4 und Releases wurden per GitHub-API geprüft.

Standard/README nennen v2.0.0, CHANGELOG.md enthält v2.0.1; die technische Korrektur ist bereits auf main. Kein Befund, dass die neue Ersteinrichtung deswegen schon enthalten wäre.

Nicht geprüft: private Geräte, Kontokonfigurationen, tatsächlich installierte Skills anderer Laufzeiten oder fremde Projekt-Repositories. Anbieterfunktionen und aktuelle Installationsdetails wurden hier nicht recherchiert; dieser Bericht bewertet ausschließlich, was im Bootstrap-Repository bereits vorhanden ist.

## Fehlende Arbeit in sachlicher Reihenfolge

1. Auf Grundlage offizieller aktueller Quellen Voraussetzungen und unterstützte Wege für beide Anbieter und alle drei Betriebssysteme klären; insbesondere lokales Gate, Skills und Sandboxmodelle.
2. Gemeinsamen situationsbezogenen Dialog und wiederaufnehmbaren Einrichtungsstand definieren.
3. Die sechs Einrichtungswege ergänzen und den bestehenden Projekt-Bootstrap am passenden Zustand einbinden.
4. Startdatei und versioniertes vollständiges Paket erzeugen; Einstieg ohne vorhandenen GitHub-Zugriff sicherstellen.
5. Dialog-, Paket- und reale Plattformnachweise getrennt durchführen und verbleibende Lücken offen ausweisen.

Das ist eine Lückenliste, kein gestarteter Implementierungsauftrag. Der bestehende Standard und das Gate wurden nicht verändert.
