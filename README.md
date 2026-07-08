# IndoMarket Insight v2 - Indonesian Market Intelligence App

## Simple overview

Hermes Analytics ID is a friendly Indonesian market dashboard. It helps you collect data, watch live signals, make charts, run forecasts, and download reports.

Fast start on Windows:

```text
START_INDOMARKET_WINDOWS.cmd
```

If something fails:

```text
CHECK_AND_FIX_WINDOWS.cmd
```

Plain guide:

```text
docs/simple/README.md
```


A starter multi-language app for Indonesian market data: scrape/import CSV, auto-store to SQLite + CSV, format/export data, graphs, and machine-learning forecasts.

## What is included

- **Python app**: Streamlit minimalist dashboard (`app/main.py`)
- **Scraping**: generic table/API scraper with presets and scheduler (`app/scraper.py`)
- **SQL**: SQLite database schema + reusable queries (`sql/schema.sql`, `sql/queries.sql`)
- **CSV**: automatic raw/processed CSV storage with clean formatting (`data/raw`, `data/processed`)
- **Graphs**: Plotly line, bar, heatmap correlation, moving averages, anomaly views
- **Analytics**: momentum, volatility, z-score anomaly detection, category/regional aggregation
- **Machine Learning**: RandomForest + Holt-style baseline forecasting (`app/ml.py`)
- **Exports**: CSV and XLSX report generation with IDR formatting
- **C++**: optional fast moving-average library (`cpp/market_math.cpp`)
- **C#**: optional CSV formatter/export utility (`cs/CsvFormatter.cs`)
- **Indonesian market defaults**: IDR formatting, Jakarta timezone, sample sectors/products, IDX/BPS/BI-friendly schema

> Scraping note: only scrape pages/APIs you are allowed to access. Respect robots.txt, rate limits, and each website's terms.

## Quick start

```bash
cd indomarket_insight
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app/init_db.py
./run.sh  # or: streamlit run app/main.py
```

The app also works with demo data if you have not configured real sources yet.

## Optional C++ acceleration

```bash
cd indomarket_insight
bash cpp/build.sh
```

The Python app will automatically use the compiled library if available.

## Optional C# CSV formatter

```bash
cd indomarket_insight/cs
# If dotnet SDK is installed:
dotnet new console -n CsvFormatterApp --force
cp CsvFormatter.cs CsvFormatterApp/Program.cs
cd CsvFormatterApp
dotnet run -- ../../data/processed/example.csv ../../data/processed/example_formatted.csv
```

## Typical workflow

1. Open **Sources** tab and add a source URL or upload a CSV.
2. Click **Scrape now** or enable an interval auto-scrape.
3. Clean/store data to SQLite and CSV.
4. View charts in **Dashboard**.
5. Train ML model in **Forecast** and export forecast CSV.

## CSV format expected

Recommended columns:

| column | example | notes |
|---|---:|---|
| date | 2026-07-07 | ISO date preferred |
| source | bps / idx / marketplace | data origin |
| category | rice / cement / stock / fx | category |
| item | Beras Premium / BBCA.JK | product/ticker/item |
| region | Indonesia / Jakarta / Sumsel | region |
| price | 15000 | IDR price/value |
| volume | 120 | optional |
| metric | retail_price / close / demand | optional |

## Project structure

```text
app/                 Python app modules
cpp/                 Optional C++ computation library
cs/                  Optional C# CSV formatter
sql/                 SQLite schema and analytical queries
data/raw/            Auto-saved raw scrapes/imports
data/processed/      Clean CSV exports
docs/                Notes and architecture
```


## v2 refinements

- Source registry saved in SQL.
- Respectful scraping options: robots.txt check and configurable delay.
- Analytics page with anomalies, correlation heatmap, regional/category aggregation.
- Forecast page compares RandomForest against Holt linear baseline.
- Export center creates both CSV and XLSX files.
- Linux/macOS `run.sh` and Windows `run.bat` launchers.

