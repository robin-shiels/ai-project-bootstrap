# GUIDED_BOOTSTRAP_V2 — Claude-Auftragskette

> **For agentic workers:** Use superpowers:executing-plans, sofern verfügbar, um diese Kette schrittweise auszuführen. Gleichwertige verfügbare Fähigkeiten sind zulässig. Die Kette selbst verlangt keine Subagenten.

**Goal:** Die geführte Einrichtung auf Einrichtung und Verknüpfung der essenziellen Dienste verschlanken, als eigenes Plugin `ai-bootstrap` mit drei Skills ausliefern und das Merge-/Deploy-Modell „Leicht“ als Standard für neue Projekte einführen.

**Architecture:** Kurzer Starter `START_HIER.md` → Plugin `ai-bootstrap` aus diesem Repository (Skills `einrichtung`, `projekt-start`, `arbeitsweise`) → kurze persönliche Regeldatei, die in jeder Sitzung gilt. Der Projektstandard bleibt der Projektkern. Superpowers bleibt die Grundlage für Planung, Fehlersuche, Testen und Git-Isolation.

**Tech Stack:** Markdown (`SKILL.md`, Anleitungen), JSON (Marktplatz, Plugin-Manifest, Zustand), Python 3.12+ Standardbibliothek für Validator, Paketbau und Tests.

**Spec:** ../superpowers/specs/2026-10-21-guided-bootstrap-v2-design.md
**Vorgänger:** [GUIDED_BOOTSTRAP_V1](GUIDED_BOOTSTRAP_V1.md), Ergebnisse in `docs/results/GUIDED_BOOTSTRAP_V1_*`

## Auftrag und Autorisierung

Diese Kette wird erst nach Owner-Freigabe dieses Entwurfs gestartet. Danach ist sie ein zusammenhängender Auftrag: Recherche, Umsetzung, Dokumentation, Paketbau und Abnahme aller Teilaufträge, ohne nach jeder Phase nachzufragen.

Im eigenen Task-Branch darf Claude nach relevanten Prüfungen committen, diesen Branch pushen und den zugehörigen PR erstellen/aktualisieren. Kein Merge, kein direkter Push auf main, kein Force-Push, kein Release-Tag, kein Deployment. Diese Kette ändert den Befugnisvertrag des Standards; ihr PR braucht deshalb eine ausdrückliche Owner-Integration und wird nie selbst gemerged, auch nicht nach „Leicht“.

Gewöhnliche technische Detailentscheidungen anhand vorhandener Regeln und offizieller Quellen selbst treffen und begründen. Nur echte neue Produkt-, Sicherheits-, Kosten- oder Befugnisentscheidungen vorlegen, im Frageformat. Bei einem Blocker unabhängige Arbeit fortsetzen und den Fortsetzungsschritt in `docs/results/GUIDED_BOOTSTRAP_V2_STATUS.json` sichern.

## Owner-Entscheidungen (2026-10-21)

Siehe Spec, Abschnitt „Owner-Entscheidungen“. Kurz: Desktop-App und Abo vorausgesetzt; nur essenzielle Dienste; Windows nativ; reiner Chat bekommt einen Kurzhinweis; Arbeitsweise = Berechtigungen + persönliche Regeln + erstes Projekt; Merge/Deploy „Leicht“ mit gemeinsamer Eskalation; Plugin mit drei Skills.

Versionsnummer: **3.0.0** (Owner-Entscheidung 2026-10-21, weil sich der Befugnisvertrag ändert). Umsetzung vom Owner am 2026-10-21 freigegeben.

## Review Focus

1. „Leicht“ darf keinen fremden PR, keinen Fork-PR und nichts Ungeprüftes mergen; der Merge bindet sich an den geprüften Commit.
2. Bestehende Projekte mit strengeren Regeln (zum Beispiel integriertem Gate) behalten sie; der neue Standard überschreibt nichts still.
3. Die KI behauptet keine Installation, Anmeldung oder Einstellung, die sie nicht in der laufenden Sitzung geprüft hat.
4. Persönliche Regeldatei und Einstellungen: vorhandene Einträge des Nutzers bleiben erhalten.
5. Der kurze Starter funktioniert auch, wenn die Plugin-Installation scheitert (eingebettete Kurzfassung).

