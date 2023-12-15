MANAGE := poetry run ./manage.py

start:
	@$(MANAGE) runserver

lint:
	poetry run flake8

test:
	poetry run coverage run --source='.' manage.py test