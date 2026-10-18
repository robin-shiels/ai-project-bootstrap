# Dev-Box-Merge-Gate als projektübergreifender Standard — V1

**Status:** startbereit für einen manuell gestarteten Coding-Agenten; nicht begonnen.
**Datum:** 18.10.2026.
**Basis:** main 217b4b3ccd75557f707a627df87c2495e36cd35c.
**Auftragstyp:** öffentlicher, produktneutraler Standard mit Referenzimplementierung; keine Integration oder Veröffentlichung durch diesen Planungsauftrag.

## Ziel und entschiedene Regeln

Ein neues oder bestehendes Repository kann ein bewusst gestartetes lokales Gate übernehmen, das den tatsächlichen Merge-Tree eines PRs und den exakten Release-Commit prüft. Eigene, ausdrücklich mergefähige Task-PRs dürfen nach bestandenem Gate standardmäßig automatisch integriert werden. Das Gate bindet den geprüften Basis-SHA und Head-SHA atomar an genau den integrierten Merge-Commit. Deployment bleibt eine separate, projektspezifische Berechtigung und benötigt einen eigenen Gate-Lauf auf dem exakten aktuellen Integrations-Commit.

PO-Entscheidung vom 18.10.2026: GitHub-hosted CI startet in allen Projekten höchstens bewusst per workflow_dispatch zur Diagnose, nie automatisch bei PR, Push, Merge-Queue oder Zeitplan. Ein ausgeführter roter Diagnoselauf ist ein Stop-Signal; ein Job, der vor dem ersten Schritt scheitert, ist kein Testergebnis. Die Regel für automatische Merges gilt nur für eigene Task-PRs ohne offene fachliche Frage, unter den strengeren lokalen Schutzregeln. Fremde, unbekannte und Fork-PRs erhalten keine automatische Mergefreigabe. Eine eng benannte Projekt-Ausnahme für bestehende eigene Task-Ketten benötigt eine dokumentierte zusätzliche PO-Entscheidung und darf nie als Wildcard-Autorisierung wirken. Kein Projekt erhält durch diese Vorlage automatisch eine Deployfreigabe.

## Quellen und Ist-Stand

- Auf main liegen UNIVERSAL_PROJECT_BOOTSTRAP.md v1.1.0, README.md, templates/CODEX_BOOTSTRAP_PROMPT.md und skills/SKILL_MANIFEST.md; es gibt dort keinen Actions-Workflow.
- Offener PR #1, Head 33e2bff83d3ffff84a2610408f677230dad2a961, führt eine CI-Policy, Checkliste und ein Python-Beispiel mit automatischen pull_request- und main-push-Triggern ein. Er wird nicht integriert.
- Die technische Referenz wurde in einem privaten Projekt als lokales Python-Gate mit check-only --pr, check-only --main, merge-ff und temporärer CAS-Probe erprobt. Übernehme nur produktneutrale Mechanik nach eigener Sicherheitsprüfung; veröffentliche weder private Konfiguration, Projektnamen, Hostpfade noch Betriebsdaten.
- GitHub-Primärquellen: https://docs.github.com/en/graphql/reference/git (updateRefs / beforeOid / afterOid / force); https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow (workflow_dispatch benötigt den Workflow auf dem Default-Branch).

Vor der Ausführung main, PR #1, alle Workflows und Regeln erneut lesen. Historische Testzahlen oder Eigenschaften anderer Hosts sind keine Qualitätsnachweise für diese Vorlage.

## Scope und Dateiverantwortung

