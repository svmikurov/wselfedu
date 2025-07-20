# Run server in development mode
runserver:
	python3 manage.py runserver

# Run deployment
deploy: create_db makemigrations migrate load_initial_data


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


# Database commands

# Create database
create_db:
	# Copy the file to the system directory available for postgres
	sudo cp create_db.sql /tmp/
	sudo -u postgres psql -f /tmp/create_db.sql
	sudo rm /tmp/create_db.sql

# Migrations
makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

# Fixture management
load_initial_data:
	python manage.py load_initial_data


# Django-extensions

# Build model graphs
# https://django-extensions.readthedocs.io/en/latest/graph_models.html#example-usage
graph_models:
	mkdir -p temp/graph_models/ && \
	python manage.py graph_models \
		-o temp/graph_models/models.png \
		--verbose-names \
		--inheritance