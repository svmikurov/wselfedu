# Run server in development mode
runserver:
	python3 manage.py runserver

# Run deployment
deploy: create_db create_tables makemigrations migrate load_initial_data


# Testing

# Code style checking
ruff:
	ruff check && ruff format --diff

format:
	ruff check --fix && ruff format

# Static type checking
mypy:
	mypy .


# Pytest
pytest:
	pytest .

# Code checking
check: format mypy pytest

# Check hexagonal architecture study code
hex:
	ruff check --fix hexagonal_arch && \
	ruff format hexagonal_arch && \
	mypy hexagonal_arch && \
	pytest hexagonal_arch


# Database commands

# Create database
create_db:
	# Copy the file to the system directory available for postgres
	sudo cp db/sql/init/001_create_db.sql       /tmp/
	sudo cp db/sql/init/002_create_role.sql     /tmp/
	sudo -u postgres psql -f /tmp/001_create_db.sql
	sudo -u postgres psql -f /tmp/002_create_role.sql
	sudo rm /tmp/001_create_db.sql
	sudo rm /tmp/002_create_role.sql

create_tables:
	python manage.py create_tables

# Migrations
makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

# Fixture management
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