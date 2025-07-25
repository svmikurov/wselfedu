"""Defines configuration for tests."""

from typing import Generator

import pytest
from django.conf import settings
from django.core.management import call_command

from utils.sql.report.reporter import SQLReporter


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


@pytest.fixture(scope='session', autouse=True)
def call_create_db_tables(  # type: ignore[no-untyped-def]
    django_db_setup: None,
    django_db_blocker,  # noqa: ANN001
) -> None:
    """Call management command to create database tables.

    Creates the database tables that are not managed by Django.
    """
    with django_db_blocker.unblock():
        call_command('create_tables')
