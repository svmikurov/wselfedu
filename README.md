# WSE

## Documentation
```bash
docker build -f docker/docs/Dockerfile -t wse-docs .
docker run -d -p 8010:8000 --name wse-docs wse-docs
```

## Docker
Run project
```bash
# Copy environment example
cp .env.example .env
# Run project
make run
```

## Install the Poetry dependency
This project uses Poetry for dependency management.
```bash
curl -SL https://install.python-poetry.org | python3 -
poetry config virtualenvs.in-project true 
```

## Install dependencies
```bash
make setup
```

## Domain-Design-Development glossary with business rules.
```bash
make docs-open
```

## Show available commands
```bash
make help
```