## Web server of the WSE project


### Install development mode
```commandline
python3 -m venv .venv_wselfedu
source .venv_wselfedu/bin/activate
pip3 install poetry
poetry install --all-extras
playwright install
```

#### Update environment values
- update secret key
- update `username`, `password`, `dbname` to connet to database
- debug mode

.env:
```text
DB_NAME=db_name
DB_USER=username
DB_PASSWORD=password
SECRET_KEY=secret_key
DATABASE_URL=postgres://username:password@localhost:5432/dbname
```

#### Add  fixtures_config.yaml
```commandline
cp db/fixtures/fixtures_config.yaml.example db/fixtures/fixtures_config.yaml
```

#### Run command:
```commandline
make deploy
```
