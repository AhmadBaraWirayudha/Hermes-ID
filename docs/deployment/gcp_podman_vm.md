# GCP Podman VM Deployment

1. Create Compute Engine Ubuntu VM.
2. Allow HTTP/HTTPS firewall rules.
3. Use cloud-init metadata from `infra/cloud-init/podman-vm-cloud-init.yaml`.
4. Copy project to the VM.
5. Run:

```bash
cd /opt/indomarket_insight
cp .env.example .env
./installers/linux/install_podman_linux.sh
./scripts/podman_run_prod.sh
```

Optional: use Cloud SQL PostgreSQL and Cloud Storage.
