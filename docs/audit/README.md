# Audit Tools

Project audit scripts for debugging and release checks.

Run:

```bash
python scripts/audit_text_policy.py
python scripts/audit_runtime_references.py
python scripts/doctor.py --fix
python scripts/validate_project.py
```

Text policy:

- no emoji in text-readable files
- no literal em dash in text-readable files

Runtime policy:

- use Podman and OCI wording for active deployment
- old runtime names appear only in migration documentation where needed
