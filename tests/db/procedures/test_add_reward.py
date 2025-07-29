"""Tests for add reward Postgres procedure."""

from typing import Callable

import pytest
from django.db import connection
from django.db.models import Sum

from apps.lang.models import LangTransaction
from apps.main.models import App
from apps.math.models.transaction import MathTransaction
from apps.users.models import Balance, CustomUser
from apps.users.models.transaction import Transaction

AMOUNT = 33
SCHEMA_NAME = 'math'


@pytest.fixture
def user() -> CustomUser:
    """Fixture provides test user."""
    return CustomUser.objects.create_user(username='test_user')


@pytest.fixture(autouse=True)
def math_app() -> App:
    """Fixture provides math app."""
    return App.objects.create(name='Adding', schema_name=SCHEMA_NAME)


@pytest.fixture
def add_reward() -> Callable[..., None]:
    """Fixture to call reward procedure."""

    def _add_reward(
        user_id: int,
        amount: int = AMOUNT,
        schema: str = SCHEMA_NAME,
    ) -> None:
        with connection.cursor() as cursor:
            cursor.execute(
                'CALL increment_user_reward(%s, %s, %s)',
                (user_id, amount, schema),
            )

    return _add_reward


class TestIncrementUserRewardProcedure:
    """Test `increment_user_reward` Postgres procedure."""

    @pytest.mark.django_db
    def test_transaction_created(
        self,
        user: CustomUser,
        add_reward: Callable[..., None],
    ) -> None:
        """Test transaction creation."""
        add_reward(user.pk)
        transaction = MathTransaction.objects.filter(user=user).first()

        assert transaction is not None
        assert transaction.amount == AMOUNT

    @pytest.mark.django_db
    def test_multiple_transactions(
        self, user: CustomUser, add_reward: Callable[..., None]
    ) -> None:
        """Test multiple reward calls."""
        add_reward(user.pk)
        add_reward(user.pk)

        transactions = MathTransaction.objects.filter(user=user)
        total = transactions.aggregate(total=Sum('amount'))

        assert transactions.count() == 2
        assert total['total'] == AMOUNT * 2

    @pytest.mark.django_db
    def test_balance_updates(
        self,
        user: CustomUser,
        add_reward: Callable[..., None],
    ) -> None:
        """Test balance updates."""
        add_reward(user.pk)
        balance = Balance.objects.get(user=user)
        assert balance.total == AMOUNT

        add_reward(user.pk)
        balance.refresh_from_db()
        assert balance.total == AMOUNT * 2


class TestTransactionIsolation:
    """Test transaction isolation between apps."""

    @pytest.mark.django_db
    def test_math_transaction_isolation(
        self,
        user: CustomUser,
        add_reward: Callable[..., None],
    ) -> None:
        """Test transactions are isolated to their apps."""
        add_reward(user.pk)

        math_count: int = MathTransaction.objects.count()
        lang_count: int = LangTransaction.objects.count()
        main_count: int = Transaction.objects.count()

        assert math_count == 1
        assert lang_count == 0
        assert main_count == 1
