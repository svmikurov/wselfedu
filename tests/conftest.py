"""Pytest configuration."""

pytest_plugins = [
    'tests.fixtures.di.container',
    'tests.fixtures.db_user',
    'tests.fixtures.lang.db.translations',
]
