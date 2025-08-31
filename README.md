
# Learn FastAPI

A simple FastAPI learning repository with authentication, PostgreSQL integration, and Docker support.

## Features

- FastAPI web framework
- User authentication
- PostgreSQL database (via Docker)
- SQLAlchemy ORM
- JWT authentication (python-jose)
- Docker & Docker Compose support

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/quangliz/learn-fastapi.git
cd learn-fastapi
```

### 2. Install dependencies

Install [uv](https://github.com/astral-sh/uv) and sync dependencies:

```bash
pip install uv
uv sync --frozen
```

### 3. Start PostgreSQL (Docker Compose)

```bash
docker compose up -d postgres
```

### 4. Run the FastAPI app (development)

```bash
uv run uvicorn app.main:app --reload
```

### 5. Or run everything with Docker Compose

```bash
docker compose up --build
```

## API Documentation

Once running, access the interactive API docs at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure

```
app/
	main.py         # FastAPI app entrypoint
	models/         # SQLAlchemy models
	routers/        # API route definitions
	schemas/        # Pydantic schemas
	auth/           # Authentication logic
	database/       # Database connection
day1.py, day2.py  # Learning scripts
Dockerfile        # Docker build file
docker-compose.yaml # Multi-service orchestration
pyproject.toml    # Project dependencies
```

## Environment Variables

Set in `docker-compose.yaml` for local development:

- `DATABASE_URL=postgresql://postgres:postgres@postgres:5432/fastapi_db`

## License

MIT