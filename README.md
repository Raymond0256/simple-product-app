# Simple Product App

> **In progress:** the app is being built test-first. Until it is, the migration and Flask
> commands below, and the addresses they serve, don't work yet.

A small reference app for creating and listing products. A Flask JSON API is backed by
PostgreSQL, and a simple web UI sits on top. It is built test-first. Flask runs directly on your
machine and PostgreSQL runs in Docker. There is no deployment target.

**Tech stack**

- **Backend:** Python 3.14 and Flask, with Poetry for dependency management
- **Database:** PostgreSQL 18 in Docker Compose, with a single `products` table
- **Data access:** the SQLAlchemy ORM over the psycopg 3 driver, with Alembic for migrations
- **Frontend:** HTML pages rendered by Flask with Jinja templates; no JavaScript build
- **Tests and checks:** pytest (written test-first), with Testcontainers for database tests;
  flake8, Black and isort; all run by pre-commit hooks

## Prerequisites

- Docker with Compose v2, such as Rancher Desktop or Docker Desktop. It runs PostgreSQL and the
  throwaway databases the tests use.
- Python 3.14 and Poetry 2.x.

## Database setup

PostgreSQL runs as the `db` service in Docker Compose, on `localhost:5432`. Its data lives in a
named Docker volume, so it survives restarts.

The schema is one table:

| Table      | Column | Type | Rules       |
|:-----------|:-------|:-----|:------------|
| `products` | `id`   | UUID | Primary key |
| `products` | `name` | text | Required    |

Start PostgreSQL, install the app, and create the table:

```sh
docker compose up -d
poetry env use python3.14
poetry install
poetry run alembic upgrade head
```

`poetry env use` only needs to run once; it tells Poetry which Python to use. Alembic migrations
create the schema and keep it up to date.

## Start backend

```sh
poetry run flask --app simple_product_app run --debug --port 8000
```

The API is at <http://localhost:8000/api/products>. `--debug` reloads the server when the code
changes. The app uses port 8000 because on macOS, AirPlay Receiver already listens on Flask's
default port, 5000.

## Start frontend

Nothing separate to start: the backend serves the UI at <http://localhost:8000/>.

## Verify (open local host)

Open <http://localhost:8000/>, enter a product name, and select **Create product**. The new
product appears in the list on the same page.

To check the API directly:

```sh
curl http://localhost:8000/api/products
```

## Notes

- **Checks on every commit:** run `poetry run pre-commit install` once. Each commit then runs
  isort, Black, flake8 and the full test suite with coverage.
- **Tests:** `poetry run pytest --cov` runs everything. Tests marked `integration` start a
  throwaway PostgreSQL container with Testcontainers, so Docker must be running.
- **Stopping:** `docker compose down` stops PostgreSQL. Add `-v` to delete its data too.
