# S10: Quellenmaterial

Bereinigter eigener Quelltext mit ersetzten Projekt-/Werkzeugpfaden. Lokale Verfügbarkeitsaussagen gelten nur für die Herkunftsumgebung; vor Wiederverwendung prüfen. Keine automatische Installation.

```markdown
---
name: health-dashboard-dev
description: Entwickle oder prüfe Code, Datenimporte und Betrieb des privaten Gesundheitsdashboards unter {DASHBOARD_ROOT}.
---

# Gesundheitsdashboard entwickeln

Nutze diesen Skill für Änderungen am Dashboard-Code, Datenmodell, Importen oder Dienstbetrieb. Für eine persönliche Gesundheitsäußerung ist `health-journal` zuständig; dieser Skill verarbeitet keine Chat-Aussage als Tagebucheintrag.

- Einstieg: `{DASHBOARD_ROOT}/docs/BETRIEB_V2.md`. Lies zusätzlich nur die zum Auftrag passende Fachakte, zum Beispiel `docs/HEVY.md` für Kraftdaten oder `docs/HERMES_BETRIEB.md` für die Brücke zu Hermes.
- Bestimme vor Änderungen, ob der Auftrag den privaten V2-Kandidaten, die alte Produktivbasis, einen Worker oder eine Integration betrifft. Prüfe laufende Pfade und Datenbank am aktuellen System; ältere Akten sind kein Live-Nachweis.
- Bei Datenänderungen Herkunft, Nutzerbericht, Messwert, Schätzung und unbekannte Felder erhalten. Korrekturen und wiederholte Importe dürfen keine stillen Dubletten oder Überschreibungen erzeugen.
- Vor einer Migration oder einer Änderung an gespeicherten persönlichen Daten einen konsistenten, wiederherstellbaren Stand sichern. Bestehende Produktionsdaten nicht durch eine ältere Sicherung oder Kandidatendaten ersetzen.
- Prüfe die konkret geänderte Funktion mit passenden vorhandenen Tests und, wenn die Benutzeroberfläche betroffen ist, mit einer gezielten Ansicht. Einen synthetischen Test nicht als persönlichen Live-Abgleich ausgeben.
- Berichte, was im Kandidaten beziehungsweise produktiv läuft, welche echte Nutzerprobe noch fehlt und wie eine Änderung zurückgenommen werden kann.

Der Skill verschafft keinen zusätzlichen Zugang zu den verbundenen Datenquellen oder privaten Daten. Nutze nur vorhandene und für die Aufgabe freigegebene Zugänge.
```
