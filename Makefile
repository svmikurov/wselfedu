include .env_vars/.env
include .env_vars/.env.wse

ifeq (${ENVIRONMENT}, development)
	COMPOSE := docker compose -f docker-compose.dev.yml
else ifeq (${ENVIRONMENT}, production)
	COMPOSE := docker compose -f docker-compose.prod.yml
endif

APP := @$(COMPOSE) exec wse-project
MANAGE := @$(APP) python manage.py

# Poetry
poetry-export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export --only=dev -f requirements.txt --output requirements.dev.txt --without-hashes

# Docker
update:
	@$(COMPOSE) down wse-project && \
	$(COMPOSE) up wse-project -d


build:
	@$(COMPOSE) build

up:
	@$(COMPOSE) up -d

down:
	@$(COMPOSE) down

restart: ruff down up

rebuild: ruff down build up

# Django
makemigrations:
	@$(MANAGE) makemigrations

dry-run:
	@$(MANAGE) makemigrations --dry-run

migrate:
	@$(MANAGE) migrate

collectstatic:
	@$(MANAGE) collectstatic --noinput

createsuperuser:
	@$(MANAGE) createsuperuser

loaddata:
	@$(MANAGE) loaddata db-wse-sweb.json

loaddata-fixtures:
	@$(MANAGE) loaddata tests/fixtures/fixtures.json

dumpdata:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db-wse-sweb.json

dumpdata-fixtures:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry --exclude sessions.session --indent 2 > tests/fixtures/fixtures.json

shell:
	@$(MANAGE) shell

flush:
	@$(MANAGE) flush


# Tests
lint:
	@$(APP) flake8

ruff:
	@$(APP) ruff check && ruff format --diff

format:
	@$(APP) ruff check --fix && ruff format

test:
	@$(APP) pytest --ignore=tests_plw/ -s

plw:
	@$(APP) pytest tests_plw/

codegen:
	playwright codegen 127.0.0.1

check: ruff lint down build up test plw

test-just:
	@$(APP) pytest $(TEST_JUST)

# PostgreSQL
connect:
	@$(COMPOSE) exec wse-db-postgres psql --username=$(POSTGRES_USER) --dbname=$(POSTGRES_NAME)
