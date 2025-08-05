"""Defines Users app model administration."""

from django.contrib import admin

from apps.core.mixins.admin import UnchangeableAdminMixin
from .models import Balance, CustomUser, Mentorship, MentorshipRequest
from .models.transaction import Transaction


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Custom user model administration."""

    list_display = ['username', 'date_joined']
    ordering = ['username']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    """Mentorship model representation."""

    list_display = ['mentor', 'student']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    """Mentorship request model representation."""

    list_display = ['from_user', 'to_user']


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
