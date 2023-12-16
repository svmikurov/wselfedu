MANAGE := poetry run ./manage.py
TEST_JUST := wselfedu.users.tests.test_account

start:
	@$(MANAGE) runserver

lint:
	poetry run flake8

test:
	poetry run coverage run --source='.' manage.py test

test-just:
	@$(MANAGE) test $(TEST_JUST)

shell:
	poetry run python manage.py shell_plus --ipython