"""Defines main app model administration."""

from django.contrib import admin

from .models import Discipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):  # type: ignore
    """Discipline model administration."""

    list_display = ['name']
    ordering = ['name']
