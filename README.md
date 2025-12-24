# ToDoList Project

A modern, object-oriented ToDoList application built in Python, developed in 4 phases for the Software Engineering Course at AUT.

## Overview

This project implements a complete ToDo list manager with projects and nested tasks, evolving from a simple CLI to a full RESTful web API.

## Phases

### Phase 1 - In-Memory CLI
- Console-based application with Persian UI
- Layered architecture (Models → Repositories → Services → CLI)
- Full CRUD for projects and tasks
- Validations: word limits, unique names, max limits from `.env`, future deadlines
- Cascade delete, sorted lists, Persian messages

Run: `poetry run python -m src.cli.console`

### Phase 2 - RDB Persistence
- PostgreSQL database (via Docker)
- SQLAlchemy ORM models with `closed_at` field
- Alembic migrations
- Repository pattern for data access
- Auto-close overdue tasks (scheduler runs every 15 minutes)

Run CLI (now persistent): `poetry run python -m src.cli.console`  
Run scheduler: `poetry run python -m src.commands.scheduler`

### Phase 3 - Web API
- FastAPI RESTful API
- Pydantic schemas for validation and serialization
- Endpoints: `/v1/projects` and `/v1/projects/{id}/tasks`
- Automatic Swagger UI documentation

Run server: `poetry run uvicorn main:app --reload`  
Docs: http://127.0.0.1:8000/docs

### Phase 4 - Postman Testing
- Full API testing using Postman
- Collection covering all CRUD operations
- Proper status codes and response validation

## Tech Stack
- Python 3.12
- Poetry for dependency management
- FastAPI, SQLAlchemy, Alembic
- PostgreSQL (Docker)
- Pydantic, Uvicorn

## Setup
```bash
# Install dependencies
poetry install

# Start database
docker compose up -d

# Run migrations
poetry run alembic upgrade head

# Run CLI
poetry run python -m src.cli.console

# Run API
poetry run uvicorn main:app --reload
