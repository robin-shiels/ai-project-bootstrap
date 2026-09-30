# S08: Quellenmaterial

Bereinigter eigener Quelltext mit ersetzten Projekt-/Werkzeugpfaden. Lokale Verfügbarkeitsaussagen gelten nur für die Herkunftsumgebung; vor Wiederverwendung prüfen. Keine automatische Installation.

```markdown
---
name: pdf-documents
description: Lies, prüfe, erstelle oder bearbeite lokale PDF-Dateien einschließlich gescannter Unterlagen und Formularen.
---

# PDF-Dateien bearbeiten

Dieser Skill gilt für erreichbare lokale PDFs. Die Systembefehle `pdfinfo`, `pdftotext`, `pdftoppm` und `tesseract` sind verfügbar; `pypdf` und `pdfplumber` liegen unter `{DOCUMENT_PYTHON}`. Ein externer Speicherort oder Browser-Anhang wird dadurch nicht automatisch erreichbar.

1. Prüfe Seitenzahl, Verschlüsselung und vorhandene Textebene mit `pdfinfo` und `pdftotext`. Leere Textextraktion bei einer Bildseite bedeutet Scan, nicht leeres Dokument.
2. Bei Scans rendere die betroffenen Seiten mit `pdftoppm` und nutze `tesseract` mit passender Sprache. Behalte OCR-Ergebnisse als unsichere Transkription; kontrolliere Namen, Beträge und Fristen am Seitenbild.
3. Nutze `pypdf` für Seitenoperationen und einfache Formularfelder. Für ein neues PDF kann LibreOffice eine editierbare Ausgangsdatei exportieren. Erhalte Originale, wenn keine Änderung am Original verlangt ist.
4. Prüfe nach Änderungen Seitenzahl, Text, betroffene Formularfelder und die sichtbare Darstellung mindestens der geänderten Seiten. Ein PDF mit korrekt extrahiertem Text kann visuell trotzdem fehlerhaft sein.

Bei Steuer-, Uni- oder Vertragsunterlagen unterscheide wörtlichen Befund, OCR-Vermutung und eigene Einordnung. Eine PDF-Bearbeitung erteilt keine Freigabe zum Versand oder zur Weitergabe.
```
