"""Defines base TestCase with sql query and executing time output."""

import time

from django.conf import settings
from django.db import connection
from django.test import TestCase

from apps.users.models import CustomUser
from tests.conf.utils.sql_parse import SQLOutput

DIVIDER_DASH: str = '-' * 50
DIVIDER_EQUAL: str = '=' * 50


class SQLTestCase(TestCase):
    """Base test case with sql query and executing time output.

    For example:

        class RewardServiceTest(BaseTestCase):

            @classmethod
            def setUpTestData(cls) -> None:
                super().setUpTestData()
                cls.balance = Balance.objects.create(user=cls.test_user)
    """

    test_user: CustomUser

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        settings.DEBUG = True
        cls.test_user = CustomUser.objects.create(username='test_user')

    def setUp(self) -> None:
        """Set up before each test."""
        connection.queries.clear()
        self.start_time = time.time()

    def tearDown(self) -> None:
        """Tear down after each test."""
        execution_time = time.time() - self.start_time
        settings.DEBUG = False
        test_name = self._testMethodName

        # Output to console
        output_sql = SQLOutput(
            connection.queries,
            execution_time,
            test_name,
        )
        output_sql.output_sql()
