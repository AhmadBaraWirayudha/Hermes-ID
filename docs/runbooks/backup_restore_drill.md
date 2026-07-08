# Backup Restore Drill

Run monthly.

1. Create backup:
   ```bash
   python app/cli.py backup-db
   ```
2. Verify backup:
   ```bash
   python scripts/verify_backup.py backups/<backup>.bak
   ```
3. Restore to test environment, not production first.
4. Run health and quality checks.
5. Record results and backup age.

Success criteria:

- backup file is valid SQLite
- required tables exist
- app starts after restore
- quality score acceptable