## v3 refinements

- **Data Quality page**: quality score, duplicate detection, missing/invalid values, column profile.
- **Business Models page**: revenue, price elasticity, optimal markup, ROAS, NRR, Rule of 40, HHI, takt time, capacity utilization.
- **CLI automation**: `python app/cli.py init-db|demo|export|list-sources|run-source`.
- **Podman deployment**: `Containerfile` and `podman-compose.yml` included.
- **Source templates**: `config/sources.example.json`.
- **CSV template**: `data/templates/market_template.csv`.
- **Smoke tests**: `tests/test_smoke.py`.

### CLI examples

```bash
python app/cli.py init-db
python app/cli.py demo
python app/cli.py export
python app/cli.py list-sources
python app/cli.py run-source 1 --category commodity --region Indonesia
```

### Podman

```bash
podman-compose -f podman-compose.yml up --build
```
Then open `http://localhost:8501`.

## v4 refinements

- **Google Trends automatic extraction** using `pytrends`, storing keyword interest as raw CSV, processed CSV, and SQLite observations.
- **Expanded scraping connectors**:
  - HTML tables
  - CSV URLs
  - JSON APIs
  - CSS selector scraping
  - RSS feeds
  - Sitemap URL extraction
  - Paginated table helper
- **Timeframe support**:
  - 10 Year
  - 5 Year
  - Biannual
  - Annual
  - Quartal / Quarterly
  - Bimonthly
  - Monthly
  - Biweek
  - Weekly
  - 3 Day
  - Daily
- **Holy Grail formula library**: `app/holy_grail_formulas.py` contains executable formulas across revenue, pricing, economics, operations, Lean, profitability, DuPont, inventory, depreciation, cash flow, WACC/EVA, liquidity, valuation, risk, options, behavioral finance, MFCS scoring, reverse DCF, and portfolio decisioning.
- **Holy Grail Formulas UI page**: searchable formula registry with dynamic inputs.

### Google Trends CLI

```bash
python app/cli.py google-trends "beras,minyak goreng,gula pasir" --geo ID --timeframe "today 5-y"
```

### CSS selector source example

Use source type `html_selectors` and put selector JSON in the notes field:

```json
{"container":".product","item":".name","price":".price","date":".date"}
```

## v5 refinements

- **Report buttons in the Exports page**:
  - Generate PDF executive report
  - Generate LaTeX `.tex` report
- **CLI report generation**:

```bash
python app/cli.py report --format both
python app/cli.py report --format pdf
python app/cli.py report --format tex
```

- **Notebook documentation**:

```text
docs/indomarket_insight_documentation.ipynb
```

The notebook documents setup, data model, scraping, Google Trends, timeframes, analytics, Holy Grail formulas, ML forecasting, and report generation.

## v6 refinements

- **Backtest page**: walk-forward RandomForest forecast validation with MAE, MAPE, bias, RMSE, chart, and CSV export.
- **Source JSON import/export** from the Sources page and CLI.
- **Run all active sources** batch operation from the UI and CLI.
- **Export manifests**: every CSV/XLSX export now creates a JSON manifest containing rows, columns, and output paths.
- **Richer PDF reports**: generated reports include an embedded trend chart when matplotlib is available.
- **CLI additions**:

```bash
python app/cli.py run-active-sources --category market --region Indonesia
python app/cli.py import-sources config/sources.example.json
python app/cli.py export-sources data/processed/sources_export.json
python app/cli.py backtest "Beras Premium" --horizon 7 --min-train 45 --step 7
```

## v7 refinements

- **Alerts page and CLI**: configurable rules for stale data, quality score, z-score anomalies, large percentage changes, and item price bands.
- **Scenario Lab**: Monte Carlo price path simulation and DCF growth sensitivity scenarios.
- **Optional REST API** with FastAPI:

```bash
make api
# or
uvicorn app.api:api --host 0.0.0.0 --port 8000
```

