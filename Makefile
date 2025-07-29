include .env

# Run server in development mode
run:
	python3 manage.py runserver

# Run deployment
deploy: format \
		mypy \
		create_db \
		makemigrations \
		migrate \
		load_initial_data \
		pytest


# Testing and code checking


# Code style checking
ruff:
	ruff check && ruff format --diff

# Fix code format
format:
	ruff check --fix && ruff format

# Static type checking
mypy:
	mypy .

# Pytest
pytest:
	pytest .

# Combined checking
check: format mypy pytest


# Database commands


# Create database
create_db:
	sudo -u postgres psql \
	-v db_name=$(DB_NAME) \
	-v db_user=$(DB_USER) \
	-v db_password=$(DB_PASSWORD) \
	-f db/sql/init/create_db.sql

# Django migration creating
makemigrations:
	python manage.py makemigrations

# Apply Django migrations
migrate:
	python manage.py migrate

# Load inial data fixtures
load_initial_data:
	python manage.py load_initial_data --load-sensitive


# Django-extensions


# Build model graphs
# https://django-extensions.readthedocs.io/en/latest/graph_models.html#example-usage
graph_models:
	mkdir -p temp/graph_models/ && \
	python manage.py graph_models \
		-o temp/graph_models/models.png \
		--verbose-names \
		--inheritance