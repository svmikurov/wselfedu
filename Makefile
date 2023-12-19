MANAGE := poetry run python manage.py
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
	@$(MANAGE) shell_plus --ipython

notebook:
	@$(MANAGE) shell_plus --notebook

dry:
	@$(MANAGE) makemigrations --dry-run

mmigrate:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

.PHONY: static
static:
	@$(MANAGE) collectstatic