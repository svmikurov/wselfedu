"""Defines main app model administration."""

from django.contrib import admin

from .models import App


@admin.register(App)
class DisciplineAdmin(admin.ModelAdmin):  # type: ignore
    """Project app model administration."""

    list_display = ['name', 'schema_name']
    ordering = ['name', 'schema_name']
