# Worker Tasks

Background task scaffolding for scraping, alerts, reports, exports, and model inventory.

For small deployments, run directly with `worker_cli.py`. For production, connect these tasks to Celery, RQ, Arq, Cloud Tasks, SQS, Pub/Sub, or another queue system.
