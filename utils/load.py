"""Defines utility methods to load or get data."""

import os
import re


def get_boolean_value(env: str) -> bool:
    """Get boolean environment variable.

    For example:

        DEBUG = getenv_bool('DEBUG')
    """
    return os.getenv(env, 'False').lower() in ('true', 't', '1')


def get_db_user() -> str:
    """Get database user."""
    db_user = os.getenv('DB_USER')

    if db_user is None:
        raise ValueError('Database user not configured')

    # Validate user name
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', db_user):
        raise ValueError(f'Invalid database username: {db_user}')

    return db_user
