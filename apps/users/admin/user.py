"""Defines Users app model administration."""

from django.contrib import admin

from apps.core.mixins.admin import UnchangeableAdminMixin

from ..models import (
    Balance,
    CustomUser,
)
from ..models.transaction import Transaction


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Custom user model administration."""

    list_display = ['username', 'date_joined']
    ordering = ['username']


@admin.register(Balance)
class BalanceAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance model administration."""

    list_display = ['user', 'total', 'updated_at']
    ordering = ['user']


# TODO: Fix username link
@admin.register(Transaction)
class TransactionAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance combined transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']
    readonly_fields = [field.name for field in Transaction._meta.fields]
