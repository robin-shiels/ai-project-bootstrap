# Reale Plattformprüfung (Windows, nativ). Jede Prüfung wird mit Exitcode
# protokolliert; kein Abbruch beim ersten Fehler. Keine Secrets, keine Anmeldung.
$ErrorActionPreference = 'Continue'
$Summary = $env:GITHUB_STEP_SUMMARY
$Api = "https://api.github.com/repos/$($env:GITHUB_REPOSITORY)/contents/dist"
$Headers = @{ Authorization = "Bearer $($env:GH_TOKEN)"; Accept = "application/vnd.github.raw" }
$Work = Join-Path $env:RUNNER_TEMP 'aib'
New-Item -ItemType Directory -Force -Path $Work | Out-Null
Set-Location $Work
"| Prüfung | Erwartung | Exit | Letzte Ausgabezeile |`n| --- | --- | --- | --- |" | Out-File -Append -Encoding utf8 $Summary

function Rec([string]$Name, [string]$Expect, [scriptblock]$Block) {
  $global:LASTEXITCODE = 0
  try { $out = & $Block 2>&1 | Out-String; $code = $LASTEXITCODE }
  catch { $out = $_ | Out-String; $code = 'Fehler' }
  Write-Host "::group::$Name (exit $code, erwartet $Expect)"
  ($out -split "`n" | Select-Object -Last 40) -join "`n" | Write-Host
  Write-Host '::endgroup::'
  $last = ($out -split "`n" | Where-Object { $_.Trim() } | Select-Object -Last 1)
  if ($null -eq $last) { $last = '' }
  $last = $last.Trim().Replace('|', '/')
  if ($last.Length -gt 160) { $last = $last.Substring(0, 160) }
  "| $Name | $Expect | $code | $last |" | Out-File -Append -Encoding utf8 $Summary
}

Rec 'Betriebssystem' 'Info' { (Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty Caption); [System.Environment]::OSVersion.VersionString }
Rec 'python --version' '≥ 3.12' { python --version }
Rec 'git --version' '0' { git --version }
Rec 'gh --version' '0' { (gh --version)[0] }
Rec 'WSL: wsl --status' 'Info' { wsl --status }
Rec 'WSL: wsl -l -v' 'Info' { wsl -l -v }
Rec 'Paket laden' '0' { foreach ($f in 'START_HIER.md','AI-Bootstrap-2.1.0.zip','SHA256SUMS') { Invoke-WebRequest -UseBasicParsing -Headers $Headers -Uri "$Api/$($f)?ref=$($env:BUNDLE_COMMIT)" -OutFile $f }; Get-ChildItem | Select-Object Name, Length | Out-String }
Rec 'Prüfsummen' '0' {
  $bad = 0
  foreach ($line in Get-Content SHA256SUMS) { $hash, $name = $line -split '  ', 2; $actual = (Get-FileHash -Algorithm SHA256 $name).Hash.ToLower(); if ($actual -ne $hash) { "FALSCH $name"; $bad = 1 } else { "OK $name" } }
  $global:LASTEXITCODE = $bad
}
Rec 'Entpacken (python -m zipfile)' '0' { python -m zipfile -e AI-Bootstrap-2.1.0.zip pkg }
Set-Location (Join-Path $Work 'pkg\AI-Bootstrap-2.1.0')
Rec 'Tests Einrichtungsstand' '0' { python -m unittest tests.test_onboarding_state }
Rec 'Tests Gate-Plattformfälle' '0' { python -m unittest tests.test_devbox_merge_gate.PlatformPortabilityTests }
Rec 'Gate-Hostprobe nativ' '10 (PRECONDITION, WSL 2)' { python scripts\probe_gate_host.py }
Rec 'Gate check-only nativ außerhalb eines Repos' '10 (PRECONDITION)' {
  $cfg = Join-Path $env:RUNNER_TEMP 'gate.toml'
  (Get-Content templates\devbox_merge_gate.example.toml -Raw).Replace('systemd_scope = true ', 'systemd_scope = false') | Set-Content -Encoding utf8 $cfg
  python templates\devbox_merge_gate.py --config $cfg --repo-dir $env:RUNNER_TEMP check-only --pr 1
}
Rec 'Gate validate-config' '0' { python templates\devbox_merge_gate.py --config templates\devbox_merge_gate.example.toml validate-config }
Rec 'Einrichtungsstand validieren' '0' { python scripts\onboarding_state.py validate onboarding\STATE.example.json }
Set-Location $Work
Rec 'Claude Code installieren (install.ps1)' '0' { Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression }
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
Rec 'claude --version' '0' { claude --version }
Rec 'Codex installieren (install.ps1)' '0' { powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex" }
$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
Rec 'codex --version' '0' { codex --version }
Rec 'codex login status' '1 (nicht angemeldet)' { codex login status }
Rec 'codex sandbox (cmd /c exit 0)' 'Info' { codex sandbox -- cmd /c 'exit 0' }
exit 0
