"""Defines user model."""

from __future__ import annotations

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Balance

NO_BALANCE = None
"""User balance value if user balance relation not created yet
(`Decimal`)."""


class CustomUser(AbstractUser):
    """User model."""

    balance: Balance

    class Meta:
        """Model configuration."""

        db_table = 'users"."customuser'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def balance_total(self) -> Decimal | None:
        """Get user balance total."""
        try:
            return self.balance.total
        except ObjectDoesNotExist:
            return NO_BALANCE
