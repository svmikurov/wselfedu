"""Test reward service."""

from apps.users.models import Balance
from tests.conf.base.case import SQLTestCase


class RewardServiceTest(SQLTestCase):
    """Test reward service."""

    test_user_balance: Balance

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        super().setUpTestData()
        cls.test_user_balance = Balance.objects.create(user=cls.test_user)
