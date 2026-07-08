<#
Build the Windows one-click launcher EXE.
Run this on Windows PowerShell from the indomarket_insight folder:

    powershell -ExecutionPolicy Bypass -File .\build_one_click_exe.ps1

Output:
    dist\IndoMarketInsight.exe
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "== IndoMarket Insight one-click EXE builder ==" -ForegroundColor Cyan

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    Write-Host "dotnet SDK not found." -ForegroundColor Yellow
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Installing .NET SDK 8 using winget..." -ForegroundColor Yellow
        winget install Microsoft.DotNet.SDK.8 --accept-package-agreements --accept-source-agreements
    } else {
        throw "Please install .NET SDK 8 from https://dotnet.microsoft.com/download and run this script again."
    }
}

New-Item -ItemType Directory -Force -Path "$Root\dist" | Out-Null

dotnet publish "$Root\launcher\windows\IndoMarketInsightLauncher.csproj" `
    -c Release `
    -r win-x64 `
    --self-contained true `
    -p:PublishSingleFile=true `
    -p:PublishTrimmed=false `
    -o "$Root\dist"

$Exe = "$Root\dist\IndoMarketInsight.exe"
if (-not (Test-Path $Exe)) {
    throw "Build failed: $Exe was not created."
}

Write-Host "" 
Write-Host "SUCCESS: $Exe" -ForegroundColor Green
Write-Host "" 
Write-Host "How to use:" -ForegroundColor Cyan
Write-Host "1. Keep IndoMarketInsight.exe in this indomarket_insight folder, or copy it next to app\ and requirements.txt."
Write-Host "2. Double-click IndoMarketInsight.exe."
Write-Host "3. It will create .venv, install requirements, run Streamlit, and open the browser."
