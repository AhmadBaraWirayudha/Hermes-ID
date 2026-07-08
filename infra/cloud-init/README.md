# Cloud-init

Cloud-init templates for bootstrapping a Linux cloud VM with Podman and podman-compose.

Use `podman-vm-cloud-init.yaml` when creating a VM on AWS, GCP, Azure, or another cloud provider.

After VM creation:

```bash
cd /opt/indomarket_insight
cp .env.example .env
./scripts/podman_run_prod.sh
```
