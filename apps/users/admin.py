"""Defines Users app model administration."""

from django.contrib import admin

from apps.users.models import Balance, CustomUser, RewardLimit, Transaction


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Custom user model administration."""

    list_display = ['username', 'date_joined']


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance model administration."""

    list_display = ['user', 'total', 'created_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """User balance transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']


@admin.register(RewardLimit)
class RewardLimitAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """User reward model administration."""

    fields = ['user', 'limit']
    list_display = ['user', 'remainder', 'limit', 'created_at', 'updated_at']
