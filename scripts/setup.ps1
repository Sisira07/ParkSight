# scripts/setup.ps1 — one-shot environment setup for Windows PowerShell.
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "== Python: creating .venv and installing the package =="
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
pip install -r backend\requirements.txt

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
}
if (-not (Test-Path "backend\.env") -and (Test-Path "backend\.env.example")) {
    Copy-Item "backend\.env.example" "backend\.env"
}
if (-not (Test-Path "frontend\.env") -and (Test-Path "frontend\.env.example")) {
    Copy-Item "frontend\.env.example" "frontend\.env"
}

Write-Host "== Node: installing frontend dependencies =="
Push-Location frontend
npm install
Pop-Location

Write-Host ""
Write-Host "Setup complete."
Write-Host ""
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  python scripts\run_pipeline.py --input data\raw\violations.csv --output outputs\"
Write-Host "  python scripts\run_backend.py        # in one terminal"
Write-Host "  .\scripts\run_frontend.ps1            # in another terminal"
