MANAGE := poetry run python manage.py
TEST_JUST := task.tests.django_tests.test_lookup_params

start:
	@$(MANAGE) runserver

lint:
	poetry run flake8

create-fixtures:
	@$(MANAGE) dumpdata --exclude auth --exclude contenttypes --exclude admin --exclude sessions --indent 2 > task/tests/fixtures/wse-fixtures-.json

test:
	@$(MANAGE) test

just-test:
	@$(MANAGE) test $(TEST_JUST)

test-pytest:
	poetry run pytest

coverage:
	coverage run --source='.' ./manage.py test .
	coverage report
	coverage html

test-coverage:
	poetry run pytest --cov='.' --cov-report xml


selfcheck:
	poetry check

check: lint selfcheck test-pytest

dry:
	@$(MANAGE) makemigrations --dry-run

mmigrate:
	@$(MANAGE) makemigrations

migrate:
	@$(MANAGE) migrate

collectstatic:
	@$(MANAGE) collectstatic