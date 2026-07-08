<#
Create a Windows Task Scheduler entry to run the native pipeline daily.
Run from project root:
  powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_task_scheduler.ps1
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$Root\scripts\windows\run_pipeline_native.ps1`""
$Trigger = New-ScheduledTaskTrigger -Daily -At 7:00AM
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel LeastPrivilege
Register-ScheduledTask -TaskName "IndoMarketInsightPipeline" -Action $Action -Trigger $Trigger -Principal $Principal -Force
Write-Host "Created scheduled task: IndoMarketInsightPipeline" -ForegroundColor Green
