"""Tests for Balance model."""

from decimal import Decimal

import pytest
from django.db.utils import DataError

from apps.users.models import Balance, CustomUser


@pytest.mark.django_db
class TestBalanceModel:
    """Test suite for Balance model."""

    @pytest.fixture
    def user(self) -> CustomUser:
        """Fixture provides user."""
        return CustomUser.objects.create_user(
            username='test_user',
            password='test_pass123',
        )

    @pytest.fixture
    def balance(self, user: CustomUser) -> Balance:
        """Fixture provides balance."""
        return Balance.objects.create(
            user=user,
            total=Decimal('1000.50'),
        )

    def test_balance_creation(
        self,
        balance: Balance,
        user: CustomUser,
    ) -> None:
        """Test balance object creation."""
        assert Balance.objects.count() == 1
        assert balance.user == user
        assert balance.total == Decimal('1000.50')
        assert balance.created_at is not None
        assert balance.updated_at is not None

    def test_balance_str_representation(
        self,
        balance: Balance,
        user: CustomUser,
    ) -> None:
        """Test string representation."""
        assert str(balance) == f'Баланс {user.username}: 1000.50'

    def test_balance_fields(self) -> None:
        """Test model field definitions (no DB access needed)."""
        field_total = Balance._meta.get_field('total')
        assert field_total.max_digits == 11
        assert field_total.decimal_places == 2

    def test_user_balance_relation(
        self,
        balance: Balance,
        user: CustomUser,
    ) -> None:
        """Test user-balance relationship."""
        # Access through related_name
        assert user.balance == balance

        # Test deletion
        user.delete()
        assert not Balance.objects.filter(id=balance.id).exists()

    def test_total_validation(self, user: CustomUser) -> None:
        """Test total field validation."""
        with pytest.raises(DataError):
            Balance.objects.create(
                user=user,
                total=Decimal('100000000000.00'),  # Exceeds max_digits
            )
