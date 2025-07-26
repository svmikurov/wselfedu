"""Defines math app model administration."""

from django.contrib import admin

from apps.math.models import MathExercise
from apps.math.models.transaction import MathTransaction


@admin.register(MathExercise)
class MathExerciseAdmin(admin.ModelAdmin):  # type: ignore
    """Math app exercise model administration."""

    list_display = ['name']
    ordering = ['name']


@admin.register(MathTransaction)
class MathTransactionAdmin(admin.ModelAdmin):  # type: ignore
    """Math reward transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']