---

## GB2-01 — Quellen und Inventur

**Abhängigkeit:** keine. **Lieferung:** belegte technische Grundlage.

- [ ] Basis (main-SHA, offene PRs, Branches) inventarisieren.
- [ ] Mit aktuellen offiziellen Quellen belegen und in `docs/research/GUIDED_BOOTSTRAP_V1_SOURCE_MATRIX.md` (neuer Abschnitt v2) eintragen:
  - Claude Code: eigener Plugin-Marktplatz aus einem GitHub-Repository (`marketplace.json`, `plugin.json`, Installation per CLI, feste Version/Ref);
  - Codex: Installation eigener Skills aus einem Repository (`~/.agents/skills`, eigener Plugin-Marktplatz möglich?);
  - Projekte in ChatGPT und Claude anlegen und mit GitHub verbinden (Desktop-App, Planabhängigkeit);
  - Claude Code und Codex nativ unter Windows (Voraussetzungen wie Git for Windows, Sandbox-Grenzen);
  - Berechtigungsregeln für `gh pr merge` und Deploy-Befehle (Claude `permissions.allow`; Codex Freigabe-/Sandbox-Werte);
  - `gh pr merge --match-head-commit` und Verhalten bei veraltetem Branch.
- [ ] Für jede offene Frage aus der Spec den gewählten Weg oder den Blocker festhalten.

**Abnahme:** Jede technische Annahme der Spec ist belegt oder als Blocker mit Ersatzweg benannt.

## GB2-02 — Standard und Befugnisvertrag „Leicht“

**Abhängigkeit:** 01. Version 3.0.0.

- [ ] `UNIVERSAL_PROJECT_BOOTSTRAP.md`: Merge-/Deploy-Modell „Leicht“ als Standard für neue Projekte, mit Bedingungen, Deploy-Regel, Einmal-Frage für Produktion mit echten Nutzerdaten, Eskalationsregel und Bestandsschutz für strengere Projekte.
- [ ] `DEVBOX_GATE_POLICY.md` und `skills/SKILL_MANIFEST.md`: Gate als stärkere Option statt einziger Merge-Weg; Verweise abgleichen.
- [ ] Regeltexte für Projekte (`templates/AGENTS_*.md`, `templates/CLAUDE_*.md`) für „Leicht“ ergänzen.
- [ ] `CHANGELOG.md`, `VERSION`: neue Version mit Migrationshinweis („bestehende Projekte: nichts zu tun“).

**Abnahme:** Kein Widerspruch zwischen Standard, Manifest, Gate-Richtlinie und Vorlagen; die Gate-Tests laufen unverändert grün.

## GB2-03 — Plugin und Skills

**Abhängigkeit:** 01, 02.

- [ ] `.claude-plugin/marketplace.json` und `plugins/ai-bootstrap/.claude-plugin/plugin.json` anlegen.
- [ ] Skills `einrichtung`, `projekt-start`, `arbeitsweise` schreiben (Frontmatter mit genauer Beschreibung, wann der Skill greift; Inhalt nach Spec).
- [ ] `templates/PERSONAL_RULES.md`: kurzer, markierter Block für `~/.claude/CLAUDE.md` bzw. `~/.codex/AGENTS.md`, der auf `arbeitsweise` verweist.
- [ ] Codex-Weg nach GB2-01 umsetzen (Skill-Ordner bzw. Plugin).
- [ ] Tests: Manifeste gültig, Skill-Namen und Pfade konsistent, Frontmatter vollständig, keine Geheimnisse.

**Abnahme:** `claude plugin install` aus dem Repository-Marktplatz real erfolgreich; die drei Skills erscheinen in einer neuen Sitzung. Codex-Weg real geprüft oder als Blocker benannt.

