# Simple Product App: Design

**Date:** 2026-11-01. **Status:** approved; an implementation plan follows.

## Goal

A barebones reference app for creating and listing products, run locally. It should be simple to
start, easy to understand and easy to build on. Where two options meet the requirements equally
well, choose the one with fewer pieces.

## Requirements

- Backend: Python 3.14, Poetry and Flask.
- Database: PostgreSQL with one table, `products`. Its `id` is a UUID primary key and its `name`
  is a required string. Nothing else.
- API: list products and create a product.
- UI: a simple page that lets the user create a product. It also shows the list, so the result
  is visible.
- Built test-first, with pre-commit hooks.
- README: names the tech stack and has exactly these headings: Prerequisites, Database setup,
  Start backend, Start frontend, Verify (open local host), Notes.
- Local only: no deployment target. The git repo is local and commits go straight to `main`.

## Decisions

| Area       | Decision                                                                      |
|:-----------|:------------------------------------------------------------------------------|
| Run model  | PostgreSQL 18 runs in Docker Compose as its only service. Flask runs directly with Poetry. |
| Frontend   | HTML pages rendered by Flask with Jinja templates. No JavaScript build and no Node. |
| Data       | The SQLAlchemy 2.1 ORM over psycopg 3. Alembic migrations, configured in `pyproject.toml`. |
| Checks     | flake8 (settings in `pyproject.toml` via Flake8-pyproject), Black and isort.  |
| Hooks      | Every pre-commit hook is local and runs through `poetry run`, so `poetry.lock` pins each tool. |
| Tests      | pytest, plus Testcontainers for tests that need PostgreSQL. 100% branch coverage over `src/`. |
| Packages   | Runtime packages and dev tools are in separate lists in `pyproject.toml`.     |

## Architecture

```
src/simple_product_app/
  __init__.py        create_app(): config, SQLAlchemy engine, blueprints
  models.py          Product model
  products.py        clean_name(), list_products(), create_product(), used by the API and the UI
  api.py             GET and POST /api/products (JSON)
  ui.py              GET and POST / (HTML form and list)
  templates/index.html
migrations/          Alembic env.py and one revision
tests/
  conftest.py        shared fixtures
  test_readme.py     pins the README headings
  unit/              no database
  integration/       real PostgreSQL via Testcontainers
```

- `create_app(database_url=None)` builds one engine and keeps it on the app. Each request opens
  a short-lived SQLAlchemy `Session` from it. Nothing connects at import time.
- The API and the UI are thin. They parse input, call `products.py`, and shape the response.
- Configuration is the `DATABASE_URL` environment variable. Its default,
  `postgresql://postgres:postgres@localhost:5432/simple_product_app`, matches `compose.yaml`, so
  `flask run` and `alembic upgrade` work with no setup. Alembic's `env.py` uses the same URL, and
  tests pass their own.

## Data model

| Column | Type   | Rules                                   |
|:-------|:-------|:----------------------------------------|
| `id`   | `uuid` | Primary key, `DEFAULT uuidv7()`         |
| `name` | `text` | `NOT NULL`                              |

- One Alembic revision creates the table. Alembic also keeps its own one-row `alembic_version`
  table, which is how it tracks applied migrations.
- The list is `ORDER BY id`. UUIDv7 values are time-ordered, so this is creation order, oldest
  first, without a timestamp column.

## Name rules

`clean_name(value)` is the only place these rules live:

- The value must be a string that isn't blank once trimmed with Python's `str.strip()`.
- The trimmed value is what gets stored.
- Otherwise it raises `ValueError("Name is required.")`.

Duplicate names are allowed and there is no maximum length. Neither is a requirement.

## API

| Request                                    | Success                                              |
|:-------------------------------------------|:-----------------------------------------------------|
| `GET /api/products`                        | `200` `{"products": [{"id": "…", "name": "…"}]}`     |
| `POST /api/products` with `{"name": "…"}`  | `201` `{"id": "…", "name": "…"}`                     |

| Problem                                                        | Status | Body                          |
|:---------------------------------------------------------------|:-------|:------------------------------|
| Missing, blank or non-string `name`, or a body that isn't a JSON object | `422` | `{"error": "Name is required."}` |
| Malformed JSON                                                 | `400`  | `{"error": "<Flask's message>"}` |
| Body that isn't JSON (wrong `Content-Type`)                    | `415`  | `{"error": "<Flask's message>"}` |

- Unknown fields are ignored.
- An error handler on the API blueprint renders Flask's own 400 and 415 errors as JSON. Their
  `error` text is Flask's standard description for each error.
- There is no pagination, no lookup by id and no `Location` header.

## UI

- `GET /` shows a labelled **Name** field (`required`), a **Create product** button, and the
  product list. When there are no products, it shows "No products yet."
- `POST /` with a valid name saves the product and redirects to `/` with a 302. This is
  Post/Redirect/Get, so reloading the page doesn't resubmit the form.
- `POST /` with a blank name shows the page again with status 422, the typed value and the
  message "Name is required." The message is linked to the field with `aria-describedby`, and the
  field gets `aria-invalid="true"`.

## Testing

- Unit tests are written before integration tests. Every test has a GIVEN/WHEN/THEN docstring.
- Expected values come from fixtures or named constants, never inline literals.
- Shared fixtures live in `tests/conftest.py`.
- **Unit tests (no database):**
  - `clean_name()`
  - the app factory's database URL
  - the API's 415, 400 and 422 responses, which return before any database call
- **Integration tests** (`@pytest.mark.integration`, never skipped):
  - **Fixtures:**
    - One `postgres:18-alpine` container per test run, started by Testcontainers with explicit
      credentials.
    - The real Alembic migrations run once against it.
    - Every test starts with `DELETE FROM products`.
    - Engines are disposed of at teardown.
  - **What they cover:**
    - creating and listing through the API, in creation order
    - creating through the UI (redirect, then the list)
    - the UI's blank-name response
    - `alembic check`, which proves the model and the migrations agree
- **Coverage:** `pytest --cov` over `src/`, with branch coverage and a floor of 100%.
- The pre-commit `pytest` hook runs the whole suite, so Docker must be running to commit.

## README

The six headings are fixed and `tests/test_readme.py` enforces them. "Start frontend" says that
the backend serves the UI at <http://localhost:8000/>. The "In progress" note comes out once the
app works end to end.

## Out of scope

- Updating or deleting products, lookup by id, and pagination
- Authentication, CSRF protection, a health endpoint and logging configuration
- A Docker image for the app, deployment, and CI
