"""Defines configuration for tests."""

from typing import Generator

import pytest
from django.conf import settings

from utils.sql.report.reporter import SQLReporter


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