1. docs/tasks/DEVBOX_GATE_GLOBAL_STANDARD_V1.md lesen, main und PR #1 vergleichen, eigenen sauberen Branch von aktuellem main anlegen. Falls PR #1 oder main verändert wurden, den Diff neu bewerten.
2. DEVBOX_GATE_POLICY.md als verbindlichen produktneutralen Vertrag ergänzen: Gate für Merge-Tree und exakten Release-Commit, Autorisierung, isolierte Prüfung unbekannten Codes, Stop-Fälle, Nachweis, separater Deploy-Vertrag, Umgang mit Branch-Regeln und Merge-Queue. Keine versteckte Rückkehr zu automatisch gehosteten Jobs.
3. templates/devbox_merge_gate.py als eigenständig lauffähige Referenz-CLI auf Python mindestens 3.12 erstellen. Modi: check-only --pr N, check-only --main SHA, merge-ff --pr N --confirm-own-task-pr N und probe-ref-cas auf ausschließlich temporärer Ref. Ohne expliziten Modus keine Ausführung. Das Gate deployt nie.
4. templates/devbox_merge_gate.example.toml mit dokumentiertem, strikt validiertem Schema erstellen. Konfigurierbar sind mindestens Repository und Integrationsref, Prüfschritte als Argumentlisten samt Timeout und Laufumgebung, Dokumentations- und Vollprüfpfade, Merge-Ausschlüsse, vertrauenswürdige eigene PR-Herkunft/Branchmuster, Ressourcen-Vorbedingungen, Sperr- und Protokollpfad, temporärer Ref-Namensraum. Keine Shell-Auswertung freier Befehlsstrings, keine stillen Defaults für Autorisierung, Isolation oder Pflichtprüfungen. Beispielwerte sind Platzhalter und keine laufende Projektkonfiguration.
5. templates/AGENTS_DEVBOX_GATE.md und templates/CLAUDE_DEVBOX_GATE.md als einsetzbare Regeltexte anlegen. Sie müssen den globalen Auto-Merge-Standard für eigene Task-PRs und die getrennte Projektentscheidung für Deployments klar benennen. Bestehende strengere Regeln, offene PO-Fragen, Infrastruktur-/Migrations-Ausschlüsse und Branch-Schutz gehen vor. Vor Anwendung in einem Zielprojekt ist dessen tatsächliche Autorisierung zu prüfen und ein Konflikt sichtbar zu machen.
6. templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md für Bestandsaufnahme, lokales Tooling, vollständige Projektprüfungen, Isolation, Branch-Regeln, manuelle Diagnose, Bootstrap des ersten Gate-PRs und Nachweise ergänzen. UNIVERSAL_PROJECT_BOOTSTRAP.md, README.md, templates/CODEX_BOOTSTRAP_PROMPT.md und skills/SKILL_MANIFEST.md Datei für Datei mit der neuen Grundregel abgleichen: die bisherige Aussage, die allgemeine Veröffentlichungserlaubnis umfasse keinen Merge, bleibt für Branch-Push zutreffend, darf aber nicht den neuen eigenständigen Auto-Merge-Vertrag verdecken. Neuprojekte übernehmen ihn erst nach eingerichtetem Gate; bestehende strengere Mergeverbote sind als Konflikt offenzulegen und nicht still zu überschreiben. CHANGELOG.md und Versionsangabe als bewusst inkompatible Standardänderung aktualisieren.
7. Die automatische GitHub-Actions-Vorlage aus PR #1 nicht übernehmen. Falls ein Workflow-Beispiel sinnvoll bleibt, nur workflow_dispatch auf dem Default-Branch und ausdrücklich Diagnose ohne Secrets, Deploy oder Agentenstart. Dieses Repository selbst erhält keinen Self-hosted Runner und keinen automatischen Workflow.
8. tests/test_devbox_merge_gate.py mit temporärem Bare-Repository und Fake-GitHub/Host/Runner ergänzen. Keine echten GitHub-Minuten oder Hostdienste für die Tests verbrauchen.
9. Auf eigenem Branch committen und pushen, PR mit Handoff erstellen. Nach vorbereitetem Nachfolge-PR den alten PR #1 gemäß PO-Entscheidung begründet schließen; geeignete allgemeine Aussagen aus ihm nur nach Abgleich übernehmen. Der neue Gate-PR wird nicht vom implementierenden Agenten selbst gemergt, weil der Vertrag noch nicht auf main liegt. Bootstrap-Integration erfordert eine konkrete PO-Freigabe nach lokalem Gate-Lauf.

## Nichtziele

- Keine Produktimplementierung, keine Host-/Dienständerung, keine Runner-Registrierung, keine Billing- oder Branch-Schutz-Änderung und kein Deployment.
- Keine Übernahme privater Konfiguration, Betriebsdaten oder Projektnamen in das öffentliche Repository.
- Keine automatische Verarbeitung unbekannter PRs und keine Freigabe eines Gate-PRs durch sein eigenes Gate.

## Gate-Vertrag und Stop-Fälle

- PR-Metadaten, Basis B, Head H und Handoff exakt abgleichen. Frischen Worktree erstellen; Merge-Commit M mit Eltern B,H und Tree T bilden; alle konfigurierten Pflichtprüfungen seriell auf M ausführen. Nur eine ausdrücklich vollständige, sichere Dokumentationsklassifikation darf Anwendungstests überspringen. Unbekannte oder leere Diffs laufen voll.
- Vor Merge: eigenes Task-PR, nicht Draft, kein Blocker, keine offene Entscheidung, Gate-Vertrag auf B, keine ausgeschlossenen Pfade, vollständiger Schrittbericht. Redigierte Zusammenfassung und Prüfsumme veröffentlichen, Rohlogs lokal halten. M auf eigene temporäre Ref laden. Danach Head, Basis, Handoff, Logprüfsumme und M-Topologie erneut prüfen.
- main ausschließlich serverseitig per updateRefs mit beforeOid=B, afterOid=M und force=false fortschreiben. Bei Ablehnung, unklarer Antwort oder fehlender Berechtigung aktuellen Remote-Ref lesen und stoppen; niemals gewöhnlicher Push, Force, Admin-Bypass oder PR-Merge-API als Rückfall. Danach SHA, Tree und PR-Status prüfen. Der Test muss auch den Fall abdecken, dass main auf H oder einen anderen Vorfahren von M rückt.
- check-only schreibt niemals nach main. check-only --main SHA fordert den exakten aktuellen Remote-SHA und den vollständigen Release-Prüfplan. Ein erfolgreicher PR-Lauf ersetzt ihn nicht.
- Unbekannter/Fork-Code wird nicht unter dem Benutzer mit Projekt-/Deploy-Zugang ausgeführt; ohne nachgewiesene Isolation ISOLATION_REQUIRED vor jedem Install-, Build- oder Testschritt. Ein bereinigtes Environment ist keine Prozessisolation.
- Jeder fehlende, rote, übersprungene, abgelaufene oder OOM-beendete Pflichtschritt stoppt. Ebenso Konflikt, Ressourcenmangel, belegte Sperre, Secret-Muster im Log, fehlende Protokollintegrität, veränderter Ref, PR-Zustand oder Handoff. Kein Wiederholen bis Grün.
- Prüfe pro Zielprojekt Required Checks, Rulesets und Merge Queue. Steht eine bindende GitHub-Statusregel dem lokalen Gate entgegen, stoppt der Rollout für dieses Projekt und legt den Konflikt dem PO vor; die Vorlage ändert Schutzregeln nicht selbst.