Endpoints include `/health`, `/summary`, `/quality`, `/observations`, `/alerts`, `/forecast/{item}`, `/report/pdf`, and `/report/tex`.

- **Automated pipeline script**:

```bash
python app/pipeline.py --demo-if-empty --alerts --export --report both
```

- **Production helpers**: `Makefile`, GitHub Actions CI workflow, alert/pipeline config templates.
- **CLI alert command**:

```bash
python app/cli.py alerts
```

## v8 refinements

- **Settings & Backup page**: edit `config/settings.json`, backup SQLite, backup workspace ZIP, and restore SQLite backups.
- **Data Catalog page**: file catalog, database table catalog, and observation column profile.
- **Notifications**: send evaluated alerts to webhook or SMTP email when configured.
- **Parquet export**: full database export to `.parquet` for BI/data engineering workflows.
- **Optional API token protection**: enable in settings and set `INDOMARKET_API_TOKEN` environment variable.
- **Localization foundation**: English/Indonesian translation helper and Indonesian region template.
- **Production hardening**: `pyproject.toml`, app package `__init__.py`, settings templates, and backup utilities.

### New CLI commands

```bash
python app/cli.py backup-db
python app/cli.py backup-workspace
python app/cli.py restore-db backups/your_backup.sqlite.bak
python app/cli.py catalog
python app/cli.py export-parquet
python app/cli.py notify-alerts
```

### API token protection

Set in `config/settings.json`:

```json
{"api_token_enabled": true, "api_token_env": "INDOMARKET_API_TOKEN"}
```

Then run:

```bash
export INDOMARKET_API_TOKEN="change-me"
make api
```

Send requests with header:

```text
X-API-Token: change-me
```

## v9 refinements

- **Data Studio page**: growth metrics, rolling metrics, rebased index, pivot tables, and currency normalization.
- **Sentiment page**: lightweight Indonesian/English lexicon sentiment scoring for scraped titles/items/news.
- **Model Registry page**: lists registered/detected models, exports registry CSV, and generates scheduler snippets.
- **ML metadata auto-registration**: forecasts trained from the app now write model metadata to `models/model_registry.jsonl`.
- **Scheduler helper**: generates cron and systemd timer/service snippets for pipeline automation.
- **New CLI commands**:

```bash
python app/cli.py sentiment
python app/cli.py models
python app/cli.py scheduler-snippets
python app/cli.py growth-metrics
```

## v10 refinement: One-click Windows EXE launcher

Added a Windows one-click launcher source and build scripts:

```text
launcher/windows/Program.cs
launcher/windows/IndoMarketInsightLauncher.csproj
build_one_click_exe.ps1
package_windows_portable.ps1
ONE_CLICK_EXE_README.md
Run_IndoMarket_One_Click.vbs
```

Build the `.exe` on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_one_click_exe.ps1
```

Output:

```text
dist\IndoMarketInsight.exe
```

Create a portable ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File .\package_windows_portable.ps1
```

The launcher automatically creates `.venv`, installs requirements, initializes the DB, starts Streamlit, and opens the browser.

## v11 refinement: production layered architecture

Added a complete production architecture layer split covering:

- frontend
- API
- backend logic
- database and storage
- authentication and authorization
- hosting and deployment
- cloud compute
- CI/CD and version control
- role-level security
- rate limiting
- cache and CDN
- load balancer and scaling
- error tracking and logs
- availability and recovery

Key files:

```text
app/security.py
app/cache_layer.py
app/observability.py
config/rbac.example.json
config/users.example.json
.env.example
podman-compose.prod.yml
infra/nginx/nginx.conf
infra/systemd/
infra/kubernetes/
docs/architecture/production_layers.md
docs/architecture/recovery_runbook.md
.github/workflows/docker-ci-cd.yml
```

Run production-style local stack:

```bash
cp .env.example .env
podman-compose -f podman-compose.prod.yml up --build
```

Then open:

```text
http://localhost
http://localhost/api/health
```

