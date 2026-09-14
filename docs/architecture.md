# Architecture

This document describes the target architecture of the DevOps Task Manager.

## 1. System Overview

The system is a three-tier web application:

- **Presentation layer:** React frontend served to the browser
- **Application layer:** FastAPI backend exposing a REST API
- **Data layer:** PostgreSQL database

All layers are containerized and designed for Kubernetes deployment.

## 2. Component Responsibilities

| Component   | Responsibility                                        |
| ----------- | ----------------------------------------------------- |
| React       | UI, user interactions, calls backend API              |
| FastAPI     | Business logic, validation, persistence, REST API     |
| PostgreSQL  | Durable data store for tasks and users                |

## 3. Request Flow

A typical user request follows this path:

1. Browser loads React app (static assets)
2. React sends HTTP request to FastAPI `/api/...`
3. FastAPI validates input and queries PostgreSQL
4. FastAPI returns JSON response
5. React updates the UI

## 4. Networking & Ports (Planned)

| Service    | Default Port | Notes                               |
| ---------- | ------------ | ----------------------------------- |
| React      | 3000         | Dev server; served statically in prod |
| FastAPI    | 8000         | Uvicorn                             |
| PostgreSQL | 5432         | Internal only                       |
| Nginx      | 80 / 443     | Reverse proxy in front of React     |

## 5. State & Persistence

- Only PostgreSQL holds durable state.
- React and FastAPI are stateless (horizontally scalable).
- Database migrations handled via Alembic (to be introduced).

## 6. Failure Modes

| Failure                     | Impact                  | Mitigation                        |
| --------------------------- | ----------------------- | --------------------------------- |
| FastAPI pod crash           | Requests fail           | Replicas + readiness probes       |
| PostgreSQL unavailable      | Writes fail             | Backups, retries, connection pool |
| React asset CDN outage      | UI does not load        | Multi-region CDN (future)         |
| Misconfigured env vars      | App refuses to start    | Startup validation                |

## 7. Future Evolution

- Introduce Redis for caching and session storage
- Add observability (Prometheus, Loki, OpenTelemetry)
- Move to multi-environment (dev / staging / prod)
- Adopt GitOps with Argo CD

## 8. Non-Goals

- Microservices decomposition
- Multi-tenant support
- Real-time collaboration

This document intentionally describes a simple system so the DevOps
lifecycle — not the application itself — remains the focus.
