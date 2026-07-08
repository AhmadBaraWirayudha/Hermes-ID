# Runbook: Data Corruption

1. Stop writes/scraping jobs.
2. Backup current corrupted state for forensics.
3. Identify latest clean backup:
   ```bash
   ls -lah backups/
   ```
4. Restore:
   ```bash
   python app/cli.py restore-db backups/<backup>.bak
   ```
5. Run quality checks and reports.
6. Re-run only trusted sources.
7. Document root cause.
