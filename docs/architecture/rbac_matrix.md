# RBAC Matrix

| Permission | Admin | Analyst | Operator | Viewer |
|---|---:|---:|---:|---:|
| read dashboards/API | yes | yes | yes | yes |
| scrape/import sources | yes | no | yes | no |
| train forecasts | yes | yes | no | no |
| run backtests | yes | yes | no | no |
| generate reports | yes | yes | no | no |
| export data | yes | yes | yes | no |
| manage settings/backups | yes | no | no | no |
| manage users/RBAC | yes | no | no | no |

Config files:

- `config/rbac.example.json`
- `config/users.example.json`

Create admin:

```bash
python scripts/create_admin_user.py admin StrongPassword123
```
