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

createsuperuser:
	@$(MANAGE) createsuperuser

loaddata:
	@$(MANAGE) loaddata db-wse-sweb.json

dumpdata:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db-wse-sweb.json

dumpdata-fixtures:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry --exclude sessions.session --exclude authtoken.token --indent 2 > fixtures.json

shell:
	@$(MANAGE) shell

flush:
	@$(MANAGE) flush


# Tests
lint:
	@$(APP) flake8

ruff:
	@$(APP) ruff check && ruff format --diff

test:
	@$(APP) pytest tests/ --ignore=tests/tests_e2e --ignore=tests/tests_plw

plw:
	@$(APP) pytest tests/tests_e2e/

plw-lf:
	@$(APP) pytest tests/tests_e2e/ --lf

check: ruff down build up test plw

get-state:
	@$(APP) sh -c "pytest tests_e2e/auth/get_auth_state.py"

test-just:
	@$(APP) pytest $(TEST_JUST)

# PostgreSQL
connect:
	@$(COMPOSE) exec wse-db-postgres psql --username=$(POSTGRES_USER) --dbname=$(POSTGRES_NAME)
