"""Test the Transaction tables."""

from typing import Generic, Protocol, Type, TypeVar

import pytest
from django.db import connection
from django.db.models import Sum
from django.db.models.manager import Manager

from apps.core.models import BaseTransaction
from apps.lang.models import LangTransaction
from apps.math.models import MathTransaction
from apps.users.models import CustomUser
from apps.users.models.transaction import Transaction

AMOUNT = 33
SCHEMA_NAME = 'math'
TRANSACTION_TYPES = (
    'schema, transaction_type',
    [
        ('math', MathTransaction),
        ('lang', LangTransaction),
    ],
)

T = TypeVar('T', bound='TransactionProtocol')


class TransactionProtocol(Protocol):
    """Protocol for Transaction table interface."""

    objects: Manager[BaseTransaction]
    amount: int
    user_id: int


@pytest.fixture
def user() -> CustomUser:
    """Fixture provides test user."""
    return CustomUser.objects.create_user(username='test_user')


def create_transaction(
    user_id: int,
    schema: str,
    amount: int = AMOUNT,
) -> None:
    """Create transaction via sql."""
    with connection.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO {schema}.transaction (user_id, amount, type) '
            'VALUES (%s, %s, %s)',
            (user_id, amount, 'reward'),
        )


@pytest.mark.parametrize(*TRANSACTION_TYPES)
@pytest.mark.django_db
class TestTransactionTable(Generic[T]):
    """Test transaction DB table."""

    def test_transaction_created(
        self,
        schema: str,
        user: CustomUser,
        transaction_type: Type[T],
    ) -> None:
        """Test transaction creation."""
        create_transaction(user.pk, schema)

        # Get user transactions
        transactions = transaction_type.objects.filter(user=user).first()

        # Transaction created
        assert transactions is not None

        # Added amount to transaction
        assert transactions.amount == AMOUNT

    def test_multiple_transactions(
        self,
        schema: str,
        user: CustomUser,
        transaction_type: Type[T],
    ) -> None:
        """Test multiple reward calls."""
        # Create transaction twice
        create_transaction(user.pk, schema)
        create_transaction(user.pk, schema)

        # Get transaction data
        transactions = transaction_type.objects.filter(user=user)
        total = transactions.aggregate(total=Sum('amount'))

        # The transaction was created twice
        assert transactions.count() == 2
        assert total['total'] == AMOUNT * 2


@pytest.mark.django_db
def test_math_transaction_isolation(
    user: CustomUser,
) -> None:
    """Test transactions are isolated to their apps."""
    # Create transaction at math schema
    create_transaction(user.pk, 'math')

    # Get transactions count
    math_count: int = MathTransaction.objects.count()
    lang_count: int = LangTransaction.objects.count()
    core_count: int = Transaction.objects.count()

    # Updated only math schema and core schema transaction tables
    assert math_count == 1
    assert core_count == 1
    assert lang_count == 0
