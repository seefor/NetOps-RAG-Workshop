$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
Set-Location $Root

if (-not (Test-Path ".venv")) {
    py -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[hermes]"
python bonus\hermes-netops-copilot\scripts\desktop_profile_setup.py
python bonus\hermes-netops-copilot\scripts\desktop_preflight.py

Write-Host ""
Write-Host "Desktop bonus is configured. Launch with:"
Write-Host "python bonus\hermes-netops-copilot\scripts\launch_desktop.py"
