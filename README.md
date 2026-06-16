# WSE

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

## Show available commands
```bash
make help
```