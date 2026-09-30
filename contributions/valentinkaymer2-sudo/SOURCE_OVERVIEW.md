# Quellenüberblick

Erfasst am 30.09.2026 für `valentinkaymer2-sudo`. Basis: Bootstrap v1.1.0, `main@217b4b3ccd75557f707a627df87c2495e36cd35c`.

**25 Quellen:** 10 eigene Skillanweisungen, 3 mit Codex bereitgestellte Skillanweisungen, 1 eigenes Hilfsskript, 10 Workflow-/Projekt-/Betriebsdokumente und der aktive zugängliche Gesprächskontext. Die Bootstrap-Dateien sind eine separat untersuchte Vergleichsbasis und werden nicht als eigene Quellen gezählt.

Die [strukturierte Erfassung](sources.json) dokumentiert für jede Quelle Herkunft, Stand/Abrufzeit, Zweck, schriftliche Regeln, beobachtete Praxis, ein ausdrücklich synthetisches Anwendungsbeispiel, einen Gegenfall und Veröffentlichungsgrenzen. Originalzeitstempel sind Hilfsinformationen und belegen keine aktuelle Autorität.

| ID | Quelle / Art | Zweck | Tatsächlich belegter Stand | Öffentliches Material |
| --- | --- | --- | --- | --- |
| S01 | Globale AGENTS-Arbeitspräferenz / `workflow_document` | Sitzungsübergreifende Arbeitsweise, selektive Akten und Modellberatung | `observed_run` | [Auszug/Beschreibung](sources/01-global-rules.md) |
| S02 | Lokales Skill-Inventar und Wiederherstellung / `workflow_document` | Installation und Projektzuständigkeiten nachvollziehen | `available_not_executed` | [Auszug/Beschreibung](sources/02-inventory.md) |
| S03 | skill-learning-loop / `custom_skill` | Aus echten Erfahrungen kleine wiederverwendbare Verbesserungen ableiten | `observed_run` | [Auszug/Beschreibung](sources/03-skill-learning-loop.md) |
| S04 | code-debugging / `custom_skill` | Ursache eines konkreten Fehlers prüfen, statt vermutete Symptome zu patchen | `available_not_executed` | [Auszug/Beschreibung](sources/04-code-debugging.md) |
| S05 | web-release-check / `custom_skill` | Quellstand, Build und sichtbaren Live-Stand separat belegen | `available_not_executed` | [Auszug/Beschreibung](sources/05-web-release-check.md) |
| S06 | xlsx-workbooks / `custom_skill` | Lokale Tabellen und echte Formel-Neuberechnung prüfen | `available_not_executed` | [Auszug/Beschreibung](sources/06-xlsx-workbooks.md) |
| S07 | inspect_workbook.py / `helper_script` | Formeln, Cachefehler und Scanbegrenzung sichtbar machen | `observed_run` | [Auszug/Beschreibung](sources/07-inspect_workbook.py) |
| S08 | pdf-documents / `custom_skill` | Textebene, Scan, OCR und sichtbares Seitenbild unterscheiden | `available_not_executed` | [Auszug/Beschreibung](sources/08-pdf-documents.md) |
| S09 | wichtige-themen / `custom_skill` | Mehrstufige Vorhaben sparsam speichern und sinnvoll nachfassen | `observed_run` | [Auszug/Beschreibung](sources/09-wichtige-themen.md) |
| S10 | health-dashboard-dev / `custom_skill` | Änderungen an einem privaten Datendashboard begrenzen | `available_not_executed` | [Auszug/Beschreibung](sources/10-health-dashboard-dev.md) |
| S11 | health-journal / `custom_skill` | Eindeutige Nutzerberichte mit begrenztem Eingangsworkflow erfassen | `available_not_executed` | [Auszug/Beschreibung](sources/11-health-journal.md) |
| S12 | ideen-labor-research / `custom_skill` | Recherche mit Gegenprobe zur Entscheidung führen | `available_not_executed` | [Auszug/Beschreibung](sources/12-ideen-labor-research.md) |
| S13 | Projekt-AGENTS für Geschäftsideen / `workflow_document` | Recherche- und Kostenrahmen für ein bestimmtes Projekt | `written_only` | [Auszug/Beschreibung](sources/13-research-method-and-ranking.md) |
| S14 | Rechercheverfahren Version 1.5 / `workflow_document` | Nachfrageindikatoren, Quellenfamilien und frische Erhebungen unterscheiden | `written_only` | [Auszug/Beschreibung](sources/13-research-method-and-ranking.md) |
| S15 | Bewertungsmodell Version 1 / `workflow_document` | Unsicherheit und Evidenzgrad neben dem Ranking darstellen | `written_only` | [Auszug/Beschreibung](sources/13-research-method-and-ranking.md) |
| S16 | hermes-security-review / `custom_skill` | Agentenrechte und fremde Skilllieferketten prüfen | `available_not_executed` | [Auszug/Beschreibung](sources/14-security-review.md) |
| S17 | Allgemeine Assistentenpräferenzen mit datierten Ergänzungen / `workflow_document` | Autonom fortsetzen und dauerhafte Änderungen transparent erklären | `written_only` | [Auszug/Beschreibung](sources/15-assistant-preferences.md) |
| S18 | Projektübergabe zwischen T3/Codex und Hermes / `workflow_document` | Dateibasierte Übergabe bei getrennten Chats und Werkzeugen | `written_only` | [Auszug/Beschreibung](sources/16-runtime-boundaries.md) |
| S19 | Knappe Übersicht offener Themen / `workflow_document` | Relevante offene Schritte an maßgebliche Akten anbinden | `observed_run` | [Auszug/Beschreibung](sources/16-runtime-boundaries.md) |
| S20 | Betriebsregeln eines privaten Datendashboards / `workflow_document` | Wiederherstellbarkeit und tatsächlichen Betriebsstand prüfen | `reported_history` | [Auszug/Beschreibung](sources/16-runtime-boundaries.md) |
| S21 | Betriebsweg eines persistenten MCP-Browsers / `workflow_document` | Vorhandene Browserprofile und reale Toolverfügbarkeit prüfen | `reported_history` | [Auszug/Beschreibung](sources/16-runtime-boundaries.md) |
| S22 | Aktiver zugänglicher Gesprächskontext / `conversation` | Nutzerauftrag, jüngste Entscheidung und tatsächliche Toolschritte zuordnen | `observed_run` | [Auszug/Beschreibung](sources/18-conversation-observations.md) |
| S23 | openai-docs / `bundled_skill` | Aktuelle Produkt- und Modellfragen belegen | `available_not_executed` | [Auszug/Beschreibung](sources/17-bundled-skills.md) |
| S24 | skill-creator / `bundled_skill` | Nicht offensichtliche, eng begrenzte Skillführung erstellen | `available_not_executed` | [Auszug/Beschreibung](sources/17-bundled-skills.md) |
| S25 | skill-installer / `bundled_skill` | Installation und aktuelle Quelle von Skills unterscheiden | `observed_run` | [Auszug/Beschreibung](sources/17-bundled-skills.md) |

