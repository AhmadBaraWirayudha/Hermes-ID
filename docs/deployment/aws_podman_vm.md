# AWS Podman VM Deployment

1. Launch Ubuntu EC2 instance.
2. Open inbound ports 80, 443 if using reverse proxy, and optionally 22.
3. Use cloud-init: `infra/cloud-init/podman-vm-cloud-init.yaml`.
4. Copy or clone project to `/opt/indomarket_insight`.
5. Run:

```bash
cd /opt/indomarket_insight
cp .env.example .env
./installers/linux/install_podman_linux.sh
./scripts/podman_run_prod.sh
```

Optional: use RDS PostgreSQL and S3 by setting `DATABASE_URL` and object storage env vars.
