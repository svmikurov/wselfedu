APP := docker compose exec app-wse
MANAGE := @$(APP) python manage.py


# Docker
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down


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


# PostgreSQL
connect:
	docker compose exec db-postgres-wse psql --username=wse_user --dbname=wse_db
