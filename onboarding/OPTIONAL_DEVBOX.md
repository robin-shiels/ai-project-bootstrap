# Optional: zusätzliche Entwicklungsmaschine (Dev-Box)

Nur verwenden, wenn der Nutzer ausdrücklich eine zweite, dauerhaft laufende Maschine nutzen möchte (zum Beispiel einen eigenen Linux-Rechner oder einen gemieteten Server). Der eigene Computer bleibt der Standard; zeige diesen Weg nicht ungefragt.

Eine Dev-Box im Sinne von `DEVBOX_GATE_POLICY.md` ist jede bewusst betriebene Entwicklungsmaschine – auch der eigene Computer. Ein zusätzlicher Server ist nie Voraussetzung.

## Wann sinnvoll

- Der Nutzer möchte Prüfungen oder das Merge-Gate laufen lassen, während sein Laptop zu ist.
- Fremder Code soll in einer getrennten, isolierten Umgebung geprüft werden (`DEVBOX_GATE_POLICY.md` §5).

## Ablauf

1. **Entscheidung:** Kosten, Anbieter und Zugang wählt der Nutzer selbst. Du mietest, kaufst oder registrierst nichts.
2. **Zugang:** Der Nutzer richtet die Anmeldung (zum Beispiel SSH-Schlüssel) selbst ein. Private Schlüssel bleiben auf seinem Gerät und kommen nie in den Chat oder in den Einrichtungsstand.
3. **Einrichtung auf der Dev-Box:** Die Schritte `git`, `github_cli`, `git_identity`, `python` laufen dort nach `platforms/linux.md`, im lokalen Agenten, der auf der Dev-Box arbeitet (Codex CLI oder Claude Code CLI über SSH).
4. **Trennung:** Hat die Dev-Box Zugriff auf Projekte, Deployments oder Anbieterkonten, darf dort kein fremder Code laufen. Für fremden Code eine eigene, unprivilegierte Umgebung nach `DEVBOX_GATE_POLICY.md` §5.
5. **Nachweis:** Dieselben Prüfungen wie auf dem eigenen Computer, mit `context` = Name der Dev-Box im Einrichtungsstand.

Der Einrichtungsstand hält die Dev-Box als eigenen Kontext fest; Nachweise vom eigenen Computer gelten dort nicht.
