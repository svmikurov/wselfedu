include .env

ifeq (${ENVIRONMENT}, development)
	COMPOSE := docker compose -f docker-compose.dev.yml
else ifeq (${ENVIRONMENT}, production)
	COMPOSE := docker compose -f docker-compose.prod.yml
endif

APP := @$(COMPOSE) exec wse-project
MANAGE := @$(APP) python manage.py


# Docker
build:
	@$(COMPOSE) build

up:
	@$(COMPOSE) up -d

down:
	@$(COMPOSE) down


# Django
makemigrations:
	@$(MANAGE) makemigrations

dry-run:
	@$(MANAGE) makemigrations --dry-run

migrate:
	@$(MANAGE) migrate

collectstatic:
	@$(MANAGE) collectstatic --noinput

loaddata:
	@$(MANAGE) loaddata db-wse-sweb.json

dumpdata:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db-wse-sweb.json


# Tests
lint:
	@$(APP) flake8

ruff:
	ruff check

test:
	@$(APP) pytest tests/

plw:
	@$(APP) pytest tests_e2e/

check: lint test plw

get-state:
	@$(APP) sh -c "pytest tests_e2e/auth/get_auth_state.py"

test-just:
	@$(APP) pytest tests/tests_english_task/test_english_analytic.py

# PostgreSQL
connect:
	@$(COMPOSE) exec wse-db-postgres psql --username=wse_user --dbname=wse_db
