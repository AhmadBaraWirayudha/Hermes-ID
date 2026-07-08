# Podman Deployment: Windows 10 and Cloud

Podman is a free, open-source container engine and a practical Docker replacement. It can run on Windows 10/11 through Podman Desktop/WSL2 and on Linux cloud VMs.

## Why Podman

- Open-source and free.
- Daemonless architecture on Linux.
- OCI-compatible images.
- Works with `Containerfile`.
- Can run rootless on Linux.
- Compatible with Kubernetes/OpenShift workflows.
- Runs on Windows 10/11 via Podman Desktop.

## Windows 10 setup

1. Install Podman Desktop:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_install_podman.ps1
```

Or install manually:

```text
https://podman-desktop.io/
```

2. Open Podman Desktop once and initialize/start the Podman machine.

3. Run the app:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_run_podman.ps1
```

Open:

```text
http://localhost
```

## Linux cloud VM setup

Ubuntu/Debian example:

```bash
sudo apt-get update
sudo apt-get install -y podman python3-pip
python3 -m pip install --user podman-compose
cp .env.example .env
./scripts/podman_run_prod.sh
```

Open:

```text
http://SERVER_IP
http://SERVER_IP/api/health
```

## Local development

```bash
podman-compose -f podman-compose.yml up --build
```

Open:

```text
http://localhost:8501
```

## Production-style local stack

```bash
cp .env.example .env
podman-compose -f podman-compose.prod.yml up --build -d
```

Services:

- Frontend: `http://localhost`
- API: `http://localhost/api/health`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Build image

```bash
podman build -f Containerfile -t localhost/indomarket-insight:latest .
```

## Push image to registry

```bash
podman login REGISTRY_HOST
podman tag localhost/indomarket-insight:latest REGISTRY_HOST/indomarket-insight:latest
podman push REGISTRY_HOST/indomarket-insight:latest
```

## MinIO object storage

```bash
podman-compose -f podman-compose.storage.yml up -d
```

Open MinIO console:

```text
http://localhost:9001
```

Credentials:

```text
indomarket / indomarket-secret
```
