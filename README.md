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
# Set or copy environments
cp -r envs.example/ .envs/

# Set or copy secrets
cp -r secrets.example/ .secrets/

# Run project
...
```


## Documentation

```bash
make docs-docker-build
make docs-docker-run
make docs-docker-stop
```

## Show available commands

```bash
make help
```