## GB2-04 — Einrichtungsablauf und Zustand

**Abhängigkeit:** 03.

- [ ] Ablauf aus `onboarding/ENTRY.md` in den Skill `einrichtung` überführen und auf sieben Schritte verschlanken; `onboarding/` auf das Nötige kürzen (Anbieter- und Plattformdetails nur noch dort, wo sie sich wirklich unterscheiden).
- [ ] Windows: nativer Weg als Standard; WSL 2 nur im Gate-Zusatz.
- [ ] Einstellungen nach Spec je Anbieter beschreiben (vorlesen, nur Abweichungen ansprechen, gemeinsam setzen).
- [ ] Probelauf mit PR und Merge nach „Leicht“ gegen ein freigegebenes Test-Repository.
- [ ] `STATE.schema.json` Version 2, Migration von v1-Ständen in `scripts/onboarding_state.py`, Tests.

**Abnahme:** Jeder v1-Schritt ist einem v2-Schritt zugeordnet oder als entfallen/optional begründet; v1-Beispielstand wird korrekt migriert.

## GB2-05 — Startdatei und Paket

**Abhängigkeit:** 03, 04.

- [ ] `START_HIER.md` als kurzer Starter (unter 150 Zeilen) mit eingebetteter Kurzfassung für den Fall, dass die Plugin-Installation scheitert.
- [ ] `scripts/build_bootstrap_bundle.py` und Tests anpassen; ZIP enthält das Plugin als Offline-Weg.
- [ ] README auf den neuen Einstieg umstellen.
- [ ] Deterministischer Wiederholungsbau, `SHA256SUMS` prüfen.

**Abnahme:** Byte-identischer Wiederholungsbau; alle Tests und `ruff` grün.

## GB2-06 — Abnahme

**Abhängigkeit:** 05.

- [ ] Dialogfälle D1–D9 an den neuen Ablauf anpassen und durchführen.
- [ ] Neue Fälle: Server-Beratung rät von unnötigem Server ab; Probelauf mit Merge nach „Leicht“; `main` ändert sich zwischen Prüfung und Merge; Eskalation nach kaputtem `main`.
- [ ] Linux real vom Nullzustand in frischer VM für beide Anbieter, einschließlich echter Plugin-Installation.
- [ ] Testanleitung für Nicht-Techniker für macOS, Windows 11 und Webchat schreiben; diese Wege bleiben NOT_TESTED, bis sie real laufen.
- [ ] Befunde beheben und betroffene Nachweise wiederholen; Ergebnisse in `docs/results/GUIDED_BOOTSTRAP_V2_ACCEPTANCE.md`.

**Abnahme:** Keine offenen wesentlichen Funktions- oder Sicherheitsfehler; „alle Wege einsatzbereit“ nur mit realen Nachweisen.

## GB2-07 — Finale Prüfung und Übergabe

**Abhängigkeit:** 06.

- [ ] Aktuellen main auf Überschneidungen prüfen, abgleichen, betroffene Prüfungen erneut ausführen.
- [ ] Diff auf Scope, Geheimnisse und persönliche Angaben prüfen (das Repository ist öffentlich).
- [ ] `STATUS.json` und `ACCEPTANCE.md` vervollständigen; Branch pushen, Remote-HEAD belegen, PR aktualisieren.
- [ ] Kurze Übersicht: was funktioniert, was fehlt, nötige Owner-Aktionen, Integrationsstand.

## Fortschritts- und Fortsetzungsvertrag

Wie in v1: `docs/results/GUIDED_BOOTSTRAP_V2_STATUS.json` führt je Teilauftrag `id`, `state`, `dependencies`, `result_files`, `validation`, `blockers`, dazu `source_base`, `branch`, `last_commit`, `next_action`. Wesentliche Ergebnisse nie nur im Chat halten.

## Nicht Bestandteil

Server oder Dev-Box einrichten, bestehende Projekte umstellen, Konten oder Abos im Namen des Nutzers, hosted CI wieder einschalten.
