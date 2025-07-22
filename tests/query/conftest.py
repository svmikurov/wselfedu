"""Defines configuration for tests."""

from typing import Generator, Iterator

from django.conf import settings
from django.db import connection

import pytest


from timeit import default_timer as timer

from apps.users.models import CustomUser, Balance
from tests.conf.utils.sql_parse import SQLOutput


@pytest.fixture
def user() -> CustomUser:
    """Fixture providing user."""
    return CustomUser.objects.create(username='user')


@pytest.fixture
def balance(user: CustomUser) -> Balance:
    """Fixture providing balance."""
    return Balance.objects.create(user=user)


@pytest.fixture
def debug_sql(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[None]:
    """Output the SQL queries."""
    connection.queries.clear()
    monkeypatch.setattr(settings, 'DEBUG', True)

    start_time = timer()
    yield
    total_test_time = timer() - start_time

    output_sql = SQLOutput(
        queries=connection.queries,
        test_time=total_test_time,
        # test_name=request.node.name,
    )
    output_sql.output_sql()
