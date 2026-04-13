"""Pytest configuration."""

pytest_plugins = [
    'tests.fixtures.db_user',
    'tests.fixtures.di.container',
    'tests.fixtures.exercise.request_data',
    'tests.fixtures.exercise.lang.db.params',
    'tests.fixtures.exercise.lang.db.translations',
    'tests.fixtures.exercise.lang.no_db.params',
]
