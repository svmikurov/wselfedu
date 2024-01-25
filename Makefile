MANAGE := poetry run python manage.py
TEST_JUST := english.tests.test_update_words_knowledge_assessment_view

start:
	@$(MANAGE) runserver 0.0.0.0:8000

lint:
	poetry run flake8

create-fixtures:
	@$(MANAGE) dumpdata --exclude auth --exclude contenttypes --exclude admin --exclude sessions --indent 2 > wse-fixtures.json

test:
	poetry run coverage run --source='.' manage.py test

test-just:
	@$(MANAGE) test $(TEST_JUST)

test-coverage:
	poetry run coverage run --source="" manage.py test
	poetry run coverage xml

coverage:
	coverage run --source='.' ./manage.py test .
	coverage report
	coverage html

check: lint test

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