MANAGE := poetry run python manage.py
TEST_JUST := english.tests.django_tests.test_analytic_queries.TestFavoritesQuery.test_study_favorites_user_count_qs

start:
	@$(MANAGE) runserver 0.0.0.0:8000

lint:
	poetry run flake8

create-fixtures:
	@$(MANAGE) dumpdata --exclude auth --exclude contenttypes --exclude admin --exclude sessions --indent 2 > task/tests/fixtures/wse-fixtures-.json

test:
	poetry run coverage run --source='.' manage.py test

test-just:
	@$(MANAGE) test $(TEST_JUST)

test-coverage:
	poetry run coverage run --source="" manage.py test
	poetry run coverage xml

pytest:
	pytest

coverage:
	coverage run --source='.' ./manage.py test .
	coverage report
	coverage html

check: lint test pytest

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