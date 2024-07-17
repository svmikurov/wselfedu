DEV_FILE := docker compose -f docker-compose.dev.yml
APP := @$(DEV_FILE) exec wse-project
MANAGE := @$(APP) python manage.py


# Docker
build:
	@$(DEV_FILE) build

up:
	@$(DEV_FILE) up -d

down:
	@$(DEV_FILE) down


# Django
makemigrations:
	@$(MANAGE) makemigrations

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

test:
	@$(APP) pytest tests/

plw:
	@$(APP) pytest tests_e2e/

check: lint test plw

get-state:
	@$(APP) sh -c "pytest tests_e2e/auth/get_auth_state.py"

test-just:
	@$(APP) pytest tests_e2e/tests/test_exercise_word_study.py


# PostgreSQL
connect:
	@$(DEV_FILE) exec wse-db-postgres psql --username=wse_user --dbname=wse_db