## v12 refinement: fleshed production layers

Added deeper production scaffolding:

- `app/storage_layer.py`: `DATABASE_URL` and SQLAlchemy-ready storage abstraction.
- `app/redis_cache.py`: Redis-ready cache with in-memory fallback.
- `app/workers/`: plain Python worker task scaffolding.
- `scripts/healthcheck.py`: deployment health check script.
- `scripts/backup_rotate.py`: backup rotation helper.
- `scripts/create_admin_user.py`: local user creation helper.
- `migrations/001_sqlite_to_postgres_notes.sql`: PostgreSQL migration notes/schema.
- Terraform skeletons for AWS, GCP, and Azure.
- Architecture docs: RBAC matrix, threat model, deployment checklist, scaling playbook, ADR.

New docs:

```text
docs/layers/README.md
docs/architecture/rbac_matrix.md
docs/architecture/threat_model.md
docs/architecture/deployment_checklist.md
docs/architecture/scaling_playbook.md
docs/adr/ADR-0001-layered-architecture.md
```

Useful commands:

```bash
python scripts/healthcheck.py http://localhost/api/health
python scripts/backup_rotate.py --keep 20
python scripts/create_admin_user.py admin StrongPassword123
python app/workers/worker_cli.py alerts
```

## v13 refinement: deeper production operations

Added:

- Service/repository/API router pattern:
  - `app/repositories/`
  - `app/services/`
  - `app/api_routers/`
- Prometheus metrics endpoint: `/metrics`
- Prometheus/Grafana local configs:
  - `infra/prometheus/prometheus.yml`
  - `infra/grafana/`
- Alembic migration scaffold:
  - `alembic.ini`
  - `alembic/env.py`
  - `alembic/versions/0001_initial_schema.py`
- OpenAPI export script:
  - `python scripts/export_openapi.py`
- Blue/green deployment helper:
  - `scripts/blue_green_deploy.sh`
- SLO, secrets, and runbook docs:
  - `docs/slo/service_level_objectives.md`
  - `docs/security/secrets_policy.md`
  - `docs/runbooks/api_down.md`
  - `docs/runbooks/data_corruption.md`
- ADRs for API layering and Prometheus.

Production observability stack:

```bash
cp .env.example .env
podman-compose -f podman-compose.prod.yml up --build
# API: http://localhost/api/health
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

## v14 refinement: contracts, typed schemas, object storage, and testing

Added:

- Domain entities: `app/domain/entities.py`
- Pydantic API schemas: `app/schemas/`
- Object storage abstraction: `app/object_storage.py`
- API contract docs: `docs/api/api_contract.md`
- MinIO local object storage stack: `podman-compose.storage.yml`
- Environment overlays: `infra/environments/dev|staging|prod/.env.example`
- k6 load-test template: `tests/load/k6_api_smoke.js`
- security-test template: `tests/security/bandit.yaml`
- backup verification: `scripts/verify_backup.py`
- chaos drill script: `scripts/chaos_drill.sh`
- docs for load testing, security testing, backup restore drill, chaos drills, and cloud cost model.

Useful commands:

```bash
python scripts/export_openapi.py
BASE_URL=http://localhost/api k6 run tests/load/k6_api_smoke.js
python scripts/verify_backup.py backups/<backup>.bak
./scripts/chaos_drill.sh