## Positive und negative Abnahme

**Positiv:** Fake-Repository belegt einen grünen PR-check-only-Lauf auf M, einen exakten main-Lauf, einen autorisierten CAS-Merge mit B/H/M/T-Nachweis, Lock/Log-Zuordnung und redigierte Veröffentlichung. Konfiguration ändert Repository, Befehle, Pfadregeln, Lock und Logs ohne Codeänderung. Eine eigene temporäre GitHub-Ref darf die CAS-Semantik prüfen; nie main.

**Negativ:** Jeder Stop-Fall oben ist durch einen gezielten Test nachgewiesen, insbesondere veraltetes B trotz möglichem Fast-forward, fremder/Fork-PR ohne Isolation, ausgeschlossener Pfad, Pilot-Self-Merge, fehlender Testschritt und unveröffentlichbares Log. Vor dem Ref-Update muss jeder Stop main unverändert lassen. Bei einer mehrdeutigen Antwort nach dem Update kann main bereits auf M stehen; das Gate liest und protokolliert den tatsächlichen Ref und meldet einen Blocker statt einen unveränderten Stand zu behaupten. Ein Beispiel mit automatischem pull_request, push, merge_group oder schedule gilt als fehlgeschlagen.

## Quality Gates und Parallel-Sicherheit

- Für die Referenz-CLI: fokussierte Unit-/Integrationstests, Python-Kompilierung, Diff- und Syntaxprüfung der TOML-Beispiele, Review der Testdoubles gegen das tatsächliche Git-Verhalten. Optionaler GitHub-Probe-Lauf nur auf eigener temporärer Ref und nur wenn der tatsächliche Zugang dies erlaubt.
- Für die Dokumentation: Links, Querverweise, Konsistenz von Auto-Merge- und Deploy-Regeln, öffentlicher Datenschutz-Review und git diff --check. Keine Behauptung, dass lokale Simulation ein echter main-Merge war.
- Der PR #1 berührt dieselben Policy-, README- und Template-Dateien: NOT_PARALLEL_SAFE für Integration. Die Nachfolge zuerst fertigstellen; PR #1 danach schließen. Bei anderem offenen überlappenden Auftrag vor Beginn neu prüfen. Erwartete Integrationskosten: HIGH.
- Tests verwenden nur temporäre Repositories und Pfade; kein gemeinsamer Lock-/Logpfad des Produktiv-Gates. Keine Installation auf Zielsystemen.

## Git-, Merge- und Deploygrenzen

Dieser Auftrag erlaubt nur Änderungen am eigenen Branch und dessen PR. Kein Push auf main, kein Merge des neuen Standard-PRs, kein Deployment, keine Änderung an fremden Repositories, Branch-Schutz, Billing, Runnern oder Diensten. Eine spätere Nutzung der Vorlage in einem Projekt ist ein eigener Auftrag. Handoff: Status, Basis, Branch, Commit, exakter Remote-SHA, Dateien, tatsächlich ausgeführte Prüfungen, Stop-Fälle, PR-Links, Blocker und nächster PO-Schritt.

## Startprompt für Claude Code

Fetche zuerst den Planungsbranch codex/devbox-gate-rollout-plan-20261018, lies dort docs/tasks/DEVBOX_GATE_GLOBAL_STANDARD_V1.md und übernimm die Datei in deinen eigenen Umsetzungsbranch vom aktuellen main. Setze ausschließlich diesen Auftrag um. Lies die dortigen Quellen und prüfe PR #1 sowie parallele Arbeit. Baue die öffentliche produktneutrale Vorlage samt Tests und Regeltexten; keine privaten Daten oder Hostdetails. Prüfe lokal, pushe nur deinen Branch, erstelle den Nachfolge-PR und schließe danach PR #1 begründet. Kein Self-Merge, kein main-Push, kein Deployment.
