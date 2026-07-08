"""Create/update a local admin user in config/users.json.
Usage: python scripts/create_admin_user.py admin StrongPassword123
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from security import hash_password, USERS_PATH, ensure_default_files

if len(sys.argv) < 3:
    raise SystemExit("Usage: python scripts/create_admin_user.py <username> <password>")
username, password = sys.argv[1], sys.argv[2]
ensure_default_files()
data = json.loads(USERS_PATH.read_text(encoding="utf-8"))
users = [u for u in data.get("users", []) if u.get("username") != username]
users.append({"username": username, "password_hash": hash_password(password), "roles": ["admin"], "active": True})
data["users"] = users
USERS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"admin user saved: {username}")
