<# Run frontend and API in two PowerShell windows. #>
$Root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$Py = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { throw "Run install_native_windows.ps1 first." }
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; .\.venv\Scripts\python.exe -m streamlit run app\main.py --server.port 8501"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root'; .\.venv\Scripts\uvicorn.exe app.api:api --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 5
Start-Process "http://localhost:8501"
