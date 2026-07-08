# Chaos Drills

## API restart drill

```bash
./scripts/chaos_drill.sh
```

Expected:

- API restarts
- `/api/health` returns 200
- frontend remains available

## DB restore drill

See `backup_restore_drill.md`.

## Source failure drill

Disable network or configure a bad source URL and verify:

- scrape failure is logged
- app remains usable
- alert/report generation still works with last good data
