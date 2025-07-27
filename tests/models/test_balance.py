"""Defines Balance model test."""

from decimal import Decimal
from unittest import TestCase

import pytest
from django.db.utils import DataError
from django.utils import timezone

from apps.users.models import (
    Balance,
    CustomUser,
)


@pytest.mark.django_db
class TestBalanceModel(TestCase):
    """Test the Balance model."""

    def setUp(self) -> None:
        """Construct the test."""
        self.user = CustomUser.objects.create_user(
            username='test_user',
            password='test_pass123',
        )
        self.total = 1000.50
        self.balance = Balance.objects.create(
            user=self.user,
            total=self.total,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_balance_creation(self) -> None:
        """Test the creation balance object."""
        self.assertEqual(Balance.objects.count(), 1)
        self.assertEqual(self.balance.user, self.user)
        self.assertEqual(Decimal(self.balance.total), self.total)
        self.assertIsNotNone(self.balance.created_at)
        self.assertIsNotNone(self.balance.updated_at)

    def test_balance_str_representation(self) -> None:
        """Test balance string representation."""
        expected_str = f'Баланс {self.user.username}: {self.total}'
        self.assertEqual(str(self.balance), expected_str)

    def test_balance_fields(self) -> None:
        """Test model fields."""
        field_total = Balance._meta.get_field('total')
        self.assertEqual(field_total.verbose_name, 'Баланс')
        self.assertEqual(field_total.max_digits, 11)
        self.assertEqual(field_total.decimal_places, 2)

        field_user = Balance._meta.get_field('user')
        self.assertEqual(field_user.verbose_name, 'Пользователь')
        self.assertEqual(field_user.related_model, CustomUser)

        field_created = Balance._meta.get_field('created_at')
        self.assertEqual(field_created.verbose_name, 'Добавлен')
        self.assertTrue(field_created.blank)

        field_updated = Balance._meta.get_field('updated_at')
        self.assertEqual(field_updated.verbose_name, 'Обновлен')
        self.assertTrue(field_updated.blank)

    def test_balance_meta_options(self) -> None:
        """Test Meta model options."""
        meta = Balance._meta
        self.assertEqual(meta.verbose_name, 'Баланс')
        self.assertEqual(meta.verbose_name_plural, 'Баланс')
        self.assertEqual(meta.db_table, 'users"."balance')
        self.assertFalse(meta.managed)

    def test_user_balance_relation(self) -> None:
        """Test the User-Balance relationship."""
        # Check related_name
        self.assertEqual(self.user.balance.first(), self.balance)

        # Check on_delete=CASCADE
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(Balance.DoesNotExist):
            Balance.objects.get(user_id=user_id)

    def test_total_validation(self) -> None:
        """Test the validation of the total field."""
        # Checking the maximum number of digits
        with self.assertRaises(DataError):
            Balance.objects.create(
                user=self.user,
                total=100000000000.00,  # 12 digits (max_digits=11)
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
