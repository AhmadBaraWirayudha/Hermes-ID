# Security Policy

## Baseline controls

- API token enabled in staging and production.
- Secrets stored in environment variables or a secret manager.
- No real secrets committed to version control.
- Least privilege access for users and services.
- Regular dependency checks.
- Logs retained for incident investigation.
- Backups verified through restore drills.

## Access control

Roles:

- admin
- analyst
- operator
- viewer

Permissions are defined in the RBAC matrix.

## Vulnerability management

- Run dependency audits per release.
- Patch critical vulnerabilities promptly.
- Document accepted risk.

## Incident response

Use the incident response runbooks in `docs/runbooks`.
