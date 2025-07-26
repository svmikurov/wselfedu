## Web server of the WSE project


### Install development mode
```commandline
python3.11 -m venv .venv_wselfedu
source .venv_wselfedu/bin/activate
poetry install --all-extras
```

### Update environment values
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

Run command:
```commandline
make deploy
```
