"""Defines math app model administration."""

from django.contrib import admin

from apps.core.mixins.admin import UnchangeableAdminMixin
from apps.math.models import MathExercise, MathTransaction


@admin.register(MathExercise)
class MathExerciseAdmin(admin.ModelAdmin):  # type: ignore
    """Math app exercise model administration."""

    list_display = ['name']
    ordering = ['name']


@admin.register(MathTransaction)
class MathTransactionAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore
    """Math reward transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']
