<#
Run IndoMarket Insight using Podman on Windows 10/11.
Prerequisites:
- Podman Desktop installed
- Podman machine initialized/running
- podman-compose installed, or run: pip install podman-compose
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
if (-not (Get-Command podman -ErrorAction SilentlyContinue)) { throw "podman not found. Install Podman Desktop first." }
if (-not (Get-Command podman-compose -ErrorAction SilentlyContinue)) {
  Write-Host "podman-compose not found. Installing with pip..." -ForegroundColor Yellow
  python -m pip install --user podman-compose
}
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
podman-compose -f podman-compose.prod.yml up --build
