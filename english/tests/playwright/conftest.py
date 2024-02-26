import os

import pytest
from django.core.management import call_command

from config import settings


# https://pytest-django.readthedocs.io/en/latest/database.html#django-db-modify-db-settings
def django_db_modify_db_settings():
    """Run tests with db-wse-pytest.sqlite3 date base.

    Allows to avoid overwriting the date base used in development.
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'db-wse-pytest.sqlite3')
    }


# https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-don-t-use-transactional-or-live-server
# https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-use-transactional-or-live-server
@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    """Populate the test database from fixtures."""
    with django_db_blocker.unblock():
        call_command('loaddata', 'english/tests/fixtures/wse-fixtures-2.json')
