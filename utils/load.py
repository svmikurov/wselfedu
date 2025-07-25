"""Defines utility methods to load data."""

import os


def get_boolean_value(env: str) -> bool:
    """Get boolean environment variable.

    For example:

        DEBUG = getenv_bool('DEBUG')
    """
    return os.getenv(env, 'False').lower() in ('true', 't', '1')