`written_only` bedeutet gelesene Vorgabe, `available_not_executed` zusätzlich lokale Datei/Katalog, `reported_history` einen schriftlichen Rückblick ohne frische Nachprüfung und `observed_run` einen tatsächlich zugänglichen Schritt. Sie sind verschiedene Belegarten und keine ordinalen Qualitätsnoten.

Die öffentlichen Dateien sind Originale eigener allgemeiner Quellen, bereinigte Auszüge oder neue Paraphrasen. Eigene Skilltexte sind mit Codex erarbeitet; fremde Herstellertexte und Superpowers wurden nicht kopiert. Die eigenen Beiträge werden im Rahmen dieses ausdrücklich beauftragten Repository-Beitrags unter der vorhandenen MIT-Lizenz bereitgestellt. Private Quelldateien, Konfigurationen und nicht exportierte Teile werden dadurch nicht lizenziert oder öffentlich.

Einige öffentliche Dateien fassen mehrere private Quellen separat gekennzeichnet zusammen. Ihre Prüfsumme identifiziert das öffentliche Artefakt. Die privaten Originalpfade/-prüfsummen liegen nur in der Arbeitsumgebung. Empfänger können den veröffentlichten Beitrag anhand seines Git-Commits prüfen, die ausgelassenen privaten Originale jedoch nicht unabhängig einsehen.
