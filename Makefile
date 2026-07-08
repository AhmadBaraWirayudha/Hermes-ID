.PHONY: install run api test demo report pipeline podman podman-prod podman-build

install:
	pip install -r requirements.txt

run:
	python app/init_db.py
	streamlit run app/main.py

api:
	uvicorn app.api:api --host 0.0.0.0 --port 8000

test:
	pytest -q

demo:
	python app/cli.py demo

report:
	python app/cli.py report --format both

pipeline:
	python app/pipeline.py --demo-if-empty --alerts --export --report both

podman:
	podman-compose -f podman-compose.yml up --build

podman-prod:
	podman-compose -f podman-compose.prod.yml up --build -d

podman-build:
	podman build -f Containerfile -t localhost/indomarket-insight:latest .

openapi:
	python scripts/export_openapi.py

health:
	python scripts/healthcheck.py http://localhost/api/health

verify-backup:
	python scripts/verify_backup.py $(BACKUP)

security-test:
	bandit -r app -c tests/security/bandit.yaml || true

load-test:
	k6 run tests/load/k6_api_smoke.js

podman-quadlet:
	./scripts/podman_quadlet_install.sh

podman-kube:
	./scripts/podman_kube_play.sh

podman-clean:
	./scripts/podman_cleanup.sh

wheelhouse:
	./scripts/bootstrap/create_wheelhouse.sh

install-wheelhouse:
	./scripts/bootstrap/install_from_wheelhouse.sh

smoke-all:
	./scripts/run_smoke_all.sh

secrets:
	python scripts/bootstrap/generate_secrets.py
