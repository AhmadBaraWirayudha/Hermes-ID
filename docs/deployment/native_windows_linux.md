# Native Deployment Without Containers

If you do not want Podman/containers, the app can run directly with Python on Windows 10/11 or Linux cloud VMs.

## Windows 10/11 native

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app\init_db.py
streamlit run app\main.py
```

API:

```powershell
.\.venv\Scripts\uvicorn.exe app.api:api --host 0.0.0.0 --port 8000
```

Daily scheduled pipeline:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_task_scheduler.ps1
```

## Linux cloud VM native

```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip nginx
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app/init_db.py
streamlit run app/main.py --server.address=0.0.0.0 --server.port=8501
```

API:

```bash
.venv/bin/uvicorn app.api:api --host 0.0.0.0 --port 8000
```

Use `infra/systemd/` services for persistent native Linux operation.