podman-compose -f podman-compose.storage.yml up -d
```

## v16 refinement: full project fleshing and references

Added project-wide reference and integration materials:

- Python API SDK: `sdk/python/indomarket_client.py`
- Project validation script: `scripts/validate_project.py`
- Project inventory generator: `scripts/generate_project_inventory.py`
- Generated inventory: `docs/generated/project_inventory.md`
- Data dictionary: `docs/reference/data_dictionary.md`
- Environment variable reference: `docs/reference/environment_variables.md`
- Configuration reference: `docs/reference/configuration_reference.md`
- Mermaid diagrams:
  - `docs/diagrams/system_context.mmd`
  - `docs/diagrams/deployment_layers.mmd`
  - `docs/diagrams/data_flow.mmd`
- Checklists:
  - `docs/checklists/production_readiness.md`
  - `docs/checklists/source_onboarding.md`
  - `docs/checklists/release_checklist.md`
- Changelog: `CHANGELOG.md`

Useful commands:

```bash
python scripts/validate_project.py
python scripts/generate_project_inventory.py
```

Python SDK example:

```python
from sdk.python.indomarket_client import IndoMarketClient
client = IndoMarketClient("http://localhost/api", token="change-me")
print(client.summary())
```

## v17 refinement: replaced previous container runtime with free open-source Podman

The project now defaults to **Podman**, a free/open-source OCI container runtime that works on Windows 10/11 via Podman Desktop and on cloud Linux VMs.

Replaced container files:

```text
Containerfile
podman-compose.yml
podman-compose.prod.yml
podman-compose.storage.yml
```

Removed previous runtime-specific defaults from the current package and replaced them with Podman files.

Windows 10/11 run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_install_podman.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\windows_run_podman.ps1
```

Linux cloud VM run:

```bash
sudo apt-get update
sudo apt-get install -y podman python3-pip
python3 -m pip install --user podman-compose
cp .env.example .env
./scripts/podman_run_prod.sh
```

Build OCI image:

```bash
podman build -f Containerfile -t localhost/indomarket-insight:latest .
```

Production-style stack:

```bash
podman-compose -f podman-compose.prod.yml up --build -d
```

See:

```text
docs/deployment/podman_windows_cloud.md
docs/deployment/container_runtime_migration.md
```

## v18 refinement: deeper Podman and native deployment support

Added more free/open-source deployment paths:

- Rootless Podman Quadlet systemd files:
  - `infra/podman/quadlet/`
- `podman kube play` local Kubernetes-style manifest:
  - `infra/podman/kube/indomarket-pod.yaml`
- Cloud-init VM bootstrap:
  - `infra/cloud-init/podman-vm-cloud-init.yaml`
- Windows Task Scheduler helpers:
  - `scripts/windows/create_task_scheduler.ps1`
  - `scripts/windows/run_pipeline_native.ps1`
- Native no-container deployment guide:
  - `docs/deployment/native_windows_linux.md`
- Rootless Podman/Quadlet guide:
  - `docs/deployment/podman_rootless_quadlet.md`
- Podman operations runbook:
  - `docs/runbooks/podman_operations.md`

Useful commands:

```bash
./scripts/podman_quadlet_install.sh
./scripts/podman_kube_play.sh
./scripts/podman_cleanup.sh
```

