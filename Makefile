.PHONY: help install install-dev lint lint-fix format type-check check clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	poetry sync
	poetry install --no-root

install-dev: ## Install development dependencies
	poetry sync
	poetry install --no-root --with dev

lint: ## Run linting with ruff
	poetry run ruff check src/gtree/

lint-fix: ## Run linting with ruff and fix auto-fixable issues
	poetry run ruff check --fix src/gtree/

format: ## Format code with ruff
	poetry run ruff format src/gtree/

type-check: ## Run type checking with mypy
	poetry run mypy src/gtree/

check: ## Run all checks (lint + format check + type check)
	poetry run ruff check src/gtree/
	poetry run ruff format --check src/gtree/
	poetry run mypy src/gtree/

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage

dev-setup: install-dev ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make check' to verify everything is working."

# Database migration commands
migration: ## Create a new migration file
	poetry run alembic revision --autogenerate -m "$(msg)"

migrate: ## Apply all pending migrations
	poetry run alembic upgrade head

migrate-downgrade: ## Downgrade to previous migration
	poetry run alembic downgrade -1

migrate-history: ## Show migration history
	poetry run alembic history

migrate-current: ## Show current migration
	poetry run alembic current

migrate-stamp: ## Stamp database with current migration (without applying)
	poetry run alembic stamp head

# Docker commands
#docker-build-prod: ## Build Docker image for production
#	docker build --target production -t gtree:latest .

#docker-build-dev: ## Build Docker image for development
#	docker build --target development -t gtree:dev .

docker-up-prod: ## Start all services with docker compose
	docker compose -f docker-compose.prod.yml up -d

docker-up-dev: ## Start development environment
	docker compose -f docker-compose.yml up -d

docker-down-prod: ## Stop all services
	docker compose -f docker-compose.prod.yml down

docker-down-dev: ## Stop all services
	docker compose -f docker-compose.yml down

docker-logs-prod: ## Show logs for all services
	docker compose -f docker-compose.prod.yml logs -f

docker-logs-dev: ## Show logs for all services
	docker compose -f docker-compose.yml logs -f

docker-logs-app-prod: ## Show logs for application
	docker compose -f docker-compose.prod.yml logs -f app

docker-logs-app-dev: ## Show logs for application
	docker compose -f docker-compose.yml logs -f app-dev

docker-shell-prod: ## Open shell in running app container
	docker compose -f docker-compose.prod.yml exec app bash

docker-shell-dev: ## Open shell in running app container
	docker compose -f docker-compose.yml exec app bash

docker-clean-prod: ## Clean up Docker resources
	docker compose -f docker-compose.prod.yml down -v --remove-orphans
	docker system prune -f

docker-clean-dev: ## Clean up Docker resources
	docker compose down -v --remove-orphans
	docker system prune -f

docker-rebuild-prod: ## Rebuild and restart services
	docker compose -f docker-compose.prod.yml down
	docker compose -f docker-compose.prod.yml build --no-cache
	docker compose -f docker-compose.prod.yml up -d

docker-rebuild-dev: ## Rebuild and restart services
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml build --no-cache
	docker compose -f docker-compose.yml up -d

docker-migrate-prod: ## Run database migrations
	docker compose -f docker-compose.prod.yml run --rm migrate

docker-migrate-dev: ## Run database migrations
	docker compose -f docker-compose.yml run --rm migrate-dev

# Environment setup
setup-env: ## Create .env file from template
	bash ./scripts/setup-env.sh

# Development helpers

dev-setup-docker: setup-env ## Set up development environment with Docker
	docker compose -f docker-compose.yml up -d postgres
	@echo "Waiting for services to be ready..."
	@sleep 10
	bash ./scripts/init-db.sh
	make docker-migrate-dev
	@echo "Development environment is ready!"
	@echo "Run 'make docker-up-dev' to start the application"

ci: check ## Run CI pipeline (lint + type check)
	@echo "CI pipeline completed successfully!"
