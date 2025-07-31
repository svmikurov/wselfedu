"""Defines Lang app model administration."""

from django.contrib import admin

from apps.core.mixins.admin import UnchangeableAdminMixin
from apps.lang.models import LangExercise, LangTransaction


@admin.register(LangExercise)
class LangExerciseAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app exercise model administration."""

    list_display = ['name']


@admin.register(LangTransaction)
class LangTransactionAdmin(UnchangeableAdminMixin, admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang reward transaction model administration."""

    list_display = ['user', 'amount', 'type', 'created_at']
