include mk/docs.mk
include mk/help.mk

type-check:  ## Check types with mypy
	poetry run mypy .

test:  ## Run tests
	poetry run pytest -v

lint: ## Check code style (read-only)
	poetry run ruff check

fix:  ## Auto-fix lint issues
	poetry run ruff check --fix

ci: lint type-check test  ## CI check (read-only: lint + type-check + test)

check: format fix type-check test  ## Full check (format + fix + type-check + test)

format:  ## Format code with ruff
	poetry run ruff format

setup:  ## Install dependencies
	poetry install
	poetry run playwright install firefox

clean: ## Remove cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

run:  ## Run docker compose with build
	docker compose -f docker-compose.dev.django_orm.yml up --build

rebuild:  ## Rebuild docker compose with clean
	docker compose -f docker-compose.dev.django_orm.yml down -v || true
	docker rmi wse-django-orm wse-postgres 2>/dev/null || true
	docker builder prune -f || true
	docker compose -f docker-compose.dev.django_orm.yml up --build