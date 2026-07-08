# Runbook: API Down

1. Check health:
   ```bash
   python scripts/healthcheck.py http://localhost/api/health
   ```
2. Check containers/services:
   ```bash
   podman-compose -f podman-compose.prod.yml ps
   podman-compose -f podman-compose.prod.yml logs api --tail=200
   ```
3. Check logs:
   ```bash
   tail -200 logs/indomarket.log
   ```
4. Restart API:
   ```bash
   podman-compose -f podman-compose.prod.yml restart api
   ```
5. If DB corruption suspected, restore backup.
6. Record incident and corrective action.
