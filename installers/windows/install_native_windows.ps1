<#
Install and run IndoMarket Insight natively on Windows 10/11.
Run from project root:
  powershell -ExecutionPolicy Bypass -File .\installers\windows\install_native_windows.ps1
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
Set-Location $Root

Write-Host "== IndoMarket Insight Native Windows Installer ==" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Host "Python not found. Installing Python via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements
  } else {
    throw "Python not found. Install Python 3.10+ and enable Add Python to PATH."
  }
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
  python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app\init_db.py

Write-Host "Installation complete." -ForegroundColor Green
Write-Host "Run with: .\run.bat"
