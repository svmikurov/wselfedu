"""Defines utility methods to load data."""

import os


def getenv_bool(env: str) -> bool:
    """Get boolean environment variable.

    For example:

        DEBUG = getenv_bool('DEBUG')
    """
    return os.getenv(env, 'False').lower() in ('true', 't', '1')
