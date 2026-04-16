# Load data to create a database
include .env
DB_NAME ?= $(DB_NAME)
DB_USER ?= $(DB_USER)
DB_PASS ?= $(DB_PASS)

# Defining color for messages
GREEN  := \033[0;32m
RED    := \033[0;31m
RESET  := \033[0m

# Run server in development mode
run:
	python3 manage.py runserver

# Run deployment
deploy: check-db-connections \
		recreate_db \
		makemigrations \
		migrate \
		load_initial_data \
		pytest-cov


# Testing and code checking
# -------------------------


# Code style checking
ruff:
	ruff check && ruff format --diff

# Fix code format
format:
	ruff check --fix && ruff format

# Static type checking
mypy:
	mypy .

js-style:
	npx prettier --check static_src/js/ --write && \
	npx eslint static_src/js/ --fix

# Pytest
pytest:
	pytest

# Pytest without browser testing
pytest-no-browser:
	pytest --ignore=tests/browser/

# Pytest with configured coverage
pytest-cov:
	pytest --cov=. \
    --cov-report=term-missing:skip-covered \
    --cov-report=html

# Combined checking
check: mypy format pytest
check-cov: format mypy pytest-cov


# Database commands
# -----------------


# Check active PostgreSQL connections
check-db-connections:
	@echo "Checking active PostgreSQL connections..."
	@if [ $$(psql -U $(DB_USER) -d $(DB_NAME) -t -c "SELECT COUNT(*) FROM pg_stat_activity WHERE datname = '$(DB_NAME)' AND pid <> pg_backend_pid();") -gt 0 ]; \
	then \
		echo "$(RED)ERROR: Active connections detected. Aborting.$(RESET)"; \
		exit 1; \
	else \
		echo "$(GREEN)No active connections. Proceeding...$(RESET)"; \
	fi

# Drop existing DB and role, create role and DB
recreate_db:
	sudo -u postgres psql \
	-v db_name=$(DB_NAME) \
	-v db_user=$(DB_USER) \
	-v db_password=$(DB_PASS) \
	-f db/sql/init/create_db.sql

# Django migration creating
makemigrations:
	python manage.py makemigrations

# Apply Django migrations
migrate:
	python manage.py migrate

# Load initial data fixtures
load_initial_data:
	python manage.py load_initial_data --load-sensitive

# Reset DB with initial data
reset_db: check-db-connections \
		  recreate_db \
	      makemigrations \
	      migrate \
	      load_initial_data \


# Django-extensions
# -----------------


# Build model graphs
# https://django-extensions.readthedocs.io/en/latest/graph_models.html#example-usage
graph_models:
	mkdir -p temp/graph_models/ && \
	python manage.py graph_models \
		-o temp/graph_models/models.png \
		--verbose-names \
		--inheritance

# Dump language application models in development mode
dump-dev:
	python manage.py dumpdata \
	lang.nativeword \
	lang.englishword \
	lang.englishtranslation \
	lang.rule \
	lang.ruleclause \
	lang.ruletaskexample \
	lang.ruleexample \
	lang.ruleexception \
	lang.mark \
	lang.translationmark \
	lang.category \
	--indent 2 > temp/dumpdata/sensitive/lang.json

	python manage.py dumpdata \
	users.person \
	users.mentorship \
	users.mentorshiprequest \
	sessions.session \
	--indent 2 > temp/dumpdata/sensitive/users.json
	
	python manage.py dumpdata \
	core.discipline \
	core.exercise \
	core.period \
	core.taskio \
	--indent 2 > temp/dumpdata/public/core.json

	python manage.py dumpdata \
	glossary.termassertion \
	glossary.term \
	--indent 2 > temp/dumpdata/sensitive/glossary.json

	python manage.py dumpdata \
	core.source \
	--indent 2 > temp/dumpdata/sensitive/core.json

	python manage.py dumpdata \
	math.calculationcondition \
	math.studentcalculationcondition \
	--indent 2 > temp/dumpdata/sensitive/math.json

	python manage.py dumpdata \
	study.exerciseavailability \
	study.exercisereward \
	--indent 2 > temp/dumpdata/sensitive/study.json

# Localization
locale-make:
	python manage.py makemessages -l ru -l nl -l en
locale-compile:
	python manage.py compilemessages -l ru -l nl -l en