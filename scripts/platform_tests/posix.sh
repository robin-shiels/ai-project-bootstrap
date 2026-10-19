#!/usr/bin/env bash
# Reale Plattformprüfung (macOS). Jede Prüfung wird mit Exitcode protokolliert;
# das Skript bricht nicht beim ersten Fehler ab. Keine Secrets, keine Anmeldung.
set -u
SUMMARY="${GITHUB_STEP_SUMMARY:-/dev/stdout}"
API="https://api.github.com/repos/${GITHUB_REPOSITORY}/contents/dist"
WORK="${RUNNER_TEMP:-/tmp}/aib"
mkdir -p "$WORK" && cd "$WORK" || exit 1
printf '| Prüfung | Erwartung | Exit | Letzte Ausgabezeile |\n| --- | --- | --- | --- |\n' >> "$SUMMARY"

rec() {  # rec <name> <erwartung> <befehl ...>
  local name="$1" expect="$2"; shift 2
  local out code
  out=$("$@" 2>&1); code=$?
  echo "::group::$name (exit $code, erwartet $expect)"; printf '%s\n' "$out" | tail -n 40; echo "::endgroup::"
  local last; last=$(printf '%s\n' "$out" | grep -v '^\s*$' | tail -n 1 | tr '|' '/' | cut -c1-160)
  printf '| %s | %s | %s | %s |\n' "$name" "$expect" "$code" "$last" >> "$SUMMARY"
  return 0
}
limit() {  # limit <sekunden> <befehl ...>  (macOS hat kein timeout)
  perl -e 'alarm shift; exec @ARGV' "$@"
}

rec "Betriebssystem" "Info" bash -c 'sw_vers 2>/dev/null || cat /etc/os-release; uname -sm'
rec "python3 --version" "≥ 3.12" python3 --version
rec "git --version" "0" git --version
rec "gh --version" "0" bash -c 'gh --version | head -1'
rec "Paket laden" "0" bash -c "for f in START_HIER.md AI-Bootstrap-2.1.0.zip SHA256SUMS; do curl -fsSL -H \"Authorization: Bearer \$GH_TOKEN\" -H 'Accept: application/vnd.github.raw' -o \"\$f\" \"$API/\$f?ref=$BUNDLE_COMMIT\" || exit 1; done; ls -l"
rec "Prüfsummen" "0" bash -c 'shasum -a 256 -c SHA256SUMS'
rec "Entpacken (python3 -m zipfile)" "0" python3 -m zipfile -e AI-Bootstrap-2.1.0.zip pkg
cd pkg/AI-Bootstrap-2.1.0 || exit 1
rec "Gebündelte Tests (alle)" "0" python3 -m unittest discover -s tests
rec "Gate-Hostprobe (systemd_scope=false)" "0" python3 scripts/probe_gate_host.py
rec "Gate-Hostprobe mit systemd_scope=true" "10 (PRECONDITION)" python3 scripts/probe_gate_host.py --config templates/devbox_merge_gate.example.toml
rec "Gate validate-config" "0" python3 templates/devbox_merge_gate.py --config templates/devbox_merge_gate.example.toml validate-config
rec "Einrichtungsstand validieren" "0" python3 scripts/onboarding_state.py validate onboarding/STATE.example.json
cd "$WORK" || exit 1
export PATH="$HOME/.local/bin:$PATH"
rec "Claude Code installieren (install.sh)" "0" bash -c 'curl -fsSL https://claude.ai/install.sh | bash'
rec "claude --version" "0" claude --version
rec "claude doctor" "0, nicht angemeldet" limit 120 claude doctor </dev/null
rec "Codex installieren (install.sh)" "0" bash -c 'curl -fsSL https://chatgpt.com/codex/install.sh | sh'
rec "codex --version" "0" codex --version
rec "codex login status" "1 (nicht angemeldet)" codex login status
mkdir -p "$WORK/ws"
rec "codex sandbox -- true" "0" bash -c "cd '$WORK/ws' && codex sandbox -- true"
rec "Sandbox read-only: Schreiben gesperrt" "≠ 0" bash -c "cd '$WORK/ws' && codex sandbox -- sh -c 'echo x > probe.txt'"
rec "Sandbox workspace-write: im Projekt erlaubt" "0" bash -c "cd '$WORK/ws' && codex sandbox -c 'sandbox_mode=\"workspace-write\"' -- sh -c 'echo x > probe.txt && cat probe.txt'"
rec "Sandbox workspace-write: außerhalb gesperrt" "≠ 0" bash -c "cd '$WORK/ws' && codex sandbox -c 'sandbox_mode=\"workspace-write\"' -- sh -c 'echo x > \$HOME/aib-outside.txt'"
rec "Datei außerhalb existiert nicht" "≠ 0" test -e "$HOME/aib-outside.txt"
exit 0
