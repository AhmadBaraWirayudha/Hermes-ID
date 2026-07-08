<#
Install Podman Desktop on Windows 10/11 using winget.
Run PowerShell as normal user:
    powershell -ExecutionPolicy Bypass -File .\scripts\windows_install_podman.ps1
#>
$ErrorActionPreference = "Stop"
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
  throw "winget not found. Install Podman Desktop manually from https://podman-desktop.io/"
}
winget install RedHat.Podman-Desktop --accept-package-agreements --accept-source-agreements
Write-Host "Podman Desktop installed. Open Podman Desktop once to initialize the Podman machine." -ForegroundColor Green
