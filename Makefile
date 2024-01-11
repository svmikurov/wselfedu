MANAGE := poetry run python manage.py
TEST_JUST := english.tests.test_update_words_favorites_status_view

start:
	@$(MANAGE) runserver 0.0.0.0:8001

lint:
	poetry run flake8

create-fixtures:
	@$(MANAGE) dumpdata users.usermodel english.wordmodel english.sourcemodel english.categorymodel --indent 2 > wse-fixtures.json

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