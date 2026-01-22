# Docker Setup for Antiques project

This document describes how to set up and use Docker for the Antiques application.



## Docker Commands

### Building images

```bash
# Production image
make docker-build

# Development image
make docker-build-dev

# Testing image
make docker-build-test
```

### Starting services

```bash
# Start all services (production)
make docker-up

# Start development environment
make docker-up-dev

# Stop all services
make docker-down
```

### Database operations

```bash
# Run all database migrations
make docker-migrate
```


```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U antiques_user -d antiques
```


### Testing

```bash
# Run tests in Docker
make docker-test

# View test coverage reports
docker-compose --profile test run --rm test
```

### Debugging

```bash
# View logs
make docker-logs

# Logs for the application only
make docker-logs-app

# Open a shell in the container
make docker-shell
```

## Docker Compose Profiles

### production (default)
- app (production)

- postgres



### dev
- app-dev (with hot reload)

- postgres (with exposed ports)



### migrate
- migrate (run migrations)

### test
- test (run tests)

### dev-tools
- adminer (web interface for DB)

## Environment Variables

### Required

- DATABASE_URL - PostgreSQL connection URL



### Опциональные
- `ENVIRONMENT` - environment (production/development/testing)
- `LOG_LEVEL` - logging level
- `API_HOST` - API host
- `API_PORT` - API port
- `API_WORKERS` - number of worker processes

## Volumes

### Named Volumes

- postgres_data - PostgreSQL data


- app_logs - application logs
- test_reports - test reports

### Bind Mounts (development)
- `./src:/app/src` - source code
- `./tests:/app/tests` - tests
- `./alembic:/app/alembic` - migrations

## Network

All services are connected to the `antiques-network` for isolation.

## Health Checks

Все сервисы имеют health checks:
- **app**: HTTP request to /api/docs

- **postgres**: pg_isready



## Monitoring

### Logs
```bash
# All services
docker-compose logs -f

# Application only
docker-compose logs -f app
```

