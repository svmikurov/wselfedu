# Load data to create a database
include .env
DB_NAME ?= $(DB_NAME)
DB_USER ?= $(DB_USER)
DB_PASS ?= $(DB_PASSWORD)

# Defining color for messages
GREEN  := \033[0;32m
RED    := \033[0;31m
RESET  := \033[0m

# Run server in development mode
run:
	python3 manage.py runserver

# Run deployment
deploy: format \
		mypy \
		check-connections \
		recreate_db \
		makemigrations \
		migrate \
		load_initial_data \
		pytest-cov


# Testing and code checking


# Code style checking
ruff:
	ruff check && ruff format --diff

# Fix code format
format:
	ruff check --fix && ruff format

# Static type checking
mypy:
	mypy .

# Pytest
pytest:
	pytest .

# Pytest with configured coverage
pytest-cov:
	pytest --cov=. \
    --cov-report=term-missing:skip-covered \
    --cov-report=html

# Combined checking
check: format mypy pytest-cov


# Database commands


# Check active PostgreSQL connections
check-connections:
	@echo "Checking active PostgreSQL connections..."
	@if [ $$(psql -U $(DB_USER) -d $(DB_NAME) -t -c "SELECT COUNT(*) FROM pg_stat_activity WHERE datname = '$(DB_NAME)' AND pid <> pg_backend_pid();") -gt 0 ]; \
	then \
		echo "$(RED)ERROR: Active connections detected. Aborting.$(RESET)"; \
		exit 1; \
	else \
		echo "$(GREEN)No active connections. Proceeding...$(RESET)"; \
	fi

# Drop existing DB and role, create role and DB
recreate_db:
	sudo -u postgres psql \
	-v db_name=$(DB_NAME) \
	-v db_user=$(DB_USER) \
	-v db_password=$(DB_PASS) \
	-f db/sql/init/create_db.sql

# Django migration creating
makemigrations:
	python manage.py makemigrations

# Apply Django migrations
migrate:
	python manage.py migrate

# Load inial data fixtures
load_initial_data:
	# TODO: Fix temporary "yes" answer
	echo "yes" | python manage.py load_initial_data --load-sensitive


# Django-extensions


# Build model graphs
# https://django-extensions.readthedocs.io/en/latest/graph_models.html#example-usage
graph_models:
	mkdir -p temp/graph_models/ && \
	python manage.py graph_models \
		-o temp/graph_models/models.png \
		--verbose-names \
		--inheritance