```cfgrlanguage
import logging
```
```cfgrlanguage
logging.basicConfig(level=logging.INFO)
```

Логи запросов к БД:
```cfgrlanguage
import logging

if os.getenv('LOGGING_DB'):
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {'class': 'logging.StreamHandler'},
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            }
        }
    }
```