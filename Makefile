# Check types (mypy)
type-check:
	poetry run mypy .

# Run tests
test:
	poetry run pytest -v

# Lint code (read-only, no fixes)
lint:
	poetry run ruff check

# Auto-fix lint issues
fix:
	poetry run ruff check --fix

# CI pipeline (read-only checks, no changes)
ci: lint type-check test

# Full pre-commit check (format + fix + type-check + test)
check: format fix type-check test

# Format code
format:
	poetry run ruff format

# Install dependencies
setup:
	poetry install
	poetry run playwright install firefox

# Remove cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

# Build documentation (HTML)
docs-build:
	poetry run make -C docs clean html

# Build docs and open in default browser
docs-open: docs-build
	xdg-open docs/build/html/index.html

run-flask:
	@poetry run flask --app src/wse/entrypoints/flask_app/app.py run --port 5005 --debug

run-django:
	@poetry run src/wse/site/manage.py runserver

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make setup        - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Check code style (read-only)"
	@echo "  make fix          - Auto-fix lint issues"
	@echo "  make type-check   - Check types with mypy"
	@echo "  make format       - Format code with ruff"
	@echo "  make check        - Full check (format + fix + type-check + test)"
	@echo "  make ci           - CI check (read-only: lint + type-check + test)"
	@echo "  make clean        - Remove cache files"
	@echo "  make docs-build   - Build HTML documentation"
	@echo "  make docs-open    - Build docs and open in browser"
	@echo "  make run-flask    - Run Flask entrypoint"
	@echo "  make run-django   - Run Django entrypoint"