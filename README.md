# WSE


## Install

### Poetry

The project uses Poetry for dependency management.

```bash
curl -SL https://install.python-poetry.org | python3 -
poetry config virtualenvs.in-project true 
```

### Dependencies

```bash
make setup
```


## Run project

```bash
# Copy environment example
cp -r .envs.example/ .envs/
# Run project
...
```


## Documentation

### Run via Docker

```bash
docker build -f docker/docs/Dockerfile -t wse-docs .
docker run -d -p 8010:8000 --name wse-docs wse-docs
```

### Run via venv

### Domain-Design-Development glossary with business rules.
```bash
make docs-open
```

## Help

### Show available commands
```bash
make help
```