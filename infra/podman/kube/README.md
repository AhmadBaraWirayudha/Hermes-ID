# Podman Kube Play

Podman can run Kubernetes-style YAML locally without Docker.

Build image:

```bash
podman build -f Containerfile -t localhost/indomarket-insight:latest .
```

Run pod:

```bash
podman kube play infra/podman/kube/indomarket-pod.yaml
```

Stop/remove pod:

```bash
podman kube down infra/podman/kube/indomarket-pod.yaml
```

Open:

```text
Frontend: http://localhost:8501
API:      http://localhost:8000/health
```
