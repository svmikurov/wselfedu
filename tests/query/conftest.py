"""Defines configuration for tests."""

from typing import Generator

import pytest
from django.conf import settings

from apps.users.models import Balance, CustomUser
from utils.sql.sql_reporter import SQLReporter


@pytest.fixture
def user() -> CustomUser:
    """Fixture providing user."""
    return CustomUser.objects.create(username='user')


@pytest.fixture
def balance(user: CustomUser) -> Balance:
    """Fixture providing balance."""
    return Balance.objects.create(user=user)


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
