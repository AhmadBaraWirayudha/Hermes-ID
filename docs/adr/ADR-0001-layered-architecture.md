# ADR-0001: Layered Architecture

## Status

Accepted

## Context

The project started as a local Streamlit app but now requires production layers: API, backend logic, storage, auth, deployment, CI/CD, scaling, logging, and recovery.

## Decision

Adopt a layered architecture while keeping the local MVP runnable:

- Streamlit remains the primary frontend.
- FastAPI exposes integration endpoints.
- Backend logic stays modular in `app/`.
- SQLite remains default; PostgreSQL is supported via `DATABASE_URL` planning.
- Podman Compose is the default production-style deployment.
- Kubernetes/Terraform are provided as skeletons.

## Consequences

- Local onboarding remains simple.
- Production migration path is clearer.
- More files/configs exist, but each has a focused responsibility.
