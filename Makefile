MANAGE := poetry run ./manage.py

start:
	@$(MANAGE) runserver

lint:
	poetry run flake8