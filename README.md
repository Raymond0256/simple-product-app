# Simple Product App

> **Draft:** this README was started before the design was approved. Sections marked
> *(pending)* are waiting on open decisions:
>
> - the frontend framework
> - the migration tool
> - how pre-commit is installed
> - the ports

A small reference app for creating and listing products. A Flask JSON API is backed by
PostgreSQL, and a simple web UI sits on top. It is built test-first and runs locally with one
Docker Compose command. There is no deployment target.

**Tech stack**

- **Backend:** Python 3.14 and Flask, with Poetry for dependency management
- **Database:** PostgreSQL, with a single `products` table
- **Frontend:** *(pending: React with Vite, or something simpler)*
- **Tests and checks:** pytest, written test-first, plus pre-commit hooks
- **Local runtime:** Docker Compose

## Prerequisites

- Docker with Compose v2, such as Rancher Desktop or Docker Desktop.
- Python 3.14 and Poetry 2.x, to run the backend and its tests outside Docker.
- pre-commit *(pending: installed through Poetry or pipx)*.

## Database setup

PostgreSQL runs as the `db` service in Docker Compose. Its data lives in a named Docker volume,
so it survives restarts.

The schema is one table:

| Table      | Column | Type | Rules       |
|:-----------|:-------|:-----|:------------|
| `products` | `id`   | UUID | Primary key |
| `products` | `name` | text | Required    |

*(pending: the migration tool and the command that creates the table)*

## Start backend

*(pending: the Poetry and Flask commands, and the port)*

## Start frontend

*(pending: the frontend decision)*

## Verify (open local host)

*(pending: the ports)* Open the UI in a browser, create a product, and check that it appears
in the list. To check the API directly, request `GET /api/products`.

## Notes

- **One command:** `docker compose up --build` builds and starts the database, backend and
  frontend together.
- **Local only:** there are no Kubernetes (NSK) manifests, Standard Pipeline workflows, or New
  Relic agent.
- **Public package sources:** Python packages come from PyPI, JavaScript packages from the npm
  registry, and container images from Docker Hub. Nothing is pulled from Artifactory. This
  departs from the Python SIG's Artifactory rules (DEP-1, DEP-2) and its CIC base-image rule
  (IMG-1) in the
  [PySIG recommendations inventory](https://github.com/Nordstrom-Internal/APP08745-sig-python-decisions/blob/main/inventory/pysig-recommendations.md).
- **Python 3.14:** published SIG guidance still recommends 3.11 or 3.13 (VER-1). Enabling 3.14
  is an approved H2 2026 SIG priority (conflict X-8 in the same inventory).
