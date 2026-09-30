# S04: Quellenmaterial

Unveränderte eigene Skillquelle; keine automatische Installation oder Standardübernahme.

```markdown
---
name: code-debugging
description: Untersuche reproduzierbare Fehler, fehlgeschlagene Tests, Build-Probleme und unerwartetes Laufzeitverhalten vor einer Codekorrektur.
---

# Fehler im Code untersuchen

Nutze diesen Skill, wenn ein konkreter Fehler behoben werden soll. Für eine neue Funktion ohne Fehlersymptom ist er nicht nötig. Die Vorgehensweise ist von [Superpowers: Systematic Debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) inspiriert; maßgeblich bleiben der aktuelle Nutzerauftrag und die Regeln des Projekts.

1. Halte erwartetes und beobachtetes Verhalten fest. Reproduziere den Fehler mit dem kleinsten sicheren Fall oder sichere die aussagekräftige Fehlermeldung. Wenn er sporadisch auftritt, erfasse Bedingungen und Logs, statt eine zuverlässige Reproduktion zu behaupten.
2. Verfolge die betroffenen Daten und Aufrufgrenzen rückwärts bis zur plausiblen Ursache. Prüfe aktuelle Änderungen und einen funktionierenden Vergleichsfall. Unterscheide Befund und Vermutung.
3. Prüfe eine konkrete Ursache mit einer kleinen gezielten Beobachtung oder einem Test. Wenn der Befund die Hypothese widerlegt, ändere die Hypothese, bevor du Code umschreibst.
4. Behebe die Ursache mit einer angemessen kleinen Änderung. Ergänze einen Regressionstest, wenn er ein relevantes wiederholbares Verhalten absichert. Für eine geringfügige, leicht rücknehmbare Änderung genügt eine passende direkte Prüfung.
5. Wiederhole die ursprüngliche Fehlerprobe und die von der Änderung betroffenen Tests oder Bedienwege. Lies die Ergebnisse, bevor du „behoben“ meldest. Nach mehreren erfolglosen Versuchen überprüfe die zugrunde gelegte Architektur oder Systemgrenze.

Berichte Ursache, Änderung, konkrete Prüfergebnisse und verbleibende Unsicherheit. Dieser Skill erzwingt weder Test-First für jede Kleinigkeit noch einen Planungs- oder Freigabezyklus für gewöhnliche Fehlerbehebungen.
```
