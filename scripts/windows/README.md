# Windows Scripts

Windows PowerShell helpers for native runs and scheduling.

Create a daily pipeline scheduled task:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_task_scheduler.ps1
```

Run pipeline once natively:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\run_pipeline_native.ps1
```
