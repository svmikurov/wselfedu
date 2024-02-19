```cfgrlanguage
import psycopg2
from psycopg2.extras import RealDictCursor


def connect(db_url):
    return psycopg2.connect(db_url)


def close(connection):
    return connection.close()


def fetch_db_data(connection, sql_request):
    if '%' in sql_request or '{' in sql_request:
        raise ValueError('Only read from database by row sql request!')

    with connection.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql_request)
        db_data = curs.fetchall()
        return db_data
```
