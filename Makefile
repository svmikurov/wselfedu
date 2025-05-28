# Poetry
poetry-export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export --only=dev -f requirements.txt --output requirements.dev.txt --without-hashes

# Tests
ruff:
	ruff format && ruff check --fix

mypy:
	mypy .

pytest:
	pytest

check: ruff mypy pytest
