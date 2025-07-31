"""Test user model."""

from decimal import Decimal

import pytest

from apps.users.models import Balance, CustomUser

BALANCE_TOTAL = Decimal(54)


@pytest.fixture
def user() -> CustomUser:
    """Fixture providing user."""
    return CustomUser.objects.create_user(username='test_user')


@pytest.mark.django_db
class TestBalanceRelation:
    """Test user balance relation of user model."""

    def test_case_not_created_user_balance(
        self,
        user: CustomUser,
    ) -> None:
        """Test case then user balance not created."""
        assert user.balance_total is None

    def test_case_created_user_balance(
        self,
        user: CustomUser,
    ) -> None:
        """Test case then user balance created."""
        Balance.objects.create(user=user, total=BALANCE_TOTAL)
        assert user.balance_total == BALANCE_TOTAL
