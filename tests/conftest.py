"""Defines configuration for tests."""

from typing import Generator, Iterable

import psycopg
import pytest
from django.conf import settings
from django.db import connections

from utils.sql.report.reporter import SQLReporter


def run_sql(sql: str) -> None:
    """Run SQL command."""
    with psycopg.connect(dbname='postgres', autocommit=True) as conn:
        conn.execute(sql)


@pytest.fixture(scope='session')
def django_db_setup() -> Iterable[None]:
    """Set up DB."""
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'the_copied_db'

    run_sql('DROP DATABASE IF EXISTS the_copied_db')
    run_sql('CREATE DATABASE the_copied_db TEMPLATE wse_db')

    yield

    for conn in connections.all():
        conn.close()

    run_sql('DROP DATABASE the_copied_db')


# TODO: Fix adding sql queries from "Setup" before "Act"
@pytest.fixture
def debug_reporter(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[SQLReporter, None, None]:
    """Output the SQL queries."""
    monkeypatch.setattr(settings, 'DEBUG', True)

    reporter = SQLReporter(
        test_name=request.node.name,
        test_doc=request.node.function.__doc__,
    )

    yield reporter

    reporter.print_report()
