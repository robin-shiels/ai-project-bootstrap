# Reale Plattformprüfung (Windows, nativ). Jede Prüfung wird mit Exitcode
# protokolliert; kein Abbruch beim ersten Fehler. Keine Secrets, keine Anmeldung.
$ErrorActionPreference = 'Continue'
$env:WSL_UTF8 = '1'  # wsl.exe prints UTF-8 instead of UTF-16
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
Rec 'Paket-Quelle (Manifest)' 'Info' { python -c "import json; m=json.load(open('BUNDLE_MANIFEST.json')); print(m['source_commit'])" }
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

# WSL 2 attempt last: installing a distribution may not be possible on a
# hosted runner (nested virtualization). Each step is bounded by a timeout.
function RecTimed([string]$Name, [string]$Expect, [int]$Seconds, [string]$Exe, [string]$ArgLine) {
  $p = Start-Process -FilePath $Exe -ArgumentList $ArgLine -NoNewWindow -PassThru -RedirectStandardOutput "$Work\o.txt" -RedirectStandardError "$Work\e.txt"
  if (-not $p.WaitForExit($Seconds * 1000)) { $p.Kill($true); $script:timed = 'Zeitlimit' } else { $script:timed = $p.ExitCode }
  Rec $Name $Expect { Get-Content "$Work\o.txt", "$Work\e.txt" -ErrorAction SilentlyContinue; $global:LASTEXITCODE = $script:timed }
}
Set-Location $Work
$check = @'
set -u
cd "$1" || exit 1
echo "python: $(python3 --version 2>&1)"
python3 -m unittest discover -s tests 2>&1 | tail -n 3
python3 scripts/probe_gate_host.py
'@
[System.IO.File]::WriteAllText("$Work\wsl-check.sh", ($check -replace "`r`n", "`n"))
RecTimed 'WSL: Ubuntu-24.04 installieren' 'Info' 900 'wsl.exe' '--install -d Ubuntu-24.04 --no-launch'
RecTimed 'WSL: Distribution registrieren' 'Info' 600 'ubuntu2404.exe' 'install --root'
RecTimed 'WSL: uname in Ubuntu' 'Info' 120 'wsl.exe' '-d Ubuntu-24.04 -u root -- uname -a'
$unix = { param($path) ($path -replace '\\', '/') -replace '^([A-Za-z]):', { '/mnt/' + $_.Groups[1].Value.ToLower() } }
$pkgUnix = & $unix (Join-Path $Work 'pkg\AI-Bootstrap-2.1.0')
$scriptUnix = & $unix "$Work\wsl-check.sh"
RecTimed 'WSL: Gate-Tests und Hostprobe in Ubuntu' 'Info' 900 'wsl.exe' "-d Ubuntu-24.04 -u root -- bash $scriptUnix $pkgUnix"
exit 0
