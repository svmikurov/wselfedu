## Web server of the WSE project


### Install development mode
```commandline
python3 -m venv .venv_wselfedu
source .venv_wselfedu/bin/activate
pip3 install poetry
poetry install --all-extras
playwright install
```

#### Update or copy environment values
```commandline
cp .env.example .env
```

#### Add  fixtures_config.yaml
```commandline
cp db/fixtures/fixtures_config.yaml.example db/fixtures/fixtures_config.yaml
```

#### Run command:
```commandline
make deploy
```
