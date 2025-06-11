# my-board-job

A Django-based job board API with JWT authentication, API key support, and interactive API docs via Swagger and Redoc.

## Features

- User registration and authentication (JWT)
- Job posting and management endpoints
- API key support for secure integrations
- Interactive API documentation (Swagger, Redoc)
- Pre-commit hooks for code quality (black, isort, mypy)

## Quickstart

```bash
# Install dependencies
poetry install

# Run migrations
poetry run python manage.py migrate

# Create a superuser
poetry run python manage.py createsuperuser

# Start the development server
poetry run python manage.py runserver
```

## API Documentation

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc UI: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Code Quality

This project uses [pre-commit](https://pre-commit.com/) with hooks for:
- black (formatting)
- isort (import sorting)
- mypy (type checking)
- trailing whitespace and end-of-file fixes

To install hooks:

```bash
poetry run pre-commit install
```

To run all hooks on all files:

```bash
poetry run pre-commit run --all-files
```

## Running Tests

```bash
poetry run pytest
```
