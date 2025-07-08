# Run server in development mode
runserver:
	python3 manage.py runserver

# Code style checking
ruff:
	ruff check && ruff format --diff

format:
	ruff check --fix && ruff format

# Static type checking
mypy:
	mypy .

# Code checking
check: format mypy

# Database commands

# Create database
create_db:
	# Copy the file to the system directory available for postgres
	sudo cp create_db.sql /tmp/
	sudo -u postgres psql -f /tmp/create_db.sql
	sudo rm /tmp/create_db.sql

# Run migrations
makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

# Run deployment

deploy: create_db makemigrations migrate
