"""Defines Users app model administration."""

from django.contrib import admin

from apps.users.models import Balance, CustomUser
from apps.users.models.transaction import Transaction
from features.mixins.admin import UnchangeableAdminMixin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Custom user model administration."""

    list_display = ['username', 'date_joined']


@admin.register(Balance)
class BalanceAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance model administration."""

    list_display = ['user', 'total', 'updated_at']


# TODO: Fix username link
@admin.register(Transaction)
class TransactionAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance combined transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']
    readonly_fields = [field.name for field in Transaction._meta.fields]
