<#
Create a portable Windows zip after building the EXE.
Run on Windows:
    powershell -ExecutionPolicy Bypass -File .\build_one_click_exe.ps1
    powershell -ExecutionPolicy Bypass -File .\package_windows_portable.ps1
Output:
    dist\IndoMarketInsight_Portable.zip
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Exe = "$Root\dist\IndoMarketInsight.exe"
if (-not (Test-Path $Exe)) {
    throw "Run build_one_click_exe.ps1 first. Missing: $Exe"
}

$Stage = "$Root\dist\IndoMarketInsight_Portable"
if (Test-Path $Stage) { Remove-Item $Stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Stage | Out-Null

$Include = @(
    "app", "sql", "cpp", "cs", "config", "data", "docs", "launcher", "tests",
    "requirements.txt", "README.md", "run.bat", "Containerfile", "podman-compose.yml", "podman-compose.prod.yml", "pyproject.toml", "START_INDOMARKET_WINDOWS.cmd", "START_HERE_ONE_CLICK.md"
)
foreach ($item in $Include) {
    if (Test-Path "$Root\$item") {
        Copy-Item "$Root\$item" "$Stage\$item" -Recurse -Force
    }
}
Copy-Item $Exe "$Stage\IndoMarketInsight.exe" -Force

# Remove large/generated caches if present
Get-ChildItem $Stage -Recurse -Directory -Force -Include ".venv", "__pycache__", ".pytest_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

$Zip = "$Root\dist\IndoMarketInsight_Portable.zip"
if (Test-Path $Zip) { Remove-Item $Zip -Force }
Compress-Archive -Path "$Stage\*" -DestinationPath $Zip
Write-Host "Created portable package: $Zip" -ForegroundColor Green
