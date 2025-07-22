"""Defines configuration for tests."""

from decimal import Decimal
from typing import Iterator

import yaml
from django.conf import settings
from django.db import connection

import pytest

from timeit import default_timer as timer

from apps.users.models import CustomUser, Balance
from ..conf import CONFIG_PATH
from ..conf.report.report_config import ReportConfig
from ..conf.report.sql_reporter import SQLReporter


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

    config = ReportConfig(**yaml.safe_load(open(CONFIG_PATH)))

    reporter = SQLReporter(
        config=config,
        queries=connection.queries,
        test_time=Decimal(total_test_time),
        test_name=request.node.name,
        test_doc=request.node.function.__doc__,
    )
    reporter.print_report()

