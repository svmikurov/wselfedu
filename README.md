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
SECRET_KEY=secret_key
DATABASE_URL=postgres://username:password@localhost:5432/dbname
DEBUG=True
```

### Configure PostgreSQL database
Update the `db/sql/init/` SQL-scripts with `username`, `password` and `dbname`

Run command:
```commandline
make deploy
```
