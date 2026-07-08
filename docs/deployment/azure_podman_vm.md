# Azure Podman VM Deployment

1. Create Ubuntu VM.
2. Open NSG ports 80/443.
3. Use cloud-init from `infra/cloud-init/podman-vm-cloud-init.yaml`.
4. Copy project to the VM.
5. Run:

```bash
cd /opt/indomarket_insight
cp .env.example .env
./installers/linux/install_podman_linux.sh
./scripts/podman_run_prod.sh
```

Optional: use Azure Database for PostgreSQL and Blob Storage.
