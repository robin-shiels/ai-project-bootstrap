# S18–S21: Übergabe und Betriebsgrenzen

Nur neu formulierte Abstraktionen. Keine privaten Originaleinträge, Adressen, Loginpfade, Dienstkonfigurationen oder gespeicherten Daten kopiert.

## S18: Übergabe zwischen getrennten Laufzeiten

Gemeinsame Dateien können den belegten Stand, nächste Schritte und offene Entscheidungen tragen. Getrennte Chats, laufende Aufträge, Werkzeugverbindungen und Browserprofile werden dadurch nicht automatisch synchronisiert. Vor gleichzeitigem Schreiben auf denselben Stand tatsächliche laufende Arbeit prüfen.

## S19: Offene-Themen-Übersicht

Die beobachtete Ablage kombiniert eine kurze Übersicht und gezielt verlinkte Detailakten. Eine Übersicht enthält nur relevanten Status, nächsten Schritt, Frist oder internen Prüftermin und letzten Hinweis. Für das öffentliche Beispiel bleiben sämtliche realen Einträge ausgelassen.

## S20: Datenhaltender Betrieb

Vor Migrationen Kandidat und Produktion, alle Schreiber und die Daten-/Dateibeziehungen identifizieren. Konsistenzsicherung und Restore in ein neues isoliertes Ziel sind getrennte Nachweise. Externe Adapter bleiben beim Restore zunächst ausgeschaltet. Ein Backup prüft Integrität; es ist kein Nachweis für eine reale Geräteanmeldung, Produktionsfreigabe oder erfolgreiche Wiederzustellung. Das Betriebsdokument berichtet historische Tests; dieser Audit wiederholt sie nicht.

## S21: Persistenter Browser

Die aktive, vom Nutzer bereitgestellte angemeldete Sitzung gezielt anbinden. Neue Profile und neue Laufzeiten erhalten Logins oder neue Werkzeuge nicht automatisch. Persistenter Speicher und unabhängiges Backup sind getrennte Eigenschaften. Die Vorlage ist an eine konkrete MCP-/Desktopumgebung gebunden; der Audit hat deren Toolinventar und Betrieb nicht frisch getestet.
