<#
Create a desktop shortcut for the one-click Windows launcher.
Run from project root:
  powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_desktop_shortcut.ps1
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "IndoMarket Insight.lnk"
$Target = Join-Path $Root "START_INDOMARKET_WINDOWS.cmd"
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $Target
$Shortcut.WorkingDirectory = $Root
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Start IndoMarket Insight"
$Shortcut.Save()
Write-Host "Created desktop shortcut: $ShortcutPath" -ForegroundColor Green
