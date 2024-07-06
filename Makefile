APP := docker compose exec app-wse
MANAGE := @$(APP) python manage.py


# Git
pull:
	git pull


# Docker
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

load-fixture:
	@$(MANAGE) loaddata tests/fixtures/wse-db-fixture-users.json

dumpdata:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db-wse-sweb.json


# Tests
lint:
	@$(APP) flake8

test:
	@$(MANAGE) test

pytest:
	@$(APP) pytest

check: lint pytest