Windows daily pipeline:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_task_scheduler.ps1
```

## v19 refinement: installers, offline support, migration, and cloud VM guides

Added:

- Native Windows installer scripts: `installers/windows/`
- Native Linux and Podman install scripts: `installers/linux/`
- Caddy reverse-proxy alternative: `infra/caddy/Caddyfile`
- Offline wheelhouse install scripts: `scripts/bootstrap/create_wheelhouse.sh`, `install_from_wheelhouse.sh`
- SQLite to PostgreSQL copy helper: `scripts/db/sqlite_to_postgres.py`
- Secret generator: `scripts/bootstrap/generate_secrets.py`
- Full smoke workflow: `scripts/run_smoke_all.sh`
- Cloud VM deployment guides for AWS, GCP, Azure using Podman.

Useful commands:

```bash
./installers/linux/install_native_linux.sh
./installers/linux/install_podman_linux.sh
./scripts/bootstrap/create_wheelhouse.sh
python scripts/bootstrap/generate_secrets.py
./scripts/run_smoke_all.sh
```

Windows native install:

```powershell
powershell -ExecutionPolicy Bypass -File .\installers\windows\install_native_windows.ps1
powershell -ExecutionPolicy Bypass -File .\installers\windows\run_frontend_api_windows.ps1
```

## v20 refinement: modern flat dark UI

Updated the Streamlit interface to a modern flat visual style:

- black background
- earthy color palette
- no emojis or emoticons in text files
- no em dash characters in text files
- minimal animation only
- dark Plotly chart template aligned with the app palette
- Streamlit theme config in `.streamlit/config.toml`
- UI style guide in `docs/ui/README.md`

Primary UI palette:

```text
#050505 black
#0B0B0A panel
#C2A878 earth
#8A9A5B sage
#A66A4C clay
#D8C3A5 sand
#A99B83 muted text
#2A241D border
```

## v21 refinement: one-click start buttons

Added root-level one-click launchers for easier use:

```text
START_INDOMARKET_WINDOWS.cmd
START_INDOMARKET_WITH_API_WINDOWS.cmd
STOP_INDOMARKET_WINDOWS.cmd
START_INDOMARKET_PODMAN_WINDOWS.cmd
START_INDOMARKET_LINUX.sh
STOP_INDOMARKET_LINUX.sh
START_HERE_ONE_CLICK.md
START_HERE.html
```

Windows users can now double-click:

```text
START_INDOMARKET_WINDOWS.cmd
```

To create a desktop shortcut:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_desktop_shortcut.ps1
```

## v22 refinement: debug and diagnostics toolkit

Added practical debugging and one-click troubleshooting:

```text
CHECK_AND_FIX_WINDOWS.cmd
START_INDOMARKET_SETUP_WINDOWS.cmd
scripts/doctor.py
app/diagnostics.py
docs/debug/README.md
```

The dashboard now includes a Diagnostics page.

Run full diagnostics:

```bash
python scripts/doctor.py --fix
```

Windows users can double-click:

```text
CHECK_AND_FIX_WINDOWS.cmd
```

The Windows API launcher was also fixed so it no longer waits on the dashboard launcher before starting the API.

## v23 refinement: deeper debug and audit pass

Fixed and added:

- Fixed `scripts/doctor.py --json` so it produces clean JSON output.
- Replaced remaining active old container runtime commands with Podman commands.
- Fixed `scripts/chaos_drill.sh` to use `podman-compose`.
- Updated Windows portable packaging to include `Containerfile` and Podman compose files.
- Added text policy audit script: `scripts/audit_text_policy.py`.
- Added runtime reference audit script: `scripts/audit_runtime_references.py`.
- Added audit docs: `docs/audit/README.md`.

Debug commands:

```bash
python scripts/doctor.py --fix
python scripts/doctor.py --json
python scripts/audit_text_policy.py
python scripts/audit_runtime_references.py
pytest -q
```

## v24 refinement: support bundle and repair workflow

Added deeper debug and support tooling:

```text
scripts/create_debug_bundle.py
scripts/repair_project.py
scripts/port_report.py
scripts/dependency_report.py
app/debug_support.py
REPAIR_INDOMARKET_WINDOWS.cmd
DEPENDENCY_REPORT_WINDOWS.cmd
docs/debug/troubleshooting_matrix.md
```

New commands:

```bash
python scripts/repair_project.py --demo
python scripts/create_debug_bundle.py
python scripts/port_report.py
python scripts/dependency_report.py
```

The Diagnostics page now includes recent log viewing.

## v25 refinement: Hermes Analytics ID brand lore and attribution

Added brand attribution and lore:

```text
Developed by: Ahmad Bara Wirayudha
GitHub: https://github.com/AhmadBaraWirayudha
```

Added:

```text
docs/brand/brand_lore.md
assets/brand/hermes_analytics_id_logo.svg
```

The Streamlit UI now includes a Brand Lore page and uses the Hermes Analytics ID name in the interface. The visual language combines a black background, deep navy, mercury silver, cadmium gold, and restrained earth accents.

## v26 refinement: Hermes product modules expanded

Expanded the Hermes Analytics ID product pillars:

