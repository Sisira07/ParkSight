# scripts/run_frontend.ps1 — installs (if needed) and starts the Vite dev server.
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $RepoRoot "frontend")

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..."
    npm install
}

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
}

npm run dev
