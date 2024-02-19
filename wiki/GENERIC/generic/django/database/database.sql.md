Makefile :
```cfgrlanguage
schema-db:
	psql database_name < database.sql
```

database.sql :
```cfgrlanguage
DROP TABLE IF EXISTS urls CASCADE;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id bigint REFERENCES urls (id),
    status_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description text,
    last_checked_at DATE DEFAULT CURRENT_DATE
);
```