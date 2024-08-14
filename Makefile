include .env_vars/.env
include .env_vars/.env.wse

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

restart: lint down build up

docker-clean:
	@$(COMPOSE) down && \
	docker image prune -a -f && \
	docker volume prune -a -f && \
	docker builder prune -a -f && \
	docker system df


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

shell:
	@$(MANAGE) shell

# Tests
lint:
	@$(APP) flake8

ruff:
	ruff check

test:
	@$(APP) pytest tests/

plw:
	@$(APP) pytest tests_e2e/

check: restart test plw

get-state:
	@$(APP) sh -c "pytest tests_e2e/auth/get_auth_state.py"

test-just:
	@$(APP) pytest $(TEST_JUST)

# PostgreSQL
connect:
	@$(COMPOSE) exec wse-db-postgres psql --username=$(POSTGRES_USER) --dbname=$(POSTGRES_NAME)
