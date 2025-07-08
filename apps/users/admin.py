"""Contains model administration."""

from django.contrib import admin

from .models import (
    Balance,
    CustomUser,
    Transaction,
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Administration of custom User model."""

    date_hierarchy = 'date_joined'
    list_display = ['username', 'date_joined']

    fields = ['username', 'date_joined']
    readonly_fields = ['date_joined']


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Administration of Balance model."""

    date_hierarchy = 'updated_at'
    list_display = ['user', 'points', 'updated_at']

    fields = ['user', 'points', 'updated_at', 'created_at']
    readonly_fields = ['user', 'points', 'updated_at', 'created_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Administration of Transaction model."""

    date_hierarchy = 'created_at'
    list_display = [
        'user_balance__user',
        'content_object',
        'operation_type',
        'amount',
        'created_at',
    ]

    fields = ['user_balance', 'operation_type', 'amount', 'created_at']
    readonly_fields = [
        'user_balance',
        'operation_type',
        'amount',
        'created_at',
    ]
