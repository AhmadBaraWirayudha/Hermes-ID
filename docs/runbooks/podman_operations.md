# Podman Operations Runbook

## Check containers

```bash
podman ps
podman ps -a
```

## Logs

```bash
podman logs indomarket-api
podman logs indomarket-frontend
```

## Restart production stack

```bash
podman-compose -f podman-compose.prod.yml restart
```

## Rebuild and deploy

```bash
podman-compose -f podman-compose.prod.yml up --build -d
```

## Clean unused images/volumes

```bash
./scripts/podman_cleanup.sh
```

## Backup before upgrade

```bash
python app/cli.py backup-db
python app/cli.py backup-workspace
```
