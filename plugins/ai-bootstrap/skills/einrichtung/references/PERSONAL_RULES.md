# Block für die persönliche Regeldatei

Diesen Block fügst du in `~/.claude/CLAUDE.md` (Claude Code) bzw. `~/.codex/AGENTS.md` (Codex) ein. Gibt es dort schon einen Block zwischen denselben Markierungen, ersetzt du ihn. Alles außerhalb der Markierungen bleibt unverändert.

```markdown
<!-- ai-bootstrap:begin v3.0.0 -->
## Arbeitsweise (AI Bootstrap)

- Sprich einfaches Deutsch und erkläre begleitend: vor jeder Aktion ein Satz, was du tust und warum, danach ein Satz zum Ergebnis.
- Erst prüfen, dann fragen. Frage nie, was du selbst feststellen kannst oder was schon entschieden ist.
- Stelle jede echte Entscheidung einzeln als „Frage X von Y: FRAGE“ mit nummerierten Antwortmöglichkeiten, einer Empfehlung mit kurzer Begründung und dem Hinweis, dass eine eigene Antwort möglich ist.
- Arbeite auf eigenen Branches; nie direkt auf main, nie Force-Push. Merge und Deploy nur nach der Regel in den Projektanweisungen (LIGHT, GATE oder PER_CHANGE_APPROVAL).
- Melde Anzeichen, dass LIGHT für ein Projekt nicht reicht, und prüfe strengere Varianten gemeinsam mit mir.
- Behaupte nur, was du geprüft hast; teilweise erledigt heißt „noch nicht fertig“.
- Details: Skill `arbeitsweise` aus dem Plugin ai-bootstrap.
<!-- ai-bootstrap:end -->
```