- The Winged Messenger: real-time alerts, real-time data, and machine learning for IDX, Bank Indonesia macro news, and strategic commodities.
- The Caduceus Hub: localized market insights, regulatory explainers in Bahasa Indonesia, and AI-driven consumer trend predictions.
- The Crossroad Guide: robo-advisory and portfolio decision workflows inspired by Hermes as a guide at life's crossroads.

Added:

```text
docs/brand/product_modules.md
```

## v27 refinement: compliance, Indonesian law map, policies, and geopolitics

Added detailed governance documentation:

```text
docs/compliance/
docs/policies/
docs/geopolitics/
config/compliance/
```

Added app page:

```text
Compliance
```

Coverage includes:

- international standards such as ISO 27001, ISO 27701, ISO 22301, ISO 31000, NIST CSF, CIS Controls, OWASP, ISO 42001, OpenAPI, OAuth, and WCAG references
- Indonesian legal and regulatory domain mapping for PDP, PSE, OJK, BI, IDX data rights, Bappebti, consumer protection, e-commerce, competition, tax, IP, AML CFT, cybersecurity, and third-party risk
- policy templates for privacy, data governance, scraping, security, model risk, AI governance, AML and sanctions, marketing, business continuity, and third-party risk
- Indonesia geopolitical risk framework covering politics, BI policy, IDR, commodities, China and US competition, ASEAN, maritime security, climate, food, energy, and digital sovereignty

This material is a compliance operating framework and not legal advice.

## v28 refinement: real-time OSINT, Indonesian news, and tension monitoring

Added:

```text
app/osint_monitor.py
app/api_routers/osint.py
config/osint_sources.example.json
scripts/run_realtime_monitor.py
START_REALTIME_MONITOR_WINDOWS.cmd
START_REALTIME_MONITOR_LINUX.sh
docs/osint/README.md
```

New app page:

```text
Real-Time Monitor
```

Capabilities:

- Pentagon Pizza Index and DEFCON-style tension indicator monitoring from permitted public pages.
- Indonesian RSS and web source monitoring.
- Approved social media CSV import.
- Keyword extraction, sentiment scoring, and event storage.
- Automatic run every five minutes with `python scripts/run_realtime_monitor.py --interval 300`.
- FastAPI endpoints under `/osint`.

Compliance note: use official APIs, RSS feeds, permitted public pages, and approved social media exports. Do not bypass access controls, platform terms, paywalls, CAPTCHAs, or rate limits.

## v29 refinement: extended real-time signal capability

Added a real-time signal engine:

```text
app/realtime_engine.py
app/api_routers/realtime.py
config/realtime_watchlist.json
docs/osint/realtime_signal_engine.md
```

New capabilities:

- watchlist-based scoring for IDX, Bank Indonesia, nickel, CPO, coal, geopolitics, and regulatory terms
- real-time signal severity levels: critical, high, medium, low, info
- real-time run history
- signal export to CSV
- `/realtime` API endpoints
- enhanced Real-Time Monitor UI with Signals, Watchlist, Events, Tension Indicators, and Social Import tabs

Run every five minutes:

```bash
python scripts/run_realtime_monitor.py --interval 300
```

## v30 refinement: friendly simple wording

Updated the user-facing app labels and guides to be easier to read quickly.

Added:

```text
QUICK_START_5_SECONDS.md
docs/simple/README.md
docs/simple/plain_language_glossary.md
docs/simple/friendly_workflow.md
```

The app now uses simpler page names such as Live Monitor, Data Check, Files and Data, Data Tools, What If, Forecast, Downloads, Settings, and Checkup.

## v31 refinement: simple Start page and friendly checks

Added:

```text
docs/simple/one_page_manual.md
docs/simple/page_map.md
scripts/audit_friendly_language.py
```

The app now opens with a Start page. It gives a simple 3-step path:

1. Add data.
2. Read signals.
3. Make output.

It also includes quick buttons for demo data, app health, live sources, and watchlist rules.
