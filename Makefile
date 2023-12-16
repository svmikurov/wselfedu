MANAGE := poetry run ./manage.py

start:
	@$(MANAGE) runserver

lint:
	poetry run flake8

test:
	poetry run coverage run --source='.' manage.py test

test-just:
	@$(MANAGE) test wselfedu.users.tests.test_update.UserUpdateTest

shell:
	poetry run python manage.py shell_plus --ipython