APP := docker compose exec app-wse
MANAGE := @$(APP) python manage.py

up:
	docker compose up -d --build

down:
	docker compose down

migrate:
	@$(MANAGE) migrate

collectstatic:
	@$(MANAGE) collectstatic

loaddata:
	@$(MANAGE) loaddata db-wse-sweb.json

dumpdata:
	@$(MANAGE) dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > db-wse-sweb.json

test:
	@$(MANAGE) test

lint:
	@$(APP) flake8

pytest:
	@$(APP) pytest

check: lint pytest
