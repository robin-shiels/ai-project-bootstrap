# S16: Quellenmaterial

Bereinigter eigener Quelltext mit ersetzten Projekt-/Werkzeugpfaden. Lokale Verfügbarkeitsaussagen gelten nur für die Herkunftsumgebung; vor Wiederverwendung prüfen. Keine automatische Installation.

```markdown
---
name: hermes-security-review
description: Prüfe die Sicherheit eines Hermes-Agenten mit E-Mail-, Web- oder Telegram-Zugang und des zugehörigen Linux-Servers; nutze bei konkreten Sicherheitsreviews oder Härtungsaufträgen, nicht bei gewöhnlicher Hermes-Bedienung.
---

# Hermes und Host prüfen

Nutze den Skill für wiederkehrende Sicherheitsbewertungen und gezielte Härtung. Bei diesem Nutzer zuerst den aktuellen Stand in `{SECURITY_PROJECT_RECORD}` lesen. Projektfakten, Prüfdaten und offene Schritte gehören dorthin, nicht in diesen Skill.

1. Kläre den betrachteten Host, die Hermes-Instanz und die Eingabekanäle. Trenne belegte Live-Einstellungen, Nutzerangaben, externe Empfehlungen und noch nicht geprüfte Annahmen. Lies Konfiguration nur mit Geheimnisredaktion; gib keine Tokens, kompletten Mails oder privaten Schlüssel aus.
2. Prüfe die Kette vom fremden Inhalt bis zur möglichen Wirkung: E-Mail/Web/Anhang/Toolausgabe → Modell → Shell/Code/MCP/Plugin/Skill/Datei/Netz → Geheimnisse, Versand, Löschung, Termine oder persistente Regeln. Ein Prompt, Signal-Scanner oder Hermes-interner Approval-Filter ist keine verlässliche Sicherheitsgrenze. Beurteile die Rechte des ganzen Prozesses und aller Nebenpfade. Prüfe, ob tatsächliche Nutzerautorisierung und konkrete Aktionsparameter außerhalb des Modells validiert werden.
3. Bei einem Live-Host: Identitäten und Caller-Allowlists, Dienstnutzer, Terminal-Backend, Prozessisolation, Mounts, Egress, erreichbare Zugangsdaten, Netzwerk-Listener, SSH, Firewall, Updates, Backups und Wiederherstellung nur soweit für den Auftrag nötig lesen. Externe Erreichbarkeit und Anbieter-Backups nicht aus lokalen Einstellungen ableiten. Bei SSH-, Firewall- oder Dienstumbau zuerst einen funktionierenden Rettungsweg und Rückrollplan nachweisen; produktive Unterbrechungen in ein abgestimmtes Wartungsfenster legen.
4. Bewerte fremde Skills und Plugins als ausführbaren Lieferkettenzugang: vollständige referenzierte Dateien und Skripte, Herkunft, Abhängigkeiten, Netzwerk- und Dateizugriffe prüfen, bevor sie installiert oder ausgeführt werden. Einen Skill nie als Ersatz für OS-Isolation, begrenzte Credentials und technische Tool-Policy empfehlen.
5. Formuliere die nächsten Schritte nach Schadenspotenzial und Abhängigkeiten. Für jede umgesetzte Maßnahme Erfolg und Abbruchbedingung mit einem echten Positiv- und Negativtest prüfen; bei Mail-Prompt-Injection muss zulässiges Lesen funktionieren und unerlaubte Aktion blockiert sein. Berichte Restrisiko und aktualisiere die Projektakte mit Datum und Belegen.

Orientierung: [Hermes-Sicherheitsmodell](https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md), [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html). Prüfe bei aktuellen Produktdetails die installierte Version und die aktuelle offizielle Dokumentation.
```
