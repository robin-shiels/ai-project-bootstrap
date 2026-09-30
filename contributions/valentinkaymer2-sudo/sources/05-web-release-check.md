# S05: Quellenmaterial

Bereinigter eigener Quelltext mit ersetzten Projekt-/Werkzeugpfaden. Lokale Verfügbarkeitsaussagen gelten nur für die Herkunftsumgebung; vor Wiederverwendung prüfen. Keine automatische Installation.

```markdown
---
name: web-release-check
description: Prüfe nach Änderungen an einer Website, ob Build, Deployment und sichtbarer Live-Stand tatsächlich übereinstimmen.
---

# Website-Veröffentlichung prüfen

Nutze diesen Skill, wenn eine Website geändert, veröffentlicht oder auf einen ausstehenden Live-Stand geprüft werden soll. Der Einstieg ist `{WEBSITE_PROJECT_RECORD}`; andere Projekte haben eigene Projektakten.

1. Ermittle den beabsichtigten Quellstand, die Build- und Veröffentlichungsstrecke und die Zieladresse aus dem konkreten Projekt. Ein Commit oder ein erfolgreiches CI-Signal belegt noch keine sichtbare Veröffentlichung.
2. Führe die für die Änderung passenden lokalen Prüfungen aus, zum Beispiel Build, Lint oder eine gezielte Funktionsprobe. Ändere keine fremden Inhalte ohne entsprechenden Auftrag.
3. Prüfe nach einer beauftragten Veröffentlichung die Live-Seite neu. Vergleiche ein eindeutiges geändertes Merkmal mit dem Quellstand. Prüfe betroffene Ansichten auf schmaler und breiter Breite, falls die Änderung Darstellung betrifft.
4. Melde getrennt: Quellstand gespeichert, Build geprüft, Veröffentlichung ausgelöst, Live-Stand bestätigt. Wenn ein Schritt nicht zugänglich oder fehlgeschlagen ist, benenne genau diesen Stand und den nächsten notwendigen Schritt.

Öffentliche Veröffentlichung erfolgt nur, wenn sie Teil des konkreten Auftrags ist. Dieser Skill allein autorisiert keinen Deploy, keine Werbung und keine Änderung von Rechtsseiten.
```
