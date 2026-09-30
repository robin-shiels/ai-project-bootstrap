# S06: Quellenmaterial

Bereinigter eigener Quelltext mit ersetzten Projekt-/Werkzeugpfaden. Lokale Verfügbarkeitsaussagen gelten nur für die Herkunftsumgebung; vor Wiederverwendung prüfen. Keine automatische Installation.

```markdown
---
name: xlsx-workbooks
description: Erstelle, prüfe oder bearbeite lokale Excel-Dateien und CSVs, wenn eine Tabelle die wesentliche Ein- oder Ausgabedatei ist.
---

# Excel-Dateien und CSVs

Dieser Skill gilt für lokale Dateien. Für ein Google Sheet nutze den dafür verfügbaren Connector. Python mit `openpyxl` liegt unter `{DOCUMENT_PYTHON}`; `libreoffice` ist als Systembefehl verfügbar und berechnet Formeln tatsächlich.

1. Prüfe Datei, Blätter, Formeln, Eingabezellen und vorhandene Formatierung. Bei CSVs Kodierung, Trennzeichen, Dezimalzeichen und Zeitzonen beziehungsweise Datumsformate klären. Das Hilfsprogramm `07-inspect_workbook.py DATEI` zeigt Blätter, Formelzahl und mögliche Fehlerwerte.
2. Bearbeite eine bestehende Arbeitsmappe auf einer Kopie oder an einem neuen Ausgabepfad, sofern keine Änderung am Original verlangt ist. Erhalte Formeln, Bezüge und Eingabekonventionen. `openpyxl` berechnet Formeln nicht selbst; gespeicherte Werte können veraltet oder leer sein.
3. Für eine berechnete Ausgabedatei nutze LibreOffice zum Neuberechnen und prüfe anschließend die relevanten Ergebniszellen. Bei komplexen Makros, externen Bezügen, Pivot-Tabellen oder Diagrammen zuerst die Erhaltung im konkreten Dateityp prüfen, bevor du speicherst.
4. Teste bei einer Vorlage mindestens einen geänderten Eingabewert und die erwartete Auswirkung auf das Ergebnis. Vergleiche Summen und Einheiten mit der dokumentierten Rechenbasis. Nenne Annahmen direkt in der Datei oder in der Begleitnotiz.

Berichte Eingabedatei, Ausgabedatei und tatsächlich geprüfte Berechnungen. Eine ohne Excel oder LibreOffice neu berechnete Formel darf nicht als verifiziert gelten.
```
