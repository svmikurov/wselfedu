#### Какая база данных используется:
```cfgrlanguage
>>> from django.db import connection
```
```cfgrlanguage
>>> settings.DATABASES['default']['NAME']
```

#### Default:
```cfgrlanguage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```


#### PostgresSQL
```cfgrlanguage
poetry add psycopg2-binary
```
```cfgrlanguage
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
if os.getenv('DEFAULT_DB') == 'PostgresSQL':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_NAME'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASS'),
            'HOST': 'localhost',
            'PORT': '',
        }
    }
elif os.getenv('DEFAULT_DB') == 'Fixtures':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db-wse-fixtures.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# End Database
```