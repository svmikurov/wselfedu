"""Defines utility methods to load or get data."""

import os
import re

USERNAME_PATTERN = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
TRUE_BOOLEAN_VALUES = {'true', 't', '1'}


def get_boolean_value(env_var: str) -> bool:
    """Convert an environment variable value to a boolean.

    Args:
        env_var: Name of the environment variable to read
    Returns:
        The boolean interpretation of the environment variable's value
    For example:
        DEBUG = getenv_bool('DEBUG')

    """
    value = os.getenv(env_var, 'False').strip().lower()
    return value in TRUE_BOOLEAN_VALUES


def validate_username(username: str) -> None:
    """Validate username.

    Args:
        username: Username to validat
    Raises:
        Iv username is not valid.

    """
    if not re.match(USERNAME_PATTERN, username):
        raise ValueError(
            f'Invalid username "{username}". '
            'Username must start with a letter or underscore and contain only '
            'letters, numbers and underscores.'
        )


def get_db_user(env_var: str = 'DB_USER') -> str:
    """Get the database username from an environment variable.

    Args:
        env_var: Environment variable name (default 'DB_USER')

    Returns:
        Environment variable value
    Raises:
        ValueError: If the variable is not set or contains an invalid
        username

    """
    db_user = os.getenv(env_var)

    if db_user is None:
        raise ValueError(
            f'Database user not configured in {env_var} environment variable'
        )

    validate_username(db_user)

    return db_user
