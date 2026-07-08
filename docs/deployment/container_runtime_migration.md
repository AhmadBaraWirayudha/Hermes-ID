# Container Runtime Migration: Docker to Podman

This project now uses Podman as the default free/open-source container runtime.

## Replacements

| Old Docker item | New Podman item |
|---|---|
| `Containerfile` | `Containerfile` |
| `podman-compose.yml` | `podman-compose.yml` |
| `podman-compose.prod.yml` | `podman-compose.prod.yml` |
| `podman-compose.storage.yml` | `podman-compose.storage.yml` |
| `podman build` | `podman build` |
| `podman-compose` | `podman-compose` |
| Docker Desktop | Podman Desktop |

## Commands

```bash
podman build -f Containerfile -t localhost/indomarket-insight:latest .
podman-compose -f podman-compose.prod.yml up --build -d
podman ps
podman logs <container>
podman stop <container>
```

## Cloud compatibility

Podman builds OCI images that can be pushed to most registries and run on:

- Kubernetes
- OpenShift
- AWS ECS/EKS
- GCP Cloud Run/GKE
- Azure Container Apps/AKS
- Any Linux VM with Podman

## Windows 10 compatibility

Use Podman Desktop, backed by WSL2/Podman machine.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_install_podman.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\windows_run_podman.ps1
```
