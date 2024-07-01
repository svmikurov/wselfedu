APP := docker compose exec app-wse
MANAGE := @$(APP) python manage.py


# Git
pull:
	git pull


# Docker
up:
	docker compose up -d --build

down:
	docker compose down

restart: down up

update: down pull up


# Django
migrate:
	@$(MANAGE) migrate

collectstatic:
	@$(MANAGE) collectstatic

loaddata:
	@$(MANAGE) loaddata db-wse-sweb.json

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
